import synthesizer

def generate_data(lis_size,file_name):
    lis = synthesizer.generate_dataset([],lis_size)
    synthesizer.write_to_file(lis,file_name)

choice = int(input("\nEnter a number: "))
if choice == 1:
    generate_data(10,'dataset.txt') #passing list size, file name
 