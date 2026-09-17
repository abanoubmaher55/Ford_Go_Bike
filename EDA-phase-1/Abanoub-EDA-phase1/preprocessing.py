import pandas as pd



def read_data_file(file_name):
    """
    Read a CSV file from the data folder and return it as a DataFrame.

    Parameters:
        file_name (str): The name of the CSV file to read.

    Returns:
        pandas.DataFrame: The data stored in the CSV file.
    """
    

    df = pd.read_csv(file_name)

    return df