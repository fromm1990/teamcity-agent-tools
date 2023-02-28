from pathlib import Path
from sys import platform
from zipfile import ZipFile

import PyInstaller.__main__
import tomllib

ROOT = Path(__file__).parent
PY_INSTALLER_BUILD_DIR = ROOT.joinpath("build")
PY_INSTALLER_DIST_DIR = PY_INSTALLER_BUILD_DIR.joinpath("dist")
DIST_DIR = ROOT.joinpath("dist")
EXECUTABLE = "tctool"


DIST_DIR.mkdir(parents=True, exist_ok=True)

PyInstaller.__main__.run(
    [
        "src/__main__.py",
        "--name=tctool",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--noupx",
        f"--workpath={PY_INSTALLER_BUILD_DIR.as_posix()}",
        f"--distpath={PY_INSTALLER_DIST_DIR.as_posix()}",
        f"--specpath={PY_INSTALLER_BUILD_DIR.as_posix()}",
        "--hidden-import=rich",
        "--hidden-import=colorama",
        "--hidden-import=shellingham",
    ]
)


descriptor = ROOT.joinpath("teamcity-plugin.xml").read_text()
if platform == "linux" or platform == "linux2":
    descriptor = descriptor % {"executable": EXECUTABLE}
elif platform == "win32":
    EXECUTABLE = f"{EXECUTABLE}.exe"
    descriptor = descriptor % {"executable": EXECUTABLE}
elif platform == "darwin":
    raise NotImplementedError("OS X is not supported yet")


pyproject = tomllib.loads(ROOT.joinpath("pyproject.toml").read_text())
version = pyproject["tool"]["poetry"]["version"]
with ZipFile(DIST_DIR.joinpath(f"{version}_{platform}_tctool.zip"), mode="w") as zip_file:
    zip_file.write(PY_INSTALLER_DIST_DIR.joinpath(EXECUTABLE), f"lib/{EXECUTABLE}")
    zip_file.writestr("teamcity-plugin.xml", descriptor)
