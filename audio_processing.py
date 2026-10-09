"""Library for audio capture and feature extraction."""

import librosa
import numpy as np
import sounddevice as sd
import os
import scipy.io.wavfile as wavfile
import config

def extract_features(signal: np.ndarray, sr: int, n_mfcc: int) -> np.ndarray:
  """
  Converts raw audio to MFCC features.
  Args: 
    signal: 1D data array.
    sr: Sample rate.
    n_mfcc: Filter bank.
  Returns: 
    np.ndarray: A 2D array of MFCC features.
  """
  return librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=n_mfcc)


def capture_audio(duration: float, sr: int) -> np.ndarray:
  """
  Records audio from the default input device.
    Args:
      duration: The audio duration.
      sr: Sample rate.
    Returns:
      np.ndarray: An 1D array of audio data.
  """
  recording = np.array([])
  sd.default.device = config.INPUT_DEVICE_ID
  recording = sd.rec(int(duration * sr), samplerate=sr, channels=1)
  sd.wait()
#  sd.default.device = 4
#  sd.play(recording, 48000)
#  sd.wait()
#  return np.squeeze(recording)
  return (recording)


def list_audio_devices() -> None:
    """
    This function lists all the audio devices present on the system.
    Args: None.
    Returns: None.
    """
    devices = sd.query_devices()
    for index, device in enumerate(devices):
        print(f"Device {index}:")
        print(f"  Name: {device['name']}")
        print(f"  Input Channels: {device['max_input_channels']}")
        print(f"  Output Channels: {device['max_output_channels']}")
        print(f"  Default Sample Rate: {device['default_samplerate']}")
        print()



def save_classified_sample(signal: np.ndarray,sr: int, label: str, base_dir: str = "saved_samples",max_samples: int = 5) -> None:
    """
    Saves the classified audio signal as a WAV file in a folder named after the label.
    Ensures that no more than max_samples are stored in the folder.
    """
    # Clean up the label for a valid directory name
    safe_label = "".join([c for c in label if c.isalnum() or c.isspace() or c == '_']).strip()
    class_dir = os.path.join(base_dir, safe_label)
    
    try:
        os.makedirs(class_dir, exist_ok=True)
    except Exception as e:
        import logging
        logging.error("Failed to create directory %s: %s", class_dir, e)
        return

    # Count existing .wav files in the class folder
    try:
        existing_files = [f for f in os.listdir(class_dir) if f.endswith(".wav")]
    except Exception as e:
        import logging
        logging.error("Failed to list directory %s: %s", class_dir, e)
        return

    if len(existing_files) >= max_samples:
        return

    # Find the next available sequential index
    index = 1
    while True:
        filename = f"sample_{index:03d}.wav"
        file_path = os.path.join(class_dir, filename)
        if not os.path.exists(file_path):
            break
        index += 1
        if index > max_samples + 10:
            break

    # Save signal to WAV file
    try:
        signal_squeezed = np.squeeze(signal)
        wavfile.write(file_path, sr, signal_squeezed)
        import logging
        logging.info("Saved sample to %s (Total saved: %d/%d)", file_path, len(existing_files) + 1, max_samples)
    except Exception as e:
        import logging
        logging.error("Failed to save audio sample to %s: %s", file_path, e)
