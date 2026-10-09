"""Classification engine using pre-trained Keras models."""

import numpy as np
from tensorflow import keras

class ClassifierEngine:
  """Wrapper for ML model inference."""

  def __init__(self, model_path: str):
    self.model = keras.models.load_model(model_path)

  def classify(self, features: np.ndarray) -> tuple[str, float]:
    """Runs inference on features and returns (label, confidence)."""
    # Reshape for model (batch, n_mfcc, time, channel)
    input_data = features[np.newaxis, ..., np.newaxis]
    predictions = self.model.predict(input_data)
    
    chainsaw_prob = predictions[0, 0]
    #print(chainsaw_prob)
    label = "Chainsaw Detected" if chainsaw_prob > 0.3 else "No Chainsaw"
    return label, float(chainsaw_prob)
