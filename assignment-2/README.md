# Nursery Ordering System - Assignment 2

This project extends the Assignment 1 ordering system for Lincoln University's Nursery Greenhouse Centre
with Brent's follow-up requirements: four plant types, three customer types, orders with several items,
customer balances, payments, custom exceptions and saving/loading of data.

## 1. How to run

```
python3 main.py
```

Run it from this folder. It needs Python 3.10 or newer (it uses `X | None` and `list[tuple[int, int]]` type hints);
it was developed on Python 3.14. `main.py` is the driver program. It saves its data to `demo_data.pkl`
(next to `nurserySystem.py`) and deletes any old copy of that file when it starts, so it can be run repeatedly.

## 2. Project structure

```
main.py                     driver program
nurserySystem.py            NurserySystem: the central class
plant/                      plant.py (abstract Plant), treesAndShrubs.py, perennial.py,
                            potPlant.py, vegetableSeedling.py
customer/                   customer.py (abstract Customer), staff.py, student.py, community.py
order/                      order.py (Order), orderItem.py (OrderItem)
payment/                    payment.py (abstract Payment), creditCardPayment.py, debitCardPayment.py
nurseryErrorException/      NurseryError and the custom exceptions, one per file
```

## 3. Class design

### 3.1 Abstract and concrete classes

| Class | Kind | Abstract member(s) | Members with a default that subclasses override |
|---|---|---|---|
| `Plant` | abstract | `category` | `unit_label` ("plant"; `PotPlant` -> "pot", `VegetableSeedling` -> "punnet") |
| `Customer` | abstract | `customer_type` | `discount_rate` (0.0; Staff 1%, Student 5%), `check_can_place_order` (credit limit; `Community` overrides), `check_can_collect` (does nothing; `Community` overrides) |
| `Payment` | abstract | `payment_type` | `surcharge` (0.0; `CreditCardPayment` -> 1.5%) |
| `Order`, `OrderItem`, `NurserySystem` | concrete | - | - |

Why these choices:

- **`Plant`, `Customer`, `Payment` are abstract** because "a plant that is none of the four types", "a customer that is none of the three types" and
  "a payment that is neither credit nor debit" do not exist in Brent's notes, so they must never be created directly (Python raises a `TypeError` if you try).
- **A member is abstract only when there is no sensible shared default.** `category`, `customer_type` and `payment_type` differ for every subclass, so every subclass must supply them.
  Where most subclasses share a value, the base class supplies it and only the exceptions override it (for example `TreesAndShrubs` and `Perennial` do not write `unit_label` at all).
- **`TreesAndShrubs` and `Perennial` are separate classes** even though they currently behave the same, because Brent lists them as different types of plant and they may diverge later.
- The type of a plant is the class it was created from, so there is no separate `category` string to validate (the Assignment 1 category check is no longer needed).

### 3.2 Polymorphism

`Order` and `NurserySystem` never check which subclass they are dealing with (no `isinstance` or type-name branching; `isinstance` is only used to check that an id or quantity is a whole number). They call the same method on every object and each subclass answers in its own way:

| Call | Behaviour by subclass |
|---|---|
| `customer.discount_rate` | Staff 0.01, Student 0.05, Community 0.0 |
| `customer.check_can_place_order(total)` | Staff/Student: balance + total must not exceed $100. Community: no pending order allowed |
| `customer.check_can_collect(order)` | Staff/Student: always allowed. Community: order must be fully paid |
| `plant.unit_label` | "plant", "pot" or "punnet" |
| `payment.surcharge` | 0 for debit cards, 1.5% of the amount for credit cards |
| `str(x)` | each class prints its own details (subclasses extend the base output with `super().__str__()`) |

### 3.3 Orders and order items

