import base64
from struct import unpack


# Data encoded according to the base64 protocol.
encoded_data = "NAkAALoLAAA="

def package_parser(package):
    # Decodes the encoded data.
    decoded_data = base64.b64decode(package)

    # Unpacks the decoded data into two 32-bit signed integers.
    temp, humid = unpack('ii', decoded_data)

    # Converts temperatures from significands to decimal values.
    temp_dec = temp * 10**(-2)
    humid_dec = humid * 10**(-2)

    return (temp_dec, humid_dec,)

temp, humid = package_parser(encoded_data)

print(f"The extracted temperature is {temp}.")
print(f"The extracted humidity is {humid}.")