import openai
import json
from config import OPENAI_API_KEY, MODEL_NAME
from utils import encode_image

openai.api_key = OPENAI_API_KEY

def analyze_images(claim_text, image_paths, object_type):
    system_prompt = (
        "You are an expert claims verifier. Given a claim description and images, "
        "decide if the images support, contradict, or are insufficient. "
        "Provide a JSON response with fields: "
        "decision (supported/contradicted/insufficient), "
        "visible_issue_type (string), "
        "relevant_object_part (string), "
        "supporting_image_ids (list of integers or empty), "
        "quality_risk (boolean), mismatch_risk (boolean), authenticity_risk (boolean), "
        "user_history_risk (boolean), severity (low/medium/high), "
        "justification (string)."
    )

    image_contents = []
    for idx, path in enumerate(image_paths):
        b64 = encode_image(path)
        image_contents.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{b64}"}
        })

    user_content = [
        {"type": "text", "text": f"Claim: {claim_text}\nObject type: {object_type}"}
    ] + image_contents

    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        max_tokens=500,
        temperature=0.0,
        response_format={"type": "json_object"}  # if supported; if not, remove and parse manually
    )

    try:
        result = json.loads(response.choices[0].message.content)
    except:
        result = {"error": "Could not parse JSON"}
    return result