- An `Order` belongs to one `Customer` and holds a list of `OrderItem` objects and a list of `Payment` objects.
- An `OrderItem` is one plant plus a quantity in that plant's own unit. It works out its own cost, including the 10% discount for 10 or more.
- Adding a plant that is already on the order **adds to the existing item** instead of creating a second one, so each plant appears once per order.
- `Order.get_total()`, `get_amount_paid()` and `get_amount_owed()` are calculated from the items and payments every time. Nothing is stored, so the numbers cannot get out of step.
- **Placing an order is all-or-nothing.** `NurserySystem.place_order` builds the `Order` and adds the items. `Order.place()` then checks everything first
  (has items, customer allowed to order, enough stock for every item) and only then reduces the stock, adds the total to the customer's balance and records the order.
  If any check fails, nothing has changed. Cancelling does the reverse (stock returned, total taken off the balance).

### 3.4 Encapsulation and references

- All data members are private (`__name`) and are read through properties. Values that must not be changed freely (stock level, balance, order status, quantity) have no setter;
  they change only through methods that enforce the rules (`add_stock`, `stock_level_check_and_buy`, `add_to_balance`, `reduce_balance`, `cancel`, `collect`, `add_quantity`).
- `Order` keeps the real `Customer` object, `OrderItem` keeps the real `Plant`, and `Payment` keeps the real `Customer` and `Order`. The customer's own order list and the system's order list
  hold the same `Order` object, so a change is seen everywhere.
- Each class validates its own data (`Customer` its id, name and contact details; `Plant` its price; `OrderItem` its quantity; `Payment` its id, amount, date and card details), and `NurserySystem` only coordinates between objects.
- Circular imports (`Customer` <-> `Order`, `Payment` <-> `Order`) are avoided by importing the other class only for type hints (`TYPE_CHECKING`).

### 3.5 Money

All calculated amounts (item cost, order total, surcharge, balance) are rounded to two decimal places, so 1%, 5% and 1.5% calculations cannot leave tiny floating point differences
that would stop an order from being fully paid.

## 4. How the design supports Brent's follow-up notes

| Brent's note | How it is handled |
|---|---|
| Four types of plant | `Plant` with `TreesAndShrubs`, `Perennial`, `PotPlant`, `VegetableSeedling` |
| Trees/shrubs and perennials priced per plant | `price` is per plant; quantity counts individual plants |
| Pot plants priced by pot size | `PotPlant` has a validated `size` (small, medium, large). Each size of a plant is its own `PotPlant` object with its own price and stock (e.g. "fern, small" and "fern, large") |
| Seedlings sold and priced by the punnet | `VegetableSeedling` price is per punnet and quantity counts punnets; `seedlings_per_punnet` (default 6) is stored for information |
| Sold unit = stock unit | `price`, `quantity` and `stock_level` are always in the plant's own unit (`unit_label`) |
| An order can have several plants, each with its own quantity and cost | `Order` holds `OrderItem`s; each has a plant, a quantity and `get_cost()`. The order total is the sum of the item costs |
| 10% off for ten or more of the same plant, per item | `OrderItem.get_cost()` applies it to that item only. For pot plants the "same plant" is the same `PotPlant` object, i.e. the same plant **and** size, so 5 small + 5 large gets no discount. For seedlings it counts punnets |
| Staff 1%, students 5%, community 0% off the whole order | `Customer.discount_rate`; `Order.get_total()` takes it off the sum of the (already discounted) items, so the two discounts stack multiplicatively |
| Every customer has a balance | `Customer.balance` grows when an order is placed and shrinks with payments and cancellations |
| Community: one pending order, pay in full before collecting | `Community.check_can_place_order` rejects a new order while any order is pending; `Community.check_can_collect` requires the order to be fully paid. An order stops being pending only when it is collected, so a Community customer can order again only after paying and collecting |
| Staff/students can collect while owing; no more than $100 owing | `Staff` and `Student` inherit `check_can_collect` (no restriction) and the credit-limit check (`CREDIT_LIMIT = 100`) |
| Payments in instalments, never more than what is owed, from any customer at any time | `Order.check_can_accept_payment` rejects an amount above `get_amount_owed()`. Payments are accepted for any customer type and at any time before the order is settled (also after it was collected) |
| Cancel only while pending and unpaid; cancelling takes the total off the balance | `Order.cancel()` refuses a non-pending order or one with any payment; it returns the stock and reduces the balance |
| Payment record: id, amount, customer, order, date | `Payment` attributes (date is validated as DD-MM-YYYY) |
| Credit card: card number, expiry, 1.5% surcharge. Debit card: card number, bank | `CreditCardPayment` and `DebitCardPayment` |
| See a customer's balance and the customer types separately | `Customer.__str__` shows the balance and type; `NurserySystem.get_customers_by_type` |
| Payment history of a customer, payments toward an order, all payments | `customer_payment_history`, `order_payment_history`, `payment_list` |

