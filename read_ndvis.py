import os
import re
from osgeo import gdal
import datetime

def is_valid_date(year, month, day):
    try:
        # Try to create a date object from the components
        datetime.date(year, month, day)
        return True
    except ValueError:
        return False

def read_ndvi_data(ndvis_dir):
    """
    Read NDVI data from folders with names "NDVI_year_month_day" using GDAL.

    Args:
        ndvis_dir (str): Path to the directory of the NDVI files.

    Returns:
        dict: A dictionary with dates as keys and NDVI arrays as values, sorted by date.
    """
    ndvi_data_dict = {}
    resolutions = set()  # Store the unique NDVI resolutions

    try:
        for file in os.listdir(ndvis_dir):
            file_path = os.path.join(ndvis_dir, file)
            if os.path.isfile(file_path):
                # Check if the file name matches the expected pattern
                match = re.match(r'^NDVI_(\d{4})_(\d{2})_(\d{2})\.tif$', file)
                if match:
                    year, month, day = map(int, match.groups())
                    if is_valid_date(year, month, day):
                        # Open the NDVI file using GDAL
                        dataset = gdal.Open(file_path, gdal.GA_ReadOnly)
                        if dataset is not None:
                            # Get the resolution of the current image
                            current_resolution = (dataset.RasterXSize, dataset.RasterYSize)
                            resolutions.add(current_resolution)

                            # Read the image data into a NumPy array
                            ndvi_array = dataset.ReadAsArray()

                            # Close the dataset to free up resources
                            dataset = None

                            # Create a datetime object for sorting
                            date_obj = datetime.date(year, month, day)

                            # Add the data to the dictionary with date as key
                            ndvi_data_dict[date_obj] = ndvi_array
                        else:
                            print(f"Could not open file: {file_path}")
                    else:
                        print(f"Ignoring file with invalid date: {file}")
                else:
                    print(f"Ignoring file with invalid format: {file_path}")

        if not ndvi_data_dict:
            raise Exception("No valid NDVI files found in the directory")

        if len(resolutions) != 1:
            raise Exception("Not all images have the same resolution")

        # Sort the dictionary by dates
        sorted_ndvi_data = dict(sorted(ndvi_data_dict.items()))

        # Check if there are at least 6 entries in the dictionary
        if len(sorted_ndvi_data) < 6:
            raise Exception("Phenology Metrics needs at least 6 NDVIS to be executed!")
        else:
            print(str(len(sorted_ndvi_data)) + " NDVIs have been read")

        return sorted_ndvi_data

    except Exception as e:
        raise Exception(f"Error reading NDVI data: {str(e)}")
