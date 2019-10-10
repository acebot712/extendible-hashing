# -*- coding: utf-8 -*-

import os
import math
import random
import string

""" lis list is used to generate dataset array , it is global"""
lis=[]
lis_size=10
alpha=3 # to divide records in buckets


def total_blocks(data_size,aplha):
  total_buck=math.ceil(data_size/alpha)
  return total_buck

def make_bucket(filename):
  data_file=open(filename,"r")
  data_file_list=data_file.readlines()
  #record_list=[]
  file_name_counter=0
  for i in range(0,lis_size,alpha):
    temp_list=[]
    j=i+3
    file_name_counter=file_name_counter+1
    with open((str(file_name_counter)+'.txt'),'w') as f:
      if(j<=lis_size):
        for x in range(i,j):
          #temp_list.append(data_file.readlines().split(' '))
          temp_list.append(data_file_list[x].split('\n'))
          next_block_name=file_name_counter+1
          

          #f.write(temp_list)
        f.write(str(temp_list))
        f.write("#"+str(next_block_name)+".txt")
        
      else:
        mod=lis_size%alpha
        for y in range(i,i+mod):
          temp_list.append(data_file_list[y].split('\n'))
        f.write(str(temp_list))
        f.write("#$")
      #f.write(str(temp_list))

def clear():
  for i in range(total_blocks(lis_size,alpha)):
    if(str(i+1)+".txt"):
      os.remove(str(i+1)+".txt")
    else:
      print("not found")

"""XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXxxx """
#print_data()
#clear()
#print(total_blocks(10,alpha))
make_bucket('dataset.txt')
#clear()