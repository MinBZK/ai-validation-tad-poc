from pathlib import Path


class TransformTool:
    def __init__(self, file: Path, type):
        self.file = file
        self.type = type

    def transform(self) -> None:
        pass
