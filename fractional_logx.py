import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Load Data
# -----------------------------
# Load model lookup table
lookup = np.genfromtxt('dm_lookup.txt', names=True, delimiter='\t')

# Load ΔDM measurements
final = np.genfromtxt('allDM.txt', delimiter='\t')

# Extract relevant columns
x_values = final[:, 4]   # solar elongation (deg)
y_values = final[:, 3]   # ΔDM (pc cm^-3)
y_errors = final[:, 2]   # ΔDM error

# -----------------------------
# Model Interpolation
# -----------------------------
my_elongation = np.linspace(0.3, 6, 200)
ldb_model = np.interp(my_elongation, lookup['elongation'], lookup['dm_ldb'])
cme_model = 4 * ldb_model  # CME enhancement (factor of 4)

# Interpolate LDB model at data x-values
ldb_interp = np.interp(x_values, lookup['elongation'], lookup['dm_ldb'])

# -----------------------------
# Fractional Deviation
# -----------------------------
frac_resid_ldb = (y_values - ldb_interp) / ldb_interp
frac_err = y_errors / np.abs(ldb_interp)  # simple error propagation

# -----------------------------
# Split positive/negative ΔDM for colors
# -----------------------------
x_positive = x_values[y_values >= 0]
y_positive = y_values[y_values >= 0]
yerr_positive = y_errors[y_values >= 0]

x_negative = x_values[y_values < 0]
y_negative = y_values[y_values < 0]
yerr_negative = y_errors[y_values < 0]

# -----------------------------
# Create Figure and Subplots
# -----------------------------
fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(9, 7), dpi=180, sharex=False,
    gridspec_kw={'height_ratios': [3, 1]}
)

# ---- TOP PANEL: ΔDM vs Solar Elongation (Linear X) ----
ax1.plot(my_elongation, ldb_model, color='black', label='LDB model')
ax1.plot(my_elongation, cme_model, color='orange', ls='--',
         label='Ontiveros & Vourlidas (2009) CME enhancement')

ax1.errorbar(x_positive, y_positive, yerr=yerr_positive, fmt='o', color='blue', label='Positive ΔDM')
ax1.errorbar(x_negative, y_negative, yerr=yerr_negative, fmt='o', color='red', label='Negative ΔDM')

ax1.set_xlim(0, 6)
ax1.set_ylabel(r"Heliosphere $\Delta$DM / pc cm$^{-3}$")
ax1.grid(True, alpha=0.4)
ax1.legend(fontsize=8)
ax1.set_title("ΔDM vs Solar Elongation and Fractional Deviation (log-scale bottom panel)")

# ---- BOTTOM PANEL: Fractional Deviation (Log X) ----
ax2.errorbar(x_values, frac_resid_ldb, yerr=frac_err, fmt='o', color='black', markersize=4,
             label='(Data - LDB)/LDB')
ax2.axhline(0, color='grey', lw=1)
ax2.axhline(3, color='orange', lw=1, ls='--', label='CME enhancement (+3)')

ax2.set_xscale('log')
ax2.set_xlim(0.3, 6)
ax2.set_xlabel("Solar elongation (deg)")
ax2.set_ylabel("Fract. dev")
ax2.grid(True, which='both', alpha=0.4)
ax2.legend(fontsize=8, loc='upper right')

plt.tight_layout()
fig.savefig("J1022_alldm_with_fractional_logx_only.png", dpi=300)
print("Figure saved: J1022_alldm_with_fractional_logx_only.png")

