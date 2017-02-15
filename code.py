#!/usr/bin/python
"""
This code was authored using Python 3.6.0 as a Python coding exercise.
There is an accompanying properties.txt file which holds the
initial inventory level in addition to the name of the products.
date: 2/14/2017
platform: Mac OS X
"""
from random import randint

def getProperties():
    """Reads inventory/product names from a properties file within the same folder as this file."""
    inventory = {}
    # All the hardcoding is done in this text file away from the code.  Good practice.
    filename = "properties.txt" 
    fh = open(filename, 'r')
    rawInventoryList = fh.readline().split(',')  # Called it 'raw' because of the white spaces.
    fh.close()
    for x in rawInventoryList:
        x = x.strip() 
        product =  x.split('=')
        # validate the inventory level as read from the properties file
        try:
            inventory[product[0]]=int(product[1]) 
        except:
            print("Error: miss-typed data in " +  filename )
            inventory = None                  # Bad data! The initial inventory could not be formed.
            break
    return inventory
   
    
def getNextOrder(orderNo = 1):
    """Returns an order as a dictionary when called."""
    order = {}
    order["Header"] = orderNo
    quantities = []
    while(True):
        totalQuantities = 0
        for i in range(len(productNames)):
            quantities.append(randint(0,5))
            totalQuantities += quantities[i]
        if(totalQuantities):
            break                             # This order is valid, break out of the while-loop
    for i in range(len(productNames)):
         order[productNames[i]] = quantities[i]    
    return order   
  
 
def allocator(stream, orderNo):
    """Fills orders as they come, updates the inventory/back-log level, and shows status."""
    order = getNextOrder(orderNo)
    
    # print the Header in the status-line
    print('stream' + stream + '>header' +    str(order["Header"]) + ": ", end="")
    
    # print the order segment in the stalus-line
    printStatus(order)
    
    # calculate the new inventory, allocated, and back-order after applying the order 
    allocated = {}
    backOrder = {}
    for key, value in order.items():
        if(key != "Header"):
            if(inventory[key] >= order[key]): # Can the order on this particular product be filled?
                inventory[key] -= order[key] 
                allocated[key] = order[key]
                backOrder[key] = 0
            else:                             # The order could not be filled.
                # The inventory would not be changed for this key.
                allocated[key] = 0
                backOrder[key] = order[key]
                           
    # print the allocated
    printStatus(allocated)
            
    # print the back-order
    printStatus(backOrder,"\n")
    #print(inventory) # unrem for debuging
            
def printStatus(statusDictonary, terminatingString="::"): 
    """Prints status on order, allocations, or back-orders"""
    count = 1
    for name in productNames:
        print(statusDictonary[name], end="")
        if(count < len(productNames)):
            print(",", end="")
            count += 1
        else:
            print(terminatingString, end="")
            
# A list of streams each with an initial value of 'orderNo'
streams=[{"stream":"0","orderNo":1}, {"stream":"1","orderNo":1}, {"stream":"2","orderNo":1}]          

 
inventory = getProperties()
if(inventory != None):                        # Did the inventory pass our data-validation check?
    productNames = sorted(inventory.keys())   # Form the sorted list of product names.
    print("The initial inventory: ", inventory)
      
    while(sum(inventory.values())):           # keep processing orders till inventory is all zeros
        # Generate a random streamNo to use (0,1, or 2).  We are simulating 3 streams here.
        # An order might come from any of these 3 streams in random.
        streamNo = randint(0, 2) 
        allocator(streams[streamNo]["stream"],streams[streamNo]["orderNo"])  
        streams[streamNo]["orderNo"] +=1
    print("The final inventory: ", inventory)
else:
    print("Please correct the properties file first.")

