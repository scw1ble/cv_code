import re
import subprocess
import sys
from pathlib import Path

import streamlit as st
import yaml


PROJECT_DIR = Path(__file__).resolve().parent
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
TEMPLATE_OPTIONS = {
    "Classic": ("classic", "A traditional CV with restrained blue headings and clear spacing."),
    "Modern": ("modern", "A bold navy header with a teal accent."),
    "Elegant": ("elegant", "A centered serif design with warm gold details."),
    "Minimal": ("minimal", "A spacious monochrome layout with simple section markers."),
    "Creative": ("creative", "A distinctive purple header and highlighted section titles."),
    "Compact": ("compact", "A tighter green-accented layout for fitting more on each page."),
}
TEMPLATE_PREVIEW_COMPONENT = st.components.v2.component(
    "cv_template_previews",
    html='<div class="template-grid" role="group" aria-label="Choose a CV template"></div>',
    css="""
    .template-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }

    .template-card {
      min-width: 0;
      padding: 9px;
      border: 1px solid var(--st-border-color, #d6d9dd);
      border-radius: 10px;
      background: var(--st-secondary-background-color, #f0f2f6);
      color: var(--st-text-color, #262730);
      font: inherit;
      text-align: left;
      cursor: pointer;
    }

    .template-card:hover,
    .template-card:focus-visible {
      border-color: var(--st-primary-color, #ff4b4b);
      outline: 2px solid var(--st-primary-color, #ff4b4b);
      outline-offset: 1px;
    }

    .template-card[aria-pressed="true"] {
      border: 2px solid var(--st-primary-color, #ff4b4b);
      padding: 8px;
    }

    .template-name {
      display: block;
      margin-top: 8px;
      font-weight: 650;
    }

    .template-description {
      display: block;
      min-height: 2.5em;
      margin-top: 3px;
      color: var(--st-text-color, #50545a);
      font-size: 0.78rem;
      line-height: 1.3;
    }

    .template-paper {
      display: block;
      height: 170px;
      overflow: hidden;
      padding: 13px 12px;
      border-radius: 2px;
      background: #fff;
      box-shadow: 0 2px 6px #0002;
      color: #252b33;
      font-family: Arial, Helvetica, sans-serif;
    }

    .paper-header {
      display: block;
      margin-bottom: 8px;
      padding-bottom: 7px;
      border-bottom: 1px solid #cbd1d8;
    }

    .paper-name {
      display: block;
      width: 68%;
      height: 8px;
      margin-bottom: 5px;
      background: #202a36;
    }

    .paper-contact {
      display: block;
      width: 83%;
      height: 3px;
      background: #8d969f;
    }

    .paper-section {
      display: block;
      margin-top: 7px;
    }

    .paper-heading {
      display: block;
      width: 40%;
      height: 4px;
      margin-bottom: 4px;
      background: #34475b;
    }

    .paper-line {
      display: block;
      width: 94%;
      height: 2px;
      margin: 3px 0;
      background: #d3d7dc;
    }

    .paper-line.short {
      width: 63%;
    }

    .paper-bullet {
      display: block;
      width: 78%;
      height: 2px;
      margin: 3px 0 3px 5px;
      background: #c3c9cf;
    }

    .template-paper--modern .paper-header {
      margin: -13px -12px 8px;
      padding: 15px 12px 8px;
      border-bottom: 4px solid #42b4a5;
      background: #18324b;
    }

    .template-paper--modern .paper-name,
    .template-paper--modern .paper-contact {
      background: #fff;
    }

    .template-paper--modern .paper-heading {
      background: #176f74;
    }

    .template-paper--elegant {
      font-family: Georgia, "Times New Roman", serif;
    }

    .template-paper--elegant .paper-header {
      text-align: center;
      border-bottom: 3px double #aa8750;
    }

    .template-paper--elegant .paper-name {
      width: 55%;
      height: 7px;
      margin-right: auto;
      margin-left: auto;
      background: #715629;
    }

    .template-paper--elegant .paper-contact {
      width: 72%;
      margin: auto;
    }

    .template-paper--elegant .paper-heading {
      background: #aa8750;
    }

    .template-paper--minimal .paper-header {
      padding-bottom: 3px;
      border: 0;
    }

    .template-paper--minimal .paper-name {
      width: 76%;
      height: 10px;
      background: #222;
    }

    .template-paper--minimal .paper-heading {
      width: 43%;
      height: 5px;
      border-left: 3px solid #333;
      background: #555;
    }

    .template-paper--creative .paper-header {
      margin: -13px -12px 8px;
      padding: 15px 12px 8px;
      border: 0;
      border-left: 5px solid #7541a6;
      background: #f1e8fa;
    }

    .template-paper--creative .paper-name {
      background: #4b2673;
    }

    .template-paper--creative .paper-heading {
      width: 45%;
      height: 6px;
      background: #7541a6;
    }

    .template-paper--compact {
      padding: 10px;
    }

    .template-paper--compact .paper-header {
      margin-bottom: 5px;
      padding-bottom: 4px;
      border-bottom-color: #315a46;
    }

    .template-paper--compact .paper-name {
      height: 7px;
    }

    .template-paper--compact .paper-section {
      margin-top: 4px;
    }

    .template-paper--compact .paper-heading {
      width: 35%;
      height: 3px;
      margin-bottom: 2px;
      background: #315a46;
    }

    .template-paper--compact .paper-line,
    .template-paper--compact .paper-bullet {
      height: 1.5px;
      margin-top: 2px;
      margin-bottom: 2px;
    }
    """,
    js="""
    export default function (component) {
      const { data, parentElement, setStateValue } = component
      const grid = parentElement.querySelector(".template-grid")
      if (!grid) return

      const currentStyle = data.selected ?? "classic"
      grid.replaceChildren()

      for (const template of data.templates) {
        const card = document.createElement("button")
        card.type = "button"
        card.className = "template-card"
        card.setAttribute("aria-pressed", String(template.id === currentStyle))
        card.setAttribute(
          "aria-label",
          `${template.name} template. ${template.description}. Select template.`
        )

        const paper = document.createElement("span")
        paper.className = `template-paper template-paper--${template.id}`
        paper.setAttribute("aria-hidden", "true")
        paper.innerHTML = `
          <span class="paper-header">
            <span class="paper-name"></span>
            <span class="paper-contact"></span>
          </span>
          <span class="paper-section">
            <span class="paper-heading"></span>
            <span class="paper-line"></span>
            <span class="paper-line short"></span>
          </span>
          <span class="paper-section">
            <span class="paper-heading"></span>
            <span class="paper-line"></span>
            <span class="paper-bullet"></span>
            <span class="paper-bullet"></span>
          </span>
          <span class="paper-section">
            <span class="paper-heading"></span>
            <span class="paper-line short"></span>
          </span>
          <span class="paper-section">
            <span class="paper-heading"></span>
            <span class="paper-line"></span>
          </span>
        `

        const name = document.createElement("span")
        name.className = "template-name"
        name.textContent = template.name

        const description = document.createElement("span")
        description.className = "template-description"
        description.textContent = template.description

        card.append(paper, name, description)
        card.onclick = () => setStateValue("selected", template.id)
        grid.append(card)
      }
    }
    """,
)


