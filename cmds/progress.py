import time
from encode_str import encode_str

def detect_percentage(char, file="progress.txt"):
    time.sleep(1)
    file_path = file
    
    while True:
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                if lines is not None:
                    last_line = lines[-1] if lines else ''
                    whole = ''.join(lines)  # Combine all lines into a single string
                    if 'successfully' in whole.lower() or 'success' in whole.lower() or 'DEC_OK' in whole or '100%' in whole.lower():
                        print("Success keyword detected. Exiting...")
                        char.WriteValue(encode_str('DONE'))
                        break

                    percentage = None
                    for word in last_line.split():
                        if word.endswith('%'):
                            try:
                                percentage = str(word[:-1])+str('%')
                                break
                            except ValueError:
                                pass

                    if percentage is not None and isinstance(percentage, str):
                        char.WriteValue(encode_str(percentage))

            time.sleep(0.5)  # Adjust the sleep duration as needed

        except FileNotFoundError:
            print("progress.txt file not found. Exiting...")
            break