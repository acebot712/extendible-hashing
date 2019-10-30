import synthesizer
import simulated_secondary_memory
from directory import Directory
from directory import DirectoryRecord
from bucket import Bucket
from file_converter import file_converter

def generate_data(lis_size,file_name):
    lis = synthesizer.generate_dataset([],lis_size)
    synthesizer.write_to_file(lis,file_name)

""" Entire operation needs to be put in a function at least """
empty_spaces = int(input("Enter Bucket Size: "))
bucket_list = [] # list of buckets
bucket_list.append(Bucket(local_depth = 0, index_records = [], empty_spaces = empty_spaces))

directory_records = [] # list of hash prefix with bucket pointers
directory_records.append(DirectoryRecord(hash_prefix = 0, value = bucket_list[0]))

# Declaring the directory here
directory = Directory(global_depth = 0, directory_records = directory_records) # Directory initialized here with global depth 1

chain_trigger = 0

#%%
""" insert function """    
def insert(index_record):
    global directory,chain_trigger
    # 1. Extract TID
    TID = index_record[0]
    # 2. Convert it ot binary
    TID_binary = format(TID,'018b')
    # 3. Extract global depth number of MSB given in directory.global_depth
    if TID_binary[:directory.global_depth]=='':
        hash_prefix = 0
    else:
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
        bucket.empty_spaces=empty_spaces
        if(directory.global_depth > bucket.local_depth):
            num_links = 2**(directory.global_depth - bucket.local_depth) # num links to same bucket
            num_links_modify = num_links/2 # second half of the links to be changed
            bucket.local_depth = bucket.local_depth + 1
            new_bucket = Bucket(local_depth=bucket.local_depth,index_records=[],empty_spaces=empty_spaces)
            bucket_list.append(new_bucket)
            # print("Bucket List len: {}".format(len(bucket_list)))
            for dr in directory.directory_records:
                # print(bucket)
                if(dr.value == bucket):
                    
                    if(num_links_modify != 0):
                        num_links_modify = num_links_modify - 1
                    else:
                        dr.value = bucket_list[-1] # Pointer to new_bucket
            for i in range(len(temp_index_records)):
                insert(temp_index_records[i])
        elif(directory.global_depth == bucket.local_depth): # address expansion
            if bucket.next != None:
                temp = bucket
                temp.index_records = temp_index_records[:-1]    # culprit1
                bucket.empty_spaces = 0
                while temp.next != None:
                    temp = temp.next
                if temp.empty_spaces > 0:
                    # insert in the overflow bucket
                    temp.index_records.append(temp_index_records[-1])
                    temp.empty_spaces = temp.empty_spaces - 1
                    return
                else:
                    # address expand, then create new overflow bucket with trigger
                    
                    if chain_trigger == TID:
                        chain_trigger = 0
                        bucket.index_records = temp_index_records[:-1] #culprit2
                        bucket.empty_spaces = 0
                        # Create new overflow bucket
                        temp.next = Bucket(local_depth = bucket.local_depth, index_records = [temp_index_records[-1]], empty_spaces = empty_spaces - 1)
                        return
                    else:
                        chain_trigger = TID
                        
                        bucket.index_records = []
                        bucket.empty_spaces = empty_spaces
                        pass
            else:
                
                if chain_trigger == TID:
                    chain_trigger = 0
                    bucket.index_records = temp_index_records[:-1] #culprit3
                    bucket.empty_spaces = 0
                    # Create new overflow bucket
                    bucket.next = Bucket(local_depth = bucket.local_depth, index_records = [temp_index_records[-1]], empty_spaces = empty_spaces - 1)
                    return
                else:
                    chain_trigger = TID
                    pass
                    
                
            num_new_directory_records = len(directory.directory_records) * 2
            # print("Directory Records: {}".format(num_new_directory_records))
            new_directory_records = []
            for drhash in range(num_new_directory_records): # keys added to new_directory
                new_directory_records.append(DirectoryRecord(hash_prefix=drhash,value=None))
            new_directory = Directory(global_depth=directory.global_depth + 1,directory_records=new_directory_records)
                            # ALL right till here

            # Creating new directory complete
            # Create links to appropriate bucket in new directory now
            for dr_index in range(num_new_directory_records):
                match_index = format(new_directory.directory_records[dr_index].hash_prefix,'0'+str(new_directory.global_depth)+'b')[:-1]
                if match_index == '':
                    match_index = 0
                else:
                    match_index = int(match_index,2)
                new_directory.directory_records[dr_index].value = directory.directory_records[match_index].value
                # print("Bucket Data in order:\n{}".format(new_directory.directory_records[dr_index].value.index_records))
            directory = new_directory # Reassign old directory
            for i in range(len(temp_index_records)):
                insert(temp_index_records[i])

#%%
""" Complete this part after writing insert() """
""" file handling for bulkloading done here """
def bulk_hash():
    j = 1
    while(1): #This range needs to be changed, just reads 3 records now
        with open(str(j)+'.txt','r') as fin:
            for line in fin:
                if line[0] != '[':
                    if line[0] != '#':
                        j = int(line[0])
                        break
                    else:
                        return
                else:
                    line_modified = line[1:].rstrip(']\n').split(', ')
                    line_modified = [int(line_modified[i]) if i!=2 else line_modified[i].strip("\'") for i in range(len(line_modified))]
                    # I have a record properly stored in a list in line_modified
                    # call insert() for all records
                    index_record = [line_modified[0],str(j)+'.txt']
                    insert(index_record)

#%%
def visualize():
    global directory
    print("\nGlobal depth: "+str(directory.global_depth)+"\n")
    for i in directory.directory_records:
        print("Hash Prefix: {}\n-> {}".format(i.hash_prefix,i.value.index_records))
        while(1):
            if(i.value.next != None):
                i.value = i.value.next
                print("-> {}".format(i.value.index_records))
            else:
                break
        print("Local Depth: {}\n".format(i.value.local_depth))
    
while(1):
    print("\nEnter A Choice: ")
    print("1. Generate Data")
    print("2. File Converter")
    print("3. Simulate Secondary Memory")
    print("4. Bulk Hash")
    print("5. Insert an Index Record")
    print("6. Visualize Extendible hash")
    print("7. Visualize Secondary Memory (Warninig: Might crash your system)")
    choice = int(input())

    if choice == 1:
        total_index_records = int(input("\nEnter how number of records for 'dataset.txt': "))
        generate_data(total_index_records,'dataset.txt') #passing list size, file name
    elif choice == 2:
        file_converter(input("Enter file name for conversion: "),'dataset.txt')
    elif choice == 3:
        alpha = int(input("\nEnter a block size: "))
        simulated_secondary_memory.simulate_secondary_memory('dataset.txt',alpha)
    elif choice == 4:
        bulk_hash()
    elif choice == 5:
        tid = int(input("Enter TID: "))
        fname = input("Enter blockname (filename) where TID is stored: ")
        insert([tid,fname])
    elif choice == 6:
        visualize()
    elif choice == 7:
        print(bucket_list)
        if(len(directory.directory_records)>=3):
            for i in range(2,len(directory.directory_records)):
                print(directory.directory_records[i].value)