## 5. Brent's original notes (Assignment 1), and what changed

| Original requirement | Where it is handled now |
|---|---|
| Know the stock of each plant; refuse an order if there is not enough; check stock before ordering | `Plant.stock_level`, `stock_level_check`; `stock_level_check_and_buy` raises `InsufficientStockError`; `Order.place()` checks every item before changing anything |
| Stock goes down straight away and never below zero | `Order.place()` reserves the stock; the check and the deduction are one method on `Plant` |
| Plant details: id, name, category, price, stock | `Plant` (the category is the class). Price must not be negative; 0 means a free plant |
| Customer details: id, name, email or phone | `Customer`: positive unique id, non-blank name, at least one of email or phone; duplicates rejected with `Customer.conflicts_with` |
| Order details: customer, plant, quantity, date DD-MM-YYYY, status, total | `Order` and `OrderItem`; the date is validated; status is pending, collected or cancelled |
| **One plant type per order** | **Replaced by the follow-up notes:** an order now holds several items, one per plant |
| 10% off for ten or more | now per `OrderItem` |
| Cancel only while pending; stock returned | `Order.cancel()`; a collected order can never go back to pending or be cancelled |
| A customer's order history | `NurserySystem.customer_order_history` (includes cancelled orders) |
| Catch mistakes at entry (zero plants, negative price) | `OrderItem` rejects quantities that are not positive whole numbers; `Plant` rejects negative prices |
| No duplicate plants or customers | duplicate ids rejected for plants and customers; duplicate email or phone rejected for customers |
| Lists of available plants, orders and customers | `available_plant_list`, `plant_list`, `order_list`, `customer_list` (plus `payment_list`) |

## 6. Custom exceptions

All custom exceptions inherit from `NurseryError`, which has a default message, so `except NurseryError` catches any of them while each can also be caught individually.
Each subclass has its own default message and accepts a more specific message when raised.

| Exception | Raised when | Raised by |
|---|---|---|
| `InsufficientStockError` | not enough stock for an item | `Plant.stock_level_check_and_buy`, `Order.place` |
| `CreditLimitExceededError` | a Staff/Student order would take the balance over $100 | `Customer.check_can_place_order` |
| `PendingOrderExistsError` | a Community customer already has a pending order | `Community.check_can_place_order` |
| `PaymentExceedsOwedError` | a payment is more than what is still owed, or the order is already settled or cancelled (two different messages) | `Order.check_can_accept_payment` |

Invalid **input** (negative price, zero quantity, bad date, bad card number, unknown id, duplicate id) raises the built-in `ValueError`, because the argument itself is wrong.
The custom exceptions are used for **business-rule** violations. `main.py` triggers every custom exception and catches it by its own class, and also shows `except NurseryError` catching them all.

## 7. Saving and loading data

- `NurserySystem.save()` writes customers, plants, orders and payments to one file with `pickle`. They are written in a **single** `pickle.dump`, so objects that are shared
  (the same `Customer` is in the customer list, in its orders and in its payments) are still the same single object after loading.
- `NurserySystem.__init__` calls `load()` and then registers `save` with `atexit`, so the data is loaded when the system is created and saved automatically when the program exits, even if it stops with an error.
- If the file does not exist (first run) the system starts empty. If it cannot be read, a warning is printed and the system starts empty instead of crashing.
- The data file sits next to `nurserySystem.py`, so it is found wherever the program is started from.
- `pickle` restores each object as its own class (a `Staff` stays a `Staff`, a `PotPlant` a `PotPlant`), which `main.py` shows after reloading.

