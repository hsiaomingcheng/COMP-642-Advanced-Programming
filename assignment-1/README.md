## Structure

This project includes 5 files.

nurserySystem.py, customer.py, order.py, plant.py, and main.py. The first four are the core of the project.

nurserySystem is like a central system or platform. User can do different operate through this system, and it connects the other classes.

customer.py is a class document the details of a customer and methods

order.py is a class document the details of a order and methods

plant.py is a class document the details of a plant and methods

lastly, main.py is a driver program that display all scenerios and testing.

## Requirements

1. >The system needs to know exactly how much stock we have for each plant, and it needs to stop an order going through if there is not enough.  
We should also be able to check whether a specific plant has enough stock before someone orders it, that comes up all the time on the phone

    For stock of each plant, user can check the stock through plantInfo method, it return the specific plant, then it shows the stock level through its getter, `stockLevel`.

    In nerserySysyem, user can place an order through `placeOrder` method and if the user is trying to place an order amount that is greater than stock level, it would be stop by `stockLevelCheckAndBuy` and `stockLevelCheck` these methods' checking.

2. >When an order does go through, the stock on hand needs to go down straight away, and it should never be allowed to go below zero

    This is also done by `placeOrder` method, it calls `stockLevelCheckAndBuy` to check stock and once it confirm the plant has enough stock, it would reduct the stock level immediately, and because it confirm it has enought stock level. Thus, it would nevel go below zero.

3. >we currently keep track of an ID... We also note the name, the category (trees and shrubs, perennials, pot plants, or vegetable seedlings), the price, and the stock level

    This one is handled by `Plant` class, it has all the attributes it required.

4. >we really need something that tells them apart, a customer ID. We also need their name and either an email address or phone number

    This one is done by `Customer` class, document every attributes.

5. >which customer it is for, which plant it is for, how many they ordered, when they ordered it, dates written as DD-MM-YYYY... the current status (pending, collected, or cancelled), and the order total

    `Order` class has these attributes, including the date with specific date format, and order total.

6. >Each order is just for one type of plant at a time, if someone wants two different plants, we treat that as two separate orders

    Currently, the `placeOrder` only accept one plantId as parameter, which means it only handle one plant at a time. If customer want two plants, they need to place two orders.

7. >If someone orders ten or more of the same plant type in one order, the order total should have a ten percent discount applied

    This one is implemented in `Order` class, a private method called `__totalAmount`, it has two parameters, `plantPrice` and `amount`, then if the amount is equal or greater than 10. It would times 0.9 of its total price.

8. >An order can be cancelled and the stock returned to what is available, but only while it is still pending. Once it has been collected, it can no longer be cancelled

    This has two part, `cancelOrder` for cancel those orders with `pending` status. `updateOrderStatus` is reponsible for changing status to `collected` or `pending`, and this method does not allow switch status to `cencelled` or trying switch back to `pending` or `collected` from `cencelled`. The reason why `updateOrderStatus` allow status change to `pending` or `collected` is in real world, someone may decide to switch back to `pending` from `collected` due to some reasons. Thus, I allow `pending` and `collected` can switch its status.

9. >be able to pull up a customer's order history when we need it, without having to go through the whole notebook

    `customerOrderHistory` is the method that handle this requirement. It allow user to enter the specific customer's id, then it shows all the order(including cancenlled) of this customer's.

10. >someone once wrote down an order for zero plants by mistake... another time a plant's price got written down as a negative number by mistake... Whatever gets built should catch mistakes like these at the point they are entered, not afte

    In `placeOrder` method, it checked the amount at the top of the method, if the amount is smaller than 0, then it would be stopped by `raise ValueError("The amount need to be greatter than 0.")`.
    For the plant price, we check the plant price in `Plant` class's initializer, the price cannot smaller than 0. It allows to set as 0 because maybe some plant really need to be 0 for the price.

11. >we need to be able to add new plants and customers in the first place, without accidentally adding the same one twice

    In `addPlant`, I verify the plant id before add a new one. For customer, `addCustomer` method stop adding a new customer if it does not provide `email` or `phone number`. Then, verify the `email` and `phone number` separately because the customer are allowed to only provide one of them.

12. >see lists of what plants are available, every order we have got on record, and who our customers are

    These are implemented by customerList, plantList, and orderList. Each list do a for loop of its list in nurserySystem.py file.

## Assumptions

1. The requirements do not mention if a `colleted` order can switch back to `pending` or not. In my opinion, someone could make a mistake, they may find out the order is actually not done yet. So, it should change back to `pending` status and that's why I let `updateOrderStatus` allow it update order status when it is `pending` or `colleted`.

2. In `placeOrder` method, I verify the customer ID and plant ID that come from the parameters before making an order. In case the user entered the wrong customer ID or plant ID that is not created before.

3. When cancelling an order, I verify the order ID is an actual ID before cancelling. The owner did not mention this, but I set an info message for the user when they try to cancel a non-existent order.

## Driver program

`main.py` is the driver program. It create `NurserySystem` at the very beginning then starts to create `customer`, `plant`, and `order`.

Before create `order`, it conducted a checking of stock level.

Then, showing `customer order history`, and mocking `cancel order` and `update order status` process.

Lastly, display the lists of `customer`, `plant`, and `order`.