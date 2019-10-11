# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 18:59:14 2019

@author: asterdan712
"""

class DirectoryRecord:
    def __init__(self, hash_prefix,value):
        self.hash_prefix = hash_prefix # Its a string
        self.value = value # value is a bucket

class Directory:
    def __init__(self,global_depth,directory_records):
        self.global_depth = global_depth
        self.directory_records = directory_records