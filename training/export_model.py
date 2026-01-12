"""
Model Export Script - Convert TensorFlow/Keras models to TensorFlow.js format
"""

import tensorflow as tf
import tensorflowjs as tfjs
from pathlib import Path
import json
import argparse


def export_model_to_tfjs(
    model_path: str,
    output_dir: str,
    quantization: bool = True,
    metadata: dict = None
):
    """
    Export a Keras model to TensorFlow.js format
    
    Args:
        model_path: Path to saved Keras model (.h5 or SavedModel directory)
        output_dir: Output directory for TensorFlow.js model
        quantization: Whether to apply 16-bit quantization
        metadata: Optional metadata to save with the model
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"Loading model from {model_path}...")
    model = tf.keras.models.load_model(model_path)
    
    print(f"Model summary:")
    model.summary()
    
    # Prepare conversion options
    quantization_dtype = None
    if quantization:
        quantization_dtype = 'uint16'  # 16-bit quantization
        print("Applying 16-bit quantization...")
    
    print(f"Exporting to {output_path}...")
    tfjs.converters.save_keras_model(
        model,
        str(output_path),
        quantization_dtype_map={'uint8': quantization_dtype} if quantization else None
    )
    
    # Save metadata
    if metadata:
        metadata_file = output_path / "metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"Metadata saved to {metadata_file}")
    
    # Calculate model size
    total_size = sum(f.stat().st_size for f in output_path.rglob('*') if f.is_file())
    size_mb = total_size / (1024 * 1024)
    
    print(f"\n✅ Export complete!")
    print(f"   Output directory: {output_path}")
    print(f"   Model size: {size_mb:.2f} MB")
    print(f"   Quantized: {quantization}")
    
    return output_path


def create_dummy_model(output_dir: str):
    """
    Create a dummy model for testing infrastructure
    This model doesn't actually work but validates the pipeline
    """
    print("Creating dummy test model...")
    
    # Simple model: 11 input features -> Dense layers -> 1 output (score 0-10)
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(32, activation='relu', input_shape=(11,)),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(1, activation='sigmoid')  # Output 0-1, scale to 0-10 later
    ])
    
    model.compile(
        optimizer='adam',
        loss='mse',
        metrics=['mae']
    )
    
    print("Model architecture:")
    model.summary()
    
    # Save temporary model
    temp_model_path = Path("temp_dummy_model.h5")
    model.save(temp_model_path)
    
    # Export to TensorFlow.js
    metadata = {
        "name": "dummy_quality_scorer",
        "version": "0.1.0",
        "type": "quality_assessment",
        "input_features": 11,
        "output_type": "regression",
        "description": "Dummy model for infrastructure testing. Not trained on real data.",
        "created_at": "2026-01-07"
    }
    
    export_model_to_tfjs(
        str(temp_model_path),
        output_dir,
        quantization=True,
        metadata=metadata
    )
    
    # Cleanup
    temp_model_path.unlink()
    
    print("\n⚠️  This is a DUMMY model for testing only!")
    print("   It has not been trained and will produce random predictions.")
    print("   Use this to validate the ML infrastructure, not for actual scoring.")


def main():
    parser = argparse.ArgumentParser(description='Export TensorFlow models to TensorFlow.js')
    parser.add_argument('--model', type=str, help='Path to Keras model (.h5 or SavedModel)')
    parser.add_argument('--output', type=str, required=True, help='Output directory for TensorFlow.js model')
    parser.add_argument('--no-quantization', action='store_true', help='Disable 16-bit quantization')
    parser.add_argument('--dummy', action='store_true', help='Create dummy model for testing')
    
    args = parser.parse_args()
    
    if args.dummy:
        create_dummy_model(args.output)
    elif args.model:
        export_model_to_tfjs(
            args.model,
            args.output,
            quantization=not args.no_quantization
        )
    else:
        parser.error("Either --model or --dummy must be specified")


if __name__ == "__main__":
    main()
