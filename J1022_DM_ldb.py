import numpy as np
import matplotlib.pyplot as plt

# Load data from dm_lookup.txt
lookup = np.genfromtxt('dm_lookup.txt', names=True, delimiter='\t')

# Load data from final.txt
#final = np.genfromtxt('final.txt', delimiter='\t')

# Load data from J1022_allDM.txt
final = np.genfromtxt('allDM.txt', delimiter='\t')

# Validate the shape of final
print("Shape of final array:", final.shape)

# Extract columns
x_values = final[:, 4]  # Column 1
y_values = final[:, 3]  # Column 2
y_errors = final[:, 2]  # Column 3

# Separate values based on condition
x_positive = x_values[y_values >= 0]
y_positive = y_values[y_values >= 0]
yerr_positive = y_errors[y_values >= 0]

x_negative = x_values[y_values < 0]
y_negative = y_values[y_values < 0]
yerr_negative = y_errors[y_values < 0]

# Create the plot
fig, ax = plt.subplots(figsize=(9, 5), dpi=180)

# Plot data from dm_lookup.txt
my_elongation = np.linspace(0.3, 6, 100)
ax.plot(my_elongation, np.interp(my_elongation, lookup['elongation'], lookup['dm_ldb']), color='black', label='LDB model')
ax.plot(my_elongation, np.interp(my_elongation, lookup['elongation'], 4 * lookup['dm_ldb']), color='orange', label='Ontiveros&Vourlidas (2009) CME enhancement', ls='--')

# Overplot data from final.txt (column 4 vs column 3)
#ax.scatter(final['solar_elongation'], final['DM_sol'], color='green', label='DM_sol', s=20)  # Adjust `s` for point size
#ax.scatter(final[:, 4], final[:, 3], color='green', label='Final Data', s=20)  # Column 3 is index 2, Column 4 is index 3

#ax.scatter(final[:, 4], final[:, 3], color='green', label='Final Data', s=20)  # Column 3 is index 2, Column 4 is index 3
#ax.errorbar(final[:, 4], final[:, 3], final[:, 2], fmt='.', color='green', label='DM_sol_err')

# Plot positive and negative values with different colors
ax.errorbar(x_positive, y_positive, yerr=yerr_positive, fmt='.', color='blue', label='Positive Values')
ax.errorbar(x_negative, y_negative, yerr=yerr_negative, fmt='.', color='red', label='Negative Values')

# Set x-axis limits from 0 to 6
ax.set_xlim(0, 6)

# Add labels, grid, and legend
ax.set_xlabel("solar elongation / deg")
ax.set_ylabel(r"Heliosphere $\Delta$DM / pc cm$^{-3}$")
ax.grid()
ax.legend()

# Show the plot
#plt.show()

fig.savefig("J1022_alldm+model_clr.png", dpi=300)
print("Figure saved: J1022_alldm+model_clr.png")
