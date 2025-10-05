# 🎙️ HMM-Based Speech Recognition on Fruit Voice Dataset

A lightweight **isolated word speech recognition system** built with **Hidden Markov Models (HMMs)** and **MFCC features**. This project demonstrates classical machine learning approaches to speech recognition using a simple fruit voice dataset.


## 🧩 Project Overview

This implementation showcases how HMMs can effectively recognize spoken words by modeling the temporal patterns of speech. Each fruit name (apple, banana, mango, etc.) is represented by its own HMM trained on MFCC features extracted from audio recordings.

### Key Highlights

- 🎯 **100% accuracy** on test dataset
- 🔊 MFCC-based feature extraction
- 📈 Gaussian HMM modeling per word
- 📊 Confusion matrix visualization
- 🎨 MFCC heatmap analysis
- 🚀 Lightweight alternative to deep learning for small datasets


## ⚙️ Features

| Feature | Description |
|---------|-------------|
| **Feature Extraction** | MFCC coefficients computed using `python_speech_features` |
| **Temporal Modeling** | Gaussian HMMs with configurable number of states |
| **Prediction** | Maximum likelihood estimation across all trained models |
| **Evaluation** | Accuracy metrics and confusion matrix |
| **Visualization** | MFCC heatmaps showing temporal patterns |


## 📊 Results

### Performance Metrics

| Metric | Value |
|--------|-------|
| **Accuracy** | 100% |

## 💡 How It Works

### 1. Feature Extraction
Each audio file is converted into a sequence of MFCC vectors representing the spectral characteristics of speech over time.

### 2. HMM Training
For each fruit, an HMM learns the probability distribution of MFCC sequences, capturing:
- State transitions (temporal progression of sounds)
- Emission probabilities (acoustic characteristics)

### 3. Recognition
Given a new recording:
1. Extract MFCCs
2. Compute log-likelihood for each trained HMM
3. Select fruit with highest score
