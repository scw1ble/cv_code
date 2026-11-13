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

Install the Python dependencies:

```sh
python -m pip install -r requirements.txt
```

On macOS, install WeasyPrint's native Pango dependency first:

```sh
brew install pango
export DYLD_FALLBACK_LIBRARY_PATH="$(brew --prefix)/lib"
```

Run the build from the same shell session so WeasyPrint can locate Homebrew's native libraries.

## Generate the CV

Edit `example.yaml`, then run:

```sh
python build.py
```

The generated PDF is written to `output/cv.pdf`.

## Virtual environment activation

```sh
source .venv/bin/activate
```