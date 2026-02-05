# services/ai/utils.py
import json

def extract_json_objects(text: str):
    objs = []
    depth = 0
    start = None

    for i, ch in enumerate(text):
        if ch == '{':
            if depth == 0:
                start = i
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0 and start is not None:
                chunk = text[start:i+1]
                try:
                    objs.append(json.loads(chunk))
                except Exception:
                    pass
                start = None

    return objs


def extract_best_json(text: str):
    objs = extract_json_objects(text)
    if not objs:
        raise ValueError("No valid JSON found in AI output")

    return max(objs, key=lambda o: len(o.keys()))
