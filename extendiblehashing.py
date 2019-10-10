import synthesizer
import simulated_secondary_memory

def generate_data(lis_size,file_name):
    lis = synthesizer.generate_dataset([],lis_size)
    synthesizer.write_to_file(lis,file_name)

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
        print("Bulk Loading here")
    