/**
 * ML Engine - TensorFlow.js model loader and inference engine
 * Runs in the service worker for efficient model management
 */

import * as tf from '@tensorflow/tfjs';
import '@tensorflow/tfjs-backend-webgl';
import { ModelMetadata, MLPrediction, MLFeatures } from '../../types';

export class MLEngine {
  private static instance: MLEngine;
  private models: Map<string, tf.LayersModel | tf.GraphModel> = new Map();
  private modelMetadata: Map<string, ModelMetadata> = new Map();
  private isInitialized = false;
  private initializationPromise: Promise<void> | null = null;

  private constructor() {}

  /**
   * Get singleton instance
   */
  static getInstance(): MLEngine {
    if (!MLEngine.instance) {
      MLEngine.instance = new MLEngine();
    }
    return MLEngine.instance;
  }

  /**
   * Initialize TensorFlow.js backend
   */
  async initialize(): Promise<void> {
    if (this.isInitialized) {
      return;
    }

    if (this.initializationPromise) {
      return this.initializationPromise;
    }

    this.initializationPromise = (async () => {
      try {
        console.log('[ML Engine] Initializing TensorFlow.js...');
        
        // Try WebGL backend first
        try {
          await tf.setBackend('webgl');
          await tf.ready();
          console.log('[ML Engine] WebGL backend initialized');
        } catch (error) {
          console.warn('[ML Engine] WebGL backend failed, falling back to CPU:', error);
          await tf.setBackend('cpu');
          await tf.ready();
          console.log('[ML Engine] CPU backend initialized');
        }

        this.isInitialized = true;
        console.log('[ML Engine] Backend:', tf.getBackend());
        console.log('[ML Engine] TensorFlow.js version:', tf.version.tfjs);
      } catch (error) {
        console.error('[ML Engine] Initialization failed:', error);
        throw error;
      }
    })();

    return this.initializationPromise;
  }

  /**
   * Load a model from URL or IndexedDB cache
   */
  async loadModel(modelName: string, modelUrl: string): Promise<void> {
    await this.initialize();

    if (this.models.has(modelName)) {
      console.log(`[ML Engine] Model ${modelName} already loaded`);
      return;
    }

    try {
      console.log(`[ML Engine] Loading model ${modelName} from ${modelUrl}...`);
      const startTime = Date.now();

      // Try to load from IndexedDB cache first
      const cachedModel = await this.loadFromCache(modelName);
      if (cachedModel) {
        this.models.set(modelName, cachedModel);
        console.log(`[ML Engine] Model ${modelName} loaded from cache in ${Date.now() - startTime}ms`);
        return;
      }

      // Load from URL
      const model = await tf.loadLayersModel(modelUrl);
      this.models.set(modelName, model);

      // Cache the model
      await this.saveToCache(modelName, model);

      const loadTime = Date.now() - startTime;
      const modelSize = this.estimateModelSize(model);

      const metadata: ModelMetadata = {
        name: modelName,
        version: '2.0.0',
        size: modelSize,
        loadedAt: new Date(),
        inputShape: model.inputs[0].shape as number[],
        outputShape: model.outputs[0].shape as number[],
      };

      this.modelMetadata.set(modelName, metadata);

      console.log(`[ML Engine] Model ${modelName} loaded in ${loadTime}ms (${(modelSize / 1024 / 1024).toFixed(2)}MB)`);
    } catch (error) {
      console.error(`[ML Engine] Failed to load model ${modelName}:`, error);
      throw error;
    }
  }

  /**
   * Load model from IndexedDB cache
   */
  private async loadFromCache(modelName: string): Promise<tf.LayersModel | null> {
    try {
      const model = await tf.loadLayersModel(`indexeddb://${modelName}`);
      return model;
    } catch (error) {
      // Model not in cache
      return null;
    }
  }

  /**
   * Save model to IndexedDB cache
   */
  private async saveToCache(modelName: string, model: tf.LayersModel | tf.GraphModel): Promise<void> {
    try {
      await model.save(`indexeddb://${modelName}`);
      console.log(`[ML Engine] Model ${modelName} cached to IndexedDB`);
    } catch (error) {
      console.warn(`[ML Engine] Failed to cache model ${modelName}:`, error);
    }
  }

  /**
   * Estimate model size in bytes
   */
  private estimateModelSize(model: tf.LayersModel | tf.GraphModel): number {
    let totalSize = 0;
    if ('getWeights' in model) {
      const weights = (model as tf.LayersModel).getWeights();
      weights.forEach((weight: tf.Tensor) => {
        totalSize += weight.size * 4; // Assuming float32 (4 bytes per value)
      });
    } else {
      // For GraphModel, weights is already an array
      const weights = (model as tf.GraphModel).weights;
      if (Array.isArray(weights)) {
        weights.forEach((weight: tf.Tensor) => {
          totalSize += weight.size * 4;
        });
      }
    }
    return totalSize;
  }

  /**
   * Run inference on a model
   */
  async predict(modelName: string, features: MLFeatures): Promise<MLPrediction> {
    if (!this.models.has(modelName)) {
      throw new Error(`Model ${modelName} not loaded`);
    }

    const model = this.models.get(modelName)!;
    const metadata = this.modelMetadata.get(modelName);

    const startTime = Date.now();

    try {
      // Convert features to tensor
      const inputTensor = tf.tensor2d([features.featureVector]);

      // Run inference
      const outputTensor = model.predict(inputTensor) as tf.Tensor;
      const output = await outputTensor.data();

      // Clean up tensors
      inputTensor.dispose();
      outputTensor.dispose();

      const inferenceTime = Date.now() - startTime;

      // Assuming binary classification or regression output
      const score = output[0];
      const confidence = output.length > 1 ? output[1] : 1.0;

      return {
        score,
        confidence,
        modelVersion: metadata?.version || '2.0.0',
        inferenceTimeMs: inferenceTime,
      };
    } catch (error) {
      console.error(`[ML Engine] Prediction failed for model ${modelName}:`, error);
      throw error;
    }
  }

  /**
   * Unload a model to free memory
   */
  async unloadModel(modelName: string): Promise<void> {
    const model = this.models.get(modelName);
    if (model) {
      model.dispose();
      this.models.delete(modelName);
      this.modelMetadata.delete(modelName);
      console.log(`[ML Engine] Model ${modelName} unloaded`);
    }
  }

  /**
   * Get model status
   */
  getModelStatus(modelName: string): ModelMetadata | null {
    return this.modelMetadata.get(modelName) || null;
  }

  /**
   * Get all loaded models
   */
  getLoadedModels(): string[] {
    return Array.from(this.models.keys());
  }

  /**
   * Get memory usage info
   */
  getMemoryInfo(): { numTensors: number; numBytes: number } {
    return tf.memory();
  }

  /**
   * Cleanup all resources
   */
  async cleanup(): Promise<void> {
    console.log('[ML Engine] Cleaning up resources...');
    for (const modelName of this.models.keys()) {
      await this.unloadModel(modelName);
    }
    this.isInitialized = false;
    this.initializationPromise = null;
  }
}
