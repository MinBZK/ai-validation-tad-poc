import logging
from pathlib import Path

from tad_core.tools.arg_parser import ArgParser


def setup_logger():
    log_directory = Path(Path.cwd(), "logs")
    Path(log_directory).mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename="logs/tad.log",
        encoding="utf-8",
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s [%(name)s:%(lineno)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # uncomment line below to show logging in console
    # logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


def main():
    # Setup logging and get command line input
    setup_logger()
    args = ArgParser().get_args()
    logging.info("TAD CLI started %s", args)

    # Determine what action we need to execute
    match args.action:
        case ArgParser.Actions.SHAP:
            from tad_core.loaders.data_loader import DataLoader
            from tad_core.loaders.model_loader import ModelLoader
            from tad_core.tools.shap_tool import ShapTool

            model = ModelLoader.load(args.model)
            data = DataLoader.load(args.data)
            shap_tool = ShapTool(model, data)
            shap_values = shap_tool.get_results()
            shap_tool.save_results(shap_values, args.outputdir)
        case ArgParser.Actions.ASSESSMENT:
            from tad_core.tools.assessment_tool import QuestionnaireTool

            QuestionnaireTool.run_questionnaire(args)
        case ArgParser.Actions.REPORT:
            from tad_core.tools.report_tool import ReportTool

            ReportTool.render()
        case _:
            print(f"Unsupported action {args.action}")


if __name__ == "__main__":
    main()
