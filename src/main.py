import json
from pathlib import Path
from typing import Any

import tomllib
import xmltodict
from typer import Typer

app = Typer()

def __resolve(dictionary: dict[str, Any], query: str) -> Any:
    result = dictionary
    for part in query.split("."):        
        result = result[part]
    return result

@app.command()
def query_toml(query: str, path: Path) -> None:
    result = tomllib.loads(path.read_text())
    print(__resolve(result, query))

@app.command()
def query_json(query: str, path: Path) -> None:
    result = json.loads(path.read_text())
    print(__resolve(result, query))
    
@app.command()
def query_xml(query: str, path: Path) -> None:
    result = xmltodict.parse(path.read_text(encoding="utf-8-sig"))
    print(__resolve(result, query))

@app.command()
def set_parameter(name: str, value: str) -> None:
    print(f"##teamcity[setParameter name='{name}' value='{value}']")

if __name__ == "__main__":
    app()