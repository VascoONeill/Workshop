import pandas as pd
import numpy as np
from scipy import signal


def smooth(sig, n):
    # Make an array containing only zeros and with length = length_of_signal + 2*n
    extremes_zeros = np.zeros(len(sig) + 2 * n)
    for i in range(len(sig)):
        if i < n:
            # mirror the start of signal
            extremes_zeros[i] = sig[n - i]
            # mirror the end of signal
            extremes_zeros[len(sig) + n + i] = sig[len(sig) - i - 2]
        # fill the remaining with the signal itself
        extremes_zeros[i + n] = sig[i]

    # Build the array
    smoothen_signal = np.zeros(len(sig))

    # Fill the array
    for i in range(n, len(extremes_zeros) - n):
        # Calculate the mean of the neighours - we have to look at the surrounding neighbours,
        # thus we divide the total by 2 look back and further
        mean_neighbours = np.mean(extremes_zeros[i - n // 2:i + n // 2])
        smoothen_signal[i - n] = mean_neighbours

    return smoothen_signal


def data_process(data):
    """Signal Processing for Synthesis"""
    "Normalise Data"
    mean_value = np.mean(data)  # Calculate the mean of the signal
    abs_signal = np.abs(data)  # Calculate the absolute of the signal
    max_abs_signal = np.max(abs_signal)  # Get the maximum value of the absolute signal
    normalised_signal = (data - mean_value) / max_abs_signal

    ecg_column = normalised_signal.iloc[:, 0]
    ecg_list_using_get = ecg_column.tolist()

    "Subsampling"
    sub_sample = signal.decimate(ecg_list_using_get, 5)

    "Denoise Signals"
    # Define n
    n = 3
    # Make an array containing only zeros and with length = length_of_signal + 2*n
    extremes_zeros = np.zeros(len(sub_sample) + 2 * n)

    for i in range(len(sub_sample)):
        if i < n:
            # mirror the start of signal
            extremes_zeros[i] = sub_sample[n - i]
            # mirror the end of signal
            extremes_zeros[len(sub_sample) + n + i] = sub_sample[len(sub_sample) - i - 2]
        # fill the remaining with the signal itself
        extremes_zeros[i + n] = sub_sample[i]

    smoothen_signal = np.zeros(len(sub_sample))

    # Fill the array
    for i in range(n, len(extremes_zeros) - n):
        # Calculate the mean of the neighours - we have to look at the surrounding neighbours,
        # thus we divide the total by 2 look back and further
        mean_neighbours = np.mean(extremes_zeros[i - n // 2:i + n // 2])
        smoothen_signal[i - n] = mean_neighbours

    "Remove Baseline Wander"
    baseline_wander = smooth(smoothen_signal, 40)
    filtered_signal = smoothen_signal - baseline_wander

    "Remove minimum"
    interval_signal = filtered_signal - min(filtered_signal)

    "Quantization"
    d = 1000

    scaled_signal = interval_signal * d
    rounded_signal = np.around(scaled_signal)

    quantised_signal = np.array(rounded_signal, dtype=int)

    "Dataframe transformation"
    df = pd.DataFrame(quantised_signal)

    return df
