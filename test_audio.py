"""Unit tests for audio processing logic."""

import unittest
import numpy as np
import audio_processing

class TestAudioProcessing(unittest.TestCase):

  def test_mfcc_extraction_shape(self):
    """Verify that MFCC extraction returns correct dimensions."""
    sample_rate = 16000
    dummy_signal = np.random.uniform(-1, 1, sample_rate)
    n_mfcc = 30
    
    features = audio_processing.extract_features(dummy_signal, sample_rate, n_mfcc)
    
    self.assertEqual(features.shape[0], n_mfcc)
    self.assertGreater(features.shape[1], 0)

if __name__ == '__main__':
  unittest.main()
