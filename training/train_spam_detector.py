"""
Train Spam Detection Model for Upwork Jobs
Uses Kaggle datasets to train a binary classifier for spam job detection
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Reduce TF logging

import json
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import re

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

# Note: tensorflowjs import moved to export function to avoid startup issues
# import tensorflowjs as tfjs

# Paths
TRAINING_DIR = Path(__file__).parent
DATA_DIR = TRAINING_DIR / "data"
MODELS_DIR = TRAINING_DIR / "models"
MODELS_DIR.mkdir(exist_ok=True)


class SpamDetectorTrainer:
    """Train and export spam detection model"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.max_sequence_length = 200
        self.max_words = 5000
        self.embedding_dim = 128
        
    def load_data(self, data_path: Path) -> pd.DataFrame:
        """Load training data from CSV or JSON"""
        print(f"\n📂 Loading data from {data_path}")
        
        if data_path.suffix == '.csv':
            df = pd.read_csv(data_path)
        elif data_path.suffix == '.json':
            df = pd.read_json(data_path)
        else:
            raise ValueError(f"Unsupported file format: {data_path.suffix}")
        
        print(f"   Loaded {len(df)} jobs")
        return df
    
    def prepare_spam_labels(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert quality labels to binary spam/not-spam
        spam = 1, not-spam = 0
        """
        print("\n🏷️  Preparing spam labels...")
        
        # Map quality labels to spam (1) or not spam (0)
        spam_mapping = {
            'spam': 1,
            'poor': 0,  # Poor quality but not spam
            'good': 0,
            'excellent': 0
        }
        
        df['is_spam'] = df['quality_label'].map(spam_mapping)
        
        # Remove rows without labels
        df = df.dropna(subset=['is_spam'])
        
        spam_count = df['is_spam'].sum()
        not_spam_count = len(df) - spam_count
        
        print(f"   Not Spam: {not_spam_count}")
        print(f"   Spam: {spam_count}")
        print(f"   Class balance: {spam_count / len(df) * 100:.1f}% spam")
        
        return df
    
    def extract_text_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extract features from job text"""
        print("\n📝 Extracting text features...")
        
        # Combine title and description
        df['combined_text'] = df['title'].fillna('') + ' ' + df['description'].fillna('')
        
        # Clean text
        df['combined_text'] = df['combined_text'].apply(self.clean_text)
        
        return df
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if pd.isna(text) or not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\.\S+', ' ', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', ' ', text)
        
        # Remove phone numbers
        text = re.sub(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', ' ', text)
        text = re.sub(r'\+?\d{1,3}[-.\s]?\d{3,}', ' ', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def tokenize_text(self, texts):
        """Tokenize and pad text sequences"""
        print("\n🔤 Tokenizing text...")
        
        # Create tokenizer
        self.tokenizer = Tokenizer(
            num_words=self.max_words,
            oov_token='<OOV>',
            lower=True
        )
        
        self.tokenizer.fit_on_texts(texts)
        
        # Convert to sequences
        sequences = self.tokenizer.texts_to_sequences(texts)
        
        # Pad sequences
        padded = pad_sequences(
            sequences,
            maxlen=self.max_sequence_length,
            padding='post',
            truncating='post'
        )
        
        vocab_size = len(self.tokenizer.word_index) + 1
        print(f"   Vocabulary size: {vocab_size}")
        print(f"   Sequence length: {self.max_sequence_length}")
        
        return padded
    
    def balance_dataset(self, X, y):
        """Balance dataset by oversampling minority class"""
        print("\n⚖️  Balancing dataset...")
        
        spam_indices = np.where(y == 1)[0]
        not_spam_indices = np.where(y == 0)[0]
        
        print(f"   Original - Spam: {len(spam_indices)}, Not Spam: {len(not_spam_indices)}")
        
        # Oversample spam class if underrepresented
        if len(spam_indices) < len(not_spam_indices) * 0.3:
            # We want at least 30% spam examples
            target_spam_count = int(len(not_spam_indices) * 0.3)
            oversample_count = target_spam_count - len(spam_indices)
            
            if oversample_count > 0:
                # Randomly oversample spam examples
                oversample_indices = np.random.choice(
                    spam_indices,
                    size=oversample_count,
                    replace=True
                )
                
                X_oversampled = np.vstack([X, X[oversample_indices]])
                y_oversampled = np.hstack([y, y[oversample_indices]])
                
                print(f"   Oversampled {oversample_count} spam examples")
                print(f"   New total: {len(X_oversampled)}")
                
                return X_oversampled, y_oversampled
        
        print("   Dataset already balanced")
        return X, y
    
    def build_model(self):
        """Build LSTM-based spam detection model"""
        print("\n🏗️  Building model architecture...")
        
        model = keras.Sequential([
            # Embedding layer
            layers.Embedding(
                self.max_words,
                self.embedding_dim,
                input_length=self.max_sequence_length
            ),
            
            # Bidirectional LSTM
            layers.Bidirectional(layers.LSTM(64, return_sequences=True)),
            layers.Dropout(0.3),
            
            # Another LSTM layer
            layers.Bidirectional(layers.LSTM(32)),
            layers.Dropout(0.3),
            
            # Dense layers
            layers.Dense(32, activation='relu'),
            layers.Dropout(0.2),
            
            # Output layer (binary classification)
            layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy', tf.keras.metrics.AUC(name='auc')]
        )
        
        print("\n📊 Model Summary:")
        model.summary()
        
        self.model = model
        return model
    
    def train(self, X_train, y_train, X_val, y_val, epochs=20):
        """Train the spam detection model"""
        print(f"\n🚀 Training model for {epochs} epochs...")
        
        # Calculate class weights for imbalanced data
        total = len(y_train)
        pos = np.sum(y_train)
        neg = total - pos
        
        weight_for_0 = (1 / neg) * (total / 2.0)
        weight_for_1 = (1 / pos) * (total / 2.0)
        
        class_weight = {0: weight_for_0, 1: weight_for_1}
        
        print(f"   Class weights: Not Spam={weight_for_0:.2f}, Spam={weight_for_1:.2f}")
        
        # Callbacks
        callbacks = [
            keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=3,
                restore_best_weights=True
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=2,
                min_lr=1e-6
            )
        ]
        
        # Train
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=32,
            class_weight=class_weight,
            callbacks=callbacks,
            verbose=1
        )
        
        return history
    
    def evaluate(self, X_test, y_test):
        """Evaluate model performance"""
        print("\n📈 Evaluating model...")
        
        # Predictions
        y_pred_proba = self.model.predict(X_test)
        y_pred = (y_pred_proba > 0.5).astype(int).flatten()
        
        # Metrics
        print("\n" + "="*60)
        print("CLASSIFICATION REPORT")
        print("="*60)
        print(classification_report(
            y_test, y_pred,
            target_names=['Not Spam', 'Spam'],
            digits=4
        ))
        
        print("\n" + "="*60)
        print("CONFUSION MATRIX")
        print("="*60)
        cm = confusion_matrix(y_test, y_pred)
        print(f"                Predicted")
        print(f"                Not Spam  Spam")
        print(f"Actual Not Spam    {cm[0][0]:5d}  {cm[0][1]:5d}")
        print(f"Actual Spam        {cm[1][0]:5d}  {cm[1][1]:5d}")
        
        # ROC AUC
        auc = roc_auc_score(y_test, y_pred_proba)
        print(f"\n🎯 ROC AUC Score: {auc:.4f}")
        
        # Calculate metrics
        tn, fp, fn, tp = cm.ravel()
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        metrics = {
            'accuracy': float(np.mean(y_pred == y_test)),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1),
            'auc': float(auc),
            'confusion_matrix': cm.tolist()
        }
        
        return metrics
    
    def export_to_tfjs(self, output_dir: Path, model_name="spam_detector"):
        """Export model to TensorFlow.js format"""
        print(f"\n💾 Exporting model to TensorFlow.js...")
        
        model_output = output_dir / model_name
        model_output.mkdir(exist_ok=True, parents=True)
        
        # Save Keras model first
        keras_path = model_output / "keras_model.keras"
        self.model.save(keras_path)
        print(f"   ✅ Keras model saved to: {keras_path}")
        
        # Try to convert to TensorFlow.js
        tfjs_path = model_output / "tfjs"
        try:
            import tensorflowjs as tfjs
            tfjs.converters.save_keras_model(
                self.model,
                str(tfjs_path),
                quantization_dtype_map={'uint16': '*'}  # 16-bit quantization
            )
            print(f"   ✅ TensorFlow.js model saved to: {tfjs_path}")
        except Exception as e:
            print(f"   ⚠️  TensorFlow.js conversion failed: {e}")
            print(f"   Keras model still saved at: {keras_path}")
            print("   You can convert it later using: tensorflowjs_converter")
        
        # Save tokenizer
        tokenizer_config = {
            'word_index': self.tokenizer.word_index,
            'max_words': self.max_words,
            'max_sequence_length': self.max_sequence_length,
            'oov_token': '<OOV>'
        }
        
        tokenizer_path = model_output / "tokenizer.json"
        with open(tokenizer_path, 'w') as f:
            json.dump(tokenizer_config, f, indent=2)
        
        print(f"   ✅ Tokenizer saved to: {tokenizer_path}")
        
        return keras_path
    
    def save_metadata(self, output_dir: Path, metrics: dict, training_info: dict):
        """Save model metadata"""
        metadata = {
            'model_name': 'spam_detector',
            'model_type': 'binary_classification',
            'version': '1.0.0',
            'created_at': datetime.now().isoformat(),
            'metrics': metrics,
            'training_info': training_info,
            'input_shape': [self.max_sequence_length],
            'output_shape': [1],
            'preprocessing': {
                'tokenizer': 'keras_tokenizer',
                'max_words': self.max_words,
                'max_sequence_length': self.max_sequence_length,
                'padding': 'post',
                'truncating': 'post'
            }
        }
        
        metadata_path = output_dir / "spam_detector" / "metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"   ✅ Metadata saved to: {metadata_path}")


