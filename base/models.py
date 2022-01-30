from ssl import create_default_context
from django.db import models

# Create your models here.

class Room(models.Model):
    # host = 
    # topic = 
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # participants =    Stores all the users that are currently active in the room
    updated = models.DateTimeField(auto_now=True)       # Updated on every updation
    created = models.DateTimeField(auto_now_add=True)   # Only updated when created
    
    def __str__(self):
        return str(self.name)