from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_term = models.CharField(max_length=255, null=True, blank=True)
    location_name = models.CharField(max_length=255, blank=True, null=True)
    location_image = models.URLField(blank=True, null=True)
    searched_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.search_term} by {self.user.username}"
