import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


upper_lim = -2.0  #[-5.0, -4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0]  # found that upper limit 10 and lower 0 has higher counts as we increase lower limit and higher the counts decrease
# upper lim -2.0 lower = -12.0, got me even higher counts so that means that ch1 is 10 naco secs behind ch0

#for i in range(len(upper_lim)):
lower_lim = upper_lim - 10.0

print('upper_lim:',upper_lim)
print('lower_lim:',lower_lim)

if upper_lim - lower_lim > 0:
    print('ch1 is behind ch0 by:', np.linalg.norm(upper_lim), 'nano sec')
else:
    print('ch0 is behind ch1 by:', np.linalg.norm(lower_lim), 'nano sec')

lower_range = 99
upper_range = 100

r = {'#NAME?'}

def cc_timstamps(tim1, tim0, lower_lim, upper_lim):
    time_set = set()

    for i in range(len(tim1)):
        time_set.update(
            timestamp
            for j in range(len(tim0))
            if lower_lim <= (timestamp := tim1[i] - tim0[j]) < upper_lim
        )

    return list(time_set)

def remove_certain_strings(original_list, strings_to_remove):
    filtered_test = [item for item in original_list if item not in strings_to_remove]
    new_filtered_test = [float(i) for i in filtered_test]
    return new_filtered_test

def cc_finder(tim1, tim0, lower_lim, upper_lim):
    cc_set = set()
    
    for i in range(len(tim1)):
        for j in range(min(len(tim0), i + lower_range), max(0, i - upper_range), -1):
            if lower_lim <= tim1[i] - tim0[j] < upper_lim:
                cc_set.add(tim1[i])

    return list(cc_set)

df = pd.read_csv('/Users/brettbamfo/Desktop/Unfiltered_Data.csv')

timetag1test_o = df["TIMETAG1_nano sec"].tolist()
timetag0test_o = df["TIMETAG0_nano sec"].tolist()
energy1test_o = df["ENERGY_1"].tolist()

print("Python is running this code (Got lists from excel).")

# Use sets for faster membership checks

timetag1test = remove_certain_strings(timetag1test_o, r)
timetag0test = remove_certain_strings(timetag0test_o, r)
energy1test = remove_certain_strings(energy1test_o, r)

print(len(timetag1test))
print(len(energy1test))

#print("\nPython is running this code (took out the #NAME?).")

# Use NumPy for numeric operations
cc = cc_finder(timetag1test, timetag0test, lower_lim, upper_lim)

# Find corresponding elements in energy1test and timetag1test
corresponding_elements = [(elem1, elem3) for elem1, elem3 in zip(timetag1test, energy1test) if elem1 in cc]

# Separate the corresponding elements back into timetag1test and energy1test
cc_new, energy1test = zip(*corresponding_elements)
energy1test = list(energy1test)
cc_new = list(cc_new)

# Print the results
print('\n# of cc:', len(cc_new))
print("This is the cc in order from", lower_lim, "to",  upper_lim,":\n", cc_new)

print("Corresponding energy values for cc:\n", energy1test)

baby_girl = []
for i in range(len(energy1test)):
    b = (energy1test[i] * 300.6) / 10**6
    baby_girl.append(b)

plt.figure(figsize=(10,6))
plt.scatter(baby_girl, cc_new, color='#F5CB26', edgecolor='black', marker='o')
#plt.scatter(energy1test, cc_new, color='skyblue', edgecolor='black', marker='o')
plt.xlabel('Energy (MeV)')
plt.ylabel('Time Tag (Nano Sec)')
plt.title('Time Tag vs Energy')
plt.legend()
plt.show()

hist, edges = np.histogram(baby_girl, bins=50)
#hist, edges = np.histogram(energy1test, bins = 50)
#print('This is max counts between 1600 and 1800:', hist[33])
total_counts = np.sum(hist)

plt.figure(figsize=(10,6))
plt.bar(edges[:-1], hist, width=edges[1] - edges[0], color='#F5CB26', edgecolor='black')
plt.xlabel('Energy (MeV)')
plt.ylabel('# of cc counts')
plt.title('Histogram: # of cc counts vs Energy')
plt.show()