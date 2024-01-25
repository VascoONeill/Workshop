import pandas as pd
from src.features import camara as cm
from src.features import animation as ani
from src.data import data_processor as pr

"Cleaning Data"
data = pd.read_csv('C:/Users/PC/PycharmProjects/Workshop/src/data/samples.csv')
ecg = data.drop(0, axis=0).drop("'Elapsed time'", axis=1)
ecg["'ECG'"] = pd.to_numeric(ecg["'ECG'"])

"Processing Data"
signal = pr.data_process(ecg)

"Signal Graphic"
ani.graphic(signal)
