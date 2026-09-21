# Assignment 1 → Assignment 2 Feedback Tracker

Source: teacher feedback on Assignment 1 (61.6/100 total). Assignment 2's starting
code was copied from Assignment 1, so every item below is being fixed here.
Status: `[ ]` pending, `[x]` done.

## Classes Design — 9/15
- [ ] `Order` should hold `Plant` and `Customer` objects directly, not just their ids.
- [ ] `Plant` missing an explicit `add_stock` method (separate from the buy/reduce path).
- [ ] `NurserySystem` missing: check-order-status method, a generic find-by-id method
      usable for all three collections, and an available-plants-list method.
- [ ] Order status transitions: either one `set_order_status` controlling both
      cancel + collect, or two explicit methods (`cancel_order` / `collect_order`).

## Core Business Logic — 8/9
- [ ] A `collected` order can currently be set back to `pending` — must be blocked.

## Edge Cases & Validation — 3.5/9
- [ ] Plant category not validated against the allowed set.
- [ ] Plant price should be a positive float; decide how free (price = 0) plants
      are represented/handled.
- [ ] Order date format not validated.
- [ ] Customer id not validated when adding a customer.

## Functionality — 8/12
- [ ] `main.py` driver missing demos for: individual plant stock check, a plant
      with a negative price (error case), a zero-quantity order (error case), and
      listing only available (in-stock) plants.

## Encapsulation — 5/5
- [x] No action needed.

## Getters and Setters — 2/5
- [ ] `Order` has no getter for `date`.
- [ ] `Plant` has no getter for `category`; add setters for `category` and `price`.
- [ ] `Customer` has no getter for `name`.

## Overloading (`__str__`) — 2.6/5
- [ ] Every `__str__` should clearly name its class.
- [ ] `Order.__str__` should include customer name and plant name, not just ids.

## Readability — 2.5/3
- [ ] Minor pass: simplify flow in a few spots.

## Modularity — 4/5
- [ ] Customer validation logic (duplicate email/phone, required fields) should
      live in `Customer`, not `NurserySystem`.

## PEP 8 Compliance — 1/2
- [ ] Rename all methods (and ideally variables) from camelCase to snake_case.
- [ ] Wrap a few overly wide lines.

## Docstrings — 1/7
- [ ] Add/complete docstrings throughout: every method needs at least a one-line
      summary; non-trivial methods need Args/Returns; getters/setters need at
      least a one-line summary each.

## Type Hints — 2/4
- [ ] Add return type hints everywhere, e.g. `-> Order`, `-> bool`, `-> None`.

## Comments — 2/4
- [ ] Fill in sparse spots with useful inline comments.

## README — 11/15
- [ ] Bring README into `assignment-2/` and strengthen justification tying design
      choices back to the 6 requirements (currently thin in places).
