"""
Driver program for the Nursery ordering system.

It walks through Brent's original notes (Assignment 1) and his follow-up notes
(Assignment 2): four plant types, three customer types, multi-item orders,
discounts, customer balances, payments, custom exceptions and persistence.

Every situation that the system is expected to reject is wrapped in a
try/except so the program keeps running and shows the error message.
"""
import atexit
import os
from datetime import date
from typing import Callable

from nurserySystem import NurserySystem
from order.order import Order
from plant.treesAndShrubs import TreesAndShrubs
from plant.perennial import Perennial
from plant.potPlant import PotPlant
from plant.vegetableSeedling import VegetableSeedling
from customer.staff import Staff
from customer.student import Student
from customer.community import Community
from payment.creditCardPayment import CreditCardPayment
from payment.debitCardPayment import DebitCardPayment
from nurseryErrorException.NurseryError import NurseryError
from nurseryErrorException.InsufficientStockError import InsufficientStockError
from nurseryErrorException.CreditLimitExceededError import CreditLimitExceededError
from nurseryErrorException.PendingOrderExistsError import PendingOrderExistsError
from nurseryErrorException.PaymentExceedsOwedError import PaymentExceedsOwedError

DATA_FILE = "demo_data.pkl"
TODAY = date.today().strftime("%d-%m-%Y")


def section(title: str) -> None:
    """Print a heading so the output is easy to follow."""
    print(f"\n{'=' * 72}\n{title}\n{'=' * 72}")


def attempt(description: str, action: Callable[[], object]) -> None:
    """Run an action that the system should reject, and show the error message."""
    try:
        action()
        print(f"  [UNEXPECTED] {description}: no error was raised")
    except (ValueError, NurseryError) as error:
        print(f"  [Rejected] {description}: {error}")


def show_state(nursery: NurserySystem, plant_ids: list[int], customer_ids: list[int]) -> None:
    """Print the stock of some plants and the balance of some customers."""
    stock = ", ".join(
        f"#{i} {nursery.plant_info(i).name} = {nursery.plant_info(i).stock_level}"
        for i in plant_ids
    )
    balances = ", ".join(
        f"{nursery.customer_info(i).name} = ${nursery.customer_info(i).balance:.2f}"
        for i in customer_ids
    )
    if plant_ids:
        print(f"  Stock:    {stock}")
    if customer_ids:
        print(f"  Balances: {balances}")


def show_order(nursery: NurserySystem, order_id: int) -> None:
    """Print an order with its items, discounts, total, paid and owed amounts."""
    order = nursery.order_info(order_id)
    print(order)
    for item in order.order_items:
        print(f"    - {item}")
    print(
        f"    Subtotal ${order.get_subtotal():.2f} | "
        f"{order.customer.customer_type} discount {order.customer.discount_rate:.0%} | "
        f"Total ${order.get_total():.2f}"
    )


def print_quote(nursery: NurserySystem, title: str, customer_id: int, items: list[tuple[int, int]]) -> None:
    """Price a basket without placing an order (nothing is reserved or charged)."""
    customer = nursery.customer_info(customer_id)
    quote = Order(0, customer, TODAY)
    for plant_id, quantity in items:
        quote.add_item(nursery.plant_info(plant_id), quantity)
    print(f"  {title}")
    for item in quote.order_items:
        print(f"    - {item}")
    print(f"    Subtotal ${quote.get_subtotal():.2f}, total for a {customer.customer_type} customer ${quote.get_total():.2f}")


def debit(nursery: NurserySystem, payment_id: int, amount: float, order_id: int, payer=None) -> DebitCardPayment:
    """Build a debit card payment toward an order (by default paid by the order's customer)."""
    order = nursery.order_info(order_id)
    return DebitCardPayment(payment_id, amount, payer or order.customer, order, TODAY, "4111111111111111", "ANZ")


def credit(nursery: NurserySystem, payment_id: int, amount: float, order_id: int, payer=None) -> CreditCardPayment:
    """Build a credit card payment toward an order (by default paid by the order's customer)."""
    order = nursery.order_info(order_id)
    return CreditCardPayment(payment_id, amount, payer or order.customer, order, TODAY, "5500000000000004", "12/30")


