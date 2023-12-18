import numpy as np

class PhenoPhaseDetector:
    def __init__(self, ndvi_data, interpolated_time_series):
        self.ndvi_data = ndvi_data
        self.interpolated_time_series = interpolated_time_series

    def start_of_season(self, threshold, height, width):
        """
        Detects the start of the growing season.
        """
        sos = np.empty((height, width))
        for i in range(height):
            for j in range(width):
                sos[i,j] = np.interp(threshold, self.interpolated_time_series[(i, j)], list(self.ndvi_data.keys()))
        return sos

    def peak_of_season(self, height, width):
        """
        Detects the peak of the growing season.
        """
        pos = np.empty((height, width))
        for i in range(height):
            for j in range(width):
                max_value = np.argmax(self.interpolated_time_series[(i, j)])
                pos[i,j] = np.interp(max_value, range(len(list(self.ndvi_data.keys()))), list(self.ndvi_data.keys()))
        return pos

    def end_of_season(self, threshold, height, width):
        """
        Detects the end of the growing season.
        """
        eos = np.empty((height, width))
        #for i in range(height):
            #for j in range(width):
                
        return eos