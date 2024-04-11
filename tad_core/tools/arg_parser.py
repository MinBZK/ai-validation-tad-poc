import argparse
from argparse import Namespace
from enum import StrEnum
from pathlib import Path


class ArgParser:
    """
    This class is responsible for the command line userinput. Because the project has different requirements
    depending on the use case, the logic for those use cases can be defined in custom methods.
    """

    class Actions(StrEnum):
        SHAP = "shap"
        ASSESSMENT = "assessment"
        REPORT = "report"

        @classmethod
        def list(cls):
            return list(map(lambda c: c.value, cls))

    _start_parser = None
    _user_namespace = argparse.Namespace()

    def __init__(self):
        self._start_parser = argparse.ArgumentParser(description="CLI tool for TAD", conflict_handler="resolve")
        self._set_shared_cli_args()
        self._set_additional_cli_args()

    def get_args(self) -> Namespace:
        return self._start_parser.parse_args()

    def _set_shared_cli_args(self) -> None:
        self._start_parser.add_argument(
            "--action",
            choices=ArgParser.Actions.list(),
            required=True,
            type=str,
            dest="action",
            help="Which action to perform. This can be the shap test on a model, or a questionnaire to fill out.",
        )
        self._start_parser.add_argument(
            "--outputdir",
            required=False,
            type=Path,
            default=(Path.cwd() / "out").resolve(),
            help="the output folder containing answered assessments",
        )
        # validate the first input before we continue
        self._start_parser.parse_known_args(namespace=self._user_namespace)

    def _set_assessment_cli_args(self) -> None:
        """
        Defines the input parameters for the questionnaire.
        :return: None
        """
        self._start_parser.add_argument(
            "--inputdir",
            required=False,
            type=Path,
            default=(Path.cwd() / "assessments").resolve(),
            help="the input folder containing questionnaires",
        )

    def _set_shap_cli_args(self) -> None:
        """
        Defines the input parameters for a SHAP test.
        :return: None
        """
        self._start_parser.add_argument("--model", required=True, type=str, help="the path of the model to use")
        self._start_parser.add_argument("--data", required=True, type=str, help="the path of the data to use")

    def _set_report_cli_args(self) -> None:
        """
        Defines the input parameters for a REPORT generation.
        :return: None
        """
        self._start_parser.add_argument("--card", required=True, type=Path, help="the path of the system card to use")

    def _set_additional_cli_args(self) -> None:
        """
        Adds more (required) parameters depending on the current use case
        :return: None
        """
        if self._user_namespace.action == ArgParser.Actions.ASSESSMENT:
            self._set_assessment_cli_args()
        elif self._user_namespace.action == ArgParser.Actions.SHAP:
            self._set_shap_cli_args()
        elif self._user_namespace.action == ArgParser.Actions.REPORT:
            self._set_report_cli_args()

    def print_user_args(self) -> None:
        """
        This function is mostly for debug purposes. It prints the current given arguments.
        :return: None
        """
        args = self._start_parser.parse_args(namespace=self._user_namespace)
        for key, val in vars(args).items():
            print(f"{key}: {val}")
