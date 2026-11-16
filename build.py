import argparse
import os
import subprocess
import sys
from pathlib import Path


def ensure_python_dependencies() -> None:
    missing = []
    for package_name, import_name in (("PyYAML", "yaml"), ("Jinja2", "jinja2")):
        try:
            __import__(import_name)
        except ModuleNotFoundError:
            missing.append(package_name)

    if missing:
        raise SystemExit(
            "Missing Python dependencies: "
            + ", ".join(missing)
            + ". Activate the project virtual environment and install them with: "
            "'source .venv/bin/activate && python -m pip install -r requirements.txt'"
        )


ensure_python_dependencies()

import yaml
from jinja2 import Environment, FileSystemLoader


def ensure_homebrew_native_libraries() -> None:
    if sys.platform != "darwin":
        return

    lib_paths = []
    for value in os.environ.get("DYLD_FALLBACK_LIBRARY_PATH", "").split(":"):
        if value:
            lib_paths.append(value)

    brew_prefix = subprocess.run(
        ["brew", "--prefix"],
        capture_output=True,
        text=True,
        check=False,
    )
    if brew_prefix.returncode != 0:
        return

    homebrew_lib = Path(brew_prefix.stdout.strip()) / "lib"
    if not homebrew_lib.exists():
        return

    if str(homebrew_lib) not in lib_paths:
        lib_paths.insert(0, str(homebrew_lib))
        os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = ":".join(lib_paths)


ensure_homebrew_native_libraries()

try:
    from weasyprint import HTML
except (ImportError, OSError) as exc:
    raise SystemExit(
        "WeasyPrint could not load its native libraries or package is missing. "
        "Install the project dependencies and, on macOS, Homebrew's Pango package: "
        "'source .venv/bin/activate && python -m pip install -r requirements.txt' ; "
        "'brew install pango'"
    ) from exc


project_dir = Path(__file__).resolve().parent
output_dir = project_dir / "output"
output_dir.mkdir(exist_ok=True)


# Parse the selected visual style, defaulting to the original classic CV design.
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate the CV PDF.")
    parser.add_argument(
        "--template-style",
        choices=("classic", "modern", "elegant", "minimal", "creative", "compact"),
        default="classic",
        help="Choose one of the six CV designs.",
    )
    return parser.parse_args()


args = parse_args()
loader = FileSystemLoader(project_dir / "web")
env = Environment(loader=loader)

with open(project_dir / "cv.yaml", "r", encoding="utf-8") as file:
    data = yaml.safe_load(file)

template = env.get_template("template.html")
rendered = template.render(data=data, template_style=args.template_style)
pdf_path = output_dir / "cv.pdf"
base_url = f"{output_dir.as_uri()}/"
HTML(string=rendered, base_url=base_url).write_pdf(pdf_path)
print(f"Generated {pdf_path}")
