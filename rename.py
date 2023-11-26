import os
import datetime

# Specify the folder containing the files
folder_path = "C:/Users/lefkats_local/Desktop/phenology_python/data3"

# List all files in the folder
file_list = os.listdir(folder_path)

# Iterate through the files
for file_name in file_list:
    day = file_name[5:7]
    month = file_name[8:10]
    year = file_name[11:15]

    print(day, month, year)

    # Format the date in the desired format (NDVI_year_month_day)
    new_file_name = f"NDVI_{year}_{month}_{day}.tif"

    # Rename the file with the new name
    old_file_path = os.path.join(folder_path, file_name)
    new_file_path = os.path.join(folder_path, new_file_name)

    os.rename(old_file_path, new_file_path)