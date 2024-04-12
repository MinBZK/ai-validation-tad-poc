import logging
from pathlib import Path

import yaml
import yaml_include
from jinja2 import Template

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

        with open(Path(Path.cwd(), "ui", "reference.html")) as f:
            reference_file = f.read()

        reference_template = Template(reference_file)
        reference_html_output = reference_template.render(data)

        with open(Path(Path.cwd(), "ui", "template.html")) as f:
            template_file = f.read()

        template_template = Template(template_file)
        template_html_output = template_template.render(content=reference_html_output)

        with open(Path(Path.cwd(), "ui", "output.html"), "w") as f:
            f.write(template_html_output)
