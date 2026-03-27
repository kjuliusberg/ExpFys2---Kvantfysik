import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

file_Na = pd.read_csv('dataanalys/mätningar/Natrium_FULL_SPEKTRA.csv', sep=';')
file_H1 = pd.read_csv('dataanalys/mätningar/Väte_mätning_1.csv', sep = ';')

files = [file_Na, file_H1]

R = 1.097e-2

def spectra(file, plot=True):
    file['Intensity'] = file['Intensity'].str.replace(',', '.').astype(float)
    file['Wavelenght'] = file['Wavelenght'].str.replace(',', '.').astype(float)

    wavelenghts = np.array(file['Wavelenght'].values)
    intensities = np.array(file['Intensity'].values)

    peaks = find_peaks(intensities, height=0.01, prominence=0.005*np.max(intensities))[0]
    intensity_peaks = intensities[peaks]
    wavelenghts_peaks = wavelenghts[peaks]

    fig, ax = plt.subplots()

    plt.plot(wavelenghts, intensities)
    plt.scatter(wavelenghts_peaks, intensity_peaks, color = 'r')
    if plot == True:
        plt.show()

    return np.sort(wavelenghts_peaks)

Na_peaks = spectra(files[0])

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


H_peaks = spectra(files[1])
what = match_lines(H_peaks, H_peaks_teo)

print(what)
