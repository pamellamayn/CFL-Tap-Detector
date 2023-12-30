# -*- coding: utf-8 -*-
"""

@author: pam
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
import os

def load_data(file_path, timestamp_header):
    """
    Load data from a file.

    Parameters:
    - file_path: Path to the data file.
    - timestamp_header: The column header for timestamps.

    Returns:
    - timestamps: Numpy array of timestamps.
    - data: Numpy array of all data columns.
    """
    data = pd.read_csv(file_path)
    timestamps = data[timestamp_header].to_numpy()
    data_values = data.drop(columns=[timestamp_header]).to_numpy()

    return timestamps, data_values

# TODO: have an additional parameter that takes the data from the specific data column name that was called

def extract_data(file_dir, file_base_names, timestamp_id, time_window=[0, 50000]):
    """
    Extract and organize data from multiple files.

    Parameters:
    - file_dir: Base directory of the parsed data files.
    - file_base_names: Array of file bases of the data files.
    - timestamp_id: Timestamp identifier to use for timestamps.
    - time_window: Window (in secs) from the beginning of the file to look for taps.

    Returns:
    - data_array: Structured array containing organized data.
    """
    data_array = []

    for file_base in file_base_names:
        file_path = os.path.join(file_dir, f"{file_base}.csv")
        timestamps, data_values = load_data(file_path, timestamp_id)

        # Create time segment
        timestamps_rel = timestamps - timestamps[0]
        time_mask = np.where((timestamps_rel > time_window[0]) & (timestamps_rel < time_window[1]))

        # Extract data within the time window
        data_window = data_values[time_mask]

        data_array.append((file_base, timestamps_rel[time_mask], data_window))

    return np.array(data_array, dtype=[('FileName', 'U50'), ('RelativeTimestamp', 'f8'), ('Data', 'f8', data_window.shape[1])])

