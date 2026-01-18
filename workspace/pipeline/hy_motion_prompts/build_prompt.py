import json
import sys
import os

# ------------------------------------------------------------
# Usage:
# python build_prompt.py locomotion walk_cycle
#
# This loads:
#   prompt_library.json
# Selects:
#   category = locomotion
#   prompt_key = walk_cycle
# Builds:
#   motion.txt (final assembled prompt)
# ------------------------------------------------------------

LIB_PATH = "prompt_library.json"
OUTPUT_PATH = "motion.txt"


def load_library(path):
    with open(path, "r") as f:
        return json.load(f)


def build_prompt_block(prompt_dict):
    """
    Assembles the 5-field HY-Motion prompt into a single text block.
    """
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


def write_prompt(text, path):
    with open(path, "w") as f:
        f.write(text)
    print(f"Prompt written to {path}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python build_prompt.py <category> <prompt_key>")
        sys.exit(1)

    category = sys.argv[1]
    prompt_key = sys.argv[2]

    library = load_library(LIB_PATH)

    if category not in library:
        print(f"Category '{category}' not found.")
        sys.exit(1)

    if prompt_key not in library[category]:
        print(f"Prompt '{prompt_key}' not found in category '{category}'.")
        sys.exit(1)

    prompt_dict = library[category][prompt_key]
    final_text = build_prompt_block(prompt_dict)
    write_prompt(final_text, OUTPUT_PATH)


if __name__ == "__main__":
    main()