# Start every run from a clean data file, otherwise the customers and plants
# below would be loaded from the previous run and rejected as duplicates.
data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), DATA_FILE)
if os.path.exists(data_path):
    os.remove(data_path)

system = NurserySystem(DATA_FILE)

# ---------------------------------------------------------------------------
section("1. Plants: four types, each with its own details")
system.add_plant(TreesAndShrubs(1, "griselinia", 10.0, 30))
system.add_plant(Perennial(2, "lavender", 6.0, 40))
system.add_plant(PotPlant(3, "fern", 8.0, 20, "small"))                   # a pot size is its own stock item
system.add_plant(PotPlant(4, "fern", 15.0, 10, "large"))
system.add_plant(VegetableSeedling(5, "tomato", 5.0, 40))                 # default: 6 seedlings per punnet
system.add_plant(VegetableSeedling(6, "lettuce", 4.0, 20, seedlings_per_punnet=8))
system.add_plant(TreesAndShrubs(7, "free sample sapling", 0.0, 5))        # a free plant
system.add_plant(PotPlant(8, "orchid", 25.0, 0, "medium"))                # out of stock
system.plant_list()

# ---------------------------------------------------------------------------
section("2. Stock checks and plant validation")
griselinia = system.plant_info(1)
print(f"{griselinia.name}: {griselinia.stock_level} {griselinia.unit_label}s in stock")
print("  enough for 25?", griselinia.stock_level_check(25))
print("  enough for 35?", griselinia.stock_level_check(35))
print("\nOnly the plants that are in stock (the orchid is left out):")
system.available_plant_list()
print()
attempt("plant with a negative price", lambda: system.add_plant(TreesAndShrubs(9, "bad plant", -5.0, 3)))
attempt("plant with a duplicate id", lambda: system.add_plant(Perennial(1, "copy", 5.0, 5)))
attempt("pot plant with an invalid size", lambda: system.add_plant(PotPlant(9, "bad pot", 5.0, 3, "huge")))

# ---------------------------------------------------------------------------
section("3. Customers: three types, each with a balance")
system.add_customer(Staff(1, "Edward Xin", "edward@mail.com", "020-111-1111"))
system.add_customer(Student(2, "Mandy Garcia", "mandy@mail.com", "020-222-2222"))
system.add_customer(Community(3, "Mike Hardy", "mike@mail.com", "020-333-3333"))
system.add_customer(Staff(4, "Sarah Lee", "sarah@mail.com", "020-444-4444"))
system.customer_list()
for customer_type in ("Staff", "Student", "Community"):
    print(f"\n--- {customer_type} customers only ---")
    system.get_customers_by_type(customer_type)
print()
attempt("customer with a duplicate id", lambda: system.add_customer(Community(1, "Someone Else", "else@mail.com", "020-999-9999")))
attempt("customer with a duplicate email", lambda: system.add_customer(Student(9, "Copy Cat", "edward@mail.com", "")))
attempt("customer with a duplicate phone number", lambda: system.add_customer(Student(9, "Copy Cat", "copy@mail.com", "020-222-2222")))
attempt("customer with no email and no phone number", lambda: system.add_customer(Student(9, "No Contact", "", "")))
attempt("customer with an invalid id", lambda: system.add_customer(Staff(0, "Zero", "zero@mail.com", "")))

# ---------------------------------------------------------------------------
section("4. One order with several plant types (Brent's example)")
print("4 griselinias, 2 large pot ferns and 1 punnet of tomato seedlings for Edward.\n")
print("Before the order:")
show_state(system, [1, 4, 5], [1])
brent_order = system.place_order(1, [(1, 4), (4, 2), (5, 1)])
print()
show_order(system, brent_order)
print("\nAfter the order (stock went down straight away, the total was added to Edward's balance):")
show_state(system, [1, 4, 5], [1])