def main():
    """Main training pipeline"""
    print("="*70)
    print("SPAM DETECTOR TRAINING PIPELINE")
    print("="*70)
    
    trainer = SpamDetectorTrainer()
    
    # 1. Load data - try multiple sources
    data_files = [
        DATA_DIR / "large_dataset.csv",
        DATA_DIR / "kaggle_imported_jobs.csv",
        DATA_DIR / "sample_jobs.csv",
        DATA_DIR / "labeled_jobs.csv"
    ]
    
    data_file = None
    for file in data_files:
        if file.exists():
            data_file = file
            break
    
    if data_file is None:
        print(f"\n❌ No data file found!")
        print("\nPlease run one of the following first:")
        print("  1. python create_sample_dataset.py  (create sample data)")
        print("  2. python quick_import_example.py   (import from Kaggle)")
        print("  3. python collect_data.py           (manual labeling)")
        return
    
    df = trainer.load_data(data_file)
    
    # 2. Prepare labels
    df = trainer.prepare_spam_labels(df)
    
    if len(df) < 50:
        print(f"\n⚠️  Warning: Only {len(df)} labeled jobs found.")
        print("   This is too small for reliable training. Minimum recommended: 100+")
        print("   Continuing with sample dataset for demonstration...")
    elif len(df) < 200:
        print(f"\n⚠️  Note: {len(df)} jobs found.")
        print("   For production use, collect 200+ jobs for better performance.")
        print("   Proceeding with available data...")
    
    # 3. Extract text features
    df = trainer.extract_text_features(df)
    
    # 4. Tokenize text
    X = trainer.tokenize_text(df['combined_text'].values)
    y = df['is_spam'].values
    
    # 5. Balance dataset
    X, y = trainer.balance_dataset(X, y)
    
    # 6. Split data
    print("\n✂️  Splitting data...")
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
    )
    
    print(f"   Training set: {len(X_train)}")
    print(f"   Validation set: {len(X_val)}")
    print(f"   Test set: {len(X_test)}")
    
    # 7. Build model
    trainer.build_model()
    
    # 8. Train model
    history = trainer.train(X_train, y_train, X_val, y_val, epochs=20)
    
    # 9. Evaluate
    metrics = trainer.evaluate(X_test, y_test)
    
    # 10. Export
    print("\n" + "="*70)
    print("EXPORTING MODEL")
    print("="*70)
    
    trainer.export_to_tfjs(MODELS_DIR)
    
    # 11. Save metadata
    training_info = {
        'dataset_size': len(df),
        'train_size': len(X_train),
        'val_size': len(X_val),
        'test_size': len(X_test),
        'epochs_trained': len(history.history['loss']),
        'final_train_loss': float(history.history['loss'][-1]),
        'final_val_loss': float(history.history['val_loss'][-1])
    }
    
    trainer.save_metadata(MODELS_DIR, metrics, training_info)
    
    # 12. Summary
    print("\n" + "="*70)
    print("✅ TRAINING COMPLETE!")
    print("="*70)
    print(f"\n📁 Model files:")
    print(f"   • {MODELS_DIR / 'spam_detector' / 'tfjs'}")
    print(f"   • {MODELS_DIR / 'spam_detector' / 'tokenizer.json'}")
    print(f"   • {MODELS_DIR / 'spam_detector' / 'metadata.json'}")
    
    print(f"\n📊 Performance:")
    print(f"   • Accuracy: {metrics['accuracy']:.2%}")
    print(f"   • Precision: {metrics['precision']:.2%}")
    print(f"   • Recall: {metrics['recall']:.2%}")
    print(f"   • F1 Score: {metrics['f1_score']:.2%}")
    print(f"   • AUC: {metrics['auc']:.4f}")
    
    print(f"\n🎯 Next steps:")
    print("   1. Copy model files to extension:")
    print(f"      cp -r {MODELS_DIR / 'spam_detector'} ../src/models/")
    print("   2. Test model in extension")
    print("   3. Monitor performance on real Upwork jobs")
    print("   4. Collect edge cases and retrain if needed")


if __name__ == "__main__":
    main()
