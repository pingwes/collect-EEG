import csv
import os
import threading
from neurosity import NeurositySDK

neurosity = NeurositySDK({
    "device_id": os.getenv("NEUROSITY_DEVICE_ID"),
})
neurosity.login({
    "email": os.getenv("NEUROSITY_EMAIL"),
    "password": os.getenv("NEUROSITY_PASSWORD")
})

# 1: upward
# 2: down
file = open('data/EEG/movements_5/aug-30-2023.csv', 'a', newline='')
writer = csv.writer(file)

classification = 0
brainwaves = []
classified_brainwaves = []
up_count = 0
down_count = 0


def unpack_data(data):
    unpacked_data = []
    for i in range(0, len(data['data'])):
        unpacked_data = unpacked_data + (data['data'][i])
    return unpacked_data

def brainwave_callback(data):
    print(data)
    brainwaves.append(unpack_data(data))

    if len(brainwaves) == 32:
        try:
            if classification == 1 or classification == "1":
                print("Upward")
            elif classification == 2 or classification == "2":
                print("Down")

            writer.writerow([brainwaves, classification])
            callback_completed.set()
            unsubscribe_brainwaves()

        except Exception as e:
            pass


command = input("Enter a command: ")

while True:
    callback_completed = threading.Event()

    if command == "start" or command == "1" or command == "2" or command == "":
        if command != "": classification = command
        if classification == "1": up_count += 1
        if classification == "2": down_count += 1
        unsubscribe_brainwaves = neurosity.brainwaves_raw(brainwave_callback)
        brainwaves = []
    if command == "stop":
        file.close()
        break

    callback_completed.wait()

    print("Up count: " + str(up_count))
    print("Down count: " + str(down_count))
    command = input("Enter a command: ")