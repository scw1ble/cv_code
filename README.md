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

## Streamlit YAML form

The project now includes a simple form-based app that creates the same YAML structure as the example files without writing YAML by hand.

Start it with:

```sh
source .venv/bin/activate
streamlit run app.py
```

The app writes YAML files in the project root using the same lowercase `.yaml` naming pattern, shows a live preview, and can load an existing YAML file to edit it.
