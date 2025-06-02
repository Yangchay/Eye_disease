from django.shortcuts import render
from .forms import ImageUploadForm
from .utils import predict_image # Import the predict_image function
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
# No longer strictly need JsonResponse unless you're making an API endpoint

def home(request):
    result = None
    form = ImageUploadForm()
    
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Handle file upload
                image_file = request.FILES['image']
                
                # Save the file. Consider saving to a more permanent path
                # if you want the user to see the image on the results page.
                # Let's use 'media/uploaded_images/' for example
                # Ensure MEDIA_ROOT and MEDIA_URL are configured in your Django settings.py
                upload_dir = 'uploaded_images'
                file_name = default_storage.save(os.path.join(upload_dir, image_file.name), ContentFile(image_file.read()))
                
                # Construct the full path to the saved file for utils.py
                # default_storage.path() is useful for getting the absolute path
                # Note: default_storage.path() requires MEDIA_ROOT to be local filesystem path
                uploaded_file_path = default_storage.path(file_name)
                
                # Make prediction using the updated utils.py which returns a dict
                prediction_result = predict_image(uploaded_file_path)
                
                # Now, unpack the dictionary returned by predict_image
                if 'error_message' in prediction_result:
                    # If utils.py returned an error
                    result = {
                        'class': prediction_result.get('prediction', 'Error'),
                        'confidence': prediction_result.get('confidence', 0),
                        'error_message': prediction_result.get('error_message', 'Unknown error'),
                        'image_url': default_storage.url(file_name) # Still show the image
                    }
                else:
                    # If prediction was successful
                    result = {
                        'class': prediction_result['prediction'],
                        'confidence': prediction_result['confidence'],
                        'all_confidences': prediction_result['all_confidences'], # Pass all confidences
                        'image_url': default_storage.url(file_name) # URL to display image
                    }
                
                # IMPORTANT: DO NOT DELETE THE FILE HERE if you want to display it on the page.
                # If you need to clean up, do it later (e.g., a scheduled task, or after session ends)
                # For development, leaving it can be fine, but manage storage in production.
                # Example: If you really need to delete quickly, consider doing it from the template
                # via an AJAX call or on a subsequent page load if not displaying it.
                # For now, let's remove os.remove(tmp_file)

            except Exception as e:
                # This catch-all for unexpected errors in the view itself
                result = {
                    'class': 'Critical Error',
                    'confidence': 0,
                    'error_message': f"An unexpected error occurred: {str(e)}",
                    'image_url': None # No image URL if the upload failed
                }
    
    return render(request, 'disease_detector/home.html', {
        'form': form,
        'result': result
    })

def about(request):
    developer = {
        'name': 'Yangchen Dema',
        'role': 'Developer',
        'bio': 'I am a passionate and driven Data Science student currently pursuing my degree at Sherubtse College. Eager to explore the fascinating world of data and its applications, I am constantly seeking opportunities to learn and grow in this rapidly evolving field.',
        'image': 'images/developer.jpg'
    }
    return render(request, 'disease_detector/about.html', {'developer': developer})