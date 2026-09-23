## Structure

This project includes 5 files: `customer.py`, `plant.py`, `order.py`, `nurserySystem.py`, and `main.py`. The first four are the core of the project.

`nurserySystem.py` is the central system. It owns the collections of customers, plants, and orders, and coordinates operations that need more than one of them (e.g. placing an order needs a valid customer and a valid plant). It does not duplicate validation that a class already owns for itself.

`customer.py` documents a customer's details and owns all validation of its own data (id, name, and having at least an email or a phone number), including whether two customers would conflict on email/phone.

`plant.py` documents a plant's details (id, name, category, price, stock level) and owns its own validation (valid category, non-negative price) and its own stock operations (`add_stock`, `stock_level_check`, `stock_level_check_and_buy`).

`order.py` documents an order's details. An `Order` holds the actual `Customer` and `Plant` objects it belongs to, not just their ids — this lets it derive the customer/plant id, name, and total price directly, and lets `cancel()` return stock to its own plant without `NurserySystem` having to look the plant up again.

Lastly, `main.py` is a driver program that displays all scenarios and testing, including the error cases (negative price, zero-quantity order, invalid ids) that the system is expected to reject.

## Requirements

1. > The system needs to know exactly how much stock we have for each plant, and it needs to stop an order going through if there is not enough. We should also be able to check whether a specific plant has enough stock before someone orders it, that comes up all the time on the phone.

    `plant_info(plant_id)` returns the `Plant` object, and its `stock_level` getter exposes the current stock — this is what lets staff answer "how much do we have" on the phone before an order is even placed (demonstrated directly in `main.py`). `stock_level_check(amount)` lets anyone ask "is there enough?" without changing anything.

    When an order actually goes through, `place_order()` doesn't call `stock_level_check` and then separately reduce the stock — it calls `stock_level_check_and_buy(amount)`, a single method on `Plant` that does both the check and the deduction together. Keeping check-and-deduct as one atomic operation on `Plant` itself (rather than `NurserySystem` checking, then separately telling `Plant` to reduce) means the "never go below zero" rule is enforced in exactly one place, and there's no window where two different callers could both see "enough stock" before either one actually deducts it.

2. > When an order does go through, the stock on hand needs to go down straight away, and it should never be allowed to go below zero.

    This is handled the same way as Requirement 1 — `place_order()` calls `stock_level_check_and_buy()`, which checks and deducts stock as a single step on `Plant` itself. Because the deduction only happens after the check succeeds, and both happen inside the same method call with no other code running in between, the stock level can never be pushed below zero — there is no separate "reduce stock" call that a caller could make without first checking.

3. > we currently keep track of an ID... We also note the name, the category (trees and shrubs, perennials, pot plants, or vegetable seedlings), the price, and the stock level.

    `Plant` holds all five attributes (`id`, `name`, `category`, `price`, `stock_level`) as required. Beyond just storing them, `Plant` validates `category` against the exact four options listed in the requirement (`VALID_CATEGORIES`) and rejects a negative `price` — both in the constructor and again in their setters, so an invalid category or price can never enter the system, whether it's set at creation time or updated later.

4. > we really need something that tells them apart, a customer ID. We also need their name and either an email address or phone number.

    `Customer` holds `id`, `name`, `email`, and `phone_number`. The requirement says "either an email address or phone number", so the constructor enforces exactly that: it rejects a customer with both fields blank, but allows either one to be blank as long as the other is filled in. `id` is also validated as a positive integer at creation.

5. > which customer it is for, which plant it is for, how many they ordered, when they ordered it, dates written as DD-MM-YYYY... the current status (pending, collected, or cancelled), and the order total.

    `Order` holds all of these: which customer and which plant it's for, quantity, date, status, and total price. "Which customer it is for" and "which plant it is for" are modeled as direct references to the actual `Customer` and `Plant` objects, not just their id numbers — `__str__` prints the customer's and plant's actual names.

    The date format is enforced, not just documented: the constructor validates it's in DD-MM-YYYY using `datetime.strptime`, and rejects anything else. Status is restricted to exactly the three values the requirement names — there's no way to set it to an arbitrary string, since it can only change through `cancel()` or `collect()`, both of which only ever set it to `'cancelled'` or `'collected'`.

6. > Each order is just for one type of plant at a time, if someone wants two different plants, we treat that as two separate orders.

    `place_order(customer_id, plant_id, amount)` takes a single `plant_id`, and `Order.__init__` takes a single `plant: Plant` — not a list. This isn't just a calling convention; it's enforced by the shape of `Order`'s own data: there is no way to construct an `Order` referencing more than one plant, so a customer wanting two different plants necessarily has to place two separate orders, each producing its own `Order` object.

