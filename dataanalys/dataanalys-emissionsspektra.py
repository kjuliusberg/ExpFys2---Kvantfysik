import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks



# importera alla filer
file_NA = pd.read_csv('dataanalys/mätningar/Natrium_Full_Spectra_v2.csv', sep=';')
file_H1 = pd.read_csv('dataanalys/mätningar/Väte_mätning_1.csv', sep=';')
file_H2 = pd.read_csv('dataanalys/mätningar/Väte_mätning_2.csv', sep=';')
file_H3 = pd.read_csv('dataanalys/mätningar/Väte_mätning_3.csv', sep=';')

files = [file_NA, file_H1, file_H2, file_H3]

# Fixa decimal format
for file in files:
    file['Intensity'] = file['Intensity'].str.replace(',', '.').astype(float)
    file['Wavelenght'] = file['Wavelenght'].str.replace(',', '.').astype(float)

# NATRIUM
# Variabler för att hitta toppar
prominence_NA = 0.008
distance_NA = 10

wavelengths_NA = file_NA['Wavelenght'].values
intensities_NA = file_NA['Intensity'].values

# Hitta toppar
peaks_NA, props = find_peaks(intensities_NA, prominence=prominence_NA, distance=distance_NA)

H1_wave_peaks = wavelengths_NA[peaks_NA]
H1_ints_peaks = intensities_NA[peaks_NA]

# Plotta spektra med toppar markerade
plt.figure()
plt.plot(wavelengths_NA, intensities_NA)
plt.scatter(wavelengths_NA[peaks_NA], intensities_NA[peaks_NA], color='red')
plt.xlabel('Våglängd [nm]')
plt.ylabel('Intensitet [arb.]')
plt.title('Emissionsspektra-Natrium')
#plt.savefig('NA_spectra.png')

# Zooma in på dubbeltopp
na_min = np.where(wavelengths_NA.astype(int) == 585)[0][0]
na_max = np.where(wavelengths_NA.astype(int) == 595)[0][0]

plt.figure()
plt.plot(wavelengths_NA[na_min:na_max], intensities_NA[na_min:na_max])
#plt.scatter(wavelengths_NA[peaks_NA], intensities_NA[peaks_NA], color='red')
plt.xlabel('Våglängd [nm]')
plt.ylabel('Intensitet [arb.]')
plt.title('Emissionsspektra-Natrium')
#plt.savefig('NA_spectra_doublepeaks.png')

# VÄTE - FIL 1
prominence_H1 = 0.008
distance_H1 = 10

wavelengths_H1 = file_H1['Wavelenght'].values
intensities_H1 = file_H1['Intensity'].values

# Hitta toppar
peaks_H1, props = find_peaks(intensities_H1, prominence=prominence_H1, distance=distance_H1)

H1_wave_peaks = wavelengths_H1[peaks_H1]
H1_ints_peaks = intensities_H1[peaks_H1]

# Plotta spektra med toppar markerade
plt.figure()
plt.plot(wavelengths_H1, intensities_H1)
plt.scatter(wavelengths_H1[peaks_H1], intensities_H1[peaks_H1], color='red')
plt.xlabel('Våglängd [nm]')
plt.ylabel('Intensitet [arb.]')
plt.title('Väte-spektra')
#plt.savefig('H1-spektra.png')

# VÄTE - FIL 2 Identisk med fil 1
prominence_H2 = 0.008
distance_H2 = 10

wavelengths_H2 = file_H2['Wavelenght'].values
intensities_H2 = file_H2['Intensity'].values

peaks_H2, props = find_peaks(intensities_H2, prominence=prominence_H2, distance=distance_H2)

H2_wave_peaks = wavelengths_H2[peaks_H2]
H2_ints_peaks = intensities_H2[peaks_H2]

plt.figure()
plt.plot(wavelengths_H2, intensities_H2)
plt.scatter(wavelengths_H2[peaks_H2], intensities_H2[peaks_H2], color='red')
plt.xlabel('Våglängd [nm]')
plt.ylabel('Intensitet [arb.]')
plt.title('H2-spektra')
#plt.savefig('H2-spektra.png')

# VÄTE - FIL 3 Identisk med fil 1 och 2
prominence_H3 = 0.008
distance_H3 = 10

wavelengths_H3 = file_H3['Wavelenght'].values
intensities_H3 = file_H3['Intensity'].values

peaks_H3, props = find_peaks(intensities_H3, prominence=prominence_H3, distance=distance_H3)

