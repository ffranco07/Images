from PIL import Image
import math

my_image = Image.new('RGB', (50, 50), 'white')

pixels = my_image.load()
for i in range(my_image.size[0]):
    for j in range(my_image.size[1]):
        #               (red, green, blue)
        pixels[i, j] = ((0xff // 50) * i, int(0xff * abs(math.sin(j / 10))), 0)

my_image.save("image.bmp", "bmp")

message = "hello"

# 1. converting a message into bits
# 2. hiding those bits in an image (and saving it)
# 3. read in the bits from an image
# 4. convert those bits back a message

def convert_message(message):
    message_bits = []

    for char in message:
        num = ord(char)
        bin_num = bin(num)[2:]

        for i in range(0, 8 - len(bin_num)):
            message_bits.append(0)
        for bit in bin_num:
            message_bits.append(int(bit))
        
    return message_bits


def hide_message(filename, message_bits):
    with open(filename, 'rb') as image:
        data = image.read()
        usable_data = bytearray(data)

        for i in range(len(message_bits)):
            if message_bits[i] == 0:
                usable_data[54 + i] &= 0xfe
            elif message_bits[i] == 1:
                usable_data[54 + i] |= 0x01

        with open(filename, 'wb') as write_file:
            write_file.write(usable_data)

def read_message(filename):
    with open(filename, 'rb') as image:
        data = image.read()
        usable_data = bytearray(data)

        message_bits = []

        for i in range(54, len(usable_data)):
            message_bits.append(usable_data[i] & 0x01)

        return message_bits

def unconvert_message(message_bits):
    message = ""
    chunk = 0

    for i in range(0, len(message_bits) - 8, 8):
        for j in range(8):
            chunk <<= 1
            chunk += message_bits[i + j]

        char = chr(chunk)
        message += char

        chunk = 0

    return message

bits = convert_message("hello this is a secret message")
hide_message("image.bmp", bits)
recovered_bits = read_message("image.bmp")
recovered_message = unconvert_message(recovered_bits)
print(recovered_message)
