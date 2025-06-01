import os
import numpy as np
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
import tensorflow as tf
from PIL import Image
import cv2
from .forms import ImageUploadForm
from .models import Detection

# Load the model once when the module is imported
MODEL_PATH = settings.MODEL_PATH
model = None

def load_model():
    global model
    try:
        if model is None:
            model = tf.keras.models.load_model(MODEL_PATH)
            print("Model loaded successfully")
    except Exception as e:
        print(f"Error loading model: {e}")
        model = None

# Load model on startup
load_model()

# Define class names - adjust these based on your model's training
CLASS_NAMES = [
    'normal',
    'cataract',
    'diabetic_retinopathy',
    'glaucoma'
]

def preprocess_image(image_path):
    """Preprocess image for model prediction"""
    try:
        # Load image
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Resize to model input size (adjust size based on your model)
        img = cv2.resize(img, (224, 224))
        
        # Normalize pixel values
        img = img.astype(np.float32) / 255.0
        
        # Add batch dimension
        img = np.expand_dims(img, axis=0)
        
        return img
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

def predict_disease(image_path):
    """Make prediction using the loaded model"""
    global model
    
    if model is None:
        return None, 0.0
    
    try:
        # Preprocess image
        processed_img = preprocess_image(image_path)
        if processed_img is None:
            return None, 0.0
        
        # Make prediction
        predictions = model.predict(processed_img)
        
        # Get predicted class and confidence
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx]) * 100
        
        predicted_class = CLASS_NAMES[predicted_class_idx] if predicted_class_idx < len(CLASS_NAMES) else "Unknown"
        
        return predicted_class, confidence
        
    except Exception as e:
        print(f"Error making prediction: {e}")
        return None, 0.0

def home(request):
    """Home page with image upload"""
    if request.method == 'POST':
        print("POST request received")
        print("FILES:", request.FILES)
        print("POST data:", request.POST)
        
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid")
            detection = form.save(commit=False)
            
            # Save the file first
            detection.save()
            print(f"Detection saved with ID: {detection.id}")
            
            # Get the uploaded image path
            image_path = detection.image.path
            print(f"Image path: {image_path}")
            
            # Make prediction
            prediction, confidence = predict_disease(image_path)
            print(f"Prediction: {prediction}, Confidence: {confidence}")
            
            if prediction:
                detection.prediction = prediction
                detection.confidence = confidence
                detection.save()
                
                messages.success(request, 'Image processed successfully!')
                return render(request, 'result.html', {
                    'detection': detection,
                    'form': ImageUploadForm()
                })
            else:
                messages.error(request, 'Error processing image. Please try again.')
                print("Prediction failed")
        else:
            print("Form is not valid")
            print("Form errors:", form.errors)
            messages.error(request, 'Please upload a valid image file.')
    
    form = ImageUploadForm()
    recent_detections = Detection.objects.all()[:5]  # Show last 5 detections
    
    return render(request, 'home.html', {
        'form': form,
        'recent_detections': recent_detections
    })

def about(request):
    """About page"""
    return render(request, 'about.html')

def result(request, detection_id=None):
    """Result page"""
    if detection_id:
        try:
            detection = Detection.objects.get(id=detection_id)
            return render(request, 'result.html', {'detection': detection})
        except Detection.DoesNotExist:
            messages.error(request, 'Detection not found.')
            return redirect('home')
    
    return redirect('home')