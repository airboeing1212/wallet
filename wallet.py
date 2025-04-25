import os
import json
import sys
from datetime import datetime
import re


def main():

    balance = Balance()
    expense = Expense()
    ini(balance, expense)


def expense_table_h(expence):
    expense = Expense()

    expense_table = expense.load_expense_table()
    print(expense_table)


def file_save():
    pass
    


def ini(balance, expense ):
    while True:
        first_selection = int(input('please select Balance(1) or Expences(2). İf you want to quit the program please press (3)'))

        if first_selection == 1:
    
            
            while True:
                print('What do you want to do with your balance?')
                print('-'*10)
                second_selections = int(input('add(1), withdraw(2), view(3), and if you want to go back please press(4)'))

                if second_selections == 1:
                    amount = int(input('please enter the amount you want to enter = '))
                    balance.add_balance(amount)

                elif second_selections == 2:


                    print(f'you have {balance.load_balance()}$ available')


                    amount2 = int(input('please enter the amount you want to withdraw = '))
                    balance.withdraw_balance(amount2)

                elif second_selections == 3:
                    balance.view_balance()
                
                elif second_selections == 4:
                    break

                
                else:
                    print('try again')

        elif first_selection == 3:
            break


        elif first_selection == 2:
           

            while True:
               
                expense_selection = int(input('add_expense(1),  delete_expense(2),  show_expenses(3),   go back(4)'))

                if expense_selection == 1:


                    name = input('expense name : ')
                    print('-'*10)
                    #print(f'You have {Balance.ret_balance}$ in your account ')
                    price = int(input('the price : '))

                    expense.add_expense(name,price)

                elif expense_selection == 2:
                    name1 = input('enter the NAME of expenset : ')
                    print('-'*10)
                    price1 = int(input('please enter the price for payment : '))

                    expense.delete_expense(name1, price1)

                

                elif expense_selection == 3:
                    all_table = int(input('Do you want to see whole table(1) or specific one(2)'))

                    if all_table == 1:
                        expense_table_h(expense)

                    elif all_table == 2:

                        name2 = input('Please enter the name you want to see for expenses : ')

                        expense.view_expense(name2)
                    else:
                        print('try again')


                elif expense_selection == 4:
                    break

        else:
            print('please try again')


class Balance():

    def __init__(self, first_balance=0, filename='balance.json', filename1= 'expenses.json'):

        self.filename=filename
        self.filename1 = filename1
        if os.path.exists(self.filename):
            self.balance = self.load_balance()
        else:
            self.balance = first_balance
            self.save_balance()



     
        if not os.path.exists(self.filename1):
            with open(self.filename1, 'w') as f:
                json.dump([], f)
        

    def expenses_table(self, expenses):
        with open(self.filename1, 'w')as f:
            json.dump(expenses, f, indent=4)


    def load_expense_table(self):
        with open(self.filename1, 'r') as f:
            return json.load(f)   



    def load_balance(self):
        with open(self.filename, 'r') as f:
            return json.load(f)['balance']
          

    def save_balance(self):
        
        with open(self.filename, 'w') as f:
            json.dump({'balance': self.balance}, f)
        

    def add_balance(self, x):
        
        self.balance = self.load_balance()
        self.balance += x

        self.save_balance()

        deposites = self.load_expense_table()
        new_deposit ={'DEPOSIT': x, "timestamp": datetime.now().isoformat()}
        deposites.append(new_deposit)

        self.expenses_table(deposites)

        print(f'your {x}$ has been added to your balance, total amount is {self.balance}$')
        print('--------------------------------------------------------------------------')

    def withdraw_balance(self, y):

        self.balance = self.load_balance()
    
        if y <= self.balance:
            self.balance -= y
            self.save_balance()

            withdraws = self.load_expense_table()
            new_withdraw = {'WITHDRAW': y, "timestamp": datetime.now().isoformat()}
            withdraws.append(new_withdraw)

            self.expenses_table(withdraws)



            print(f'Your {y}$ has been deducted from your balance, total amount is {self.balance}$')
            print('--------------------------------------------------------------------------')
        else:
            print(f'Insufficient balance. Your current balance is {self.balance}$')
            print('--------------------------------------------------------------------------')


    def view_balance(self):
        
        self.balance = self.load_balance()
        print(f'Your balance is {self.balance}$')
        print('-'*30)



class Expense():


    def __init__(self, filename1='expenses.json', filename2 = 'balance.json'):

        self.filename1=filename1
        self.filename2 = filename2
        self.balance = self.load_balance()


        if not os.path.exists(self.filename1):
            with open(self.filename1, 'w') as f:
                json.dump([], f)
        

    def expenses_table(self, expenses):
        with open(self.filename1, 'w')as f:
            json.dump(expenses, f, indent=4)


    def load_expense_table(self):
        with open(self.filename1, 'r') as f:
            return json.load(f)
        


    
    def load_balance(self):
        
        with open(self.filename2, 'r') as f:
            return json.load(f)['balance']
        

    def save_balance(self):

        with open(self.filename2, 'w') as f:
            json.dump({'balance': self.balance}, f)


    def add_expense(self, name, price):

        
        self.balance = self.load_balance()
        

        if self.balance - price >= 0:
            self.balance -= price

            self.save_balance()

            expenses = self.load_expense_table()
            new_expense = {'name': name, 'price': price, "timestamp":datetime.now().isoformat()}
            expenses.append(new_expense)

            self.expenses_table(expenses)


            print(f'you have made an expense that is {price}$, your current balance is {self.balance}')
            print('-' * 20)
      

        else:
            print("You don't have any avadiable balance to make that payment !! ")
            print('-'*15)
            print(f'you have {self.balance}$ in your account')

    def delete_expense(self, name, price):
       
        expenses = self.load_expense_table()
        def matches_criteria(expense):
            return (expense.get('name') == name and
                    expense.get('price') == price)

        # Filter out the expenses that match the criteria
        updated_expenses = [expense for expense in expenses if not matches_criteria(expense)]
        self.expenses_table(updated_expenses)

        self.balance = self.load_balance()
        self.balance += price
        self.save_balance()      

        print(f'The expens to the name of {name} with the price of {price} has now been deleted. ')
        print('-'* 20)
        print(f'{price}$ has now been added to your balance, current balance is {self.balance}') 



    def view_expense(self, name):
        
        
        expensess = self.load_expense_table()
               
        for  x in expensess:
            
            if  'name' in x and  x['name'] == name:
                print(x['name'], x['price'])
                print('-'*20)
            else:
                pass
        
                
        



if __name__=='__main__':
    main()




