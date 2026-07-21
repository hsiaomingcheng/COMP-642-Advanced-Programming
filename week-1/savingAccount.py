# We want to build a simple application that will manage a savings account.
# The transactions supported are: deposit, withdraw, calculate interest, and check balance.

# Work through:
# 1. What is the problem?
# 2. What is the object? What is the class?
# 3. What data does it need? What methods does it need?
# 4. How do we use the class to assemble the application?

# Implement it in Python.

class SavingAccount:
    def __init__(self, accountName, accountNumber):
        self.accountName = accountName
        self.accountNumber = accountNumber
        self.balance = 0

    def deposit(self, number):
        self.balance = self.balance + number

    def withdraw(self, number):
        if self.balance < number:
            return False

        self.balance = self.balance - number
        return True
            

    def calculateInterest(self, interest):
        return self.balance * interest

    def checkBalance(self):
        return self.balance
            
# assign a person
personA = SavingAccount("Chris", 112233)

# deposit
personA.deposit(100)

# withdraw
withdrawSuccess = personA.withdraw(20)

if not withdrawSuccess:
    print("The saving balance is not enough")

# calculate interest
print(f"The interest of your balance is {personA.calculateInterest(0.5)}")

# check user account
print(f"Helle, {personA.accountName}")
print(f"Your balance of {personA.accountNumber} is {personA.checkBalance()}")