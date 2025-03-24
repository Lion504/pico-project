from filefifo import Filefifo

#put data into list 
test_signal = []
data = Filefifo(1000, name = '/sample_data/capture_250Hz_02.txt')
for a in range(1000):
    test_signal.append(data.get())
#Print original and scaled signals
print(f"Original Signal: \n{", " .join(map(str, test_signal[:10]))} ... {", " .join(map(str, test_signal[-10:]))} ... ")

#scale the value
max_value = max(test_signal)
min_value = min(test_signal)
scaled_signal = [(x - min_value) * 100 / (max_value - min_value) for x in test_signal]
#Print scaled signal
print("\nScaled Signal (0-100):")
scaled_start = ", ".join(["{:.2f}".format(x) for x in scaled_signal[:10]])
scaled_end = ", ".join(["{:.2f}".format(x) for x in scaled_signal[-10:]])
print(scaled_start + " ... " + scaled_end)

#print scaled values in plotter
for i in scaled_signal:
   print(f"{i:.2f}")