from filefifo import Filefifo

sample_rate = 1000
signal_fre = 250

#put data into list 
test_signal = []
data = Filefifo(10000, name = '/sample_data/capture_250Hz_01.txt')
for a in range(10000):
    test_signal.append(data.get())

print(f"Test Signal: \n{"," .join(map(str, test_signal[:5]))} ... {"," .join(map(str, test_signal[-5:]))}")

# find peaks store into peaks list
peaks = []
for i in range(1, len(test_signal) - 1):
    if (test_signal[i] - test_signal[i - 1]) > 0 and (test_signal[i + 1] - test_signal[i]) <= 0:
        peaks.append(i)
print(f"Find {len(peaks)} Peaks:\n{"," .join(map(str, peaks))}")       

if len(peaks) >= 2:
    # Calculate intervals between consecutive peaks
    interval_samples = [peaks[j+1] - peaks[j] for j in range (len(peaks) - 1)]
    # Convert to time intervals
    interval_seconds = [interval/sample_rate for interval in interval_samples]
    # Calculate instantaneous frequencies
    frequency = [1 / interval for interval in interval_seconds]
    
    print ("signal frequency:\n", signal_fre, "\n")
    #interval
    print (f"Total intervals: {len(interval_samples)}")
    for i, (samples,secs) in enumerate (zip(interval_samples[:10], interval_seconds[:10])):
        print(f"{i + 1}: {samples} samples ({secs:.3f}sec) ⇒ {1/secs:.2f}Hz")
    print (f"...")
    
    # Calculate statistics
    avg_interval = sum(interval_samples)/len(interval_samples)
    avg_frequency = 1/(avg_interval/sample_rate)
    print(f"\nAdditional information:")
    print(f"Average frequency: {avg_frequency:.2f} Hz")
    print(f"Minimum interval: {min(interval_samples)} samples")
    print(f"Maximum interval: {max(interval_samples)} samples")
else:
    print("Not enough peaks detected for frequency calculation!")
    
