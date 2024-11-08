import os
import uuid
# Specify the file path
file_path = '/home/ayach/code/uuid.txt'

# Check if the file exists
if os.path.exists(file_path):
	print("The file exists.")
else:
	print("The file does not exist.")
	file= open("code/uuid.txt", "w") 
	myuuid=uuid.uuid1()
	file.write(str(myuuid))
	file.close()
	print(myuuid)
