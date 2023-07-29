from rest_framework import serializers
from .models import Building, Elevator, ElevatorRequest


class BuildingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Building
        fields = '__all__'


class ElevatorSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Elevator
        fields = '__all__'


class ElevatorRequestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ElevatorRequest
        fields = (
            'requested_floor',
            'destination_floor',
        )


class ElevatorRequestSerializerAll(serializers.ModelSerializer):
    
    class Meta:
        model = ElevatorRequest
        fields = '__all__'


class ElevatorRequestSerializer(serializers.Serializer):
    
    elevator_id = serializers.IntegerField(required=True)
    building_id = serializers.IntegerField(required=True)
    destination_floor = serializers.IntegerField(required=True)


class ElevatorRequestOutsideSerializer(serializers.Serializer):
    
    building_id = serializers.IntegerField(required=True)
    destination_floor = serializers.IntegerField(required=True)


class ElevatorStatusSerializer(serializers.Serializer):
    
    elevator_id = serializers.IntegerField(required=True)