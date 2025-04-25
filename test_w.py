import os
import json
import pytest
from wallet import Balance, Expense

@pytest.fixture
def setup_balance():
    balance = Balance(first_balance=0)

    if os.path.exists(balance.filename):
        os.remove(balance.filename)

    balance.save_balance()
    return balance

@pytest.fixture
def setup_expense():
    expense = Expense()

    if os.path.exists(expense.filename1):
        os.remove(expense.filename1)

    with open(expense.filename1, 'w') as f:
        json.dump([], f)
    return expense

def test_add_balance(setup_balance):
    balance = setup_balance
    balance.add_balance(100)
    assert balance.load_balance() == 100

def test_withdraw_balance(setup_balance):
    balance = setup_balance
    balance.add_balance(100)
    balance.withdraw_balance(50)
    balance.save_balance()
    assert balance.load_balance() == 150

def test_withdraw_insufficient_balance(setup_balance):
    balance = setup_balance
    balance.add_balance(50)
    balance.withdraw_balance(100)
    balance.save_balance()
    assert balance.load_balance() == 100 

def test_add_expense(setup_expense, setup_balance):
    balance = setup_balance
    balance.add_balance(100) 
    expense = setup_expense
    expense.add_expense("Lunch", 10)
    expenses = expense.load_expense_table()
    assert any(exp.get('name') == "Lunch" and exp.get('price') == 10 for exp in expenses)
    assert balance.load_balance() == 190

def test_delete_expense(setup_expense, setup_balance):
    balance = setup_balance
    balance.add_balance(100)
    expense = setup_expense
    expense.add_expense("Lunch", 10)
    expense.delete_expense("Lunch", 10)
    expenses = expense.load_expense_table()
    balance.save_balance()


    expense_deleted =  any(exp.get('name') == "Lunch" and exp.get('price') == 10 for exp in expenses)
    assert expense_deleted == False


    assert balance.load_balance() == 290, "Balance was not updated correctly after deleting expense"


if __name__ == "__main__":
    pytest.main()
