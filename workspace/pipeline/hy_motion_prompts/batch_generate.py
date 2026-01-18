import json
import os

LIB_PATH = "prompt_library.json"
OUTPUT_ROOT = "batch_output"


def load_library(path):
    with open(path, "r") as f:
        return json.load(f)


def build_prompt_block(prompt_dict):
    motion = prompt_dict.get("motion", "")
    style = prompt_dict.get("style", "")
    constraints = prompt_dict.get("constraints", "")
    camera = prompt_dict.get("camera", "")
    output = prompt_dict.get("output", "")

    text = (
        f"MOTION:\n{motion}\n\n"
        f"STYLE:\n{style}\n\n"
        f"CONSTRAINTS:\n{constraints}\n\n"
        f"CAMERA:\n{camera}\n\n"
        f"OUTPUT:\n{output}\n"
    )

    return text


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def write_prompt(text, out_path):
    with open(out_path, "w") as f:
        f.write(text)


def batch_generate():
    library = load_library(LIB_PATH)

    for category, prompts in library.items():
        category_dir = os.path.join(OUTPUT_ROOT, category)
        ensure_dir(category_dir)

        for prompt_key, prompt_dict in prompts.items():
            prompt_dir = os.path.join(category_dir, prompt_key)
            ensure_dir(prompt_dir)

            out_path = os.path.join(prompt_dir, "motion.txt")
            text = build_prompt_block(prompt_dict)
            write_prompt(text, out_path)

            print(f"Generated: {category}/{prompt_key}")


if __name__ == "__main__":
    batch_generate()
