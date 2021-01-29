import base64
import struct
import random


# Decodes and unpacks a package.
def package_parser(package):
    # Decodes the encoded data.
    decoded_data = base64.b64decode(package)

    # Unpacks the decoded data into two 32-bit signed integers.
    temp, humid = struct.unpack("ii", decoded_data)

    # Converts temperatures from significands to decimal values.
    temp_dec = temp * 10**(-2)
    humid_dec = humid * 10**(-2)

    return (temp_dec, humid_dec,)


# Packs and encodes a two integer tuple.
def pack_and_encode(data):
    # Packs the data through an iterable unpacking of the data tuple.
    packed_data = struct.pack("ii", *data)
    encoded_data = base64.b64encode(packed_data)

    return encoded_data


# Generates random temperature and humidity data.
def generate_data():
    # Generates random data.
    rand_temp = round(random.uniform(-50, 120), 2)
    rand_humid = round(random.uniform(0, 100), 2)

    # Converts float to an integer representation.
    significand_temp = round(rand_temp * 10**2)
    significand_humid = round(rand_humid * 10**2)

    return (significand_temp, significand_humid)
