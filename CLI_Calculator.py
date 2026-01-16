import math
import os
from decimal import Decimal
from fractions import Fraction
app_active = True


def clear():
    # \033[H moves cursor to top, \033[2J clears the screen
    print("\033[H\033[2J", end="")
    
def user_display():
    text = f"""\t- CLI Calculator -
    Choose your operation.
    Type 'e' for Expression mode -  types something like 12 * (3 + 4) and gets a result.
    Type 'c' for Command mode - chooses an operation then enters numbers step-by-step.
    Type Abort to Exit the app [or 'a']
    """
    print(text)

def expression_mode():
    print("DEBUG expression")
def command_mode():
    clear()
    current_operator = get_input_operator()
    
    num1 = get_input_number("Enter the first number. ")
    num2 = get_input_number("Enter the second number. ")
    while current_operator == "/" and num2 == 0:
        num2 = get_input_number("Error: Division by zero is not allowed. Please try again with a non-zero value.")
    
    # Calc
    result = calc(num1, current_operator, num2)
    print(f"{num1} {current_operator} {num2} = {result}")

def calc(num1, operator, num2):
     match operator:
        case "*": return num1 * num2 
        case "/": return num1 / num2 
        case "**": return math.pow(num1, num2)
        case "sq": return math.sqrt(num1)
        case "+": return num1 + num2 
        case "-": return num1 - num2 
    
    
def get_input_operator(input_msg ="Enter operation [+,-,*,/]"):
    user_input = input(input_msg)
    while (user_input is not "+"
           and user_input is not "-"
           and user_input is not "*"
           and user_input is not "/"):
        user_input = input("Enter operation, a valid one")
    return user_input
    
def get_input_number(input_msg =""):
    while True:
        user_input =input(input_msg)
        try:
            if user_input.find("/") == -1:
              num = Decimal(user_input)
            else:
              num = float(Fraction(user_input))
              return num
        except ValueError:
            print("Error! Please make sure you type a Number!\n")      
    


# Core Loop
while(app_active):
    clear()
    user_display()
    
    user_input= input()
    while user_input is None or user_input == "":
        user_input=input("Please enter a VALID input [e/c/abort] ")
    user_input = str.lower(user_input)
        
    match user_input:
        case "e":
            expression_mode()
        case "c":
            command_mode()
        case "a" | "abort":
            print("Thx for aborting! Ill stop now, hopefully")
            app_active = False
        case _: continue
    app_active = False
    
# TODO
# add using 1/2 numbers

