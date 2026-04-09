import pandas as pd

# Create a series with name
data = ["a", "b", "c", "d"]
series = pd.Series(data, name="A")
print(series, "\n")

# Create a series with name and custom index
custom_index = [2, 4, 6, 8]
series_with_index = pd.Series(data, name="B", index=custom_index)
print(series_with_index, "\n")

# Create a series without name and custom_index
series_without_name_index = pd.Series(data)
print(series_without_name_index, "\n")
