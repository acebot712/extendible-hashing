import synthesizer
import simulated_secondary_memory
from directory import Directory
from directory import DirectoryRecord
from bucket import Bucket

def generate_data(lis_size,file_name):
    lis = synthesizer.generate_dataset([],lis_size)
    synthesizer.write_to_file(lis,file_name)

""" Entire operation needs to be put in a function at least """
empty_spaces = 3
bucket_list = [] # list of buckets
bucket_list.append(Bucket(local_depth = 1, index_records = [], empty_spaces = empty_spaces))
bucket_list.append(Bucket(local_depth = 1, index_records = [], empty_spaces = empty_spaces))   

directory_records = [] # list of hash prefix with bucket pointers
directory_records.append(DirectoryRecord(hash_prefix = 0, value = bucket_list[0]))
directory_records.append(DirectoryRecord(hash_prefix = 1, value = bucket_list[1]))

# Declaring the directory here
directory = Directory(global_depth = 1, directory_records = directory_records) # Directory initialized here with global depth 1


#%%
""" insert function """    
def insert(directory,index_record):
    # 1. Extract TID
    TID = index_record[0]
    # 2. Convert it ot binary
    TID_binary = format(TID,'018b')
    # 3. Extract global depth number of MSB given in directory.global_depth
    hash_prefix = int(TID_binary[:directory.global_depth],2) #in decimal
    # 4. IndexRecord to be stored in a bucket
    # search using hash prefix in directory
    # key is hash_prefix itself
    # directory.directory_records[key].value is a bucket
    bucket = directory.directory_records[hash_prefix].value # bucket where insertion is to be done
    bucket.index_records.append(index_record)
    # Insertion step complete. Now check for overflow
    bucket.empty_spaces = bucket.empty_spaces - 1
    if(bucket.empty_spaces < 0):    #Overflow
        temp_index_records = bucket.index_records # temp list for rehashing
        bucket.index_records = []
        if(directory.global_depth > bucket.local_depth):
            num_links = 2**(directory.global_depth - bucket.local_depth) # num links to same bucket
            num_links_modify = num_links/2 # second half of the links to be changed
            bucket.local_depth = bucket.local_depth + 1
            new_bucket = Bucket(local_depth=bucket.local_depth,index_records=[],empty_spaces=empty_spaces)
            for dr in directory.directory_records:
                if(dr.value == bucket):
                    if(num_links_modify != 0):
                        num_links_modify = num_links_modify - 1
                    else:
                        dr.value = new_bucket
                        for ir in temp_index_records:
                            insert(directory,ir)
        elif(directory.global_depth == bucket.local_depth): # address expansion
            num_new_directory_records = len(directory.directory_records) * 2
            new_directory_records = []
            for drhash in range(num_new_directory_records): # keys added to new_directory
                new_directory_records.append(DirectoryRecord(hash_prefix=drhash,value=None))
            new_directory = Directory(global_depth=directory.global_depth + 1,directory_records=new_directory_records)
            # Creating new directory complete
            # Create links to appropriate bucket in new directory now
            for dr_index in range(num_new_directory_records):
                match_index = format(new_directory.directory_records[dr_index].hash_prefix,'0'+str(new_directory.global_depth)+'b')[:-1]
                match_index = int(match_index,2)
                new_directory.directory_records[dr_index].value = directory.directory_records[match_index].value
            directory = new_directory
            for ir in temp_index_records:
                insert(directory,ir)
            
            
""" Complete this part after writing insert() """
""" file handling for bulkloading done here """
def bulk_hash():
    for j in range(1,4): #This range needs to be changed
        with open(str(j)+'.txt','r') as fin:
            for line in fin:
                line_modified = line[1:].rstrip(']\n').split(', ')
                line_modified = [int(line_modified[i]) if i!=1 else line_modified[i].strip("\'") for i in range(len(line_modified))]
                # I have a record properly stored in a list in line_modified
                # call insert() for all records
                index_record = [line_modified[0],str(j)+'.txt']
                insert(directory,index_record)

#%%
    
while(1):
    print("\nEnter A Choice: ")
    print("1. Generate Data")
    print("2. Simulate Secondary Memory")
    print("3. Bulk Hash")
    print("4. Visualize Extendible hash")
    choice = int(input())

    if choice == 1:
        generate_data(int(input("\nEnter how number of records for 'dataset.txt': ")),'dataset.txt') #passing list size, file name
    elif choice == 2:
        alpha = int(input("\nEnter a block size: "))
        simulated_secondary_memory.simulate_secondary_memory('dataset.txt',alpha)
    elif choice == 3:
        print("\nBucket List\n {}".format(bucket_list[0].index_records))
        print("Bucket List\n {}".format(bucket_list[1].index_records))
        bulk_hash()
        print("\nBucket List\n {}".format(bucket_list[0].index_records))
        print("Bucket List\n {}".format(bucket_list[1].index_records))
