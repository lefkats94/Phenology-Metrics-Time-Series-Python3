from read_ndvis import read_ndvi_data

if __name__ == "__main__":
    # Call the read_ndvi_data function
    ndvis_dir = input("Enter the NDVIS directory:")
    ndvi_data = read_ndvi_data(ndvis_dir)