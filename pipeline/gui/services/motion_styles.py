# services/motion_styles.py
"""
SpriteForge – Motion Style System
---------------------------------
Defines built‑in motion style presets and helpers for applying them
to motion JSON structures.

Unlike sprite styles, motion styles are NOT project‑scoped assets.
They are global presets that influence:
- exaggeration
- timing
- weight
- arcs
- stylization
- anticipation / overshoot
- squash / stretch
"""

import copy


# ---------------------------------------------------------
# 1. Built‑in motion style presets
# ---------------------------------------------------------

MOTION_STYLE_PRESETS = {
    "neutral": {
        "exaggeration": 0.0,
        "timing": "balanced",
        "weight": "medium",
        "notes": "Default balanced motion with no stylistic bias."
    },

    "fluid": {
        "exaggeration": 0.2,
        "timing": "smooth",
        "weight": "light",
        "arcs": "emphasized",
        "notes": "Continuous arcs, gentle transitions, flowing movement."
    },

    "snappy": {
        "exaggeration": 0.4,
        "timing": "fast transitions",
        "weight": "medium",
        "anticipation": "strong",
        "overshoot": "strong",
        "notes": "Punchy timing with sharp transitions and strong posing."
    },

    "weighty": {
        "exaggeration": 0.3,
        "timing": "slow transitions",
        "weight": "heavy",
        "notes": "Slower, grounded motion with a sense of mass."
    },

    "cartoony": {
        "exaggeration": 0.6,
        "timing": "elastic",
        "squash_stretch": "strong",
        "anticipation": "exaggerated",
        "overshoot": "exaggerated",
        "notes": "Highly expressive, exaggerated, animation‑style motion."
    },

    "chibi": {
        "exaggeration": 0.5,
        "timing": "bouncy",
        "weight": "light",
        "squash_stretch": "medium",
        "notes": "Cute, bouncy, stylized motion with small proportions."
    },
}


# ---------------------------------------------------------
# 2. Utility: deep merge dictionaries
# ---------------------------------------------------------

def deep_merge(base: dict, override: dict) -> dict:
    """
    Recursively merge two dictionaries.
    Values in 'override' take precedence.
    """
    result = copy.deepcopy(base)

    for key, value in override.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)

    return result


# ---------------------------------------------------------
# 3. List available motion styles
# ---------------------------------------------------------

def list_motion_styles():
    """
    Returns a list of available motion style names.
    """
    return sorted(MOTION_STYLE_PRESETS.keys())


# ---------------------------------------------------------
# 4. Apply a motion style to a motion JSON structure
# ---------------------------------------------------------

def apply_motion_style(fields: dict, style_name: str) -> dict:
    """
    Merge a motion style preset into an existing motion JSON structure.

    Parameters:
        fields (dict): The existing motion JSON.
        style_name (str): The style preset name.

    Returns:
        dict: A new motion JSON with style applied.
    """
    preset = MOTION_STYLE_PRESETS.get(style_name)
    if not preset:
        return fields  # unknown style → no change

    return deep_merge(fields, preset)