7. > If someone orders ten or more of the same plant type in one order, the order total should have a ten percent discount applied.

    This is implemented in `Order.__total_amount(plant_price, amount)`, a private method called once from `__init__`: if `amount >= 10` it multiplies the total by `0.9`. Using `>=` matches the requirement's "ten or more" exactly.

    The total is computed once, at construction, and there's no setter for `purchase_amount` afterwards — so `total_price` can never drift out of sync with the quantity it was calculated from. Calling `__total_amount` from inside `__init__`, rather than recomputing it on demand every time `total_price` is read, also keeps the discount logic in exactly one place instead of needing to be reapplied correctly wherever the total is used.

8. > An order can be cancelled and the stock returned to what is available, but only while it is still pending. Once it has been collected, it can no longer be cancelled.

    `Order.cancel()` and `Order.collect()` are two separate methods, each enforcing its own legality rule: `cancel()` only works while the order is `'pending'`; `collect()` only works while the order is `'pending'`, rejecting both an already-cancelled order and an already-collected one. Once an order reaches `'collected'` or `'cancelled'`, neither status is reachable from the other, and `collected` can never move back to `'pending'` — the requirement's own wording ("once it has been collected, it can no longer be cancelled") implies collected is a final state, not one a user can freely toggle between.

    There is no general-purpose "set status to anything" method exposed — status can only change through these two named actions, so calling code can't accidentally reach an illegal transition that these two methods don't already guard against.

    When `cancel()` succeeds, it also returns the purchased stock to the plant itself (`self.plant.add_stock(...)`), fulfilling "the stock returned to what is available" as part of the same operation, not a separate step `NurserySystem` has to remember to do.

9. > be able to pull up a customer's order history when we need it, without having to go through the whole notebook.

    `customer_order_history(cus_id)` filters `self.__orders` down to just the orders belonging to that one customer, instead of showing the full `order_list()` — this is a direct answer to "without having to go through the whole notebook": staff only see the one customer's orders, not everyone's.

    It also validates `cus_id` exists first (via `customer_info`), rather than silently printing "0 orders" for a invalid id. An invalid id and "a real customer with no orders yet" are different situations, and the error message makes that distinction clear instead of leaving staff to wonder which one happened.

10. > someone once wrote down an order for zero plants by mistake... another time a plant's price got written down as a negative number by mistake... Whatever gets built should catch mistakes like these at the point they are entered, not after.

    `place_order` checks `amount <= 0` as the very first thing it does, before touching the customer, the plant, or the stock — the mistake is caught immediately, before any other work happens.

    For price, `Plant` validates `price >= 0` not just in `__init__`, but also in the `plant_price` setter — so "the point they are entered" covers both when a plant is first created and when its price is updated later.

    `main.py` now demonstrates both mistakes directly — attempting to create a plant with a negative price, and attempting to place a zero-quantity order — each wrapped in `try/except` to show the system actually rejecting them, not just claiming to.

11. > we need to be able to add new plants and customers in the first place, without accidentally adding the same one twice.

    `add_plant` and `add_customer` now reject a duplicate ID to prevent users from accidentally adding the same thing twice.

12. > see lists of what plants are available, every order we have got on record, and who our customers are.

    `customer_list()` and `order_list()` cover "who our customers are" and "every order we have got on record" — full listings, unfiltered.

    "What plants are available" refers only to plants currently in stock, not the full catalogue. `plant_list()` still shows every plant, but `available_plant_list()` was added specifically to answer this part of the requirement literally: it filters to only plants with `stock_level >= 1`, so an out-of-stock plant doesn't show up as something a customer could currently be sold.

## Assumptions

1. `place_order` verifies both the `customer_id` and `plant_id` parameters exist before creating an order, in case the caller passes an id that doesn't correspond to any customer or plant in the system.

2. `cancel_order` and `collect_order` both verify the `order_id` exists before doing anything else, and raise a clear error if it doesn't — the requirement doesn't say what should happen for a non-existent order id, so this fills that gap rather than letting it fail silently or crash with an unrelated error.

3. The requirements don't mention how to represent a free plant. This project assumes `price = 0` is a valid, deliberate value meaning "this plant is free" — not an error — while any negative price is still rejected. No separate flag or field was added; `0` itself carries the meaning.

4. The requirements don't specify how a customer id should be validated, only that it exists to "tell customers apart". This project assumes it must be a positive integer, and unique within the system — mirroring the rule already applied to plant ids — since an id that could repeat or be zero/negative wouldn't reliably tell two customers apart.

## Driver program

`main.py` is the driver program. It creates a `NurserySystem`, then creates customers and plants — including an attempt to add a plant with a negative price, which is rejected and caught with `try/except` to demonstrate the validation.

Before creating orders, it checks a specific plant's stock level. It then places several orders, including an attempt to place a zero-quantity order, again caught to show it's rejected rather than crashing the program.

It then shows a specific customer's order history, and walks through cancelling an order and collecting another one.

Lastly, it displays the full customer, plant, and order lists, plus a separate `available_plant_list()` showing only in-stock plants — demonstrated against a deliberately out-of-stock plant so the difference from the full plant list is visible.
