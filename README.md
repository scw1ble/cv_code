```
├── build.py
├── example.yaml
├── output
├── requirements.txt
├── README.md
└── web
    ├── style.css
    └── template.html
```

# CV generator

## Setup

Activate the project virtual environment, then install the Python dependencies:

```sh
source .venv/bin/activate
python -m pip install -r requirements.txt
```

If you are not using the project venv, install the same requirements with:

```sh
python -m pip install -r requirements.txt
```

On macOS, install the native Pango dependency if it is missing:

```sh
brew install pango
```

The build script automatically adds Homebrew's library folder to `DYLD_FALLBACK_LIBRARY_PATH` when it is available, so the PDF generation can run without a manual export step in the same shell.

## Generate the CV

Edit `cv.yaml`, then run:

```sh
python build.py
```

The generated PDF is written to `output/cv.pdf`.

The build script supports six visual styles: `classic` (default), `modern`, `elegant`, `minimal`, `creative`, and `compact`. For example:

```sh
python build.py --template-style modern
```

All six styles use the same CV fields and content structure.
The Classic style follows a moderate-margin Word layout and requests the DenXian font family. If DenXian/DengXian is not installed on the system generating the PDF, WeasyPrint uses the configured sans-serif fallback.

## Streamlit YAML form

The project now includes a simple form-based app that creates the same YAML structure as the example files without writing YAML by hand.

Start it with:

```sh
source .venv/bin/activate
streamlit run app.py
```

The app writes YAML files in the project root using the same lowercase `.yaml` naming pattern, shows a live preview, lets you choose between six CV designs, and can load an existing YAML file to edit it.
Experience and education entries use separate `start_date` and `end_date` fields. Dates can be entered as `MM/YYYY`; use `Present` for an ongoing experience or education entry. When loading older YAML, the app maps experience `duration` ranges and education `graduation_year` values to the new fields.
The **Fill page vertically** option is enabled by default and spreads CV sections over the printable page. To use the same layout from the command line, run:

```sh
python build.py --fill-page
```

This distributes available space between sections while preserving the chosen template's font sizes. If the CV content exceeds one page, it continues onto additional pages rather than shrinking text.
