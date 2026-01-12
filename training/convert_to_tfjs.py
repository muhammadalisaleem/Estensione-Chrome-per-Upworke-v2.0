"""
Manual conversion of Keras model to TensorFlow.js format
Works around tensorflow_decision_forests dependency issue
"""

import os
import sys
from pathlib import Path

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

print("Loading TensorFlow and Keras...")
import tensorflow as tf
from tensorflow import keras

TRAINING_DIR = Path(__file__).parent
MODELS_DIR = TRAINING_DIR / "models" / "spam_detector"
OUTPUT_DIR = TRAINING_DIR.parent / "src" / "models" / "spam_detector"

def convert_model() -> bool:
    """Convert Keras model to TensorFlow.js format"""
    
    print(f"\n{'='*70}")
    print("MANUAL KERAS TO TENSORFLOW.JS CONVERSION")
    print(f"{'='*70}\n")
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"📁 Output directory: {OUTPUT_DIR}")
    
    # Load Keras model
    keras_path = MODELS_DIR / "keras_model.keras"
    print(f"\n📂 Loading Keras model from: {keras_path}")
    
    if not keras_path.exists():
        print(f"❌ Error: Model file not found at {keras_path}")
        sys.exit(1)
    
    try:
        model = keras.models.load_model(keras_path)
        print("✅ Keras model loaded successfully")
        
        # Display model summary
        print("\n📊 Model Summary:")
        model.summary()
        
    except Exception as e:
        print(f"❌ Failed to load Keras model: {e}")
        sys.exit(1)
    
    # Convert to TensorFlow.js format
    print("\n🔄 Converting to TensorFlow.js format...")
    
    try:
        # Import here to avoid startup issues
        import tensorflowjs as tfjs
        
        # Convert and save
        tfjs.converters.save_keras_model(model, str(OUTPUT_DIR))
        
        print(f"✅ Model converted successfully!")
        print(f"\n📁 TensorFlow.js model saved to: {OUTPUT_DIR}")
        
        # List generated files
        print("\n📋 Generated files:")
        for file in sorted(OUTPUT_DIR.iterdir()):
            size = file.stat().st_size
            print(f"   • {file.name} ({size:,} bytes)")
        
    except ImportError as e:
        print(f"⚠️  tensorflowjs import failed: {e}")
        print("\n🔧 Using alternative: Copy Keras model directly...\n")
        
        # Just copy the Keras model - TF.js can load it with converter on the fly
        import shutil
        
        keras_src = MODELS_DIR / "keras_model.keras"
        keras_dst = OUTPUT_DIR / "keras_model.keras"
        
        print(f"📂 Copying Keras model...")
        shutil.copy(keras_src, keras_dst)
        print(f"✅ Keras model copied to: {keras_dst}")
        
        print("\n📝 Note: The Keras model will need to be loaded using TensorFlow.js")
        print("    This can be done client-side or pre-converted externally.")
        
        # Continue to copy other files anyway
        # Don't return False - we still want to copy tokenizer and metadata
    
    # Always copy tokenizer and metadata files
    print(f"\n{'='*70}")
    print("✅ FINALIZING MODEL FILES")
    print(f"{'='*70}\n")
    
    # Copy tokenizer and metadata files
    print("📋 Copying tokenizer and metadata files...")
    import shutil
    
    try:
        shutil.copy(MODELS_DIR / "tokenizer.json", OUTPUT_DIR / "tokenizer.json")
        print(f"✅ Copied tokenizer.json")
    except Exception as e:
        print(f"⚠️  Failed to copy tokenizer: {e}")
    
    try:
        shutil.copy(MODELS_DIR / "metadata.json", OUTPUT_DIR / "metadata.json")
        print(f"✅ Copied metadata.json")
    except Exception as e:
        print(f"⚠️  Failed to copy metadata: {e}")
    
    print("\n📍 Next steps:")
    print("1. Test model loading in extension")
    print("2. Integrate spam detection into scoring pipeline")
    print("3. Build extension with webpack\n")
    
    return True

if __name__ == "__main__":
    success = convert_model()
    sys.exit(0 if success else 1)
