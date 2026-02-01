a = 5
b = 2
if a > b: print("a is greater than b")
#Note: You still need the colon : after the condition.

a = 2
b = 330
print("A") if a > b else print("B")
#This is called a conditional expression (sometimes known as a "ternary operator").

a = 10
b = 20
bigger = a if a > b else b
print("Bigger is", bigger)

a = 330
b = 330
print("A") if a > b else print("=") if a == b else print("B")

x = 15
y = 20
max_value = x if x > y else y
print("Maximum value:", max_value)

username = ""
display_name = username if username else "Guest"
print("Welcome,", display_name)

"""Shorthand if statements and ternary operators should be used when:

The condition and actions are simple
It improves code readability
You want to make a quick assignment based on a condition"""