H3_wave_peaks = wavelengths_H3[peaks_H3]
H3_ints_peaks = intensities_H3[peaks_H3]

plt.figure()
plt.plot(wavelengths_H3, intensities_H3)
plt.scatter(wavelengths_H3[peaks_H3], intensities_H3[peaks_H3], color='red')
plt.xlabel('Våglängd [nm]')
plt.ylabel('Intensitet [arb.]')
plt.title('H3-spektra')
#plt.savefig('H3-spektra.png')


# Medelvärdera toppar och intensiteter
all_peaks = np.array([H1_wave_peaks, H2_wave_peaks, H3_wave_peaks])
all_ints = np.array([H1_ints_peaks, H2_ints_peaks, H3_ints_peaks])

average_peaks = np.mean(all_peaks, axis=0)
average_ints = np.mean(all_ints, axis=0)

# Hitta standardavvikelse
std_peaks = np.std(all_peaks, axis=0, ddof=1)
std_ints = np.std(all_ints, axis=0)

# Ta fram medelfelet av medelvärdet
sem_peaks = std_peaks / np.sqrt(3)

# Kombinera osäkerheter
instrument_uncert = 0.05 # step-size
total_uncert = np.sqrt(sem_peaks**2 + instrument_uncert**2)

wavelengths = np.mean([wavelengths_H1, wavelengths_H2, wavelengths_H3], axis=0)
intensities = np.mean([intensities_H1, intensities_H2, intensities_H3], axis=0)

# Plotta medelvärderat spektra
plt.figure()
plt.plot(wavelengths, intensities)
plt.scatter(average_peaks, average_ints, color='red')
plt.xlabel('Våglängd [nm]')
plt.ylabel('Intensitet [arb.]')
plt.title('Medelvärderat spektra')
#plt.savefig('Medelvärderat_spektra.png')


# Normalize intensities
peak_ints = np.log10(average_ints + 1e-6)
peak_ints = peak_ints - peak_ints.min()
peak_ints = peak_ints / peak_ints.max()

# Matcha våglängd till färg
def wavelength_to_rgb(wavelength):
    
    if wavelength < 380:  # UV
        return (0.3, 0.0, 0.5)  # dim purple
    
    elif wavelength > 780:  # IR
        return (0.5, 0.0, 0.0)  # dim red
    
    # Visible spectrum
    if 380 <= wavelength <= 440:
        r, g, b = -(wavelength - 440) / (440 - 380), 0.0, 1.0
    elif 440 < wavelength <= 490:
        r, g, b = 0.0, (wavelength - 440) / (490 - 440), 1.0
    elif 490 < wavelength <= 510:
        r, g, b = 0.0, 1.0, -(wavelength - 510) / (510 - 490)
    elif 510 < wavelength <= 580:
        r, g, b = (wavelength - 510) / (580 - 510), 1.0, 0.0
    elif 580 < wavelength <= 645:
        r, g, b = 1.0, -(wavelength - 645) / (645 - 580), 0.0
    else:  # 645–780
        r, g, b = 1.0, 0.0, 0.0

    return (r, g, b)

# Plotta linjespektra
plt.figure(figsize=(12, 2))
plt.xlim(200, 1100)
plt.ylim(0, 1)

for wl, inten in zip(average_peaks, peak_ints):
    color = wavelength_to_rgb(wl)
    plt.vlines(wl, 0, 1, colors=[color], alpha=inten, linewidth=2)

plt.gca().set_facecolor("black")
plt.xticks([200, 400, 600, 800, 1000])
plt.xlabel('Våglängd [nm]')
plt.yticks([])
plt.title("Emissionsspektra")

#plt.savefig('Emissionsspektra-colorfull.png')

# Beräkna teoretiska emissionslinjer för väte
R = 1.097e-2

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

# Kolla om mätta toppar matchar teoretiska linjer inom osäkerhet
def match_lines(measured, transitions, total_uncert, tol=0.005):
    matches = []
    
    for lam_meas, uncert in zip(measured, total_uncert):
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
                "uncertainty_nm": uncert,
                "n1": best["n1"],
                "n2": best["n2"],
                "theory_nm": best["lambda"],
                "rel_error": best_error
            })
        else:
            matches.append({
                "measured_nm": lam_meas,
                "uncertainty_nm": uncert,
                "n1": None,
                "n2": None,
                "theory_nm": None,
                "rel_error": None
            })
    
    return pd.DataFrame(matches)


matches = match_lines(average_peaks, H_peaks_teo, total_uncert)
print(matches)