# Build the default CV structure with the same keys, nesting, and order as the example YAML files.
def build_default_data():
    return {
        "name": "",
        "phone": "",
        "email": "",
        "summary": "",
        "languages": ["English"],
        "experience": [
            {
                "company": "",
                "position": "",
                "duration": "",
                "responsibilities": [""],
            }
        ],
        "education": [
            {
                "institution": "",
                "degree": "",
                "graduation_year": "",
            }
        ],
        "skills": [""],
    }


# Load an existing YAML file and convert it into the same form structure used by the app.
def load_existing_data(file_path):
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle) or {}

    data = build_default_data()
    for key, value in loaded.items():
        if key in data:
            data[key] = value

    if not isinstance(data["languages"], list) or not data["languages"]:
        data["languages"] = [""]
    if not isinstance(data["experience"], list) or not data["experience"]:
        data["experience"] = [
            {
                "company": "",
                "position": "",
                "duration": "",
                "responsibilities": [""],
            }
        ]
    if not isinstance(data["education"], list) or not data["education"]:
        data["education"] = [
            {
                "institution": "",
                "degree": "",
                "graduation_year": "",
            }
        ]
    if not isinstance(data["skills"], list) or not data["skills"]:
        data["skills"] = [""]

    for item in data["experience"]:
        item.setdefault("company", "")
        item.setdefault("position", "")
        item.setdefault("duration", "")
        item.setdefault("responsibilities", [""])
        if not isinstance(item["responsibilities"], list) or not item["responsibilities"]:
            item["responsibilities"] = [""]

    for item in data["education"]:
        item.setdefault("institution", "")
        item.setdefault("degree", "")
        item.setdefault("graduation_year", "")

    return data


