# api/ai.py
from flask import Blueprint, request, jsonify
import logging

from services.ai.provider import run_ai_task
from services.ai.prompt_builder import (
    build_motion_suggest_prompt,
    build_motion_refine_prompt,
    build_motion_style_prompt,
    build_motion_translation_prompt,
    build_sprite_suggest_prompt,
    build_sprite_refine_prompt,
)

ai_bp = Blueprint("ai", __name__, url_prefix="/api/ai")


# ------------------------------------------------------------
#  MOTION ENDPOINTS
# ------------------------------------------------------------

@ai_bp.post("/motion/suggest")
def motion_suggest():
    data = request.get_json(force=True)
    payload = build_motion_suggest_prompt(
        user_prompt=data.get("prompt", ""),
        preset=data.get("preset", {})
    )
    return jsonify(run_ai_task("motion_suggest", payload))


@ai_bp.post("/motion/refine")
def motion_refine():
    data = request.get_json(force=True)
    payload = build_motion_refine_prompt(
        user_prompt=data.get("prompt", ""),
        existing_motion=data.get("existing_motion", {})
    )
    return jsonify(run_ai_task("motion_refine", payload))


@ai_bp.post("/motion/style")
def motion_style():
    data = request.get_json(force=True)
    payload = build_motion_style_prompt(
        style_name=data.get("style", ""),
        existing_motion=data.get("existing_motion", {})
    )
    return jsonify(run_ai_task("motion_style", payload))


@ai_bp.post("/motion/translate")
def motion_translate():
    data = request.get_json(force=True)
    payload = build_motion_translation_prompt(
        existing_motion=data.get("existing_motion", {}),
        target_language=data.get("target_language", "en")
    )
    return jsonify(run_ai_task("motion_translate", payload))


# ------------------------------------------------------------
#  SPRITE ENDPOINTS
# ------------------------------------------------------------

@ai_bp.post("/sprite/suggest")
def sprite_suggest():
    data = request.get_json(force=True)
    payload = build_sprite_suggest_prompt(
        user_prompt=data.get("prompt", ""),
        preset=data.get("preset", {}),
        reference_descriptions=data.get("reference_descriptions", [])
    )
    return jsonify(run_ai_task("sprite_suggest", payload))


@ai_bp.post("/sprite/refine")
def sprite_refine():
    data = request.get_json(force=True)
    payload = build_sprite_refine_prompt(
        user_prompt=data.get("prompt", ""),
        existing_prompt=data.get("existing_prompt", {}),
        reference_descriptions=data.get("reference_descriptions", [])
    )
    return jsonify(run_ai_task("sprite_refine", payload))


# ------------------------------------------------------------
#  PROVIDER LIST
# ------------------------------------------------------------

@ai_bp.get("/providers")
def providers():
    return jsonify({
        "providers": ["ollama", "groq"],
        "active": "ollama"
    })