# ---------------------------------------------------------------------------
section("5. Discounts: 10% for 10 or more of the same plant, then the customer discount")
print("The same basket (10 punnets of tomato at $5.00 = $50.00, less 10% = $45.00) for each customer type:\n")
staff_order = system.place_order(4, [(5, 10)])
student_order = system.place_order(2, [(5, 10)])
community_order = system.place_order(3, [(5, 10)])
for order_id in (staff_order, student_order, community_order):
    show_order(system, order_id)
    print()
print("Pot plants need 10 of the SAME size for the item discount (price quotes only, nothing is ordered):")
print_quote(system, "10 small ferns", 3, [(3, 10)])
print_quote(system, "5 small + 5 large ferns (mixed sizes, no item discount)", 3, [(3, 5), (4, 5)])
print_quote(system, "10 griselinias", 3, [(1, 10)])

# ---------------------------------------------------------------------------
section("6. Business rules and custom exceptions")
print("Stock and balances before the orders that will be rejected:")
show_state(system, [4, 7], [1, 2, 3])
print()

try:
    system.place_order(1, [(7, 6)])
except InsufficientStockError as error:
    print(f"  [InsufficientStockError] 6 free saplings, only 5 in stock: {error}")

try:
    system.place_order(1, [(4, 3)])
except CreditLimitExceededError as error:
    print(f"  [CreditLimitExceededError] Staff customer over $100: {error}")

try:
    system.place_order(2, [(4, 5)])
except CreditLimitExceededError as error:
    print(f"  [CreditLimitExceededError] Student customer over $100: {error}")

try:
    system.place_order(3, [(2, 1)])
except PendingOrderExistsError as error:
    print(f"  [PendingOrderExistsError] Community customer with a pending order: {error}")

try:
    system.place_order(3, [(2, 1)])
except NurseryError as error:
    print(f"  [NurseryError] the base class catches any of the errors above: {error}")

print("\nNothing changed because of the rejected orders:")
show_state(system, [4, 7], [1, 2, 3])
print("\nOther invalid orders:")
attempt("order for an unknown customer", lambda: system.place_order(77, [(1, 1)]))
attempt("order containing an unknown plant", lambda: system.place_order(1, [(1, 1), (99, 5)]))
attempt("order with no items", lambda: system.place_order(1, []))
attempt("order for zero plants", lambda: system.place_order(1, [(1, 0)]))

# ---------------------------------------------------------------------------
section("7. Payments: instalments, two card types and the 1.5% credit card surcharge")
print("Brent's order before any payment:")
show_order(system, brent_order)

print("\nInstalment 1: $30.00 by debit card")
first_payment = debit(system, 1, 30.00, brent_order)
system.make_payment(first_payment)
print(first_payment)

print("\nInstalment 2: $20.00 by credit card (surcharge is charged to the card, but only $20.00 counts as paid)")
second_payment = credit(system, 2, 20.00, brent_order)
system.make_payment(second_payment)
print(second_payment)

print("\nAfter two instalments:")
show_order(system, brent_order)
show_state(system, [], [1])

try:
    system.make_payment(debit(system, 3, 40.00, brent_order))
except PaymentExceedsOwedError as error:
    print(f"\n  [PaymentExceedsOwedError] $40.00 is more than is still owed: {error}")

print("\nInstalment 3: the remaining $24.25")
system.make_payment(debit(system, 4, 24.25, brent_order))
show_order(system, brent_order)
show_state(system, [], [1])

try:
    system.make_payment(debit(system, 5, 1.00, brent_order))
except PaymentExceedsOwedError as error:
    print(f"\n  [PaymentExceedsOwedError] paying an order that is already settled: {error}")

print("\nOther invalid payments:")
mandy = system.customer_info(2)
attempt("payment by a customer who does not own the order", lambda: system.make_payment(debit(system, 6, 5.00, staff_order, payer=mandy)))
attempt("payment with a duplicate payment id", lambda: system.make_payment(debit(system, 1, 5.00, staff_order)))
attempt("payment of zero dollars", lambda: system.make_payment(debit(system, 6, 0, staff_order)))
attempt("debit card number that is not 16 digits", lambda: DebitCardPayment(6, 5.00, system.customer_info(4), system.order_info(staff_order), TODAY, "1234", "ANZ"))
attempt("credit card with an invalid expiry date", lambda: CreditCardPayment(6, 5.00, system.customer_info(4), system.order_info(staff_order), TODAY, "5500000000000004", "13/30"))

