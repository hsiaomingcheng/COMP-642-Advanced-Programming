# Create a class called Elevator based on the information below.
# Write a simple application to simulate the elevator's operation.
# You may assume that the building has 6 floors.
#
# attributes: int currentFloor;
# methods: gotoFloor(), gotoGround(), openDoor(), closeDoor()

class Elevator:
    def __init__(self):
        self.currentFloor = 0

    def gotoFloor(self, floor):
        self.currentFloor = floor

        if floor == 0:
            return
        
        if floor <= 6 and floor > 0:
            print(f"We're at the {floor} floor")
        else:
            print("Please enter valid floor number")
    
    def gotoGround(self):
        self.gotoFloor(0)
        print("We're at the ground floor")
    
    def openDoor(self):
        print("The door is opening!")
    
    def closeDoor(self):
        print("The door is closing!")

# assign Elevator class to ele
ele = Elevator()

# open door
ele.openDoor()

# close door
ele.closeDoor()

# to ground floor
ele.gotoGround()

# to 2 floor
ele.gotoFloor(2)

# invalid floor number
ele.gotoFloor(10)