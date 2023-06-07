from neurosity import neurosity_sdk
import os
import csv
import threading

neurosity = neurosity_sdk({
    "device_id": os.getenv("NEUROSITY_DEVICE_ID"),
})
neurosity.login({
    "email": os.getenv("NEUROSITY_EMAIL"),
    "password": os.getenv("NEUROSITY_PASSWORD")
})

# 1: blue
# 2: red
# 3: green
# 4: yellow
file = open('data/june-6-2023.csv', 'a', newline='')
writer = csv.writer(file)

classification = 0
brainwaves = []
classified_brainwaves = []
count = 0


def unpack_data(data):
    unpacked_data = []
    for i in range(0, len(data['data'])):
        unpacked_data = unpacked_data + (data['data'][i])
    return unpacked_data


def signal_quality_callback(data):
    print(data)


def brainwave_callback(data):
    print(data)
    brainwaves.append(unpack_data(data))

    if len(brainwaves) == 32:
        try:
            if classification == 1 or classification == "1":
                print("Blue")
            elif classification == 2 or classification == "2":
                print("Red")
            elif classification == 3 or classification == "3":
                print("Green")
            elif classification == 4 or classification == "4":
                print("Yellow")

            writer.writerow([brainwaves, classification])
            callback_completed.set()
            unsubscribe_brainwaves()

        except Exception as e:
            pass


command = input("Enter a command: ")

while True:
    # Create an event object
    callback_completed = threading.Event()

    if command == "start" or command == "1" or command == "2" or command == "3" or command == "4" or command == "":
        if command != "": classification = command
        unsubscribe_brainwaves = neurosity.brainwaves_raw(brainwave_callback)
        brainwaves = []
    if command == "stop":
        file.close()
        break

    # Wait for the callback to complete
    callback_completed.wait()
    count += 1
    print("Count: " + str(count))
    command = input("Enter a command: ")