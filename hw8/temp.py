#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import matplotlib.pyplot as plt
import numpy as np


# In[2]:


inps = []
def get_input():
    direction = input("Enter the direction to Move:")
    print(direction)
    if ('a' or 'd' or 's' or 'w') not in direction:
        print('wrong input')
    else:
        distance = float(input("Enter the distance"))
        inps.append((distance,direction))
        #print(inps)
        resume  = input("Do you want to continue?")
        if resume == 'y':
            get_input()
        else:
            print("Starting execution")
    return inps
            


# In[3]:


coms = get_input()
print(coms)

