# Create a class called Box in Python that has three attributes: length, width, and height.

# Define two methods for this class:

# A method to calculate the volume of the box.
# A method to display the box's information, including its volume.
# Write a driver program (a small piece of code that creates and uses your class) that:

# Creates two Box objects, with different dimensions.
# Displays each Box object's information.

class Box:
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height

    def calculate_volume(self):
        return self.length * self.width * self.height
    
    def box_detail(self):
        print(f"Length: {self.length}, Width: {self.width}, Height: {self.height}, Volume: {self.calculate_volume()}")

myFirstBox = Box(10, 10, 5)
mySecondBox = Box(20, 5, 10)

myBoxList = []
myBoxList.append(myFirstBox)
myBoxList.append(mySecondBox)

for box in myBoxList:
    box.box_detail()