# Validate the form values and return a list of user-friendly error messages.
def validate_data(data):
    errors = []

    if not data.get("name", "").strip():
        errors.append("Name is required.")
    if not data.get("phone", "").strip():
        errors.append("Phone is required.")
    if not data.get("email", "").strip():
        errors.append("Email is required.")
    elif not EMAIL_PATTERN.match(data["email"].strip()):
        errors.append("Email must look like an address such as name@example.com.")
    if not data.get("summary", "").strip():
        errors.append("Summary is required.")

    for index, value in enumerate(data.get("languages", []), start=1):
        if not str(value).strip():
            errors.append(f"Language {index} cannot be empty.")

    for index, item in enumerate(data.get("experience", []), start=1):
        if not str(item.get("company", "")).strip():
            errors.append(f"Experience {index} company is required.")
        if not str(item.get("position", "")).strip():
            errors.append(f"Experience {index} position is required.")
        if not str(item.get("duration", "")).strip():
            errors.append(f"Experience {index} duration is required.")
        if not item.get("responsibilities"):
            errors.append(f"Experience {index} needs at least one responsibility.")
        for responsibility_index, responsibility in enumerate(item.get("responsibilities", []), start=1):
            if not str(responsibility).strip():
                errors.append(
                    f"Experience {index} responsibility {responsibility_index} cannot be empty."
                )

    for index, item in enumerate(data.get("education", []), start=1):
        if not str(item.get("institution", "")).strip():
            errors.append(f"Education {index} institution is required.")
        if not str(item.get("degree", "")).strip():
            errors.append(f"Education {index} degree is required.")
        if not str(item.get("graduation_year", "")).strip():
            errors.append(f"Education {index} graduation year is required.")

    for index, value in enumerate(data.get("skills", []), start=1):
        if not str(value).strip():
            errors.append(f"Skill {index} cannot be empty.")

    return errors


# Convert the form data into YAML text while keeping the original key order and Unicode characters.
def dump_yaml(data):
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)


# Clear personal data from a YAML file while preserving the CV keys, order, and value types.
def clear_cv_yaml(file_path=PROJECT_DIR / "cv.yaml"):
    empty_data = {
        "name": "",
        "phone": "",
        "email": "",
        "summary": "",
        "languages": [],
        "experience": [],
        "education": [],
        "skills": [],
    }
    file_path.write_text(dump_yaml(empty_data), encoding="utf-8")


# Display a list of text inputs for a simple YAML list and support add/remove actions.
def render_simple_list(section_key, label, placeholder):
    data = st.session_state["yaml_data"]
    items = data.get(section_key, [])

    for index, item in enumerate(items):
        col_text, col_remove = st.columns([5, 1])
        with col_text:
            data[section_key][index] = st.text_input(
                f"{label} {index + 1}",
                value=str(item),
                key=f"{section_key}_{index}",
                placeholder=placeholder,
            )
        with col_remove:
            if st.button("Remove", key=f"remove_{section_key}_{index}"):
                data[section_key].pop(index)
                st.rerun()

    if st.button(f"Add {label}", key=f"add_{section_key}"):
        data[section_key].append("")
        st.rerun()


