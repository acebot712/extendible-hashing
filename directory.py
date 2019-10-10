# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 18:59:14 2019

@author: asterdan712
"""

class DirectoryRecord:
    def __init__(self, hash_prefix):
        self.hash_prefix = hash_prefix
        self.value = None

class Directory:
    def __init__(self,global_depth,directory_records):
        self.global_depth = global_depth
        self.directory_records = directory_records