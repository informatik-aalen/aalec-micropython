import importlib.metadata
import json
import pathlib
import subprocess

from colorama import Fore, Style
import mpy_cross
from InquirerPy import inquirer

root = pathlib.Path(__file__).parent.parent
src = root / "src"
out = root / "aalec-micropython-stubs/src"


def get_version(dist: str = "aalec-micropython") -> str:
    """Get version of the given distribution.

    Args:
        dist: A distribution name.

    Returns:
        A version number.
    """
    try:
        return importlib.metadata.version(dist)
    except importlib.metadata.PackageNotFoundError:
        return "0.0.0"


def rm_stubs():
    print(Fore.BLUE, "⚒️  Remove old stubs ", end="")
    for path in out.rglob("*.pyi"):
        path.unlink()
    print(Fore.GREEN + "✔" + Style.RESET_ALL)


def stubgen():
    print(Fore.BLUE, "⚒️  Generate new subs in 'out/aalec' ", end="")
    cmd = [
        "stubgen",
        "--include-docstrings",
        "--output",
        str(out),
        str(src),
    ]
    subprocess.run(cmd)  # , stdout=subprocess.PIPE)
    print(Fore.GREEN + "✔" + Style.RESET_ALL)


def rm_compiled():
    print(Fore.BLUE, "⚒️  Remove old compiled micropython files ", end="")
    for path in src.rglob("*.mpy"):
        path.unlink()
    print(Fore.GREEN + "✔" + Style.RESET_ALL)


def compile():
    print(Fore.BLUE, "⚒️  Compile micropython files ", end="")
    for path in sorted(src.rglob("*.py")):
        p = mpy_cross.run(path)
        p.wait()
    print(Fore.GREEN + "✔" + Style.RESET_ALL)


def collect_urls() -> list[list[str]]:
    """Collect the name of the python files from src.

    Returns:
        list[list[str]]: List of destination and source files pairs.
    """
    urls = []
    for path in sorted(src.rglob("*.mpy")):
        module_path = path.relative_to(src)
        src_path = path.relative_to(root)
        urls.append([str(module_path), str(src_path)])
    return urls


def create_package_json(version: str):
    print(Fore.BLUE, "⚒️  Create 'package.json' file ", end="")
    content = json.dumps({"urls": collect_urls(), "version": version}, indent=2)
    package_json = root / "package.json"
    package_json.write_text(content)
    print(Fore.GREEN + "✔" + Style.RESET_ALL)


if __name__ == "__main__":
    try:
        version = inquirer.text(  # type: ignore
            message="Choose the version number for the release:", default=get_version()
        ).execute()

        rm_stubs()
        stubgen()
        rm_compiled()
        compile()
        create_package_json(version)
    except KeyboardInterrupt:
        print(Fore.RED, "Command aborted! 😭 💥 😱", Style.RESET_ALL)
    print(Fore.GREEN, "Command successful! 🐍 🌟 ✨", Style.RESET_ALL)
