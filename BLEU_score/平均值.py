# Given data (2 rows, 3 columns)
row1 = [0.446171248, 0.524918522, 0.542062096]
row2 = [0.216239407, 0.206510725, 0.256216202]

# Calculate column-wise averages
col1_avg = (row1[0] + row2[0]) / 2  # (0.446171248 + 0.216239407) / 2
col2_avg = (row1[1] + row2[1]) / 2  # (0.524918522 + 0.206510725) / 2
col3_avg = (row1[2] + row2[2]) / 2  # (0.542062096 + 0.256216202) / 2

print("Column 1 average:", col1_avg)  # ≈ 0.3312053275
print("Column 2 average:", col2_avg)  # ≈ 0.3657146235
print("Column 3 average:", col3_avg)  # ≈ 0.3991391490