# Display one experience entry block with all required fields and responsibility list support.
def render_experience_block(index, item):
    data = st.session_state["yaml_data"]
    experience_item = data["experience"][index]

    st.subheader(f"Experience {index + 1}")
    experience_item["company"] = st.text_input(
        "Company",
        value=str(item.get("company", "")),
        key=f"experience_company_{index}",
    )
    experience_item["position"] = st.text_input(
        "Position",
        value=str(item.get("position", "")),
        key=f"experience_position_{index}",
    )
    experience_item["duration"] = st.text_input(
        "Duration",
        value=str(item.get("duration", "")),
        key=f"experience_duration_{index}",
    )

    responsibilities = item.get("responsibilities", [""])
    for responsibility_index, responsibility in enumerate(responsibilities):
        col_text, col_remove = st.columns([5, 1])
        with col_text:
            experience_item["responsibilities"][responsibility_index] = st.text_input(
                f"Responsibility {responsibility_index + 1}",
                value=str(responsibility),
                key=f"experience_responsibility_{index}_{responsibility_index}",
                placeholder="Describe the task or result",
            )
        with col_remove:
            if st.button("Remove", key=f"remove_exp_resp_{index}_{responsibility_index}"):
                experience_item["responsibilities"].pop(responsibility_index)
                st.rerun()

    if st.button("Add responsibility", key=f"add_exp_resp_{index}"):
        experience_item["responsibilities"].append("")
        st.rerun()


# Display one education entry block with the same nested fields as the YAML example.
def render_education_block(index, item):
    data = st.session_state["yaml_data"]
    education_item = data["education"][index]

    st.subheader(f"Education {index + 1}")
    education_item["institution"] = st.text_input(
        "Institution",
        value=str(item.get("institution", "")),
        key=f"education_institution_{index}",
    )
    education_item["degree"] = st.text_input(
        "Degree",
        value=str(item.get("degree", "")),
        key=f"education_degree_{index}",
    )
    education_item["graduation_year"] = st.text_input(
        "Graduation year",
        value=str(item.get("graduation_year", "")),
        key=f"education_year_{index}",
        placeholder="2026",
    )


# Store the style chosen in the interactive preview cards before Streamlit reruns the app.
def store_template_selection():
    selected_style = st.session_state["cv_template_previews"].selected
    valid_styles = {style for style, _description in TEMPLATE_OPTIONS.values()}
    if selected_style in valid_styles:
        st.session_state["selected_template_style"] = selected_style


# Render clickable visual CV previews and return the selected template style.
def render_template_picker():
    templates = [
        {"name": name, "id": style, "description": description}
        for name, (style, description) in TEMPLATE_OPTIONS.items()
    ]
    selected_style = st.session_state.get("selected_template_style", "classic")
    st.caption("Click a preview to select it.")
    result = TEMPLATE_PREVIEW_COMPONENT(
        key="cv_template_previews",
        data={"templates": templates, "selected": selected_style},
        default={"selected": selected_style},
        on_selected_change=store_template_selection,
    )
    valid_styles = {style for style, _description in TEMPLATE_OPTIONS.values()}
    if result.selected in valid_styles:
        st.session_state["selected_template_style"] = result.selected
        return result.selected
    return selected_style if selected_style in valid_styles else "classic"


