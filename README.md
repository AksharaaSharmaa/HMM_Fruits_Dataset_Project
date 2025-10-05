# 🔊 HMM-Based Speech Recognition & Pronunciation Generator

A comprehensive NLP project combining speech recognition and pronunciation generation using Hidden Markov Models (HMMs).

## 🧩 Project Overview

This implementation showcases two powerful applications of HMMs in speech processing:

1. **Speech Recognition**: Recognizes isolated words using MFCC features and HMM modeling
2. **Pronunciation Generator**: Generates phonetic representations and audio pronunciations for words

## 🚀 Key Features

### Speech Recognition System
- 🎯 **100% accuracy** on fruit voice dataset test set
- 🔊 MFCC-based feature extraction
- 📈 Gaussian HMM modeling per word
- 📊 Confusion matrix visualization
- 🎨 MFCC heatmap analysis
- 🚀 Lightweight alternative to deep learning for small datasets

### Pronunciation Generator
- 🗣️ Phoneme extraction using eSpeak NG
- 🧠 HMM-based phoneme learning and prediction
- 🔄 Training on custom word datasets
- 🎵 Audio pronunciation generation
- 🌐 Web interface for easy interaction

## ⚙️ Features

| Feature | Description |
|---------|-------------|
| **Speech Recognition** | |
| Feature Extraction | MFCC coefficients computed using `python_speech_features` |
| Temporal Modeling | Gaussian HMMs with configurable number of states |
| Prediction | Maximum likelihood estimation across all trained models |
| Evaluation | Accuracy metrics and confusion matrix |
| Visualization | MFCC heatmaps showing temporal patterns |
| **Pronunciation Generator** | |
| Phoneme Extraction | Uses eSpeak NG to extract phonetic representations |
| HMM Learning | Learns phoneme patterns from training data |
| Audio Generation | Generates audio pronunciations for any word |
| Web Interface | FastAPI-based web interface for easy interaction |

## 📊 Results

### Performance Metrics

| Metric | Value |
|--------|-------|
| Speech Recognition Accuracy | 100% |
| Phoneme Extraction Success | Varies by language |

## 💡 How It Works

### Speech Recognition

1. **Feature Extraction**
   - Each audio file is converted into a sequence of MFCC vectors representing the spectral characteristics of speech over time.

2. **HMM Training**
   - For each word (fruit), an HMM learns the probability distribution of MFCC sequences, capturing:
     - State transitions (temporal progression of sounds)
     - Emission probabilities (acoustic characteristics)

3. **Recognition**
   - Given a new recording:
     - Extract MFCCs
     - Compute log-likelihood for each trained HMM
     - Select word with highest score

### Pronunciation Generator

1. **Phoneme Extraction**
   - Uses eSpeak NG to extract phonetic representations of words
   - Builds a database of word-to-phoneme mappings

2. **HMM Learning**
   - Learns patterns between graphemes (letters) and phonemes (sounds)
   - Builds statistical models of phoneme sequences

3. **Pronunciation Generation**
   - For unseen words:
     - Predicts phoneme representation using learned patterns
     - Generates audio using eSpeak NG

## 🔄 From Recognition to Generation

By training on a fruit dataset for speech recognition, the system learns the acoustic patterns of speech. This knowledge is then leveraged to generate pronunciations for unseen words by:

1. **Pattern Recognition**: Understanding how phonemes map to acoustic features
2. **Statistical Modeling**: Using HMMs to capture the temporal dynamics of speech
3. **Generalization**: Applying learned patterns to new, unseen words
4. **Audio Synthesis**: Generating audio based on predicted phoneme sequences

This bidirectional approach (recognition → generation) demonstrates the versatility of HMM-based approaches in speech processing tasks.

## 🛠️ Installation & Usage

### Prerequisites
- Python 3.6+
- eSpeak NG installed on your system

### Installation
```bash
pip install -r requirements.txt
```

### Running the Pronunciation Generator
```bash
python app.py
```
Access the web interface at http://localhost:8001

### Running Speech Recognition
```bash
cd speech-recognition-hmm/isolated_word_recognition
python fruits_speech_recognition.py
```

## 📚 Technologies Used

- FastAPI for web API
- Uvicorn for ASGI server
- eSpeak NG for text-to-speech
- HMM algorithms for both recognition and generation
- MFCC feature extraction for speech processing

## 🔮 Future Work

- Integration of both systems into a unified interface
- Support for more languages and accents
- Improved phoneme prediction for complex words
- Real-time speech recognition capabilities
