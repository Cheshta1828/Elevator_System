from enum import Enum
class RunningStatus(Enum):
    """
    Running status has 4 choices 
    """
    
    GOING_UP = 'going_up'
    STANDING_STILL = 'standing_still'
    GOING_DOWN = 'going_down'
    NOT_WORKING = 'not_working'