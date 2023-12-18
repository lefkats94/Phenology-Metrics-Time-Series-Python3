import numpy as np
from scipy import interpolate, ndimage
import matplotlib.pyplot as plt

class NDVIInterpolator:
    def __init__(self, ndvi_data):
        """
        Initialize the NDVIInterpolator with NDVI data.

        Args:
            ndvi_data (dict): A dictionary with number of days from the start as keys and NDVI arrays as values.
        """
        self.ndvi_data = ndvi_data

    def interpolate_ndvi(self, method, sigma=1):
        """
        Interpolate NDVI values for each pixel using various interpolation methods.

        Parameters:
            method (str): Interpolation method ('linear', 'gaussian', 'spline').
            sigma (float): Standard deviation of the Gaussian kernel for smoothing.

        Returns:
            dict: A dictionary with pixel coordinates as keys and interpolated time series as values.
        """
        if method == 'linear':
            return self.interpolate_linear()
        elif method == 'gaussian':
            return self.interpolate_gaussian(sigma)
        elif method == 'spline':
            return self.interpolate_spline()
        else:
            raise ValueError(f"Unsupported interpolation method: {method}")

    def interpolate_linear(self):
        dates = list(self.ndvi_data.keys())
        image_arrays = list(self.ndvi_data.values())

        height, width = image_arrays[0].shape
        interpolated_time_series = {}

        # Create a common range of indices for interpolation
        common_indices = np.arange(len(dates))

        for i in range(height):
            for j in range(width):
                pixel_time_series = [image_array[i, j] for image_array in image_arrays]
                interpolator = interpolate.interp1d(common_indices, pixel_time_series, kind='linear', bounds_error=False, fill_value="extrapolate")
                interpolated_values = interpolator(common_indices)

                interpolated_time_series[(i, j)] = interpolated_values

        return interpolated_time_series, height, width

    def interpolate_gaussian(self, sigma=1):
        dates = list(self.ndvi_data.keys())
        image_arrays = list(self.ndvi_data.values())

        height, width = image_arrays[0].shape
        interpolated_time_series = {}

        for i in range(height):
            for j in range(width):
                pixel_time_series = [image_array[i, j] for image_array in image_arrays]
                smoothed_values = ndimage.gaussian_filter1d(pixel_time_series, sigma=sigma, mode='constant', cval=0.0)
                interpolator = interpolate.interp1d(range(len(dates)), smoothed_values, kind='linear', fill_value="extrapolate")
                interpolated_values = interpolator(np.arange(len(dates)))
                interpolated_time_series[(i, j)] = interpolated_values

        return interpolated_time_series, height, width

    def interpolate_spline(self):
        dates = list(self.ndvi_data.keys())
        image_arrays = list(self.ndvi_data.values())

        height, width = image_arrays[0].shape
        interpolated_time_series = {}

        for i in range(height):
            for j in range(width):
                pixel_time_series = [image_array[i, j] for image_array in image_arrays]
                interpolator = interpolate.splrep(range(len(dates)), pixel_time_series, s=0)
                interpolated_values = interpolate.splev(np.arange(len(dates)), interpolator)
                interpolated_time_series[(i, j)] = interpolated_values

        return interpolated_time_series, height, width

    def visualize_interpolation_pixel(self, interpolated_time_series, x, y):
        pixel_to_visualize = (x, y)

        time_series = interpolated_time_series[pixel_to_visualize]
        x_dates = list(self.ndvi_data.keys())
        print(x_dates)
        # Find the index of the maximum y value
        max_y_index = np.argmax(time_series)

        # Use the index to get the corresponding x value
        target_x =np.interp(max_y_index, range(len(x_dates)), x_dates)
        target_y = time_series[max_y_index]

        # Create a plot
        plt.figure(figsize=(10, 6))
        plt.plot(x_dates, time_series, label=f'Pixel {pixel_to_visualize}')
        plt.scatter([target_x], [target_y], color='red', label=f'Maximum Y Value: {target_y} at Day {target_x}', marker='o')
        plt.xlabel('Day')
        plt.ylabel('Interpolated Value')
        plt.title(f'Interpolation for Pixel {pixel_to_visualize}')
        plt.legend()
        plt.grid(True)

        # Show the plot
        plt.show()

        return None
