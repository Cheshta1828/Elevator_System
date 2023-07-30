import time
import threading
from .models import Elevator
import time
from queue import Queue
from .constants import RunningStatus



class ElevatorController(threading.Thread):
    """Threading implemented to ease the multiple elevator system"""
    
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
        
    def get_array(self): 
        """ function for getting array of floors"""
        return self.arr

    def update_running_status(self, elevator_status,elevator):
        """ function for updating the status of elevator """
        elevator_status["running_status"] = self.running_status
        elevator.running_status=self.running_status
        elevator.save()
        

    def update_door(self, elevator_status,elevator):
        """ function for updating the door status of elevator """
        elevator_status["is_door_open"] = int(self.is_door_open)
        elevator.is_door_open=self.is_door_open
        elevator.save()
       

    def update_current_floor(self, elevator_status,elevator):
        """ function for updating the current floor status of elevator """
        elevator_status["current_floor"] = self.current_floor
        elevator.current_floor=self.current_floor
        elevator.save()
        

    def run(self):
        print("I am run method") #debug
        self.is_running = True #update the running status 
        while self.is_running: #run until all requests are dealt 

            
            if not self.queue.empty(): #checking if the queue still has requests  
                request = self.queue.get()
                """checking if in between floor requests are already processed then delete them  """
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
               

                elevator = Elevator.objects.get(id=self.elevator_id) #get that elevator
                elevator.is_busy = True
                elevator.running_status = self.running_status
                print("is running",self.is_running)
                elevator.save()
                print("is running",self.is_running)
                self.update_running_status(elevator_status,elevator)#update running status
                elevator = Elevator.objects.get(id=self.elevator_id)
                elevator.running_status = self.running_status
                print("is running",self.is_running)
                elevator.save()
                while self.current_floor != request.destination_floor:
                    
                    if self.arr[self.current_floor - self.min] == 1:
                        print("door open")
                        self.is_door_open = True
                        self.update_door(elevator_status,elevator)
                        time.sleep(2) 
                        """ as opening and closing of doors take some time  """
                        
                        self.is_door_open = False
                        self.update_door(elevator_status,elevator)
                        self.arr[self.current_floor - self.min] = 0
                        print("door close")
                    
                    
                    time.sleep(2)
                    self.current_floor += 1 if self.running_status == RunningStatus.GOING_UP.value else -1
                    print(f"Elevator {self.elevator_id} is at floor {self.current_floor} and destination {request.destination_floor} .")
                    print("is running",self.is_running) #debug
                    self.update_current_floor(elevator_status,elevator)#update the current floor 
                """When reached the destination """
                self.arr[self.current_floor - self.min] = 0
                self.running_status = RunningStatus.STANDING_STILL.value
                self.update_running_status(elevator_status,elevator)
                print("door open")
                self.is_door_open = True
                self.update_door(elevator_status,elevator)
                time.sleep(2)
                self.is_door_open = False
                self.update_door(elevator_status,elevator)
                print("door close")
                elevator.current_floor = self.current_floor
                elevator.running_status = self.running_status
                print("is running",self.is_running)
                elevator.is_busy = False
                print(f"Elevator {self.elevator_id} is at floor {self.current_floor} and destination {request.destination_floor} .")
                print("is runnning",self.is_running)
                elevator.save()
                """request is completed ,delete it """
               
                request.delete() 
                
            else:
                
                time.sleep(2)

    def add_request(self, request): 
        """ function to add request to queue"""
        
        index = request.destination_floor - self.min
        self.arr[index] = 1 #mark the array index as 1 i.e lift need to stop at that position if lies in between 
        self.queue.put(request)
        print(f"Request added to Elevator {self.elevator_id} queue: {request}") #just for checking the status of lift
