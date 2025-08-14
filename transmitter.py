import numpy as np
import sounddevice as sd
import time
fs = 48000
duration = 0.01
pause_duration = 0.1

f0 = 18200
f1 = 18400
f2 = 18000

text = "l'aigle est dans le nid"
sequence = ""
for char in text:
    sequence += f"{bin(ord(char))[2:].zfill(8)} "
sequence += " "
print(sequence)
#sequence = "01000011 01100101 01100011 01101001 00100000 01100101 01110011 01110100 00100000 01010101 01001110 00100000 01101101 01100101 01110011 01110011 01100001 01100111 01100101 00100000 01110001 01110101 01101001 00100000 01100100 01101111 01101001 01110100 00100000 01100001 01100010 01110011 01101111 01101100 01110101 01101101 01100101 01101110 01110100 00100000 01110100 01101111 01110010 01110100 01110101 01110010 01100101 01110010 00100000 01101100 01100101 01110011 00100000 01101111 01110010 01100101 01101001 01101100 01101100 01100101 01110011 00100000 01100100 01100101 01110011 00100000 01100011 01101000 01101001 01100101 01101110 01110011 00100000 01110000 01100001 01110011 01110011 01100001 01101110 01110100 01110011 00101110 00101110 00101110 "

time.sleep(0)
signal = np.array([])
t = np.linspace(0, duration, int(fs * duration), endpoint=False)
pause_t = t = np.linspace(0, pause_duration, int(fs * pause_duration), endpoint=False)

paused_sequence = ""
for i in range(len(sequence) - 2):
    paused_sequence += sequence[i]
    if(sequence[i+1] == sequence[i] or (sequence[i + 1] == " " and sequence[i] == sequence[i + 2])):
        paused_sequence += "2"
print(paused_sequence)
for bit in paused_sequence:
    if bit == " ":
        continue
    if bit == "0":
        wave = np.sin(2 * np.pi * f0 * t)
    if bit == "1":
        wave = np.sin(2 * np.pi * f1 * t)
    if bit == "2":
        wave = np.sin(2 * np.pi * f2 * pause_t)

    #signal = np.concatenate((signal, wave, pause))  # ajout du silence après chaque bit
    signal = np.concatenate((signal, wave))

signal = signal * (2**15 - 1) / np.max(np.abs(signal))
signal = signal.astype(np.int16)

sd.play(signal, fs)
sd.wait()
