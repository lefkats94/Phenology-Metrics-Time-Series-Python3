from read_ndvis import NDVIProcessor
from osgeo import gdal

class CreateOutputs:
    def __init__(self, ndvis_dir):
        self.ndvis_dir = ndvis_dir
    
    def create_tif(self, array, phase):
        """
        Creates output files including a GeoTIFF and a PNG images for the Phenology Metrics.
        """
        inputs_directory = self.ndvis_dir
        inputs_directory = inputs_directory.replace("\\", "/")
        if not inputs_directory.endswith("/"):
            inputs_directory += "/"

        x, y = array.shape

        driver = gdal.GetDriverByName('GTiff')
        dataset = driver.Create(inputs_directory + phase + ".tif", y, x, 1, gdal.GDT_Float32)
        dataset.GetRasterBand(1).WriteArray(array)
        dataset.GetRasterBand(1).SetNoDataValue(-1)

        random_ndvi = NDVIProcessor.get_metadata(inputs_directory)
        geotrans = random_ndvi.GetGeoTransform()
        proj = random_ndvi.GetProjection()
        dataset.SetGeoTransform(geotrans)
        dataset.SetProjection(proj)

        dataset = None
        return None