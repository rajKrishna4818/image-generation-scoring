import os
import random

def score_creative(image_path, criteria):
    """
    Dummy scoring logic for the creative.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError("Image not found for scoring.")
    
    # Randomized scoring logic for demonstration
    scoring = {k: random.randint(15, v) for k, v in criteria.items()}
    scoring["total_score"] = sum(scoring.values())
    return scoring
