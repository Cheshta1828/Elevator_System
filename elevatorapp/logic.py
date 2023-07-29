import time
import threading
from .models import Elevator
import time
from queue import Queue
from .constants import RunningStatus



class ElevatorController(threading.Thread):
    
    def __init__(self, elevator_id, initial_floor, building_id, min, max):
        
        super().__init__()
        self.elevator_id = elevator_id
        self.current_floor = initial_floor
        self.building_id = building_id
        self.queue = Queue()
        self.is_running = False
        self.is_door_open = False
        self.min = min
        
        self.arr = [0] * (max-min+1)

    def update_running_staus(self, elevator_status,):
        elevator_status["running_status"] = self.running_status
        

    def update_door(self, elevator_status,):
        elevator_status["is_door_open"] = int(self.is_door_open)
       

    def update_current_floor(self, elevator_status,):
        elevator_status["current_floor"] = self.current_floor
        

    def run(self):
        
        self.is_running = True
        while self.is_running:
            
            if not self.queue.empty():
                request = self.queue.get()
                if self.arr[request.destination_floor - self.min] == 0:
                    
                    request.delete()
                    continue

                if request.destination_floor > self.current_floor:
                    self.running_status = RunningStatus.GOING_UP.value
                else:
                    self.running_status = RunningStatus.GOING_DOWN.value

                elevator_status = {
                    "current_floor": self.current_floor,
                    "is_door_open": int(self.is_door_open),
                    "running_status": self.running_status
                }
               

                elevator = Elevator.objects.get(id=self.elevator_id)
                elevator.is_busy = True
                elevator.running_status = self.running_status
                elevator.save()
                self.update_running_staus(elevator_status)
                elevator = Elevator.objects.get(id=self.elevator_id)
                elevator.running_status = self.running_status
                elevator.save()
                while self.current_floor != request.destination_floor:
                    
                    if self.arr[self.current_floor - self.min] == 1:
                        print("door open")
                        self.is_door_open = True
                        self.update_door(elevator_status)
                        time.sleep(2)
                        
                        self.is_door_open = False
                        self.update_door(elevator_status)
                        self.arr[self.current_floor - self.min] = 0
                        print("door close")
                    
                    time.sleep(2)
                    self.current_floor += 1 if self.running_status == RunningStatus.GOING_UP.value else -1
                    print(
                        f"Elevator {self.elevator_id} is at floor {self.current_floor} and destination {request.destination_floor} .")
                    self.update_current_floor(elevator_status)

                self.arr[self.current_floor - self.min] = 0
                self.running_status = RunningStatus.STANDING_STILL.value
                self.update_running_staus(elevator_status)
                print("door open")
                self.is_door_open = True
                self.update_door(elevator_status)
                time.sleep(2)
                self.is_door_open = False
                self.update_door(elevator_status)
                print("door close")
                elevator.current_floor = self.current_floor
                elevator.running_status = self.running_status
                elevator.is_busy = False
                elevator.save()
               
                request.delete()
            else:
                
                time.sleep(2)

    def add_request(self, request):
        
        index = request.destination_floor - self.min
        self.arr[index] = 1
        self.queue.put(request)
        print(f"Request added to Elevator {self.elevator_id} queue: {request}")