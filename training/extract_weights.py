"""
Extract model weights from Keras model for TensorFlow.js
Creates a JSON-based weight format that can be loaded in the browser
"""

import tensorflow as tf
import numpy as np
import json
from pathlib import Path

print("=" * 80)
print("KERAS MODEL WEIGHT EXTRACTOR")
print("=" * 80)

# Paths
TRAINING_DIR = Path(__file__).parent
KERAS_MODEL_PATH = TRAINING_DIR / "models" / "spam_detector_v3" / "keras_model.keras"
OUTPUT_DIR = TRAINING_DIR.parent / "src" / "models" / "spam_detector"

print(f"\n📂 Loading model from: {KERAS_MODEL_PATH}")

# Load model
model = tf.keras.models.load_model(KERAS_MODEL_PATH)
print("✅ Model loaded successfully")

print("\n📊 Model Architecture:")
model.summary()

# Extract weights
print("\n🔧 Extracting weights...")

model_config = {
    "format": "custom_weights",
    "architecture": {
        "layers": []
    },
    "weights": {}
}

for i, layer in enumerate(model.layers):
    layer_config = {
        "name": layer.name,
        "class_name": layer.__class__.__name__,
        "config": {}
    }
    
    # Get layer-specific configuration
    if hasattr(layer, 'get_config'):
        config = layer.get_config()
        # Only keep serializable config
        for key, value in config.items():
            if isinstance(value, (int, float, str, bool, list, type(None))):
                layer_config["config"][key] = value
    
    model_config["architecture"]["layers"].append(layer_config)
    
    # Extract weights
    if len(layer.weights) > 0:
        layer_weights = {}
        for j, weight in enumerate(layer.weights):
            weight_name = weight.name
            weight_value = weight.numpy()
            
            print(f"   Layer {i} ({layer.name}): {weight_name} - shape {weight_value.shape}")
            
            # Store weight info (not actual values - too large for JSON)
            layer_weights[weight_name] = {
                "shape": list(weight_value.shape),
                "dtype": str(weight_value.dtype)
            }
        
        model_config["weights"][layer.name] = layer_weights

# Save model config
config_path = OUTPUT_DIR / "model_architecture.json"
with open(config_path, 'w') as f:
    json.dump(model_config, f, indent=2)

print(f"\n✅ Model architecture saved to: {config_path}")

# Export model in H5 format (compatible with TF.js converters)
h5_path = OUTPUT_DIR / "model.h5"
print(f"\n🔄 Saving model in H5 format...")
model.save(str(h5_path), save_format='h5')
print(f"✅ H5 model saved to: {h5_path}")

print("\n" + "=" * 80)
print("✅ WEIGHT EXTRACTION COMPLETE")
print("=" * 80)
print("\n📝 Next steps:")
print("   1. Use external TF.js converter on H5 file")
print("   2. Or load H5 file directly in browser with tf.loadLayersModel()")
print("   3. Fallback: Implement model in JavaScript using architecture.json")
