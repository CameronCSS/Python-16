record_last_session = ["John", "12/20/2022", "08:17:32 pm", "No loading errors"]

file = open("register.txt", 'a')

for text in record_last_session:
    file.writelines(text+"\t")
    
    
file.close()


new_file = open("register.txt", 'r')

print(new_file.read())
    
new_file.close()