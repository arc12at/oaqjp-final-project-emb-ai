
import unittest
from unittest.mock import patch, Mock

from EmotionDetection import emotion_detector


class TestEmotionDetector(unittest.TestCase):
    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_dominant_anger(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "emotionPredictions": [
                {
                    "emotion": {
                        "anger": 0.9,
                        "disgust": 0.1,
                        "fear": 0.2,
                        "joy": 0.05,
                        "sadness": 0.3,
                    }
                }
            ]
        }
        mock_post.return_value = mock_response

        result = emotion_detector("I am really mad about this")

        self.assertEqual(result["dominant_emotion"], "anger")
        self.assertEqual(result["anger"], 0.9)

    def test_blank_input(self):
        result = emotion_detector("   ")
        self.assertIsNone(result["dominant_emotion"])

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_http_400(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        result = emotion_detector("Invalid input")
        self.assertIsNone(result["dominant_emotion"])


if __name__ == "__main__":
    unittest.main()
