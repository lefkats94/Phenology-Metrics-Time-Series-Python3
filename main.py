from read_ndvis import NDVIProcessor
from interpolation import NDVIInterpolator 
from events_detection import PhenoPhaseDetector
from create_outputs import CreateOutputs

if __name__ == "__main__":
    # Call the read_ndvi_data method of NDVIProcessor
    '''
    ndvis_dir = input("Enter the NDVIS directory:")
    interpolation_method = input("Enter interpolation method:")
    sos_threshold = input("Enter start of season threshold:")
    eos_threshold = input("Enter end of season threshold:")
    '''

    ndvis_dir = "C:/Users/lefkats_local/Desktop/phenology_data"
    interpolation_method = "linear"
    sos_threshold = 0
    eos_threshold = 0

    ndvi_processor = NDVIProcessor(ndvis_dir)
    ndvi_data = ndvi_processor.read_ndvi_data()

    # Create an instance of NDVIInterpolator and interpolate NDVI values
    ndvi_interpolator = NDVIInterpolator(ndvi_data)
    interpolated_time_series, height, width = ndvi_interpolator.interpolate_ndvi(interpolation_method)

    #ndvi_interpolator.visualize_interpolation_pixel(interpolated_time_series, 5, 12)

    #sos = PhenoPhaseDetector(ndvi_data, interpolated_time_series).start_of_season(-0.2, height, width)
    #pos = PhenoPhaseDetector(ndvi_data, interpolated_time_series).peak_of_season(height, width)
    eos = PhenoPhaseDetector(ndvi_data, interpolated_time_series).end_of_season(0,height, width)

    #CreateOutputs(ndvis_dir).create_tif(sos, "sos")

    #print(eos)

