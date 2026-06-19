from image_analyzer import analyze_images
from utils import append_log
from config import LOG_FILE, IMAGES_DIR

def process_claim(row):
    claim_id = row.get("claim_id")
    conversation = row.get("conversation", "")
    object_type = row.get("object_type", "unknown")
    image_ids_str = row.get("image_ids", "")
    image_ids = [int(x.strip()) for x in image_ids_str.split(",") if x.strip()]
    
    # Build image paths – adjust if images have a different naming convention
    image_paths = [f"{IMAGES_DIR}/{img_id}.jpg" for img_id in image_ids]
    # If some images are .png or in subfolders, you may need to handle that.

    # For simplicity, use whole conversation as claim text.
    claim_text = conversation

    analysis = analyze_images(claim_text, image_paths, object_type)

    output_row = {
        "claim_id": claim_id,
        "decision": analysis.get("decision", "insufficient"),
        "visible_issue_type": analysis.get("visible_issue_type", ""),
        "relevant_object_part": analysis.get("relevant_object_part", ""),
        "supporting_image_ids": ",".join(map(str, analysis.get("supporting_image_ids", []))),
        "quality_risk": str(analysis.get("quality_risk", False)).lower(),
        "mismatch_risk": str(analysis.get("mismatch_risk", False)).lower(),
        "authenticity_risk": str(analysis.get("authenticity_risk", False)).lower(),
        "user_history_risk": str(analysis.get("user_history_risk", False)).lower(),
        "severity": analysis.get("severity", "medium"),
        "justification": analysis.get("justification", "")
    }

    # Log the interaction (for chat transcript)
    log_entry = {
        "claim_id": claim_id,
        "input_conversation": conversation,
        "image_paths": image_paths,
        "analysis": analysis
    }
    append_log(log_entry, LOG_FILE)

    return output_row
