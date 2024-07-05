# Define a dictionary with electronic device types as keys and True as values
electronic_device_types = {
"indoor":True,
"outdoor":True
    # Add more device types as needed
}

# Create a list of items to filter

electronic_devices = [
    "Laptop", "Refrigerator", "Smartphone", "Security camera", "Television",
    "Air purifier", "Toaster", "Microwave", "Vacuum cleaner", "Washing machine",
    "Ceiling fan", "Hair dryer", "Coffee maker", "Humidifier", "Dehumidifier",
    "Electric kettle", "Gaming console", "Projector", "Printer", "Scanner",
    "Tablet", "Smartwatch", "Wireless speaker", "Robot vacuum", "Drone",
    "Electric toothbrush", "Electric shaver", "Curling iron", "Straightener",
    "Clothes iron", "Sewing machine", "Power bank", "Headphones", "Mouse",
    "Keyboard", "Desktop computer", "Monitor", "Projector screen",
    "Security system", "Smoke detector", "Carbon monoxide detector",
    "Thermostat", "Video doorbell", "Smart speaker", "Electric car",
    "Electric bike", "Electric scooter", "Hair straightener", "Clothes steamer",
    "Electric blanket", "Electric heater", "Portable heater", "Air conditioner",
    "Dehumidifier", "Portable fan", "Electric lawnmower", "Hedge trimmer",
    "Pressure washer",  "Electric grill", "Food processor", "Blender",
    "Electric mixer", "Toaster oven", "Popcorn maker", "Ice cream maker",
    "Espresso machine", "Deep fryer",  "Rice cooker", "Slow cooker",
    "Electric can opener", "Garbage disposal",  "Electric oven", "Range hood",
]

# Print the dataset (optional)
# print(electronic_devices)

# Filter the items using list comprehension and dictionary lookup
electronic_devices = [item for item in electronic_devices if electronic_device_types.get(item, False)]

# Print the filtered list of electronic devices
print(electronic_devices)
