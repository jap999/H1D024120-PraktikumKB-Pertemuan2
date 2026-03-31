import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl

# 1. Definisi Variabel Input (Antecedent) dan Output (Consequent)
suhu = ctrl.Antecedent(np.arange(0, 41, 1), 'suhu')
kelembapan = ctrl.Antecedent(np.arange(0, 101, 1), 'kelembapan')
kecepatan = ctrl.Consequent(np.arange(0, 101, 1), 'kecepatan')

# 2. Definisi Himpunan Fuzzy (Membership Function)
# Suhu: Dingin, Normal, Panas
suhu['dingin'] = fuzzy.trimf(suhu.universe, [0, 0, 20])
suhu['normal'] = fuzzy.trimf(suhu.universe, [15, 25, 35])
suhu['panas'] = fuzzy.smf(suhu.universe, 30, 40)

# Kelembapan: Kering, Lembap, Basah
kelembapan['kering'] = fuzzy.trimf(kelembapan.universe, [0, 0, 50])
kelembapan['lembap'] = fuzzy.trimf(kelembapan.universe, [30, 50, 70])
kelembapan['basah'] = fuzzy.trimf(kelembapan.universe, [60, 100, 100])

# Kecepatan Kipas: Lambat, Sedang, Cepat
kecepatan['lambat'] = fuzzy.trimf(kecepatan.universe, [0, 0, 50])
kecepatan['sedang'] = fuzzy.trimf(kecepatan.universe, [30, 50, 70])
kecepatan['cepat'] = fuzzy.trimf(kecepatan.universe, [60, 100, 100])

# 3. Definisi Aturan Fuzzy (Rules)
rule1 = ctrl.Rule(suhu['dingin'] | kelembapan['basah'], kecepatan['lambat'])
rule2 = ctrl.Rule(suhu['normal'], kecepatan['sedang'])
rule3 = ctrl.Rule(suhu['panas'] & kelembapan['kering'], kecepatan['cepat'])

# 4. Membuat Kontrol Sistem dan Simulasinya
kipas_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
simulasi_kipas = ctrl.ControlSystemSimulation(kipas_ctrl)

# 5. Input Kondisi Lingkungan (Contoh: Suhu 33 C dan Kelembapan 40%)
simulasi_kipas.input['suhu'] = 33
simulasi_kipas.input['kelembapan'] = 40

# 6. Menghitung Output (Compute)
simulasi_kipas.compute()

# 7. Output Hasil
print(f"Hasil Defuzzifikasi Kecepatan Kipas: {simulasi_kipas.output['kecepatan']:.2f}%")

# Menampilkan Grafik
suhu.view()
kelembapan.view()
kecepatan.view(sim=simulasi_kipas)

input("Tekan ENTER untuk menutup grafik...")

plt.show()

