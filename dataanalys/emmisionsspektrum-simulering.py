import numpy as np
import matplotlib.pyplot as plt

wavelengths = np.linspace(300, 800, 1000)

noise = np.random.normal(1,0.2,len(wavelengths))
cents = np.array([450, 600, 720])
ints = np.array([10, 6, 8])
sigma = 2

peaks = np.zeros_like(wavelengths)
for i in range(len(cents)):
    peaks += ints[i]*np.e**((-(wavelengths-cents[i])**2)/(2*sigma**2))

intensity = noise + peaks
plt.style.use('ggplot')

fig, ax = plt.subplots()
plt.plot(wavelengths, intensity)
plt.xlabel('Våglängd [nm]')
plt.ylabel('Intensitet [arb.]')

plt.savefig('Exempel_emissionsspektra.png')