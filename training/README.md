# Spam Detection Model Training

## Quick Start

### 1. Setup Environment
```bash
# Create virtual environment (from project root)
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
cd training
pip install -r requirements.txt
```

### 2. Generate Training Data
```bash
# Create 210 labeled job examples
python create_large_dataset.py

# Output: data/large_dataset.csv
# Contains: 60 spam, 40 poor, 70 good, 40 excellent jobs
```

### 3. Train Model
```bash
# Train LSTM spam detector
python train_spam_detector.py

# Model saved to: models/spam_detector/
# Files: keras_model.keras, tokenizer.json, metadata.json
```

### 4. Integrate Into Extension
```bash
# Copy model files to extension
python convert_to_tfjs.py

# Rebuild extension
cd ..
npm run build
```

## Training Scripts

### `create_large_dataset.py`
Generates synthetic training data with realistic spam patterns:
- Phone numbers and email addresses
- Messaging app mentions (WhatsApp, Telegram)
- Urgency tactics and excessive punctuation
- Payment keyword abuse
- Various job quality levels

### `train_spam_detector.py`
Trains Bidirectional LSTM model:
- Input: Job title + description text
- Architecture: Embedding → BiLSTM(64) → BiLSTM(32) → Dense(32) → Output
- Output: Binary classification (spam/not spam)
- Exports: Keras model, tokenizer, and metadata

### `convert_to_tfjs.py`
Converts model for browser deployment:
- Attempts TensorFlow.js conversion
- Falls back to copying Keras model if conversion fails
- Copies tokenizer and metadata files to extension

## Model Performance

**Current Version (v2.0)**
- **Accuracy**: 100% on test set (32 samples)
- **Training Data**: 210 labeled jobs
  - 60 spam (28.6%)
  - 150 legitimate (71.4%)
- **Vocabulary**: 569 unique words
- **Sequence Length**: 200 tokens
- **Model Size**: 9.5 MB (Keras)

## Directory Structure

```
training/
├── requirements.txt              # Python dependencies
├── train_spam_detector.py        # Main training script
├── create_large_dataset.py       # Synthetic data generation
├── convert_to_tfjs.py            # Model conversion for extension
├── export_model.py               # Legacy export utilities
├── data/
│   ├── large_dataset.csv         # 210 labeled jobs
│   └── sample_jobs.csv           # Initial 24-job sample
├── models/
│   └── spam_detector/
│       ├── keras_model.keras     # Trained LSTM model
│       ├── tokenizer.json        # Word tokenizer
│       └── metadata.json         # Training metadata
└── TRAINING_REPORT_V2.md         # Detailed training documentation
```

## Custom Training

### Using Your Own Data

Create CSV with required columns:
```csv
job_id,title,description,quality_label
1,"Job Title","Job description text","spam"
2,"Another Job","Description...","good"
```

Labels: `spam`, `poor`, `good`, `excellent`

Then train:
```bash
python train_spam_detector.py --data your_data.csv
```

### Adjusting Model Parameters

Edit `train_spam_detector.py`:

```python
# Model hyperparameters (line ~40)
self.max_sequence_length = 200    # Token sequence length
self.max_words = 5000              # Vocabulary size
self.embedding_dim = 128           # Word embedding dimensions
lstm_units_1 = 64                  # First BiLSTM layer
lstm_units_2 = 32                  # Second BiLSTM layer
```

## Requirements

- Python 3.13+
- TensorFlow 2.20+
- Keras 3.13+
- pandas, numpy, scikit-learn
- tensorflowjs (optional, for conversion)

See `requirements.txt` for complete list.

## Troubleshooting

**TensorFlow.js conversion fails**
- Expected: tensorflow_decision_forests dependency issue
- Solution: Model still copied, can be used with fallback loading

**Low accuracy**
- Increase training data size (aim for 500+ examples)
- Balance class distribution (equal spam/non-spam)
- Adjust model architecture or hyperparameters

**Out of memory**
- Reduce batch_size in train() method
- Reduce max_sequence_length or max_words
- Use smaller LSTM units

## Next Steps

1. Collect real Upwork job data for training
2. Implement user feedback collection
3. Retrain model periodically with new examples
4. A/B test model vs rule-based detection

For detailed training documentation, see [TRAINING_REPORT_V2.md](TRAINING_REPORT_V2.md).

## Best Practices

1. **Data Quality**
   - Follow labeling guidelines strictly
   - Review labels periodically for consistency
   - Aim for balanced dataset across quality tiers

2. **Version Control**
   - Commit dataset regularly
   - Tag model versions
   - Document changes in training approach

3. **Privacy**
   - Anonymize all personal information
   - Don't include client names or identifying details
   - Only store job descriptions and metadata

4. **Validation**
   - Hold out 20% of data for validation
   - Test model on real Upwork jobs before deployment
   - Monitor prediction accuracy continuously

## Troubleshooting

### TensorFlow Installation Issues

If TensorFlow installation fails:
```bash
# Try CPU-only version
pip install tensorflow-cpu
```

### Memory Errors During Training

Reduce batch size in training scripts or close other applications.

### Model Export Errors

Ensure model is saved in Keras format (.h5) or SavedModel directory format.

## Next Steps

**Phase 2 (Current):**
- [ ] Collect 100 labeled jobs
- [ ] Validate data quality
- [ ] Create dummy model for testing
- [ ] Test export pipeline

**Phase 3 (Next):**
- [ ] Train spam detector model
- [ ] Achieve >85% accuracy
- [ ] Export and integrate into extension

**Phase 4 (Future):**
- [ ] Collect 300+ additional labels
- [ ] Train quality classifier
- [ ] Implement ensemble scoring

---

For questions or issues, see the main project README.
