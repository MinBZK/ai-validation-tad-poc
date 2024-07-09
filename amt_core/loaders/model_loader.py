import logging
from enum import StrEnum
from pathlib import Path
from typing import Type

import joblib
from sklearn.base import BaseEstimator


class ModelLoader:
    """
    ModelLoader class offers methods to load supported models
    """

    class SupportedExtensions(StrEnum):
        SAV = ".sav"

    @staticmethod
    def load(path: str) -> Type[BaseEstimator]:
        """
        Load a model from disk and return the instance.
        :param path: the path of the model, can be relative
        :return: an instance of the model
        """
        resolved_model_path: Path = (Path.cwd() / path).resolve()
        if not resolved_model_path.is_file():
            raise FileNotFoundError(f"File not found at path {resolved_model_path} ")
        try:
            match resolved_model_path.suffix:
                case ModelLoader.SupportedExtensions.SAV:
                    model = joblib.load(resolved_model_path)
                case _:
                    raise TypeError(
                        f"Model extension {resolved_model_path.suffix} is not supported,"
                        f"supported types are {ModelLoader.SupportedExtensions}"
                    )

            # TODO models can be saved in older/newer versions of skleanr and
            #  may not be compatible with the version we use
            if not issubclass(type(model), BaseEstimator):
                raise TypeError("Model type is not supported")
        except Exception as e:
            raise e
        else:
            logging.info(f"Model {resolved_model_path} loaded, it is of type {type(model)} ")
            return model
