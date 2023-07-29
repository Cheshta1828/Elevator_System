from django.db import models
from .constants import RunningStatus
class Building(models.Model):
    """
    Building model having some number of elevators that can go from minimum floors to totalfloors

    """

    b_name = models.CharField(max_length=50)
    total_elevators = models.PositiveSmallIntegerField()
    minimumfloors= models.IntegerField(default=0)
    totalfloors = models.IntegerField()#maximum floors 
    def __str__(self) -> str:
        return str(self.id)+ ":" +str(self.b_name)   
    def create_elevators(self, building_id, total_elevators): 
        """
        As soon as building is created with certain number of elevators then thaat number of elevator 
        objects are also saved in database to avoid redundancy

    """
        for i in range(total_elevators):
            elevator_object = Elevator.objects.create(
                building_id=building_id,
                e_number=i+1,
            )
            elevator_object.save()

class Elevator(models.Model):
    """
    Elevator model associated with  particular building 
    
    
    """
    

    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    e_number = models.IntegerField()
    running_status = models.CharField(max_length=20, choices=[(status.value, status.name.title(
    )) for status in RunningStatus], default=RunningStatus.STANDING_STILL.value)
    current_floor = models.IntegerField(default=0)
    is_running = models.BooleanField(default=False)
    is_door_open = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.e_number} on building {self.building}"
class ElevatorRequest(models.Model):
    """
    Model for handling requests for elevator 
    
    """
    
    destination_floor = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)