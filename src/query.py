import json
from pathlib import Path
from typing import Any

import tomllib
import xmltodict
from typer import Typer

typer = Typer(name="query")


def __resolve(dictionary: dict[str, Any], query: str) -> Any:
    result = dictionary
    for part in query.split("."):        
        result = result[part]
    return result

@typer.command()
def toml(query: str, path: Path) -> None:
    result = tomllib.loads(path.read_text())
    print(__resolve(result, query))

@typer.command()
def json(query: str, path: Path) -> None:
    result = json.loads(path.read_text())
    print(__resolve(result, query))
    
@typer.command()
def xml(query: str, path: Path) -> None:
    result = xmltodict.parse(path.read_text(encoding="utf-8-sig"))
    print(__resolve(result, query))
