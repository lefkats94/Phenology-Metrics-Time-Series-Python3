import os
import re
from osgeo import gdal
import datetime

class NDVIProcessor:
    def __init__(self, ndvis_dir):
        """
        Initialize the NDVIProcessor with the directory containing NDVI files.

        Args:
            ndvis_dir (str): Path to the directory of the NDVI files.
        """
        self.ndvis_dir = ndvis_dir
        self.ndvi_data_dict = {}
        self.resolutions = set()
    
    def get_metadata(self):
        """
        Retrieves metadata from an NDVI image.

        Parameters:
        - inputs_directory (str): The directory containing NDVI images.

        Returns:
        GDAL Dataset: Metadata information for the specified band.
        """
        print(self.ndvis_dir)
        try:
            for file in os.listdir(self.ndvis_dir):
                file_path = os.path.join(self.ndvis_dir, file)
                if os.path.isfile(file_path):
                    match = re.match(r'^NDVI_(\d{4})_(\d{2})_(\d{2})\.tif$', file)
                    if match:
                        year, month, day = map(int, match.groups())
                        if self.is_valid_date(year, month, day):
                            random_ndvi = gdal.Open(file_path, gdal.GA_ReadOnly)
                            return random_ndvi
        except Exception as e:
            raise Exception(f"Error reading NDVI data: {str(e)}")

    def is_valid_date(self, year, month, day):
        try:
            datetime.date(year, month, day)
            return True
        except ValueError:
            return False

    def read_ndvi_data(self):
        try:
            for file in os.listdir(self.ndvis_dir):
                file_path = os.path.join(self.ndvis_dir, file)
                if os.path.isfile(file_path):
                    match = re.match(r'^NDVI_(\d{4})_(\d{2})_(\d{2})\.tif$', file)
                    if match:
                        year, month, day = map(int, match.groups())
                        if self.is_valid_date(year, month, day):
                            dataset = gdal.Open(file_path, gdal.GA_ReadOnly)
                            if dataset is not None:
                                current_resolution = (dataset.RasterXSize, dataset.RasterYSize)
                                self.resolutions.add(current_resolution)
                                ndvi_array = dataset.ReadAsArray()
                                dataset = None
                                date_obj = datetime.date(year, month, day)
                                self.ndvi_data_dict[date_obj] = ndvi_array
                            else:
                                print(f"Could not open file: {file_path}")
                        else:
                            print(f"Ignoring file with invalid date: {file}")
                    else:
                        print(f"Ignoring file with invalid format: {file_path}")

            if not self.ndvi_data_dict:
                raise Exception("No valid NDVI files found in the directory")

            if len(self.resolutions) != 1:
                raise Exception("Not all images have the same resolution")

            min_date = min(self.ndvi_data_dict.keys())
            first_date = datetime.date(min_date.year, min_date.month, min_date.day)

            for date_obj in self.ndvi_data_dict.keys():
                days_elapsed = (date_obj - first_date).days + 1
                self.ndvi_data_dict[days_elapsed] = self.ndvi_data_dict.pop(date_obj)

            sorted_ndvi_data = dict(sorted(self.ndvi_data_dict.items()))

            if len(sorted_ndvi_data) < 6:
                raise Exception("Phenology Metrics needs at least 6 NDVIS to be executed!")
            else:
                print(str(len(sorted_ndvi_data)) + " NDVIs have been read")

            return sorted_ndvi_data

        except Exception as e:
            raise Exception(f"Error reading NDVI data: {str(e)}")