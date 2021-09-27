from bit import wif_to_key

key = wif_to_key("cNKdS8V3i7fdbZfYgXVQaUonVvpciTFqnYnEjXsYa4SRrpFfSGU4")

print(key.get_balance("btc"))

#send to address

addresses = [
    "mvX5NEqfFcPthUX9QpEzMbnCXddDP7cACA"
]

outputs = []

for address in addresses:
    outputs.append((address, 0.00005, "btc"))

print(key.send(outputs))

print(key.get_balance("btc"))
