print(bool("Hello"))
print(bool(15))

x = "Hello"
y = 15

print(bool(x))
print(bool(y))

#All True
bool("abc")
bool(123)
bool(["apple", "cherry", "banana"])

#All False 
bool(False)
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})



class myclass():
  def len(self):
    return 0

myobj = myclass()
print(bool(myobj)) #False



def myFunction() :
  return True

print(myFunction()) #True



def myFunction() :
  return True

if myFunction():
  print("YES!")
else:
  print("NO!") 



x = 200
print(isinstance(x, int)) #if an object is of a certain data type