import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import jsonschema
import questionary
import yaml

logger = logging.getLogger(__name__)


@dataclass
class Questionnaire:
    name: str
    questions: List[Dict[str, str]]


class QuestionnaireTool:
    """
    The QuestionnaireTool class provides methods for interacting with Questionnaire
    """

    @staticmethod
    def run_questionnaire(args):
        question_dir = args.inputdir
        output_dir = args.outputdir

        questionnaire_schema = Path.cwd() / "schemas/questions.json"
        answers_schema = Path.cwd() / "schemas/answers.json"

        Path(output_dir).mkdir(parents=True, exist_ok=True)

        print("=" * 50)
        print("Welcome to AMT! We have a few questions for you.")
        print("=" * 50)

        questionnaires = QuestionnaireTool.load_questionnaires(question_dir, questionnaire_schema)
        questionnaires_with_answers = QuestionnaireTool.load_filled_questionnaires(
            question_dir, output_dir, answers_schema
        )

        user_aborted = False
        for questionnaire in questionnaires:
            output = {}
            try:
                # load answers from user
                question_and_answers = None
                if questionnaire.name in questionnaires_with_answers:
                    question_and_answers = questionnaires_with_answers[questionnaire.name]

                for question in questionnaire.questions:
                    if question_and_answers is not None and question["name"] in question_and_answers:
                        print(question["name"])

                        if isinstance(question_and_answers[question["name"]], list):
                            print("Previously given answer: " + ", ".join(question_and_answers[question["name"]]))
                        else:
                            print(f"Previously given answer: {question_and_answers[question["name"]]}")

                        confirm = questionary.confirm(message="Keep this answer?").ask()
                        if confirm:
                            tmp = {question["name"]: question_and_answers[question["name"]]}
                        else:
                            tmp = questionary.unsafe_prompt(question)
                    else:
                        tmp = questionary.unsafe_prompt(question)
                    output.update(tmp)
            except KeyboardInterrupt:
                logging.info("user aborted")
                user_aborted = True

            output_filepath = output_dir / f"{questionnaire.name}.yaml"

            # Reformatted answers to a list containing dicts of the form {"question": "q", "answer": "a"}
            # so that we can export it nicely to yaml.
            q_and_a_list = [{"question": question, "answer": answer} for question, answer in output.items()]

            with open(output_filepath, "w") as file:
                yaml.safe_dump(q_and_a_list, file, sort_keys=False)

            logging.info(f"saved answers of {questionnaire.name} to {output_filepath}")

            print("\nYou have finished filling out this questionnaire.\n")
            # End if the user aborted
            if user_aborted:
                break

    @staticmethod
    def load_questionnaires(
        question_dir: Path,
        questionnaire_schema_path: Path,
    ) -> List[Questionnaire]:
        """
        Given a directory containing json files with questions, produces a lis of Questionnaire
        objects, one Questionnaire for each source file. Validates the questionnaire according
        to the schema given in questionnaire_schema.

        :param question_dir: Path to a directory expected to contain questionnaires as json files.
        :param questionnaire_schema: Path to a file containg the schema of the questionnaire.
        :return: A list of Questionnaires.
        :raises: TypeError: If question_dir is not a directory path.
        :raises: RuntimeError: If an unexpected question format is encountered.
        """

        if not question_dir.is_dir():
            logging.error(f"got invalid argument: {question_dir} must be a directory")
            raise TypeError(f"{question_dir} must be a directory")

        with open(questionnaire_schema_path) as f:
            questionnaire_schema = json.load(f)

        questionnaires = []
        for questionnaire_filepath in question_dir.iterdir():
            if questionnaire_filepath.suffix != ".json":
                logging.warning(f"ignoring unexpected file format '{questionnaire_filepath.suffix}'")
                continue

            with open(questionnaire_filepath) as f:
                questionnaire = json.load(f)

            try:
                jsonschema.validate(questionnaire, questionnaire_schema, cls=None)
            except jsonschema.exceptions.ValidationError:
                logging.exception(f"questionnaire {questionnaire_filepath} has invalid schema")

            questions = []
            for group in questionnaire["groups"]:
                for question in group["questions"]:
                    match question["type"]:
                        case "FREESINGLE":
                            questions.append(
                                {
                                    "type": "text",
                                    "name": question["question"],
                                    "message": question["question"],
                                }
                            )

                        case "FREEMULTIPLE":
                            # TODO: Deal with 'FREEMULTIPLE' questions.
                            # For now we ignore if we encounter them.
                            continue

                        case "CHOICESINGLE":
                            questions.append(
                                {
                                    "type": "select",
                                    "name": question["question"],
                                    "message": question["question"],
                                    "choices": question["options"],
                                }
                            )
                        case "CHOICEMULTIPLE":
                            questions.append(
                                {
                                    "type": "checkbox",
                                    "name": question["question"],
                                    "message": question["question"],
                                    "choices": question["options"],
                                }
                            )
                        case _:
                            logging.error(f"got unexpected question type {question["type"]}")
                            raise RuntimeError(f'unexpected question type {question["type"]}')

                questionnaires.append(Questionnaire(name=questionnaire_filepath.stem, questions=questions))

        return questionnaires

    @staticmethod
    def load_filled_questionnaires(
        question_dir: Path, output_dir: Path, answers_schema_path: Path
    ) -> Dict[str, Dict[str, str]]:
        """
        Loads already (partially) filled in questionnaires from yaml files in the output_dir.

        :param answers_schema_path: Path to the schema for validating answer files
        :param question_dir: Path to a directory containing the questionnaires
        :param output_dir: Path to a directory containing question and answer yaml files.
        :return: A dictionary mapping the name of a questionnaire to a dictionary with keys being
        the question and the value being the answer.
        :raises: TypeError: If output_dir is not a directory path.

        """
        if not output_dir.is_dir():
            logging.error(f"got invalid argument: {question_dir} must be a directory")
            raise TypeError(f"{output_dir} must be a directory")

        with open(answers_schema_path) as f:
            answers_schema = json.load(f)

        q_and_a_sources = {}
        for q_and_a_filepath in output_dir.iterdir():
            if q_and_a_filepath.suffix != ".yaml":
                logging.warning(f"ignoring unexpected file format '{q_and_a_filepath.suffix}'")
                continue

            with open(q_and_a_filepath) as f:
                q_and_a_yaml = yaml.safe_load(f)

            # make sure we only parse files from the answers_schema
            try:
                jsonschema.validate(q_and_a_yaml, answers_schema, cls=None)
                q_and_a_sources[q_and_a_filepath.stem] = {}
                for q_and_a in q_and_a_yaml:
                    q_and_a_sources[q_and_a_filepath.stem][q_and_a["question"]] = q_and_a["answer"]
            except jsonschema.exceptions.ValidationError:
                logging.exception(f"answers {q_and_a_filepath} has invalid schema")

        return q_and_a_sources
