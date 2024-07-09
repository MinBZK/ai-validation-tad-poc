import logging
from enum import StrEnum
from pathlib import Path

import joblib
import pandas as pd
from pandas import DataFrame
from pandas.io.parsers import TextFileReader


class DataLoader:
    """
    DataLoader class offers methods to load supported data formats
    """

    class SupportedExtensions(StrEnum):
        CSV = ".csv"
        SAV = ".sav"

    @staticmethod
    def load(path: str) -> DataFrame | TextFileReader:
        """
        Load a datafile from disk and return the instance.
        :param path: the path of the file, can be relative
        :return: an instance of the data
        """
        resolved_data_path: Path = (Path.cwd() / path).resolve()
        if not resolved_data_path.is_file():
            raise FileNotFoundError(f"File not found at path {resolved_data_path} ")
        try:
            # TODO support more formats
            match resolved_data_path.suffix:
                case DataLoader.SupportedExtensions.CSV:
                    data = pd.read_csv(resolved_data_path)
                case DataLoader.SupportedExtensions.SAV:
                    data = joblib.load(resolved_data_path)
                case _:
                    raise TypeError(
                        f"Data extension {resolved_data_path.suffix} is not supported,"
                        f" supported types are {DataLoader.SupportedExtensions}"
                    )
            # check if the data type is supported
            if not issubclass(type(data), (DataFrame, TextFileReader)):
                raise TypeError("Data type is not supported")
        except Exception as e:
            raise e
        else:
            logging.info(f"Data {resolved_data_path} loaded, it is of type {type(data)} ")
            return data
