import base64
from struct import unpack

# To-Do List:
# - Write some kind of test for this code with PyTest.

# Data encoded according to the base64 protocol.
encoded_data = "NAkAALoLAAA="

# Decodes the encoded data.
decoded_data = base64.b64decode(encoded_data)

# Unpacks the decoded data into two 32-bit signed integers.
temp, humid = unpack('ii', decoded_data)

# Converts temperatures from significands to decimal values.
temp_dec = temp * 10**(-2)
humid_dec = humid * 10**(-2)

print("The extracted temperature is %s." % temp_dec)
print("The extracted humidity is %s." % humid_dec)