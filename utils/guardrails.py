

def validate_recommendations(data):
    """
    Manually validates the 'recommendations' payload structure.
    Expects a dict with a 'recommendations' key containing a list of objects
    with 'name' (str), 'artist' (str), and 'explicit' (bool).
    """
    try:
        recommendations = data.get("recommendations", [])
        if not isinstance(recommendations, list):
            raise ValueError("❌ 'recommendations' must be a list.")

        for i, track in enumerate(recommendations):
            if not isinstance(track, dict):
                raise ValueError(f"Track #{i+1} is not a dictionary.")
            if not isinstance(track.get("name"), str):
                raise ValueError(f"Track #{i+1} 'name' must be a string.")
            if not isinstance(track.get("artist"), str):
                raise ValueError(f"Track #{i+1} 'artist' must be a string.")
            if not isinstance(track.get("explicit"), bool):
                raise ValueError(f"Track #{i+1} 'explicit' must be a boolean.")

        return {
            "validated_output": {"recommendations": recommendations},
            "validation_passed": True
        }

    except Exception as e:
        print(f" Validation error: {e}")
        return {
            "validated_output": {},
            "validation_passed": False
        }
