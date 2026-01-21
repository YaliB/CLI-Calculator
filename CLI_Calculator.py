import math
# import os
from decimal import Decimal
from fractions import Fraction
app_active = True
operators_list = ["**","^", "_","sq", "*","/", "+","-"]

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
    num1 = float(num1)
    num2 = float(num2)
    match operator:
        case "*": return num1 * num2 
        case "/": return num1 / num2 
        case "**" | "^": return math.pow(num1, num2)
        case "sq": return math.sqrt(num1)
        case "+": return num1 + num2 
        case "-": return num1 - num2 

def solve(txt):
    if txt.find("(") != -1:
        sub_equation = extracting_equation_from_brackets(txt)
        if sub_equation[1] != -1:
            #replacing the (content) with result
            txt = txt[:sub_equation[1]] + str(solve(sub_equation[0])) + txt[sub_equation[2]+1:]
            
    # Prioritize order of operations
    # separate equations
    if txt.find("^") !=-1:
        index_start, index_end, num1, num2 = decoding_symbols_in_line(txt, "^")
        txt=txt[:index_start] +str(calc(num1=num1,operator="^",num2=num2))+ txt[index_end:]
    if txt.find("_") !=-1:
        index_start, index_end, num1, num2 = decoding_symbols_in_line(txt, "_")
        txt=txt[:index_start] +str(calc(num1=num1,operator="_",num2=num2))+ txt[index_end:]
    if txt.find("*") !=-1:
        index_start, index_end, num1, num2 = decoding_symbols_in_line(txt, "*")
        txt=txt[:index_start] +str(calc(num1=num1,operator="*",num2=num2))+ txt[index_end:]
    if txt.find("/") !=-1:
        index_start, index_end, num1, num2 = decoding_symbols_in_line(txt, "/")
        txt=txt[:index_start] +str(calc(num1=num1,operator="/",num2=num2))+ txt[index_end:]
    if txt.find("+") !=-1:
        index_start, index_end, num1, num2 = decoding_symbols_in_line(txt, "+")
        txt=txt[:index_start] +str(calc(num1=num1,operator="+",num2=num2))+ txt[index_end:]
    if txt.find("-") !=-1:
        index_start, index_end, num1, num2 = decoding_symbols_in_line(txt, "-")
        txt=txt[:index_start] +str(calc(num1=num1,operator="-",num2=num2))+ txt[index_end:]
    
    for op in operators_list:
        if op in txt:
            print(txt)
            return solve(txt)
    return txt

def decoding_symbols_in_line(txt, operator):
    index_start=-1
    index_end=-1
    temp_op_id = txt.find(operator)

    # get the first number-
    temp = temp_op_id
    while(temp >= 0):
        temp-=1
        if temp == 0:
            num1 = txt[temp:temp_op_id]
            index_start=temp
            break
        elif txt[temp] in operators_list:
            num1 = txt[temp+1:temp_op_id]
            index_start=temp+1
            break
    
    # get the second number-
    temp = temp_op_id+1
    while(temp <= len(txt)):
        if temp == len(txt):
            num2 = txt[temp_op_id+1:temp]
            index_end=temp
            break
        elif txt[temp] in operators_list:
            num2 = txt[temp_op_id+1:temp]
            index_end=temp
            break
        temp+=1
    return index_start,index_end,num1,num2

def parse_input(input):
    """
    ()
    ** = ^
    SQ = _
    *
    /
    +
    -
    """
    txt = str(input).replace(" ", "")
    txt = txt.lower()
    txt= txt.replace("**","^")
    txt= txt.replace("sq","_")
    if txt[0] in operators_list or txt[len(txt)-1] in operators_list:
        print("Error invalid syntax")
        return
    if bracket_validtest(txt):
        return solve(txt) 
    else: 
        print("ERROR bracket are invaild!")
        return
    
    
def bracket_validtest(txt):
    opener_count =0
    closer_count =0
    for ch in txt:
        if ch == "(": opener_count+=1
        elif ch == ")": closer_count+=1
    return opener_count==closer_count # If so - valid
def extracting_equation_from_brackets(txt):
        starting_index =-1
        ending_index =-1
        extra_brackets =0
        for index, value in enumerate(txt):
            if value == "(": 
                if starting_index == -1: # find the first (
                    starting_index =index
                else: extra_brackets+=1
            elif value == ")": 
                if extra_brackets == 0: #find the last relevant )
                    ending_index=index
                    break
                else: extra_brackets-=1
        return [txt[starting_index+1:ending_index], starting_index,ending_index]
def extracting_number_from_string(str1):
    
    return 0
        
    
def get_input_operator(input_msg ="Enter operation [+,-,*,/]"):
    user_input = input(input_msg)
    while (user_input != "+" #TODO update valid operators from the operators list
           and user_input != "-"
           and user_input != "*"
           and user_input != "/"):
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
def get_inline_operator(txt):
    for op in operators_list:
        if str(txt).find(op) != -1:
            num1= str(txt).split(op)[0]
            num2= str(txt).split(op)[1]
            print(f"DEBUG | txt={txt}")
            print(f"DEBUG | num1={num1} | num2={num2}")
            operator = op
            break
    if operator == None: return None
    return [num1, operator, num2 ]
def is_operator(txt):
    for op in operators_list:
        if op == txt: return True
    return False
            
    

# -- DEBUG area --
clear()
print("\t-- DEBUG AREA START --")
# test_input = "12 * (3 + 4 (1+1)) -7"
# test_input = "12 * (1+1)"
test_input = "10+10*(7-5)"
# test_input = "2+2*8+4-3/4+8"
print(f"THE TEST IS=> {test_input}")
print(parse_input(test_input))

print("\t-- DEBUG AREA END --")
# Core Loop
while(app_active and False):
    clear()
    user_display()
    
    user_input= input()
    while user_input is None or user_input == "":
        user_input=input("Please enter a VALID input [e/c/abort] ")
    user_input = str.lower(user_input)
        
    match user_input:
        case "e" | "expression":
            expression_mode()
        case "c" | "command":
            command_mode()
        case "a" | "abort":
            print("Thx for aborting! Ill stop now, hopefully")
            app_active = False
        case _: continue
    app_active = False
    
# TODO
# add using 1/2 numbers

