// Main JavaScript for Eye Disease Detection System

document.addEventListener('DOMContentLoaded', function() {
    initializeImageUpload();
    initializeFormValidation();
    initializeAnimations();
});

// Image Upload Functionality
function initializeImageUpload() {
    const imageInput = document.getElementById('imageInput');
    const uploadZone = document.querySelector('.upload-zone');
    const previewContainer = document.getElementById('previewContainer');
    const imagePreview = document.getElementById('imagePreview');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const uploadForm = document.getElementById('uploadForm');

    if (!imageInput || !uploadZone) {
        console.log('Image input or upload zone not found');
        return;
    }

    // Click to upload
    uploadZone.addEventListener('click', function(e) {
        e.preventDefault();
        imageInput.click();
    });

    // Drag and drop functionality
    uploadZone.addEventListener('dragover', function(e) {
        e.preventDefault();
        e.stopPropagation();
        uploadZone.classList.add('dragover');
    });

    uploadZone.addEventListener('dragleave', function(e) {
        e.preventDefault();
        e.stopPropagation();
        uploadZone.classList.remove('dragover');
    });

    uploadZone.addEventListener('drop', function(e) {
        e.preventDefault();
        e.stopPropagation();
        uploadZone.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            imageInput.files = files;
            const event = new Event('change', { bubbles: true });
            imageInput.dispatchEvent(event);
        }
    });

    // File input change
    imageInput.addEventListener('change', function(e) {
        console.log('File input changed');
        handleImageSelect();
    });

    function handleImageSelect() {
        const file = imageInput.files[0];
        console.log('Selected file:', file);
        
        if (file) {
            // Validate file type
            if (!file.type.startsWith('image/')) {
                alert('Please select a valid image file.');
                imageInput.value = '';
                return;
            }

            // Validate file size (max 10MB)
            if (file.size > 10 * 1024 * 1024) {
                alert('File size should be less than 10MB.');
                imageInput.value = '';
                return;
            }

            // Show preview
            const reader = new FileReader();
            reader.onload = function(e) {
                if (imagePreview) {
                    imagePreview.src = e.target.result;
                }
                if (previewContainer) {
                    previewContainer.style.display = 'block';
                    previewContainer.classList.add('fade-in');
                }
                
                // Enable analyze button
                if (analyzeBtn) {
                    analyzeBtn.disabled = false;
                    analyzeBtn.classList.remove('btn-primary');
                    analyzeBtn.classList.add('btn-success');
                    analyzeBtn.innerHTML = '<i class="fas fa-microscope me-2"></i>Analyze Image';
                    console.log('Analyze button enabled');
                }

                // Update upload zone (but preserve the file input)
                const fileInputHtml = uploadZone.innerHTML;
                uploadZone.innerHTML = `
                    <div class="upload-icon mb-3">
                        <i class="fas fa-check-circle fa-3x text-success"></i>
                    </div>
                    <div class="upload-text">
                        <h5>Image Selected Successfully</h5>
                        <p class="text-muted">${file.name}</p>
                        <p class="text-muted">Click "Analyze Image" to proceed</p>
                    </div>
                    ${fileInputHtml}
                `;
                
                // Re-attach event listeners after DOM update
                const newFileInput = uploadZone.querySelector('input[type="file"]');
                if (newFileInput) {
                    newFileInput.files = imageInput.files;
                }
            };
            reader.readAsDataURL(file);
        }
    }

    // Form submission with loading state
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            console.log('Form submitted');
            
            // Check if file is selected
            if (!imageInput.files || imageInput.files.length === 0) {
                e.preventDefault();
                alert('Please select an image file first.');
                return false;
            }
            
            if (analyzeBtn) {
                analyzeBtn.innerHTML = `
                    <span class="spinner-border spinner-border-sm me-2" role="status"></span>
                    Analyzing Image...
                `;
                analyzeBtn.disabled = true;
            }
            
            // Show loading overlay
            showLoadingOverlay();
        });
    }

    // Direct button click handler as backup
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', function(e) {
            console.log('Analyze button clicked');
            if (!imageInput.files || imageInput.files.length === 0) {
                e.preventDefault();
                alert('Please select an image file first.');
                return false;
            }
        });
    }
}

// Form Validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// Initialize Animations
function initializeAnimations() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('fade-in');
        }, index * 100);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Alert System
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    // Insert at top of container
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto dismiss after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}

// Progress Bar Animation
function animateProgressBar(element, targetWidth) {
    let width = 0;
    const interval = setInterval(() => {
        if (width >= targetWidth) {
            clearInterval(interval);
        } else {
            width += 2;
            element.style.width = width + '%';
        }
    }, 20);
}

// Initialize progress bars on result page
document.addEventListener('DOMContentLoaded', function() {
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const targetWidth = parseFloat(bar.getAttribute('aria-valuenow'));
        setTimeout(() => {
            animateProgressBar(bar, targetWidth);
        }, 500);
    });
});

// Image zoom functionality for result page
function initializeImageZoom() {
    const images = document.querySelectorAll('.card-body img');
    images.forEach(img => {
        img.addEventListener('click', function() {
            // Create modal for image zoom
            const modal = document.createElement('div');
            modal.className = 'modal fade';
            modal.innerHTML = `
                <div class="modal-dialog modal-lg modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Image Preview</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body p-0">
                            <img src="${this.src}" class="img-fluid w-100" alt="Zoomed Image">
                        </div>
                    </div>
                </div>
            `;
            
            document.body.appendChild(modal);
            const bsModal = new bootstrap.Modal(modal);
            bsModal.show();
            
            // Remove modal after hiding
            modal.addEventListener('hidden.bs.modal', function() {
                document.body.removeChild(modal);
            });
        });
        
        // Add cursor pointer
        img.style.cursor = 'pointer';
        img.title = 'Click to zoom';
    });
}

// Initialize image zoom on page load
document.addEventListener('DOMContentLoaded', initializeImageZoom);

// Add loading overlay
function showLoadingOverlay() {
    const overlay = document.createElement('div');
    overlay.id = 'loadingOverlay';
    overlay.innerHTML = `
        <div class="d-flex justify-content-center align-items-center h-100">
            <div class="text-center text-white">
                <div class="spinner-border mb-3" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <h5>Analyzing your image...</h5>
                <p>Please wait while our AI processes your image</p>
            </div>
        </div>
    `;
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.8);
        z-index: 9999;
        display: flex;
    `;
    
    document.body.appendChild(overlay);
}

function hideLoadingOverlay() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.remove();
    }
}

// Add to form submission
document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function() {
            showLoadingOverlay();
        });
    }
});