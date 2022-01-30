from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
    #? A topic can have multiple rooms, but a room can only have one topic
    #* There can be many places(rooms) to discuss a topic(say, anime). But an 'anime room'
    #* should only be used to discuss anime, not anything else
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
        # The person that hosts the room
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
        # The topic of conversation inside the room
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # participants =    Stores all the users that are currently active in the room
    updated = models.DateTimeField(auto_now=True)       # Updated on every updation
    created = models.DateTimeField(auto_now_add=True)   # Only updated when created
    
    class Meta:
        ordering = ['-updated', '-created']
    
    def __str__(self):
        return self.name
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
        #? If a user is deleted, delete all of its messages 
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
        #? If a room is deleted, Delete all the message inside the room
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)       # Updated on every updation
    created = models.DateTimeField(auto_now_add=True)   # Only updated when created
    
    def __str__(self):
        return self.body[0:50]     #* Only the first 50 characters in the preview of message