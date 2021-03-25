import cgi, cgitb
# Create instance of FieldStorage
form = cgi.FieldStorage()
# Get data from fields
a = form.getvalue('kwInput')
print(a)


""" import time 
print("test1")
time.sleep(5)
print("test2") """