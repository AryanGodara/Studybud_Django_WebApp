from rest_framework.serializers import ModelSerializer

from base.models import Room

    #? A serializer turns a python-django model into a JSON object kinda

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'