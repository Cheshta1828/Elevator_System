from django.shortcuts import render
from .models import Building ,Elevator
from rest_framework import status
from .logic import ElevatorController

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
elevators = {}
from .models import Building, Elevator, ElevatorRequest
from .serializers import *
from .utils import get_floor_distance

from .constants import RunningStatus

# Create your views here.
class BuildingView(viewsets.ModelViewSet):
    print("in view")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.building = Building()
    
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

    def perform_create(self, serializer):
        serializer.save()
        self.building.create_elevators(
            total_elevators=serializer.data['total_elevators'],
            building_id=serializer.data['id']
        )
class ElevatorView(viewsets.ModelViewSet):
    
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer

class ElevatorOutsideRequestView(APIView):

    serializer_class = ElevatorRequestOutsideSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

    def post(self, request):
        '''
        function used when the user request for the Elevator from outside 
        we calculated the elevator which is minimum distance from this floor
        '''
        serializer = ElevatorRequestOutsideSerializer(data=request.data)
        if serializer.is_valid():
            building_id = serializer.validated_data['building_id']
            user_destination_floor = serializer.validated_data['destination_floor']
            try:
                building_obj = Building.objects.get(id=building_id)
            except Building.DoesNotExist:
                return Response("Building not found", status=status.HTTP_404_NOT_FOUND)

            if user_destination_floor > building_obj.totalfloors: 
                return Response("Destination floor should be less than max floor", status=status.HTTP_400_BAD_REQUEST)

            if user_destination_floor < building_obj.minimumfloors: 
                return Response("Destination floor should be less than min floor", status=status.HTTP_400_BAD_REQUEST)

            elevator =  Elevator.objects.filter(
                building_id=building_id).exclude(running_status=RunningStatus.NOT_WORKING.value)
            
            user_elevator = -1
            min_elevator_current_position = -1
            min_distance = 1000 
            for obj in elevator:
                
                current_floor = obj.current_floor
               
                current_lift_distance = get_floor_distance(user_destination_floor,int(current_floor))
                if current_lift_distance < min_distance:
                    user_elevator = obj.id
                    min_distance = current_lift_distance
                    min_elevator_current_position=current_floor

            if  user_elevator !=- 1 :
                elevator = elevators.get(user_elevator, None)
                if not elevator:
                    elevator = ElevatorController(
                        elevator_id=user_elevator, initial_floor=int(min_elevator_current_position), building_id=building_id, min=building_obj.minimumfloors, max=building_obj.totalfloors)
                    elevators[user_elevator] = elevator

                request = ElevatorRequest(destination_floor=user_destination_floor)
                request.save()
                elevator.add_request(request)

                if not elevator.is_alive():
                    elevator.start()

                return Response("Request sent successfully", status=status.HTTP_200_OK)
            else:
                return Response("No elevator found", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


