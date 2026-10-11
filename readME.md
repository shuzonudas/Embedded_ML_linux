# Embedded Machine Learning Audio Classification on Linux

A robust, edge-optimized machine learning pipeline deployed on remote Linux audio-recorders to test and evaluate acoustic models in real-world environments. This application continuously processes audio recordings to identify specific acoustic signatures (such as chainsaw sounds), localizes events in time, and automatically archives positive and negative sample classifications for ongoing quality assessment.

## Key Features

* **Remote Edge Deployment:** Designed to run seamlessly on headless Linux audio monitoring hardware for field-testing ML model accuracy.
* **Batch Audio Scanning:** Processes directories of audio recordings automatically to check for target sound events.
* **Sample Archiving (`saved_samples`):** Automatically saves positive and negative inference outputs to dedicated directories for verification and model fine-tuning.

## Repository Structure
```text
Embedded_ML_linux/
│
├── ML_model/                 # Directory containing the machine learning model files
├── saved_samples/            # Archives positive and negative inference output samples
│
├── audio_processing.py       # Handles audio feature extraction and signal preprocessing
├── audio_utility.py          # Utility functions and helper operations for audio handling
├── config.py                 # Global configurations, paths, and model hyperparameters
├── input_handler.py          # Manages incoming streams, batch directories, or audio file inputs
├── main.py                   # Entry point for running the continuous inference pipeline
├── model_engine.py           # Core inference engine loading and executing the ML model
├── readME                    # Documentation and repository overview
├── requirements.txt          # Python dependencies required for the environment
├── sample.wav                # Sample audio file for testing and validation
├── test_audio.py             # Unit/integration tests for audio processing functions
├── test_exit_logic.py        # Tests for loop termination and exit conditions
└── test_model.py             # Validation scripts for model inference and output checks

```

## Getting Started

Follow the instructions below to set up your environment, install dependencies, and run the audio classification pipeline on your system.

### Environment Setup

1. **Create a virtual environment:**
```bash
   python -m venv .venv
```

2. **Activate the virtual environment:**
**Linux:**
```bash
source .venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```
---

### Running the Application

* **Test Audio Functionality:**
To ensure that your input and output audio devices are configured and working properly, run the audio utility script:
```bash
python audio_utility.py

```

* **Run the Main Pipeline:**
```bash
python main.py
```
