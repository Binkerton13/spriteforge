# services/ai/prompt_builder.py
"""
Canonical SpriteForge Prompt Builder
Strict JSON-only, reference-aware, and task-specific.

Supports:
  - motion_suggest
  - motion_refine
  - motion_style
  - motion_translate
  - sprite_suggest
  - sprite_refine
"""

import json


def _json(obj):
    """Return compact JSON string with no markdown, no commentary."""
    return json.dumps(obj, ensure_ascii=False)


# ------------------------------------------------------------
#  MOTION PROMPTS
# ------------------------------------------------------------

def build_motion_suggest_prompt(user_prompt: str, preset: dict):
    """
    User gives a rough idea → LLM produces a fully structured,
    segment‑aware motion JSON object.
    """
    payload = {
        "task": "motion_suggest",
        "instructions": {
            "output_format": "strict_json",
            "rules": [
                "Return ONLY valid JSON",
                "No markdown",
                "No commentary",
                "Preserve the full motion schema",
                "Populate ALL segments with meaningful detail",
                "Use the preset as a guide when provided"
            ]
        },
        "input": {
            "user_prompt": user_prompt,
            "preset": preset
        },
        "expected_output": {
            "motion": {
                "overall": "string",
                "segments": {
                    "head": "string",
                    "torso": "string",
                    "arms": "string",
                    "hands": "string",
                    "legs": "string",
                    "feet": "string"
                },
                "timing": {
                    "beats": "string",
                    "phases": "string",
                    "duration": "number"
                },
                "style": {
                    "primary": "string",
                    "secondary": "string",
                    "notes": "string"
                },
                "constraints": {
                    "physical": "string",
                    "camera": "string",
                    "notes": "string"
                }
            }
        }
    }
    return payload


def build_motion_refine_prompt(user_prompt: str, existing_motion: dict):
    """
    Refine an existing structured motion object while preserving
    the full schema and all segment fields.
    """
    payload = {
        "task": "motion_refine",
        "instructions": {
            "output_format": "strict_json",
            "rules": [
                "Preserve the full motion schema",
                "Do not remove any fields",
                "Improve clarity and detail",
                "No markdown",
                "No commentary"
            ]
        },
        "input": {
            "user_prompt": user_prompt,
            "existing_motion": existing_motion
        },
        "expected_output": {
            "motion": existing_motion
        }
    }
    return payload


def build_motion_style_prompt(style_name: str, existing_motion: dict):
    """
    Apply a style to a structured motion object while preserving
    all segments, timing, and constraints.
    """
    payload = {
        "task": "motion_style",
        "instructions": {
            "output_format": "strict_json",
            "rules": [
                "Apply the style to the motion",
                "Preserve the full motion schema",
                "Do not remove any fields",
                "Modify segment descriptions only when appropriate",
                "No markdown"
            ]
        },
        "input": {
            "style": style_name,
            "existing_motion": existing_motion
        },
        "expected_output": {
            "motion": existing_motion
        }
    }
    return payload


def build_motion_translation_prompt(existing_motion: dict, target_language: str):
    """
    Translate all text fields in the structured motion object while
    preserving the schema and all non-text values.
    """
    payload = {
        "task": "motion_translate",
        "instructions": {
            "output_format": "strict_json",
            "rules": [
                "Translate ONLY text fields",
                "Preserve the full motion schema",
                "Do not modify numeric values",
                "Do not remove any fields",
                "No markdown"
            ]
        },
        "input": {
            "existing_motion": existing_motion,
            "target_language": target_language
        },
        "expected_output": {
            "motion": existing_motion
        }
    }
    return payload


# ------------------------------------------------------------
#  SPRITE PROMPTS (NEW)
# ------------------------------------------------------------

def build_sprite_suggest_prompt(user_prompt: str, preset: dict, reference_descriptions: list):
    """
    User gives a rough sprite idea → LLM produces structured sprite prompt JSON.
    """
    payload = {
        "task": "sprite_suggest",
        "instructions": {
            "output_format": "strict_json",
            "rules": [
                "No markdown",
                "No commentary",
                "Return only JSON",
                "Incorporate reference image descriptions"
            ]
        },
        "input": {
            "user_prompt": user_prompt,
            "preset": preset,
            "reference_descriptions": reference_descriptions
        },
        "expected_output": {
            "sprite_prompt": {
                "description": "string",
                "style": "string",
                "lighting": "string",
                "palette": [],
                "details": []
            }
        }
    }
    return payload


def build_sprite_refine_prompt(user_prompt: str, existing_prompt: dict, reference_descriptions: list):
    """
    Refine a sprite prompt using:
      - user text
      - existing prompt
      - reference image descriptors
    """
    payload = {
        "task": "sprite_refine",
        "instructions": {
            "output_format": "strict_json",
            "rules": [
                "Preserve structure",
                "Improve clarity",
                "Use reference image descriptions",
                "No markdown",
                "No commentary"
            ]
        },
        "input": {
            "user_prompt": user_prompt,
            "existing_prompt": existing_prompt,
            "reference_descriptions": reference_descriptions
        },
        "expected_output": {
            "sprite_prompt": existing_prompt
        }
    }
    return payload
