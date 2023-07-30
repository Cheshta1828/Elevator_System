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
    """
    Creating ,Updating ,Viewing and deleting the buildings

    """
    
    
    
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
    """
    Creating ,Updating ,Viewing the Elevators
    
    """
    
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer

class ElevatorOutsideRequestView(APIView):

    serializer_class = ElevatorRequestOutsideSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

    def post(self, request):
        
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
                running_status =  obj.running_status
                array_of_floors = None
                if elevator:
                        array_of_floors = elevator.get_array()
               
                current_lift_distance = get_floor_distance(user_destination_floor,int(current_floor),running_status,array_of_floors)
                if current_lift_distance < min_distance:
                    user_elevator = obj.id
                    min_distance = current_lift_distance
                    min_elevator_current_position=current_floor

            if  user_elevator !=- 1 :
                elevator = elevators.get(user_elevator, None)
                if not elevator:
                    elevator = ElevatorController(elevator_id=user_elevator, initial_floor=int(min_elevator_current_position), building_id=building_id, min=building_obj.minimumfloors, max=building_obj.totalfloors)
                    elevators[user_elevator] = elevator

                request = ElevatorRequest(destination_floor=user_destination_floor)
                """ saving request in elevator request model 
                """
                request.save()
                elevator.add_request(request)

                if not elevator.is_alive():
                    elevator.start()

                return Response("Request sent successfully", status=status.HTTP_200_OK)
            else:
                return Response("No elevator found", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ElevatorInsideRequestView(APIView):

    serializer_class = ElevatorRequestSerializer
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self, request):
        
        serializer = ElevatorRequestSerializer(data=request.data)
        if serializer.is_valid():
            building_id = serializer.validated_data['building_id']
            destination_floor = serializer.validated_data['destination_floor']
            elevator_id = serializer.validated_data['elevator_id']
            try:
                building_obj = Building.objects.get(id=building_id)
            except Building.DoesNotExist:
                return Response("Building not found", status=404)
            if destination_floor > building_obj.totalfloors: 
                return Response("Destination floor should be less than max floor", status=status.HTTP_400_BAD_REQUEST)

            if destination_floor < building_obj.minimumfloors: 
                return Response("Destination floor should be less than min floor", status=status.HTTP_400_BAD_REQUEST)
            try:
                elevator_obj = Elevator.objects.get(id=elevator_id)
            except Elevator.DoesNotExist:
                return Response("Elevator not found", status=404)
            if elevator_obj:
                
                if elevator_obj.id not in elevators:
                    elevators[elevator_obj.id] = ElevatorController(
                        elevator_id=elevator_obj.id, initial_floor=elevator_obj.current_floor, building_id=building_id, min=building_obj.minimumfloors, max=building_obj.totalfloors)
                elevator = elevators[elevator_obj.id]
                request = ElevatorRequest(destination_floor=destination_floor)
                request.save()
                elevator.add_request(request)
                
                if not elevator.is_alive():
                    elevator.start()
                return Response("Request sent ", status=200)
            
            else:
                return Response("Elevator does not exist", status=400)
        
        else:
            return Response(serializer.errors, status=400)


class ElevatorStatus(APIView):

    serializer_class = ElevatorStatusSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       

    def post(self, request):
        serializer = ElevatorStatusSerializer(data=request.data)
        if serializer.is_valid():
            elevator_id = serializer.validated_data['elevator_id']
            try:
                elevator_obj = Elevator.objects.get(id=elevator_id)
            except Elevator.DoesNotExist:
                return Response("Elevator does not exist", status=404)

           
                
            is_running = False
            
            current_floor = elevator_obj.current_floor
            is_door_open = elevator_obj.is_door_open
            running_status = elevator_obj.running_status
            is_running = elevator_obj.is_running
            print("is_running",is_running)
            elevator_status = {
                    "current_floor": int(current_floor),
                    "is_door_open": int(is_door_open),
                    "running_status": running_status
                }
                

            
            message = "data fetched"
            data = {
                "current_floor": current_floor,
                "is_door_open": is_door_open,
                "running_status": running_status,
                "is_running": is_running
            }
            result = {
                'data': data,
                "message": message
            }
            return Response(result, status=200)
        else:
            return Response(serializer.errors, status=400)
