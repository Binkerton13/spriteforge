# Exhibition/pipeline/tools/hy_motion.py

import sys
from pathlib import Path

# Add HY-Motion repo to Python path
sys.path.append("/workspace/hy-motion")

from inference import HunyuanMotionPipeline


def generate_animation(prompt_path: str, output_path: str):
    """
    Generates animation using HY-Motion Python API.
    """
    prompt_text = Path(prompt_path).read_text()

    print("\n[HY-MOTION] Loading pipeline...")
    pipe = HunyuanMotionPipeline.from_pretrained(
        "/workspace/hy-motion",
        torch_dtype="float16",
        device="cuda"
    )

    print("[HY-MOTION] Generating animation...")
    result = pipe(
        prompt=prompt_text,
        output_path=output_path
    )

    print(f"[✔] HY-Motion animation saved to: {output_path}")
    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--output", required=True)

    args = parser.parse_args()
    generate_animation(args.prompt, args.output)
