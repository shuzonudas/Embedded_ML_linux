import logging
import threading
import config
import audio_processing
import model_engine
import input_handler
from scipy.signal import resample
import numpy as np
import scipy.io.wavfile as wavfile
import sounddevice as sd

audio  = np.array([])

def run_detection():
  """Main loop for capturing and classifying audio."""
  logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
  
  stop_event = threading.Event()
  listener = threading.Thread(target=input_handler.listener_thread, args=(stop_event,), daemon=True)
  listener.start()

  try:
    engine = model_engine.ClassifierEngine(config.MODEL_PATH)
    logging.info("Model loaded. Starting monitoring. Press ANY key to stop.")
  except Exception as e:
    logging.error("Failed to initialize system: %s", e)
    returnl

  while not stop_event.is_set():
    try:
      audio = audio_processing.capture_audio(config.DURATION_SECONDS, 44100)
      # Linux can not capture audio at a specific sample rate.
      # So we capture at 44100 and then convert is to 16000 (16k, 3 sec)
      # It is suitable for both linux and windows!
      audio_16k = np.squeeze(resample(audio, 48000))
      features = audio_processing.extract_features(audio_16k, config.SAMPLE_RATE, config.N_MFCC)
      label, confidence = engine.classify(features)     
      logging.info("Result: %s (Confidence: %.2f)", label, confidence)
      # saving some audio
      audio_processing.save_classified_sample(audio_16k,config.SAMPLE_RATE,label, max_samples = 10)
      if stop_event.wait(timeout=1):
        break

    except KeyboardInterrupt:
      logging.info("System stopped by user.")
      print("\n[!] Manual stop via Ctrl+C.")
      break

if __name__ == "__main__":
  audio_processing.list_audio_devices()
  run_detection()
