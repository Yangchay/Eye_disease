import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image

# Load the model
model_path = os.path.join(os.path.dirname(__file__), '../model/keras_model.keras')
try:
    model = load_model(model_path)
except Exception as e:
    print(f"Error loading model from {model_path}: {e}")
    raise

# Correctly get model input shape from the model object
if model.input_shape:
    input_shape_with_batch = model.input_shape
    if len(input_shape_with_batch) >= 4:
        input_shape = input_shape_with_batch[1:]
    else:
        print(f"Warning: Unexpected model.input_shape format: {input_shape_with_batch}. Attempting to infer.")
        if hasattr(model, 'inputs') and len(model.inputs) > 0:
            input_shape = model.inputs[0].shape[1:]
        else:
            raise ValueError(f"Could not reliably determine model input shape from {model_path}. "
                             f"model.input_shape was {input_shape_with_batch}.")
else:
    raise ValueError(f"Model input shape is not defined for {model_path}. "
                     "Please ensure your Keras model has a defined input layer.")

target_size = input_shape[:2]
img_channels = input_shape[-1]

CLASS_NAMES = ['Cataract', 'Diabetic Retinopathy', 'Glaucoma', 'Normal', 'Unknown']

def preprocess_image(img_path):
    """Preprocess the image for prediction with proper channel handling"""
    img = Image.open(img_path)
    
    if img_channels == 1:
        if img.mode != 'L':
            img = img.convert('L')
    else:
        if img.mode != 'RGB':
            img = img.convert('RGB')
    
    img = img.resize(target_size)
    img_array = image.img_to_array(img)
    
    if img_channels == 1 and img_array.ndim == 2:
        img_array = np.expand_dims(img_array, axis=-1)
    
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    
    return img_array

def predict_image(img_path):
    """Make prediction on the image with error handling and unknown category."""
    try:
        processed_img = preprocess_image(img_path)
        predictions = model.predict(processed_img)
        
        predicted_class_index = np.argmax(predictions[0])
        confidence_score = np.max(predictions[0])

        # --- NEW LOGIC FOR UNKNOWN CATEGORY ---
        # Adjust this threshold based on your model's performance and desired strictness.
        # A common starting point is 0.7 (70%) or 0.8 (80%).
        CONFIDENCE_THRESHOLD = 0.70 # <--- THIS IS THE LINE YOU NEED TO CHANGE

        if confidence_score < CONFIDENCE_THRESHOLD:
            predicted_class = "Unknown" #
            confidence = round(100 * confidence_score, 2) # Show the low confidence
        else:
            predicted_class = CLASS_NAMES[predicted_class_index]
            confidence = round(100 * confidence_score, 2)
        # --- END NEW LOGIC ---

        all_confidences = {name: float(pred) for name, pred in zip(CLASS_NAMES, predictions[0])}

        return {
            'prediction': predicted_class,
            'confidence': confidence,
            'all_confidences': all_confidences
        }
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return {
            'prediction': "Error during prediction",
            'confidence': 0.0,
            'all_confidences': {},
            'error_message': str(e)
        }