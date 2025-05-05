# import socket
# import random
# import threading
# import base64
# from time import sleep, time

# words = [
#     "nahla", "bee", "iftar", "hout", "whale", "ramadhan", "karhba", "truck", 
#     "narkes", "dance", "fajr", "fil", "elephant", "sawm", "fromage", "cheese", 
#     "frog", "tamer", "hamster", "hamster", "shour", "qiyam", "garden", "zakat",
#     "lampe", "lamp", "hilal", "saher", "magician", "mosquee", "taraweeh", "wagon", 
#     "zebra", "zakaria", "houta", "fish", "zamzam", "khobza", "bread", "harissa",  
#     "semolina", "chorba", "zlebya", "oil", "baklawa", "mkhareq", "harissa", "bsiisa"
# ]

# def encode_to_rev_base64(word: str) -> str:
#     return base64.b64encode(word.encode())[::-1].decode()

# def encode_to_morse(word: str) -> str:
#     MORSE_CODE = {
#         'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
#         'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
#         'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
#         'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
#         '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----', ',': '--..--', '.': '.-.-.-',
#         '?': '..--..', '/': '-..-.', '-': '-....-', '(': '-.--.', ')': '-.--.-', '&': '.-...',
#         ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '_': '..--.-', '"': '.-..-.',
#         '$': '...-..-', '!': '-.-.--', '@': '.--.-.'
#     }

#     word = word.upper()
#     morse_code = []

#     for letter in word:
#         if letter in MORSE_CODE:
#             morse_code.append(MORSE_CODE[letter])
#         elif letter == ' ':
#             morse_code.append('')
#         else:
#             morse_code.append('?') 

#     return ' '.join(morse_code)


# def encode_to_phonetic(text: str)-> str:
#     phonetic_alphabet = {
#         'A': 'Alfa', 'B': 'Bravo', 'C': 'Charlie', 'D': 'Delta',
#         'E': 'Echo', 'F': 'Foxtrot', 'G': 'Golf', 'H': 'Hotel',
#         'I': 'India', 'J': 'Juliett', 'K': 'Kilo', 'L': 'Lima',
#         'M': 'Mike', 'N': 'November', 'O': 'Oscar', 'P': 'Papa',
#         'Q': 'Quebec', 'R': 'Romeo', 'S': 'Sierra', 'T': 'Tango',
#         'U': 'Uniform', 'V': 'Victor', 'W': 'Whiskey', 'X': 'X-ray',
#         'Y': 'Yankee', 'Z': 'Zulu', '0': 'Zero', '1': 'One',
#         '2': 'Two', '3': 'Three', '4': 'Four', '5': 'Five',
#         '6': 'Six', '7': 'Seven', '8': 'Eight', '9': 'Nine'
#     }

#     text = text.upper()
#     encoded_text = []
    
#     for char in text:
#         if char in phonetic_alphabet:
#             encoded_text.append(phonetic_alphabet[char])
#         else:
#             encoded_text.append(char) 
    
#     return ' '.join(encoded_text)

# def encode_to_leetspeak(text):    
#     leet_dict = {
#             'A': '4', 'B': '8', 'C': 'C', 'D': 'D', 'E': '3', 'F': 'F', 'G': '6', 'H': 'H', 'I': '1', 'J': 'J',
#             'K': '|<', 'L': '1', 'M': 'M', 'N': 'N', 'O': '0', 'P': 'P', 'Q': 'Q', 'R': 'r', 'S': '5', 'T': '7',
#             'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y', 'Z': 'Z'
#         }

#     text = text.upper()
#     encoded_text = ''
#     for char in text:
#         if char in leet_dict:
#             encoded_text += leet_dict[char]
#         else:
#             encoded_text += char
#     return encoded_text



# HOST, PORT = '0.0.0.0', 1337

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((HOST, PORT))
# server.listen(5)

# FLAG = "Securinets{u_re_s0_f4st!!m4wld5019rxa8v0o2sqd2dhftwm43y5e}"

# banner = """
#             ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡴⠂
#             ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣾⡿⠋⠀⠀
#             ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣶⣿⣿⠟⠋⠀⠀⠀⠀
#             ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣾⣿⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀
#             ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠀⠀
#             ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣿⣿⣿⣿⣿⡿⠋⠁⠀⠀⠀⠀
#             ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣿⣿⣿⣿⣿⣿⠟⠉⠀⠀⠀⠀⠀⠀⠀
#             ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣿⣿⣿⣿⣿⣿⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#             ⠀⠀⠀⠀⠀⠀⢀⣠⣶⣿⣿⣿⣿⣿⣿⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#             ⠀⠀⠀⠀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣧⣤⣤⣤⣤⡤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#             ⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣿⣿⣿⣿⣿⣿⠿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#             ⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⠿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#             ⠀⠀⠀⠀⣠⣴⣿⣿⠿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#             ⠀⠀⣠⣾⡿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#             ⠠⠞⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#         """

# start = """\n
# ASALAMU AALYKUM 🙌! inshallah bsh tjik arounnd 50 encoded words. 
# To get the flag, u need to decode each one and send back the original word. 
# You have 5 seconds to respond to each word. you gotta be as fast as ⚡ for this one. GL!
# \n
# """


# def handle_client(client_socket):
#     try :

#         client_socket.send(banner.encode()+b'\n'+start.encode())
#         sleep(0.2)

#         for i in range(50):

#             # Choix aléatoire de la méthode de chiffrement et du mot
#             word = random.choice(words)
#             method = random.choice(["reversed_base64", "phonetic", "leet_speak", "morse"])


#             if method == "reversed_base64":
#                 print(f"Sending: {word} ({method})")
#                 encoded_word = "hint: 46esab ...\ncipher: " + encode_to_rev_base64(word) + "\n"
            
#             elif method == "phonetic":
#                 print(f"Sending: {word} ({method})")
#                 encoded_word = "hint: Bravo Charlie!! \ncipher: " + encode_to_phonetic(word) + "\n"

#             elif method == "morse":
#                 print(f"Sending: {word} ({method})")
#                 encoded_word = "hint: beep boop beep beep...\ncipher: " + encode_to_morse(word) + "\n"
            
#             elif method == "leet_speak":
#                 while 'i' in word or 'l' in word:
#                     word = random.choice(words)
#                 print(f"Sending: {word} ({method})")
#                 encoded_word = "hint: 1337 ...\ncipher: " + encode_to_leetspeak(word) + "\n"

#             client_socket.send(encoded_word.encode())

#             start_time = time()
#             response = client_socket.recv(1024).decode().strip()
#             elapsed_time = time() - start_time

#             if elapsed_time > 5:
#                 client_socket.send(b'toooo slow :/ \n')
#                 client_socket.close()
#                 return

#             if response != word:
#                 client_socket.send(b'wrooong answer :( \n')
#                 client_socket.close()
#                 return

#         win = f"Congratulations!\nYou made the light slower: {FLAG}\n"
#         client_socket.send(win.encode())

#     except Exception as e:
#         print(f"Error handling client: {e}")
#     finally:
#         client_socket.close() 

# while True:
#     client_socket, addr = server.accept()
#     print(f"Connection from {addr}")
#     thread = threading.Thread(target=handle_client, args=(client_socket,))
#     thread.start()