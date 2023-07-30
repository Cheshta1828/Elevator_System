from rest_framework import serializers
from .models import Building, Elevator, ElevatorRequest


class BuildingSerializer(serializers.ModelSerializer):
    """Serializer for building """
    
    class Meta:
        model = Building
        fields = '__all__'


class ElevatorSerializer(serializers.ModelSerializer):
    """
    Serializer for elevator status  
    """
    

    class Meta:
        model = Elevator
        fields = '__all__'


class ElevatorRequestSerializer(serializers.ModelSerializer):
    """
    Handling request inside elevator 
    """
    
    class Meta:
        model = ElevatorRequest
        fields = (
            'requested_floor',
            'destination_floor',
        )





class ElevatorRequestSerializer(serializers.Serializer):
    """
    Handling request inside elevator 
    """
    
    elevator_id = serializers.IntegerField(required=True)
    building_id = serializers.IntegerField(required=True)
    destination_floor = serializers.IntegerField(required=True)


class ElevatorRequestOutsideSerializer(serializers.Serializer):
    """
    A person standing outside the building requesting for an elevator can only send information about building and 
    the destination floor 
    """
    
    building_id = serializers.IntegerField(required=True)
    destination_floor = serializers.IntegerField(required=True)


class ElevatorStatusSerializer(serializers.Serializer):
    """
    Updating the status for elevator 
    """
    
    elevator_id = serializers.IntegerField(required=True)