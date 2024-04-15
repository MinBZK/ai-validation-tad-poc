import logging
from datetime import datetime
from pathlib import Path

import jinja2
import yaml
import yaml_include

logger = logging.getLogger(__name__)


class ReportTool:
    """
    The ReportTool class provides methods for generating a report from a system card.
    """

    @staticmethod
    def render() -> None:
        """
        Renders a HTML report based on the system card
        :return: None
        """
        cards_folder_resolved = Path(Path.cwd(), "cards")

        yaml.add_constructor("!include", yaml_include.Constructor(base_dir="cards/"))
        with open(Path(cards_folder_resolved, "system_card.yaml")) as f:
            data = yaml.full_load(f)

        # Normalise model-index to model_index.
        for model in data["models"]:
            model["model_index"] = model.pop("model-index")

        templateLoader = jinja2.FileSystemLoader(searchpath="./")
        env = jinja2.Environment(loader=templateLoader)
        env.filters["timestamp_to_datetime"] = ReportTool.timestamp_to_datetime

        reference_template = env.get_template("ui/reference.html")
        reference_html_output = reference_template.render(data)

        template_template = env.get_template("ui/template.html")
        template_html_output = template_template.render(content=reference_html_output)

        with open(Path(Path.cwd(), "ui", "output.html"), "w") as f:
            f.write(template_html_output)

    @staticmethod
    def timestamp_to_datetime(timestamp: str) -> str:
        date_time = datetime.fromtimestamp(float(timestamp))
        return date_time.strftime("%m/%d/%Y, %H:%M:%S")
