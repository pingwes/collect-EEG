import argparse
import time

import matplotlib
import numpy as np
matplotlib.use('Agg')

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations


def contains_all_same_values(lst):
    return len(set(lst)) == 1


def contains_all_zeros(lst):
    return all(element == 0 for element in lst)


def main():
    BoardShim.enable_dev_board_logger()

    board_id = BoardIds.GANGLION_BOARD

    parser = argparse.ArgumentParser()
    # use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port
    parser.add_argument('--timeout', type=int, help='timeout for device discovery or connection', required=False,
                        default=0)
    parser.add_argument('--ip-port', type=int, help='ip port', required=False, default=0)
    parser.add_argument('--ip-protocol', type=int, help='ip protocol, check IpProtocolType enum', required=False,
                        default=0)
    parser.add_argument('--ip-address', type=str, help='ip address', required=False, default='')
    parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='/dev/cu.usbmodem11')
    parser.add_argument('--mac-address', type=str, help='mac address', required=False, default='')
    parser.add_argument('--other-info', type=str, help='other info', required=False, default='')
    parser.add_argument('--serial-number', type=str, help='serial number', required=False, default='')
    parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards',
                        required=False, default=board_id)
    parser.add_argument('--file', type=str, help='file', required=False, default='')
    parser.add_argument('--master-board', type=int, help='master board id for streaming and playback boards',
                        required=False, default=board_id)

    args = parser.parse_args()

    params = BrainFlowInputParams()
    params.ip_port = args.ip_port
    params.serial_port = args.serial_port
    params.mac_address = args.mac_address
    params.other_info = args.other_info
    params.serial_number = args.serial_number
    params.ip_address = args.ip_address
    params.ip_protocol = args.ip_protocol
    params.timeout = args.timeout
    params.file = args.file
    params.master_board = args.master_board

    board = BoardShim(args.board_id, params)
    sampling_rate = board.get_sampling_rate(args.board_id)
    eeg_channels = board.get_eeg_channels(args.board_id)
    board.prepare_session()
    board.start_stream()
    time.sleep(3)

    while True:

        data = board.get_current_board_data(256) # get latest 256 packages or less, doesnt remove them from internal buffer

        eeg = data[eeg_channels]

        print(eeg)

        DataFilter.perform_bandpass(eeg[1], sampling_rate, 3.0, 45.0, 2,
                                    FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)

        # DataFilter.perform_bandstop(data[channel], sampling_rate, 48.0, 52.0, 2,
        #                             FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
        # DataFilter.perform_bandstop(data[channel], sampling_rate, 58.0, 62.0, 2,
        #                             FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
        print(eeg)

        with open('emg.csv', 'ab') as f:
            # Use NumPy to save the new data to the file
            np.savetxt(f, eeg, delimiter=',', fmt='%f')

if __name__ == "__main__":
    main()