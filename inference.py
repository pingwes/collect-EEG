import csv
import os
import threading
from neurosity import NeurositySDK
import requests
import json
import time
import pyautogui

time.sleep(5)


neurosity = NeurositySDK({
    "device_id": os.getenv("NEUROSITY_DEVICE_ID"),
})
neurosity.login({
    "email": os.getenv("NEUROSITY_EMAIL"),
    "password": os.getenv("NEUROSITY_PASSWORD")
})

brainwaves = []

url = "http://184.67.78.114:40078/predict"


def unpack_data(data):
    unpacked_data = []
    for i in range(0, len(data['data'])):
        unpacked_data = unpacked_data + (data['data'][i])
    return unpacked_data


def brainwave_callback(data):

    brainwaves.append(unpack_data(data))

    # print(data)
    if len(brainwaves) == 32:

        try:
            response = requests.post(url, data=json.dumps(brainwaves), headers=headers)
            if response.status_code == 200:
                prediction_list = json.loads(response.text)[:15]
                print(prediction_list)
                total_sum = sum(prediction_list)

                if total_sum < 5:
                    # pyautogui.press('space')
                    print("upward")
                elif total_sum > 5:
                    # pyautogui.press('d')
                    print("down")
            else:
                print('Request failed with status code:', response.status_code)
        except requests.ConnectionError:
            print('Failed to connect to the URL. Please check the address and try again.')
        except Exception as e:
            print('An error occurred:', str(e))

        brainwaves.clear()


headers = {'Content-type': 'application/json'}

unsubscribe_brainwaves = neurosity.brainwaves_raw(brainwave_callback)
