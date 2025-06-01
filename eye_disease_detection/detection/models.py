from django.db import models
from django.utils import timezone

class Detection(models.Model):
    image = models.ImageField(upload_to='uploads/')
    prediction = models.CharField(max_length=100)
    confidence = models.FloatField(default=0.0)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.prediction} - {self.confidence:.2f}%"
    
    class Meta:
        ordering = ['-created_at']