# Render the full form. This is the main UI that matches the YAML structure exactly.
def render_form():
    st.title("CV YAML Builder")
    st.caption("Fill in the form and generate the YAML file used by the CV project.")

    data = st.session_state["yaml_data"]
    output_name = st.text_input(
        "Output file name",
        value=st.session_state.get("output_name", "cv.yaml"),
        key="output_name_field",
        help="Use a lowercase file name ending in .yaml, such as cv.yaml or cv.yaml.",
    )
    st.session_state["output_name"] = output_name

    st.subheader("Personal info")
    data["name"] = st.text_input("Name", value=str(data.get("name", "")), key="field_name")
    data["phone"] = st.text_input("Phone", value=str(data.get("phone", "")), key="field_phone")
    data["email"] = st.text_input("Email", value=str(data.get("email", "")), key="field_email")
    data["summary"] = st.text_area(
        "Summary",
        value=str(data.get("summary", "")),
        key="field_summary",
        height=150,
    )

    st.subheader("Languages")
    render_simple_list("languages", "Language", "English")

    st.subheader("Experience")
    experience_items = data.get("experience", [])
    for index, item in enumerate(experience_items):
        render_experience_block(index, item)
        if index < len(experience_items) - 1:
            st.markdown("---")
    if st.button("Add experience", key="add_experience"):
        data["experience"].append(
            {
                "company": "",
                "position": "",
                "duration": "",
                "responsibilities": [""],
            }
        )
        st.rerun()

    st.subheader("Education")
    education_items = data.get("education", [])
    for index, item in enumerate(education_items):
        render_education_block(index, item)
        if index < len(education_items) - 1:
            st.markdown("---")
    if st.button("Add education", key="add_education"):
        data["education"].append(
            {
                "institution": "",
                "degree": "",
                "graduation_year": "",
            }
        )
        st.rerun()

    st.subheader("Skills")
    render_simple_list("skills", "Skill", "Python")

    if st.button("Generate YAML", key="generate_yaml"):
        errors = validate_data(data)
        if errors:
            st.error("Please fix the following before saving:\n- " + "\n- ".join(errors))
        else:
            output_name_value = str(output_name).strip()
            if (
                not output_name_value
                or Path(output_name_value).name != output_name_value
                or not output_name_value.endswith(".yaml")
            ):
                st.warning("Use a valid YAML file name, for example: cv.yaml")
            else:
                yaml_text = dump_yaml(data)
                output_path = PROJECT_DIR / output_name_value
                output_path.write_text(yaml_text, encoding="utf-8")
                st.success(f"Saved YAML to {output_path}")
                st.session_state["generated_yaml"] = yaml_text
                st.session_state["saved_file"] = output_path


# Save the YAML file, preview it, and optionally generate the PDF using the existing build script.
def main():
    st.set_page_config(page_title="CV YAML Builder", layout="wide")

    if "yaml_data" not in st.session_state:
        st.session_state["yaml_data"] = build_default_data()
    if "generated_yaml" not in st.session_state:
        st.session_state["generated_yaml"] = dump_yaml(st.session_state["yaml_data"])

    left_column, right_column = st.columns([1.2, 1])
    with left_column:
        render_form()

    with right_column:
        st.subheader("YAML preview")
        preview = dump_yaml(st.session_state["yaml_data"])
        st.code(preview, language="yaml")

        st.subheader("Choose a CV template")
        selected_style = render_template_picker()
        selected_template = next(
            name for name, (style, _description) in TEMPLATE_OPTIONS.items()
            if style == selected_style
        )
        st.caption(TEMPLATE_OPTIONS[selected_template][1])

        load_path = st.text_input(
            "Existing YAML file to load",
            value=str(PROJECT_DIR / "cv.yaml"),
            help="This optional button fills the form from an existing YAML file.",
        )
        if st.button("Load existing YAML"):
            try:
                st.session_state["yaml_data"] = load_existing_data(Path(load_path))
                st.session_state["generated_yaml"] = dump_yaml(st.session_state["yaml_data"])
                st.success(f"Loaded data from {load_path}")
            except FileNotFoundError:
                st.error(f"Could not find the file: {load_path}")

        if st.button("Generate CV"):
            output_path = PROJECT_DIR / st.session_state.get("output_name", "cv.yaml")
            yaml_content = dump_yaml(st.session_state["yaml_data"])
            output_path.write_text(yaml_content, encoding="utf-8")

            if output_path.name != "cv.yaml":
                (PROJECT_DIR / "cv.yaml").write_text(yaml_content, encoding="utf-8")

            try:
                result = subprocess.run(
                    [
                        sys.executable,
                        "build.py",
                        "--template-style",
                        selected_style,
                    ],
                    cwd=PROJECT_DIR,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if result.returncode == 0:
                    clear_cv_yaml(PROJECT_DIR / "cv.yaml")
                    st.success(
                        f"The {selected_template.lower()} CV PDF was generated successfully, "
                        "and cv.yaml was cleared."
                    )
                else:
                    st.error(result.stderr or result.stdout or "The build failed.")
            except FileNotFoundError:
                st.error("Python was not found on the system path.")


if __name__ == "__main__":
    main()
