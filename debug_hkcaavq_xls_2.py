import pandas as pd

try:
    df = pd.read_excel("hkcaavq_courses_debug.xls", engine='xlrd', header=None, skiprows=4)
    print("File read successfully with skiprows=4. Here's the head of the dataframe:")
    print(df.head(10))
    print("\nDataFrame Info:")
    df.info()
except Exception as e:
    print(f"An error occurred while reading the Excel file: {e}")