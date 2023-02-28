import json
from enum import Enum
from pathlib import Path
from typing import Any

import tomllib
import xmltodict
from typer import Argument, Typer


class FileFormat(Enum):
    JSON = "json"
    TOML = "toml"
    XML = "xml"


app = Typer()


def __resolve(dictionary: dict[str, Any], query: str) -> Any:
    result = dictionary
    for part in query.split("."):
        result = result[part]
    return result


@app.command()
def set_parameter(name: str, value: str) -> None:
    print(f"##teamcity[setParameter name='{name}' value='{value}']")


@app.command()
def query(
    format: FileFormat,
    query: str = Argument(
        ...,
        help="Query string e.g. 'path.to.value' or, in case of XML, 'path.to.@attribute'",
    ),
    file: Path = Argument(..., help="Filepath"),
) -> None:
    if format == FileFormat.JSON:
        result = json.loads(file.read_text())
    elif format == FileFormat.XML:
        result = xmltodict.parse(file.read_text(encoding="utf-8-sig"))
    elif format == FileFormat.TOML:
        result = tomllib.loads(file.read_text())
    else:
        raise ValueError("Invalid format")

    print(__resolve(result, query))


if __name__ == "__main__":
    app()
