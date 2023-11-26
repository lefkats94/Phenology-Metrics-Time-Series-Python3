from read_ndvis import read_ndvi_data
import numpy as np
from scipy import interpolate

ndvi_data = read_ndvi_data("C:/Users/lefkats_local/Desktop/phenology_python/data3")

# Extract the dates and image arrays from the dictionary
dates = list(ndvi_data.keys())
image_arrays = list(ndvi_data.values())

# Assuming your image arrays have the same dimensions
# You can use the first image array to get the dimensions
height, width = image_arrays[0].shape

# Initialize empty arrays to store interpolated values
interpolated_time_series = {}

# Create a time series for each pixel using linear interpolation
for i in range(height):
    for j in range(width):
        pixel_time_series = [image_array[i, j] for image_array in image_arrays]
        interpolator = interpolate.interp1d(range(len(dates)), pixel_time_series, kind='linear')
        interpolated_values = interpolator(np.arange(len(dates)))  # Interpolate values at each time step
        interpolated_time_series[(i, j)] = interpolated_values
        print(i, j)
        



import matplotlib.pyplot as plt

# Example: Visualize the interpolation for a specific pixel at (i, j)
pixel_to_visualize = (294, 219)  # Replace with the pixel you want to visualize

if pixel_to_visualize in interpolated_time_series:
    time_series = interpolated_time_series[pixel_to_visualize]

    # Create a list of corresponding dates for the x-axis
    x_dates = list(ndvi_data.keys())

    # Create a plot
    plt.figure(figsize=(10, 6))
    plt.plot(x_dates, time_series, label=f'Pixel {pixel_to_visualize}')
    plt.xlabel('Date')
    plt.ylabel('Interpolated Value')
    plt.title(f'Interpolation for Pixel {pixel_to_visualize}')
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.show()
else:
    print(f'Pixel {pixel_to_visualize} not found in the interpolated time series.')