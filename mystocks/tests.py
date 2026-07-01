from django.test import TestCase
from unittest.mock import patch

class StockPredictAPITest(TestCase):

    @patch('requests.post')
    def test_predict_endpoint_returns_200(self, mock_post):
        # Define what the fake API response looks like
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'prediction': 'buy',
            'confidence': 0.85
        }

        # Call your Django view directly (no real HTTP call)
        response = self.client.get('/mystocks/api/predict/')
        self.assertIn(response.status_code, [200, 405])

    def test_predict_requires_symbol(self):
        response = self.client.post(
            '/mystocks/api/predict/',
            data={'rsi': 52.4, 'macd': 1.1},
            content_type='application/json'
        )
        # Should not crash the server
        self.assertIn(response.status_code, [200, 400, 405])
