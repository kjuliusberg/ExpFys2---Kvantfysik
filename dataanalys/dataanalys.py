import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

file = pd.read_csv('dataanalys/mätningar/mätning', sep=';', delimiter=',')

wavelenghts = np.array(file['Wavelenght'])
intensities = np.array(file['Intensity'])

peaks = find_peaks(intensities)
intensity_peaks = intensities[peaks]

fig, ax = plt.subplots()

plt.plot(wavelenghts, intensities)
plt.scatter(wavelenghts, intensity_peaks, color = 'r')

plt.show()