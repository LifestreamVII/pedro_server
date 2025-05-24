# Function to write to a file
def wFile(filename, content, mode='append'):
    if mode == 'overwrite':
        file_mode = 'w'
    else:  # Default to append mode
        file_mode = 'a'
    
    with open(filename, file_mode) as file:
        file.write(content)

# Function to read from a file
def rFile(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return "File not found."