import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# Since we have the data in a text format, we can directly create a dataframe and plot the data.

# # Data as provided in the text format above
# # data = {
# #     "Nom de dataset": [3960, 4950, 9900, 19800, 29700, 39600, 49500, 99000],
# #     "RH": [2202.0, 1037.0, 93.0, 34.0, 14.0, 11.0, 7.0, 2.0],
# #     "4 CPUs": [2034.0, 903.0, 119.0, 39.0, 14.0, 12.0, 8.0, 6.0],
# #     "6 CPUs": [4033.0, 1705.0, 137.0, 31.0, 14.0, 12.0, 'N/A', 3.0],
# #     "8 CPUs": [3968.0, 1703.0, 144.0, 33.0, 38.0, 12.0, 9.0, 3.0]
# # }

data1 = {
    "Connect": [2077, 2237, 2397, 2557],
    "RH": [171345, 9852, 974, 113],
    "4 CPUs": [171658, 10125, 849, 148],
    "6 CPUs": [181952, 10007, 926, 161],
    "8 CPUs": [178444, 11022, 959, 158]
}


# Create a DataFrame
df = pd.DataFrame(data1)

# Handle the 'N/A' value by converting it to a NaN
df = df.replace('N/A', np.nan)

# Convert all numerical values to floats for plotting
df["6 CPUs"] = pd.to_numeric(df["6 CPUs"], errors='coerce')
df["8 CPUs"] = pd.to_numeric(df["8 CPUs"], errors='coerce')
# Now let's plot the data
plt.figure(figsize=(12, 6))
for column in df.columns[1:]:
    plt.plot(df['Connect'].astype(str), df[column], '-o', label=column)

# Beautify the plot
plt.title('Temps de réponse pour différents CPUs')
plt.xlabel('Chess')
plt.ylabel('Temps (ms)')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()  # Adjust layout to make room for the rotated x-axis labels

# Show the plot
plt.show()


# # Re-importing necessary libraries since the execution state was reset
# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np

# # Re-defining the data
# data1 = {
#     "Connect": [40534, 43912, 47290, 50668, 54045],
#     "RH": [357233, 112281, 38308, 14432, 2382],
#     "4 CPUs": [517513, 156386, 64491, 17383, 2840],
#     "6 CPUs": [516468, 192349, 57925, 21453, 6019],
#     "8 CPUs": [378019, 165651, 57182, 23245, 6521]
# }

# # Create a DataFrame
# df = pd.DataFrame(data1)

# # Plotting the data without using scientific notation (e.g., not using 1e6 for large numbers)

# # Set the plot style for better readability
# plt.style.use('ggplot')

# # Create the plot
# plt.figure(figsize=(12, 6))

# # Plot each column
# for column in df.columns[1:]:
#     plt.plot(df['Connect'], df[column], '-o', label=column)

# # Customize the plot
# plt.title('Response Time for Different CPU Configurations')
# plt.xlabel('Connect')
# plt.ylabel('Time (ms)')
# plt.legend()
# plt.grid(True)

# # Adjust the y-axis format to show large numbers without scientific notation
# plt.ticklabel_format(style='plain', axis='y')

# # Rotate x-axis labels for better readability
# plt.xticks(rotation=45)

# # Adjust the layout
# plt.tight_layout()

# # Show the plot
# plt.show()
