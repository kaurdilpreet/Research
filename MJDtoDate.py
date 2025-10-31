from astropy.time import Time

# Open the file and read the data
file_path = "greentime_mjd.txt"  # Replace with the actual path to your .txt file

# Initialize a list to store the second column
column2_values = []

# Read the file
with open(file_path, "r") as file:
    for line in file:
        # Split each line by whitespace and extract the second column
        parts = line.split()
        if len(parts) > 1:  # Ensure the line has two columns
            column2_values.append(float(parts[1]))

# Perform element-wise addition to convert MJD to JD
jd = [value + 2400000.5 for value in column2_values]

# Convert to astropy Time object
t = Time(jd, format='jd')

# Convert to datetime and format output
utc = t.to_datetime()

# Print each datetime in the desired format
for dt in utc:
    print(dt.strftime("%Y-%m-%d %H:%M:%S.%f"))

