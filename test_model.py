"""Unit tests for the classification engine."""

import unittest
from unittest.mock import MagicMock, patch
import numpy as np
import model_engine

class TestModelEngine(unittest.TestCase):

  @patch('model_engine.keras.models.load_model')
  def test_inference_logic(self, mock_load):
    """Verify that inference correctly interprets model output."""
    mock_model = MagicMock()
    # Mocking a 'chainsaw detected' output
    mock_model.predict.return_value = np.array([[0.9, 0.1]])
    mock_load.return_value = mock_model
    
    engine = model_engine.ClassifierEngine("mock.keras")
    dummy_input = np.zeros((30, 100))
    
    label, confidence = engine.classify(dummy_input)
    
    self.assertEqual(label, "Chainsaw Detected")
    self.assertGreater(confidence, 0.5)

if __name__ == '__main__':
  unittest.main()
