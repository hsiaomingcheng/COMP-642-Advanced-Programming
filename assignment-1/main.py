from customer import Customer
from plant import Plant
from order import Order
from nurserySystem import NurserySystem

# -> create system
mainSystem = NurserySystem()


# -> create customers
mainSystem.addCustomer(Customer(1, "Edward Xin", "edward@mail.com", "020-111-1111"))
mainSystem.addCustomer(Customer(2, "Mandy Garcia", "mandy@mail.com", "020-222-2222"))
mainSystem.addCustomer(Customer(3, "Mike Hardy", "mike@mail.com", "020-333-3333"))

# -> create plants
mainSystem.addPlant(Plant(1, "pine", "trees and shrubs",100, 50))
mainSystem.addPlant(Plant(2, "cactus", "pot plants", 20, 50))
mainSystem.addPlant(Plant(3, "papermint", "pot plants", 30, 40))
mainSystem.addPlant(Plant(4, "tomato", "vegetable seedlings", 10, 40))
mainSystem.addPlant(Plant(5, "papermint", "pot plants", 30, 20))

# -> checking if the plant stock level is enough
plant = mainSystem.plantInfo(1)

print(f"The plant's stock level is {plant.stockLevel}")

if plant.stockLevelCheck(60):
    print("The plant's stock level is enough.")
else:
    print("The plant's stock level is not enough.")

print("")

# -> making orders
mainSystem.placeOrder(1, 1, 10)
mainSystem.placeOrder(2, 2, 5)
mainSystem.placeOrder(1, 3, 5)
mainSystem.placeOrder(1, 4, 5)

# -> customer order history
print("=== Specific customer's order history ===")
mainSystem.customerOrderHistory(1)
print("")

# -> cancel order
print("=== order info before cancel ===")
print(mainSystem.orderInfo(1)) # order status before cancel
print("=== plant info before cancel ===")
print(mainSystem.plantInfo(1)) # plant stock level before cancel

print('')
mainSystem.cancelOrder(1)      # cancel order

print("=== order info after cancelled ===")
print(mainSystem.orderInfo(1)) # order status after cancelled
print("=== plant info after cancelled ===")
print(mainSystem.plantInfo(1)) # plant stock level after cancelled

# -> update order status
mainSystem.updateOrderStatus(2, 'collected')
print("")
print("=== Update order status ===")
print(mainSystem.orderInfo(2))

# -> list customers / list plants / list orders
print("")
print("=== Starting display Custome list===")
mainSystem.customerList()

print("")
print("=== Starting display Plant list===")
mainSystem.plantList()

print("")
print("=== Starting display Order list===")
mainSystem.orderList()