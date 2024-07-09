import logging
from pathlib import Path
from typing import Any

import shap
import yaml
from pandas import DataFrame
from pandas.io.parsers import TextFileReader

logger = logging.getLogger(__name__)


class ShapTool:
    """
    The ShapTool class specifies methods for use of the SHAP library
    """

    _model = None
    _data: DataFrame | TextFileReader
    _labels = None
    _results = {"results": [0]}

    def __init__(self, model, data: DataFrame | TextFileReader):
        self._model = model
        self._data = data
        self._labels = self._data.columns

    def save_results(self, shap_data: dict, output_dir):
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        file_basename = "shap"
        output_filepath = Path(output_dir, file_basename).with_suffix(".yaml")
        with open(output_filepath, "w") as file:
            yaml.safe_dump(shap_data, file, sort_keys=False)
        logging.info(f"saved shap results to {output_filepath}")

    def get_results(self) -> dict[str, Any]:
        """
        Get the results from running the SHAP explain on the model and data

        Returns:
            Dict: The results to be returned for display
        """

        # TODO add support for more types of explainers
        explainer = shap.Explainer(self._model, self._data)
        shap_values = explainer(self._data)
        mean_absolute_shap_values = shap_values.timestamp_to_datetimeabs.mean(0).values

        results = [
            {
                "name": name,
                "value": str(value),
            }
            for name, value in zip(shap_values.feature_names, mean_absolute_shap_values)
        ]

        out = dict(
            {
                "type": "SHAP",
                "name": "Mean Absolute Shap Values",
                "results": results,
            }
        )

        return out
