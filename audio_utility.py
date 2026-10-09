import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile

input_device_id = 2
output_device_id = 5

def show_devices():
    print("\n--- Available Audio Devices ---")
    print(sd.query_devices())
    print("-------------------------------\n")

def select_input_device():
    global input_device_id
    try:
        input_device_id = int(input("Enter the ID of the input device: "))
        #sd.default.device[0] = device_id
        print(f"Input device set to: {input_device_id}")
    except Exception as e:
        print(f"Error selecting input device: {e}")

def select_output_device():
    global output_device_id
    try:
        output_device_id = int(input("Enter the ID of the output device: "))
        #sd.default.device[1] = device_id
        print(f"Output device set to: {output_device_id}")
    except Exception as e:
        print(f"Error selecting output device: {e}")


def show_current_selection():
    global output_device_id
    global input_device_id
    devices = sd.query_devices()

    print("\n--- Current Selection ---")

    try:
        in_name = devices[input_device_id]["name"]
        print(f"Input Device:  ID {input_device_id} ({in_name})")
    except (IndexError, KeyError):
        print(f"Input Device:  ID {input_device_id} (Not Found)")

    try:
        out_name = devices[output_device_id]["name"]
        print(f"Output Device: ID {output_device_id} ({out_name})")
    except (IndexError, KeyError):
        print(f"Output Device: ID {output_device_id} (Not Found)")

    print("-------------------------\n")


def record_and_playback():
    global output_device_id
    global input_device_id
    fs = 16000  # Sample rate
    duration = 5  # Seconds
    print(f"\nRecording for {duration} seconds...")
    try:
        # Record in mono (channels=1)
        sd.default.device = input_device_id
        device_info = sd.query_devices(input_device_id)
        max_input_channels = device_info['max_input_channels']
        print(f"Recording on device '{device_info['name']}' ({max_input_channels} channels)...")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        print("Recording complete.")
        
        # Check output device channels to ensure mono plays on stereo
        sd.default.device = output_device_id
        device_info = sd.query_devices(output_device_id)
        max_out_channels = device_info['max_output_channels']
        
        print(f"Playing back on device '{device_info['name']}' ({max_out_channels} channels)...")
        
        # If the output device is stereo (or more) and we have mono data, 
        # duplicate the channel to ensure it plays on both speakers.
        if max_out_channels >= 2:
            playback_data = np.tile(recording, (1, 2))
        else:
            playback_data = recording
            
        sd.play(playback_data, fs)
        sd.wait()
        print("Playback complete.\n")
        # signal_squeezed = np.squeeze(playback_data)
        # wavfile.write("sample.wav", fs, signal_squeezed)
        # print("File save complete!.\n")
        
    except Exception as e:
        print(f"An error occurred during record/playback: {e}")
        print("Tip: Make sure you selected valid input and output devices.")




def main_menu():
    while True:
        print("\n=== Audio Device Utility ===")
        print("1. Show all audio devices")
        print("2. Select input device")
        print("3. Select output device")
        print("4. Show currently selected devices")
        print("5. Record 5 seconds and play back")
        print("6. Quit")
        
        choice = input("Select an option (1-6): ")
        
        if choice == '1':
            show_devices()
        elif choice == '2':
            select_input_device()
        elif choice == '3':
            select_output_device()
        elif choice == '4':
            show_current_selection()
        elif choice == '5':
            record_and_playback()
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
