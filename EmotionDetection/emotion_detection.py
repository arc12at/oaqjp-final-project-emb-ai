
import requests


def emotion_detector(text_to_analyze):
    """Analyze text and return emotion scores and dominant emotion."""
    empty_result = {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None,
    }

    if not text_to_analyze or not text_to_analyze.strip():
        return empty_result.copy()

    url = (
        "https://sn-watson-emotion.labs.skills.network/"
        "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    )
    headers = {
        "grpc-metadata-mm-model-id":
            "emotion_aggregated-workflow_lang_en_stock"
    }
    payload = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(
            url, headers=headers, json=payload, timeout=5
        )

        if response.status_code == 400:
            return empty_result.copy()

        response.raise_for_status()
        emotions = response.json()["emotionPredictions"][0]["emotion"]

        result = {
            emotion: emotions[emotion]
            for emotion in ("anger", "disgust", "fear", "joy", "sadness")
        }
        result["dominant_emotion"] = max(result, key=result.get)
        return result

    except (requests.RequestException, ValueError, KeyError, IndexError):
        return empty_result.copy()
