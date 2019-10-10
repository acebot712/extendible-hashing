import synthesizer
import simulated_secondary_memory

def generate_data(lis_size,file_name):
    lis = synthesizer.generate_dataset([],lis_size)
    synthesizer.write_to_file(lis,file_name)

choice = int(input("\nEnter a number: "))
while(1):
    if choice == 1:
        generate_data(10,'dataset.txt') #passing list size, file name
    elif choice ==2:
        simulated_secondary_memory.simulate_secondary_memory('dataset.txt',3)