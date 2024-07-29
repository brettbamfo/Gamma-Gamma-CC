import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import make_interp_spline


find_range = 10000.0
increment_counts = 10000
upper_lim = list(range(0, 1000001, increment_counts)) # this allows for range to be delay time to delay time + find_range, which will cover Ex. 200 - 205 as one point and so we know the cc at interval of delay time 200 to 205
lower_lim = 0.0 #Zero axis where delay = upper_lim, we can change for moved axis
#Lower_lim shifts points because it is the number delay where (-) means ch1 is behind ch0


delay = []
for i in range(len(upper_lim)):
    d = upper_lim[i] # upper_lim - lower_lim = upper_lim, where Lower=0
    delay.append(d)

print('Delay list:', delay)

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


total_cc = []

for g in range(len(delay)):
    current_delay = delay[g] - lower_lim
    current_upper_delay = current_delay + find_range
    
    print('This should be range:', current_upper_delay - current_delay)
    
    if upper_lim[g] > 0:
        print('\nch0 is behind ch1 by:', np.linalg.norm(current_delay), 'nano sec')
    elif upper_lim[g] == 0:
        print('\nch1 and ch0 have no delay at:', current_delay, 'nano sec')
    else:
        print('\nch1 is behind ch0 by:', np.linalg.norm(current_delay), 'nano sec')
    
    # Use NumPy for numeric operations
    cc = cc_finder(timetag1test, timetag0test, current_delay, current_upper_delay)
    #print('', len(cc))

    # Find corresponding elements in energy1test and timetag1test
    corresponding_elements = [(elem1, elem3) for elem1, elem3 in zip(timetag1test, energy1test) if elem1 in cc]
    
    if len(corresponding_elements) == 0:
        energy1test_new = [0] * len(cc)
        
    else:
    # Separate the corresponding elements back into timetag1test and energy1test
        cc_new, energy1test_new = zip(*corresponding_elements)
        energy1test_new = list(energy1test_new)
        
    hist, edges = np.histogram(energy1test_new, bins=100)
    total_counts = np.sum(hist)
    print('Total histogram counts:', total_counts)
    total_cc.append(total_counts)

print('Total counts list:', total_cc)

plt.figure(figsize=(10,6))
plt.plot(delay, total_cc, color='orange')
#plt.scatter(delay, total_cc, color='skyblue', edgecolor='black', marker='o')
plt.xlabel('Delay (nanosec)')
plt.ylabel('# of CC')
plt.title('# of CC vs Delay')
plt.legend()
plt.show()

peak_index = np.argmax(total_cc)
peak_value = max(total_cc)

print(f"The peak value is {peak_value} at x = {delay[peak_index]} to {(delay[peak_index]) + find_range}.")