# ---------------------------------------------------------------------------
section("8. Cancelling and collecting orders")
print("Staff customers can collect while they still owe money:")
lavender_order = system.place_order(1, [(2, 2)])
system.collect_order(lavender_order)
show_order(system, lavender_order)

print("\nCancelling a pending order that has no payments gives the stock and the balance back:")
cancel_order = system.place_order(1, [(2, 3)])
print("Before cancelling:")
show_state(system, [2], [1])
system.cancel_order(cancel_order)
print("After cancelling:")
show_state(system, [2], [1])
print(f"Order {cancel_order} status: {system.check_order_status(cancel_order)}")

print("\nOrders that can no longer be cancelled or collected:")
part_paid_order = system.place_order(1, [(1, 2)])
system.make_payment(debit(system, 7, 5.00, part_paid_order))
attempt("cancelling an order that already has a payment", lambda: system.cancel_order(part_paid_order))
attempt("cancelling an order that was collected", lambda: system.cancel_order(lavender_order))
attempt("collecting an order twice", lambda: system.collect_order(lavender_order))
attempt("paying toward a cancelled order", lambda: system.make_payment(debit(system, 8, 5.00, cancel_order)))

print("\nCommunity customers must pay in full before they can collect:")
attempt("collecting before paying anything", lambda: system.collect_order(community_order))
system.make_payment(credit(system, 9, 20.00, community_order))
attempt("collecting after only a partial payment", lambda: system.collect_order(community_order))
system.make_payment(debit(system, 10, 25.00, community_order))
system.collect_order(community_order)
print(f"Order {community_order} status after paying in full: {system.check_order_status(community_order)}")
show_state(system, [], [3])
print("Mike has nothing pending any more, so he can order again:")
mike_second_order = system.place_order(3, [(2, 3)])
show_order(system, mike_second_order)

# ---------------------------------------------------------------------------
section("9. Reports and searches")
print("All orders:")
system.order_list()
print("\nEdward's order history (cancelled orders included):")
system.customer_order_history(1)
print("\nOrder statuses:")
for order_id in (brent_order, lavender_order, cancel_order, part_paid_order, community_order):
    print(f"  Order {order_id}: {system.check_order_status(order_id)}")
print("\nAll customers, with their balances:")
system.customer_list()
for customer_type in ("Staff", "Student", "Community"):
    print(f"\n--- {customer_type} customers only ---")
    system.get_customers_by_type(customer_type)
print("\nAll payments:")
system.payment_list()
print("\nEdward's payment history:")
system.customer_payment_history(1)
print(f"\nAll payments made toward order {brent_order}:")
system.order_payment_history(brent_order)

# ---------------------------------------------------------------------------
section("10. Saving and reloading the data")
system.save()
atexit.unregister(system.save)          # the reloaded system takes over the automatic save at exit
reloaded = NurserySystem(DATA_FILE)
print("Customers reloaded as:", [(i, type(reloaded.customer_info(i)).__name__) for i in (1, 2, 3, 4)])
print("Plants reloaded as:   ", [(i, type(reloaded.plant_info(i)).__name__) for i in range(1, 9)])
reloaded_order = reloaded.order_info(brent_order)
print("Payments on Brent's order reloaded as:", [type(p).__name__ for p in reloaded_order.order_payments])
print("The order still shares the same Customer object as the customer list:",
      reloaded_order.customer is reloaded.customer_info(1))
print()
show_order(reloaded, brent_order)
show_state(reloaded, [1, 2, 4, 5], [1, 2, 3, 4])
print("\nThe reloaded system keeps working:")
new_order = reloaded.place_order(4, [(2, 1)])
print(f"  Sarah placed order {new_order}, status {reloaded.check_order_status(new_order)}")

print("\nEnd of the demonstration. The data is saved automatically when the program exits.")
