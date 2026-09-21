from customer import Customer
from plant import Plant
from order import Order
from nurserySystem import NurserySystem

# -> create system
mainSystem = NurserySystem()


# -> create customers
mainSystem.add_customer(Customer(1, "Edward Xin", "edward@mail.com", "020-111-1111"))
mainSystem.add_customer(Customer(2, "Mandy Garcia", "mandy@mail.com", "020-222-2222"))
mainSystem.add_customer(Customer(3, "Mike Hardy", "mike@mail.com", "020-333-3333"))

# -> create plants
mainSystem.add_plant(Plant(1, "pine", "trees and shrubs",100, 50))
mainSystem.add_plant(Plant(2, "cactus", "pot plants", 20, 50))
mainSystem.add_plant(Plant(3, "papermint", "pot plants", 30, 40))
mainSystem.add_plant(Plant(4, "tomato", "vegetable seedlings", 10, 40))
mainSystem.add_plant(Plant(5, "papermint", "pot plants", 30, 20))

# -> checking if the plant stock level is enough
plant = mainSystem.plant_info(1)

print(f"The plant's stock level is {plant.stock_level}")

if plant.stock_level_check(60):
    print("The plant's stock level is enough.")
else:
    print("The plant's stock level is not enough.")

print("")

# -> making orders
mainSystem.place_order(1, 1, 10)
mainSystem.place_order(2, 2, 5)
mainSystem.place_order(1, 3, 5)
mainSystem.place_order(1, 4, 5)

# -> customer order history
print("=== Specific customer's order history ===")
mainSystem.customer_order_history(1)
print("")

# -> cancel order
print("=== order info before cancel ===")
print(mainSystem.order_info(1)) # order status before cancel
print("=== plant info before cancel ===")
print(mainSystem.plant_info(1)) # plant stock level before cancel

print('')
mainSystem.cancel_order(1)      # cancel order

print("=== order info after cancelled ===")
print(mainSystem.order_info(1)) # order status after cancelled
print("=== plant info after cancelled ===")
print(mainSystem.plant_info(1)) # plant stock level after cancelled

# -> collect order
mainSystem.collect_order(2)
print("")
print("=== Collect order ===")
print(mainSystem.order_info(2))

# -> list customers / list plants / list orders
print("")
print("=== Starting display Custome list===")
mainSystem.customer_list()

print("")
print("=== Starting display Plant list===")
mainSystem.plant_list()

print("")
print("=== Starting display Order list===")
mainSystem.order_list()
