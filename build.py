from jinja2 import Environment
from jinja2 import FileSystemLoader
import yaml
from pathlib import Path
from weasyprint import HTML


project_dir = Path(__file__).resolve().parent
output_dir = project_dir / "output"
output_dir.mkdir(exist_ok=True)

loader = FileSystemLoader(project_dir / "web")
env = Environment(loader=loader)


with open(project_dir / "example.yaml", "r", encoding="utf-8") as file:
    data = yaml.safe_load(file)

template = env.get_template("template.html")
rendered = template.render(data=data)
pdf_path = output_dir / "cv.pdf"
base_url = f"{output_dir.as_uri()}/"
HTML(string=rendered, base_url=base_url).write_pdf(pdf_path)
print(f"Generated {pdf_path}")
