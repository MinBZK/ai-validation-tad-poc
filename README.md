# ai-validation-tad-poc

A proof-of-concept for simple CLI for generating TAD reports.

## What does this tool do?

The tool can perform different actions.

A shap test can be performed against a model with testdata.
```
tad --action=shap --model=testdata/model/sample_bc_credit_sklearn_linear.LogisticRegression.sav
--data=testdata/data/sample_bc_credit_data_no_default.sav --outputdir=tests
```

Questionnaires can be filled out.

```
tad --action=questionnaire
```

### TAD

Given a model and a dataset, a TAD explainer is used to generate results which are saved for future usage.

By default, the outputfile is saved to out/shap.yaml and contains:

- shap_values: list of shap values per feature
- base_values: list of base value per feature
- feature_names: list of the feature names

### Questionnaire

The basic functionallity of this CLI is the following.
* For each file `questionnaires/questionnaire_name.json`,
the CLI will guide the user through the questions it contains and will emit a file
`out/questionnaire_name.yaml` containing questions and answers.
* A user can abort any time and the answers will
be saved.
* If a yaml file with matching name to a questionnaire exists in `out/` the answers it contains will
be loaded in the CLI and the user has the option to update any of these ansers.

#### Usage

The directory `questionnaires/` contains different questionnaires. A questionnaire is simply a json
file with questions. As two examples we have put `general_info.json` and `iama.json` in this
directory. The idea is that users can upload their own custom questionnaires. The file `schema/question.json`
contains a json schema the questionnaires in `questionnaires/` should adhere to.

To run the CLI with defaults, run `poetry run python tad/__main__.py` from the root directory of
this repository. This will guide the user through the questions in `questionnaires/`. Users can abort
at any time by CTRL+C; this will save the intermediate results as yaml files to the `out/` directory.

Optionnaly users can provide command line options to specify a path to the questionnaire validation
schema, the questionnaire directory and the output directory:
```
tad [-h] [--schema SCHEMA] [--inputdir INPUTDIR] [--outputdir OUTPUTDIR]
```

## External libraries used

* [Questionary](https://questionary.readthedocs.io/en/stable/index.html)
* [jsonschema](https://python-jsonschema.readthedocs.io/en/stable/)

## Remarks

* The output file is standalone and must not have any hard reference to the source file.

* Output files are in a machine processable format (yaml) which can be used to create final reports in different formats like MD or PDF.

* The relation between an answer in the output file and the question in the source file, is the question itself (text) and the filename.

* Answers in the output file are indexed by the name of the source file and the question, e.g. filename:question.

## Maybe later / open for discussion

* A source file contains questions and must be in the sources folder and contain a reference to a known schema.