## 8. Assumptions

The notes did not cover these points, so the following decisions were made:

1. **Pot plant sizes.** Each size is a separate plant record with its own price and stock. This keeps the `Plant` interface the same for all four types and makes "ten or more of the same plant in the same size" simply "ten or more of the same plant".
2. **Repeated plant in one order.** Adding a plant that is already on the order increases that item's quantity, because Brent describes each different plant as its own item.
3. **Order total is calculated, not stored,** so it always matches the items and the customer's discount.
4. **The $100 limit is checked against the balance after the new order** (balance + new total). Brent says a customer "should not" order more once owing goes above $100, and this stops the order that would cross it.
5. **Community customers have no dollar limit,** only the one-pending-order rule, because the notes give them no limit.
6. **A Community customer's order stays pending until it is collected.** They must pay in full before it can be collected, and only after it is collected can they order again ("settled and picked up").
7. **Credit card surcharge is not part of the repayment.** The customer is charged amount + 1.5%, but only the amount reduces what is owed, otherwise a payment for the exact balance would break the rule that a payment cannot exceed what is owed. `Payment.get_total_charged()` shows what the card is charged.
8. **Paying a settled or cancelled order is rejected with its own message** (using `PaymentExceedsOwedError`), and an order that was collected but still has money owing (Staff/Student) can still be paid.
9. **The payer must be the customer who owns the order.** A payment records one customer ("which customer it was for"), so paying another customer's order is rejected.
10. **All money values are rounded to two decimals** (see 3.5).
11. **Credit card details:** the card number must be exactly 16 digits (stored as text so a leading zero is kept) and the expiry date is written `MM/YY`. Debit card bank names must not be blank. Only the format of the expiry date is checked.
12. **Identifiers.** Customer, plant and payment ids are supplied by the caller and must be unique; order ids are generated in sequence. Order dates are set to today's date in DD-MM-YYYY format.
13. **Data is saved with `pickle` and saved automatically on exit,** because Brent wants the data kept between runs and pickle keeps the object relationships and subclasses without extra conversion code.
14. **Carried over from Assignment 1** (the notes did not change these): a collected order can never return to pending; placing an order, cancelling and collecting check that the ids exist; free plants (price 0) are allowed; a customer id must be a positive whole number.

## 9. Driver program

`main.py` builds a system and goes through ten sections, printing what happens and catching every expected error:

1. the four plant types (including a free plant and an out-of-stock plant)
2. stock checks and plant validation (negative price, duplicate id, invalid pot size), and the list of available plants
3. the three customer types, duplicate/invalid customers, and customers listed by type
4. Brent's example order (4 griselinias, 2 large ferns, 1 punnet of tomatoes) with stock and balance before and after
5. discounts: the same basket for Staff, Student and Community customers, and pot plant quotes showing that the discount needs ten of the same size
6. business rules with each custom exception, showing that a rejected order changes nothing
7. payments: instalments, debit and credit card (with the surcharge), overpaying, paying a settled order and other invalid payments
8. cancelling and collecting: stock and balance restored, orders that cannot be cancelled, Staff collecting while owing, Community paying before collecting and then ordering again
9. reports: all orders, order history, statuses, customers (with balances and by type), all payments, a customer's payments and an order's payments
10. saving, then creating a second system that loads the file, showing the restored classes and that the system keeps working

## 10. Known limitations

- An expired credit card is not rejected; only the format of the expiry date is checked.
- `get_customers_by_type` with an unknown type prints nothing instead of raising an error.
- Breaking the cancel or collect rules (for example cancelling an order that already has a payment) raises `ValueError` rather than a dedicated exception.
- Money uses floating point numbers rounded to cents, not `Decimal`.
- `pickle` files should only be loaded from a trusted source (this program only reads the file it wrote itself).
