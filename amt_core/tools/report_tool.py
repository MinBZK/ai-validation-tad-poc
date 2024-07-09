import logging
import os
from datetime import datetime, timezone
from pathlib import Path

import jinja2
import yaml
import yaml_include

logger = logging.getLogger(__name__)


class ReportTool:
    """
    The ReportTool class provides methods for generating a report from a system card.
    """

    def __init__(self, system_card: Path) -> None:
        """
        Loads a syste card for rendering.
        :param system_card: Path to the system card YAML file.
        :return: None
        """
        system_card = system_card.resolve()

        # Add constructer so we can use the "!include" directive in yaml to load
        # other yaml files directly into to the system_card.
        base_dir = os.path.dirname(system_card)
        yaml.add_constructor("!include", yaml_include.Constructor(base_dir=base_dir))

        with open(system_card) as f:
            data = yaml.full_load(f)

        # Normalise model-index to model_index to avoid conflics resulting from usage of "-".
        for model in data["models"]:
            model["model_index"] = model.pop("model-index")

        self.data = data

    def render(self) -> None:
        """
        Emits a HTML report ui/output.html based on the system card which can be rendered.
        :return: None
        """

        # Create an environment so we can use custom filters in our Jinja2 template,
        # for example to transform timestamps to ISO 8601 datetimes.
        templateLoader = jinja2.FileSystemLoader(searchpath="./")
        env = jinja2.Environment(loader=templateLoader)
        env.filters["timestamp_to_iso8601"] = ReportTool._timestamp_to_iso8601

        reference_template = env.get_template("ui/reference.html")
        reference_html_output = reference_template.render(self.data)

        template_template = env.get_template("ui/template.html")
        template_html_output = template_template.render(content=reference_html_output)

        with open(Path(Path.cwd(), "ui", "output.html"), "w") as f:
            f.write(template_html_output)

    @staticmethod
    def _timestamp_to_iso8601(timestamp: str) -> str:
        """
        Helper function to convert a Unix timestamp to ISO 8601 date and time format.
        :param timestamp: Unix timestamp.
        :return: ISO 8601 formatted datetime YYYY-MM-DDTHH:MM:SSZ
        """
        current_datetime = datetime.fromtimestamp(float(timestamp), tz=timezone.utc)
        current_datetime = current_datetime.isoformat()

        # isoformat() emits a +00:00 to designate UTC instead of "Z" as specified in ISO 8601.
        current_datetime = current_datetime.replace("+00:00", "Z")
        return current_datetime
