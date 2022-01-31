from urllib import response
from rest_framework.decorators import api_view
from rest_framework.response import Response

from base.models import Room
from .serializers import RoomSerializer


@api_view(['GET'])  #? Contains the list of 'requests/methods' permitted to access this view
def getRoutes(request):
    routes = [
        'GET /api',             # If someone just searches 'empty', they'll go to the api homepage
        'GET /api/rooms',       # Create an API to access all the rooms on our website's database
        'GET /api/rooms/:id'    # Create an API to access a particular room
    ]
    
    return Response(routes)
                    
                    
@api_view(['GET'])
def getRooms(requests):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
        #? Many just means, that there are more than one object in the queryset
    
    return Response(serializer.data)


@api_view(['GET'])
def getRoom(requests, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
        #? There can only be one room, with a particular ID
            
    return Response(serializer.data)