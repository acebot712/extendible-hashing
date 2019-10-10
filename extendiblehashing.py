import synthesizer
import simulated_secondary_memory
from .directory import Directory
from .directory import DirectoryRecord
from .bucket import Bucket

def generate_data(lis_size,file_name):
    lis = synthesizer.generate_dataset([],lis_size)
    synthesizer.write_to_file(lis,file_name)

""" Entire operation needs to be put in a function at least """
bucket_list = []    # list of buckets
directory_records = [] # list of hash prefix with bucket pointers

#%%
# Declaring the directory here
directory = Directory(global_depth = 0, directory_records = directory_records) # Directory initialized here with global depth 0
j = 1 # Name of first disk block

""" Complete this part after writing insert() """
""" file handling for bulkloading done here """
with open(str(j)+'.txt','r') as fin:
    for line in fin:
        line_modified = line[1:].rstrip(']\n').split(', ')
        line_modified = [int(line_modified[i]) if i!=1 else line_modified[i].strip("\'") for i in range(len(line_modified))]
        # I have a record properly stored in a list in line_modified
        # call insert() for all records
    
""" insert function """    
def insert(directory,index_record):
    # 1. Extract TID
    TID = index_record[0]
    # 2. Convert it ot binary
    TID_binary = "{0:b}".format(TID)
    # 3. Extract global depth number of MSB given in directory.global_depth
    hash_prefix = TID_binary[:directory.global_depth]
    # 4. IndexRecord to be stored in a bucket
    if bucket_list == []:
        bucket = Bucket(local_depth = 0,index_records = list(index_record),empty_spaces=2) # Bucket of size 3
        bucket_list.append(bucket)
    else:
        # search using hash prefix in directory
        key = directory.directory_records.index(hash_prefix)
        # key is my key
        # directory.directory_records[key].value is a bucket
        bucket = directory.directory_records[key].value
        bucket.index_records.append(index_record)
        bucket.empty_spaces=bucket.empty_spaces - 1
        if bucket.empty_spaces < 0:
            # Overflow
        else:
            # All izz well
            pass

#%%
    
while(1):
    print("\nEnter A Choice: ")
    print("1. Generate Data")
    print("2. Simulate Secondary Memory")
    print("3. Insert Record")
    print("4. Visualize Extendible hash")
    choice = int(input())

    if choice == 1:
        generate_data(10,'dataset.txt') #passing list size, file name
    elif choice == 2:
        alpha = int(input("\nEnter a block size: "))
        simulated_secondary_memory.simulate_secondary_memory('dataset.txt',alpha)
    elif choice == 3:
        bulk_hash()
    