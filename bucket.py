# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 18:38:03 2019

@author: asterdan712
"""

class Bucket:
    def __init__(self,local_depth,index_records,empty_spaces):
        self.local_depth = local_depth
        self.index_records = index_records
        self.empty_spaces = empty_spaces
        self.next = None