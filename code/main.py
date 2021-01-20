import data_functions


# Data encoded according to the base64 protocol.
encoded_data = "NAkAALoLAAA="

# Parses the data.
temp, humid = data_functions.package_parser(encoded_data)

# Formats and prints the output.
print(f"The extracted temperature is {temp}.")
print(f"The extracted humidity is {humid}.")