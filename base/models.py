from ssl import create_default_context
from tkinter import CASCADE
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
    

class Message(models.Model):
    # user = 
    room = models.ForeignKey(Room, on_delete=CASCADE)
        #? If a room is deleted, Delete all the message inside the room
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)       # Updated on every updation
    created = models.DateTimeField(auto_now_add=True)   # Only updated when created
    
    def __str__(self):
        return str(self.body[0:50])     #* Only the first 50 characters in the preview of message