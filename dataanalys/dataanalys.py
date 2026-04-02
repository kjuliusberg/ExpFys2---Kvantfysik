import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

file_Na = pd.read_csv('dataanalys/mätningar/Natrium_FULL_SPEKTRA.csv', sep=';')
file_Na_peaks_1 = pd.read_csv('dataanalys/mätningar/Natrium_FULL_Spectra_v2.csv', sep = ';')
file_Na_peaks_2 = pd.read_csv('dataanalys/mätningar/Natrium_TEST_v2-2.csv', sep = ';')
file_Na_peaks_3 = pd.read_csv('dataanalys/mätningar/Natrium_TEST_v2-3.csv', sep = ';')
file_H1 = pd.read_csv('dataanalys/mätningar/Väte_mätning_1.csv', sep = ';')
file_H2 = pd.read_csv('dataanalys/mätningar/Väte_mätning_2.csv', sep = ';')
file_H3 = pd.read_csv('dataanalys/mätningar/Väte_mätning_3.csv', sep = ';')

files = [file_Na, file_Na_peaks_1, file_Na_peaks_3, file_H1, file_H2, file_H3]

for file in files:
    file['Intensity'] = file['Intensity'].str.replace(',', '.').astype(float)
    file['Wavelenght'] = file['Wavelenght'].str.replace(',', '.').astype(float)


R = 1.097e-2

# Find peaks, and plot spectra for ONE file
def spectra(file, plot=True):
    wavelenghts = np.array(file['Wavelenght'].values)
    intensities = np.array(file['Intensity'].values)

    peaks = find_peaks(intensities, height=0.01, prominence=0.01)[0]
    intensity_peaks = intensities[peaks]
    wavelenghts_peaks = wavelenghts[peaks]
    print(len(peaks))
    fig, ax = plt.subplots()

    plt.plot(wavelenghts, intensities)
    plt.scatter(wavelenghts_peaks, intensity_peaks, color = 'r')
    plt.xlabel('Wavelength [nm]')
    plt.ylabel('Intensity')
    plt.title('Na')
    if plot == True:
        plt.show()

    return np.sort(wavelenghts_peaks)

# Plot NA-spectra
#Na_peaks = spectra(files[0])
Na_peaks = spectra(files[1])
#Na_dpeaks_3 = spectra(files[3])

H_peaks_teo = []
    
for n1 in range(1, 4):
    for n2 in range(n1+1, 15):
        inv_lambda = R * (1/n1**2 - 1/n2**2)
            
        if inv_lambda > 0:
            lam = 1 / inv_lambda
            if 200<lam<1100:    
                H_peaks_teo.append({
                    "n1": n1,
                    "n2": n2,
                    "lambda": lam
                    })

# for i in H_peaks_teo:
#     print(i['lambda'])

def match_lines(measured, transitions, tol=0.005):
    matches = []
    
    for lam_meas in measured:
        best = None
        best_error = np.inf
        
        for t in transitions:
            lam_theory = t["lambda"]
            
            error = abs(lam_meas - lam_theory) / lam_theory
            
            if error < best_error:
                best_error = error
                best = t
        
        if best_error < tol:
            matches.append({
                "measured_nm": lam_meas,
                "n1": best["n1"],
                "n2": best["n2"],
                "theory_nm": best["lambda"],
                "rel_error": best_error
            })
        else:
            matches.append({
                "measured_nm": lam_meas,
                "n1": None,
                "n2": None,
                "theory_nm": None,
                "rel_error": None
            })
    
    return pd.DataFrame(matches)


# H_peaks = []
# for file in files[4:]:
#     H_peaks.append(spectra(file))

# H_peaks = np.array(H_peaks)
# H_peaks_mean = np.mean(H_peaks, axis=0)

# result = match_lines(H_peaks_mean, H_peaks_teo)
# print(result)

def average(files, plot = True):

    wavelenghts = []
    intensities = []
    for file in files:    
        waves = file['Wavelenght']
        ints = file['Intensity']
        wavelenghts.append(waves)
        intensities.append(ints)

    intensities_mean = np.mean(np.array(intensities),axis=0)
    wavelenghts_mean = np.mean(np.array(wavelenghts),axis=0)
    ints_std = np.std(intensities, axis=0)
    peaks = find_peaks(intensities_mean, prominence=0.003, distance=2)[0]
    intensity_peaks = intensities_mean[peaks]
    wavelenghts_peaks = wavelenghts_mean[peaks]
    fig, ax = plt.subplots()

    plt.plot(wavelenghts_mean, intensities_mean)
    plt.scatter(wavelenghts_peaks, intensity_peaks, color = 'r')
    plt.xlabel('Wavelength [nm]')
    plt.ylabel('Intensity')
    plt.title('Hydrogen')
    if plot == True:
        plt.show()
    return wavelenghts_peaks

H_peaks = average(files[4:])
result = match_lines(H_peaks, H_peaks_teo)
print(result)
# spectra(file_H2)