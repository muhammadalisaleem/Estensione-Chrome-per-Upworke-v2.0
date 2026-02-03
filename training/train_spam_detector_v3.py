"""
Train Spam Detection Model on 12K+ Job Postings
Uses Employment Scam Aegean Dataset
Improved version with larger dataset for better accuracy
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['PYTHONIOENCODING'] = 'utf-8'

import sys
import io
# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.utils import class_weight

print("Loading TensorFlow and Keras...")
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

# Configuration
MAX_WORDS = 10000  # Increased vocabulary for larger dataset
MAX_SEQUENCE_LENGTH = 250  # Slightly longer sequences
EMBEDDING_DIM = 128
LSTM_UNITS_1 = 64
LSTM_UNITS_2 = 32
DENSE_UNITS = 32
DROPOUT_RATE = 0.4  # Higher dropout for larger dataset
EPOCHS = 30
BATCH_SIZE = 64  # Larger batch for 12K dataset
VALIDATION_SPLIT = 0.15

TRAINING_DIR = Path(__file__).parent
DATA_DIR = TRAINING_DIR / "data"
MODELS_DIR = TRAINING_DIR / "models" / "spam_detector_v3"

def load_and_preprocess_data():
    """Load the 12K+ job postings dataset"""
    
    print("\n" + "=" * 70)
    print("LOADING DATASET")
    print("=" * 70)
    
    csv_path = DATA_DIR / "fake_job_postings.csv"
    
    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found: {csv_path}")
    
    # Load dataset
    print(f"\n📂 Loading data from: {csv_path}")
    df = pd.read_csv(csv_path)
    
    print(f"✅ Loaded {len(df):,} job postings")
    print(f"\n📊 Dataset info:")
    print(f"   Columns: {list(df.columns)}")
    print(f"   Memory: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
    
    # Check fraudulent distribution
    fraud_counts = df['fraudulent'].value_counts()
    print(f"\n📈 Class distribution:")
    print(f"   Legitimate (0): {fraud_counts[0]:,} ({fraud_counts[0]/len(df)*100:.1f}%)")
    print(f"   Fraudulent (1): {fraud_counts[1]:,} ({fraud_counts[1]/len(df)*100:.1f}%)")
    print(f"   Imbalance ratio: 1:{fraud_counts[0]/fraud_counts[1]:.1f}")
    
    # Combine title and description (like Upwork job display)
    print(f"\n🔄 Preprocessing text...")
    df['text'] = df['title'].fillna('') + ' ' + df['description'].fillna('')
    
    # Remove very short texts (likely corrupted data)
    min_length = 20
    df = df[df['text'].str.len() >= min_length].copy()
    print(f"✅ Filtered to {len(df):,} jobs (removed < {min_length} chars)")
    
    # Extract features
    X = df['text'].values
    y = df['fraudulent'].values
    
    # Show sample
    print(f"\n📝 Sample legitimate job:")
    legit_sample = df[df['fraudulent'] == 0].iloc[0]
    print(f"   Title: {legit_sample['title'][:80]}...")
    print(f"   Description: {legit_sample['description'][:100]}...")
    
    print(f"\n🚨 Sample fraudulent job:")
    fraud_sample = df[df['fraudulent'] == 1].iloc[0]
    print(f"   Title: {fraud_sample['title'][:80]}...")
    print(f"   Description: {fraud_sample['description'][:100]}...")
    
    return X, y, df

def create_tokenizer(texts):
    """Create and fit tokenizer on training data"""
    
    print("\n" + "=" * 70)
    print("TOKENIZATION")
    print("=" * 70)
    
    print(f"\n🔤 Creating tokenizer (max words: {MAX_WORDS:,})")
    tokenizer = Tokenizer(
        num_words=MAX_WORDS,
        oov_token='<OOV>',
        filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
        lower=True
    )
    
    tokenizer.fit_on_texts(texts)
    
    vocab_size = min(len(tokenizer.word_index), MAX_WORDS)
    print(f"✅ Vocabulary size: {vocab_size:,} unique words")
    print(f"📊 Total words processed: {len(tokenizer.word_index):,}")
    
    # Show most common words
    word_freq = sorted(tokenizer.word_index.items(), key=lambda x: x[1])[:20]
    print(f"\n📈 Most common words:")
    for word, idx in word_freq:
        print(f"   {idx:3d}. {word}")
    
    return tokenizer

def prepare_sequences(tokenizer, texts):
    """Convert texts to padded sequences"""
    
    print(f"\n🔄 Converting texts to sequences...")
    sequences = tokenizer.texts_to_sequences(texts)
    
    print(f"✅ Created {len(sequences):,} sequences")
    
    # Show sequence length stats
    seq_lengths = [len(seq) for seq in sequences]
    print(f"\n📊 Sequence length statistics:")
    print(f"   Min: {min(seq_lengths)}")
    print(f"   Max: {max(seq_lengths)}")
    print(f"   Mean: {np.mean(seq_lengths):.1f}")
    print(f"   Median: {np.median(seq_lengths):.1f}")
    print(f"   95th percentile: {np.percentile(seq_lengths, 95):.1f}")
    
    # Pad sequences
    print(f"\n📏 Padding sequences to length {MAX_SEQUENCE_LENGTH}...")
    padded = pad_sequences(
        sequences, 
        maxlen=MAX_SEQUENCE_LENGTH,
        padding='post',
        truncating='post'
    )
    
    print(f"✅ Padded shape: {padded.shape}")
    
    return padded

def build_model(vocab_size):
    """Build LSTM model architecture"""
    
    print("\n" + "=" * 70)
    print("MODEL ARCHITECTURE")
    print("=" * 70)
    
    from tensorflow.keras.layers import GlobalAveragePooling1D
    
    model = keras.Sequential([
        Embedding(
            input_dim=vocab_size,
            output_dim=EMBEDDING_DIM,
            input_length=MAX_SEQUENCE_LENGTH,
            name='embedding'
        ),
        
        GlobalAveragePooling1D(name='pooling'),
        
        Dense(LSTM_UNITS_1, activation='relu', name='dense1'),
        Dropout(DROPOUT_RATE, name='dropout_1'),
        
        Dense(DENSE_UNITS, activation='relu', name='dense2'),
        Dropout(DROPOUT_RATE, name='dropout_2'),
        
        Dense(1, activation='sigmoid', name='output')
    ])
    
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    print("\n📐 Model Summary:")
    model.summary()
    
    total_params = model.count_params()
    print(f"\n📊 Total parameters: {total_params:,}")
    
    return model

def train_model(model, X_train, y_train, X_val, y_val, class_weights):
    """Train the model with callbacks"""
    
    print("\n" + "=" * 70)
    print("TRAINING")
    print("=" * 70)
    
    # Create model checkpoint directory
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    checkpoint_path = MODELS_DIR / "best_model.keras"
    
    # Callbacks
    callbacks = [
        EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True,
            verbose=1
        ),
        ModelCheckpoint(
            filepath=str(checkpoint_path),
            monitor='val_auc',
            mode='max',
            save_best_only=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,
            min_lr=0.00001,
            verbose=1
        )
    ]
    
    print(f"\n🎯 Starting training for up to {EPOCHS} epochs...")
    print(f"   Batch size: {BATCH_SIZE}")
    print(f"   Class weights: {class_weights}")
    
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        class_weight=class_weights,
        callbacks=callbacks,
        verbose=1
    )
    
    return history, model

def evaluate_model(model, X_test, y_test):
    """Evaluate model performance"""
    
    print("\n" + "=" * 70)
    print("EVALUATION")
    print("=" * 70)
    
    print(f"\n📊 Evaluating on test set ({len(y_test):,} samples)...")
    
    # Get predictions
    y_pred_proba = model.predict(X_test, verbose=0)
    y_pred = (y_pred_proba > 0.5).astype(int).flatten()
    
    # Calculate metrics
    from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
    
    print(f"\n📈 Classification Report:")
    print(classification_report(
        y_test, y_pred,
        target_names=['Legitimate', 'Fraudulent'],
        digits=4
    ))
    
    print(f"\n📊 Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"                Predicted")
    print(f"                Legit  Fraud")
    print(f"Actual Legit    {cm[0][0]:5d}  {cm[0][1]:5d}")
    print(f"Actual Fraud    {cm[1][0]:5d}  {cm[1][1]:5d}")
    
    # Calculate additional metrics
    auc = roc_auc_score(y_test, y_pred_proba)
    
    accuracy = (cm[0][0] + cm[1][1]) / cm.sum()
    precision = cm[1][1] / (cm[1][1] + cm[0][1]) if (cm[1][1] + cm[0][1]) > 0 else 0
    recall = cm[1][1] / (cm[1][1] + cm[1][0]) if (cm[1][1] + cm[1][0]) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    print(f"\n✅ Final Metrics:")
    print(f"   Accuracy:  {accuracy:.4f}")
    print(f"   Precision: {precision:.4f}")
    print(f"   Recall:    {recall:.4f}")
    print(f"   F1 Score:  {f1:.4f}")
    print(f"   ROC AUC:   {auc:.4f}")
    
    return {
        'accuracy': float(accuracy),
        'precision': float(precision),
        'recall': float(recall),
        'f1_score': float(f1),
        'auc': float(auc),
        'confusion_matrix': cm.tolist()
    }

def save_artifacts(model, tokenizer, metrics, history):
    """Save model, tokenizer, and metadata"""
    
    print("\n" + "=" * 70)
    print("SAVING ARTIFACTS")
    print("=" * 70)
    
    # Save model
    model_path = MODELS_DIR / "keras_model.keras"
    print(f"\n💾 Saving model to: {model_path}")
    model.save(model_path)
    print(f"✅ Model saved ({model_path.stat().st_size / 1024 / 1024:.2f} MB)")
    
    # Save tokenizer
    tokenizer_path = MODELS_DIR / "tokenizer.json"
    print(f"\n💾 Saving tokenizer to: {tokenizer_path}")
    tokenizer_config = {
        'word_index': tokenizer.word_index,
        'config': {
            'num_words': MAX_WORDS,
            'oov_token': '<OOV>',
        }
    }
    with open(tokenizer_path, 'w', encoding='utf-8') as f:
        json.dump(tokenizer_config, f, ensure_ascii=False)
    print(f"✅ Tokenizer saved ({tokenizer_path.stat().st_size / 1024:.2f} KB)")
    
    # Save metadata
    metadata_path = MODELS_DIR / "metadata.json"
    print(f"\n💾 Saving metadata to: {metadata_path}")
    
    metadata = {
        'model_name': 'spam_detector_v3',
        'model_type': 'binary_classification',
        'version': '3.0.0',
        'created_at': datetime.now().isoformat(),
        'dataset': 'Employment Scam Aegean Dataset (12,725 jobs)',
        'metrics': metrics,
        'training_info': {
            'dataset_size': 12725,
            'train_size': int(len(history.history['loss']) * BATCH_SIZE),
            'epochs_trained': len(history.history['loss']),
            'final_train_loss': float(history.history['loss'][-1]),
            'final_val_loss': float(history.history['val_loss'][-1]),
            'final_train_accuracy': float(history.history['accuracy'][-1]),
            'final_val_accuracy': float(history.history['val_accuracy'][-1]),
        },
        'architecture': {
            'max_words': MAX_WORDS,
            'max_sequence_length': MAX_SEQUENCE_LENGTH,
            'embedding_dim': EMBEDDING_DIM,
            'lstm_units': [LSTM_UNITS_1, LSTM_UNITS_2],
            'dense_units': DENSE_UNITS,
            'dropout_rate': DROPOUT_RATE,
        }
    }
    
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    print(f"✅ Metadata saved")
    
    # Copy to extension directory
    src_models_dir = Path(__file__).parent.parent / "src" / "models" / "spam_detector"
    print(f"\n📦 Copying to extension directory: {src_models_dir}")
    
    import shutil
    src_models_dir.mkdir(parents=True, exist_ok=True)
    
    shutil.copy(model_path, src_models_dir / "keras_model.keras")
    shutil.copy(tokenizer_path, src_models_dir / "tokenizer.json")
    shutil.copy(metadata_path, src_models_dir / "metadata.json")
    
    print(f"✅ Files copied to extension")
    
    print(f"\n📁 Saved artifacts:")
    print(f"   Model:     {model_path}")
    print(f"   Tokenizer: {tokenizer_path}")
    print(f"   Metadata:  {metadata_path}")

def main():
    """Main training pipeline"""
    
    print("\n" + "=" * 70)
    print("SPAM DETECTION MODEL TRAINING - V3.0")
    print("Employment Scam Aegean Dataset (12,725+ jobs)")
    print("=" * 70)
    
    # Load data
    X, y, df = load_and_preprocess_data()
    
    # Split data
    print(f"\n🔀 Splitting data (70% train, 15% val, 15% test)...")
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X, y, test_size=0.15, random_state=42, stratify=y
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, test_size=0.176, random_state=42, stratify=y_train_val  # 15% of 85% = 12.75% ~= 15%
    )
    
    print(f"✅ Train: {len(y_train):,} samples")
    print(f"✅ Val:   {len(y_val):,} samples")
    print(f"✅ Test:  {len(y_test):,} samples")
    
    # Create tokenizer
    tokenizer = create_tokenizer(X_train)
    
    # Prepare sequences
    X_train_seq = prepare_sequences(tokenizer, X_train)
    X_val_seq = prepare_sequences(tokenizer, X_val)
    X_test_seq = prepare_sequences(tokenizer, X_test)
    
    # Calculate class weights (handle imbalance)
    class_weights_array = class_weight.compute_class_weight(
        'balanced',
        classes=np.unique(y_train),
        y=y_train
    )
    class_weights = {i: weight for i, weight in enumerate(class_weights_array)}
    
    print(f"\n⚖️  Class weights (to handle imbalance):")
    print(f"   Legitimate (0): {class_weights[0]:.2f}")
    print(f"   Fraudulent (1): {class_weights[1]:.2f}")
    
    # Build model
    vocab_size = min(len(tokenizer.word_index) + 1, MAX_WORDS)
    model = build_model(vocab_size)
    
    # Train model
    history, trained_model = train_model(
        model, X_train_seq, y_train, X_val_seq, y_val, class_weights
    )
    
    # Evaluate model
    metrics = evaluate_model(trained_model, X_test_seq, y_test)
    
    # Save everything
    save_artifacts(trained_model, tokenizer, metrics, history)
    
    print("\n" + "=" * 70)
    print("✅ TRAINING COMPLETE!")
    print("=" * 70)
    print(f"\n🎉 Model Version 3.0 trained successfully!")
    print(f"📊 Test Accuracy: {metrics['accuracy']:.2%}")
    print(f"📊 Test F1 Score: {metrics['f1_score']:.2%}")
    print(f"📊 ROC AUC: {metrics['auc']:.4f}")
    print(f"\n💡 Next steps:")
    print(f"   1. Build extension: npm run build")
    print(f"   2. Test on Upwork jobs")
    print(f"   3. Monitor performance")
    
    return metrics

if __name__ == "__main__":
    metrics = main()
