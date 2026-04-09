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

# Use index to read values (behave like list)
data2 = ["Google", "Wiki", "Taobao"]
index2 = ["x", "y", "z"]
series2 = pd.Series(data2, index=index2)
print(series2)
print("series2[\"x\"] = ", series2["x"])
print("series2[\"y\"] = ", series2["y"])
print("series2[\"z\"] = ", series2["z"])
print("")

# Use key/value object (like a dict) to create a series
simple_dict = {1: "Google", 2: "Wiki", 3: "Taobao"}
series_by_dict = pd.Series(simple_dict)
print(series_by_dict, "\n")

# If only parts of the dict is used, then just provide necessary index
selected_index = [1, 2]
series_by_dict_selected = pd.Series(simple_dict, index=selected_index)
print(series_by_dict_selected, "\n")


### Final version
print("##### Final Version #####\n")

# Create a series
final_data = [12, 25, 45, 60, 7, 36]
final_index = ["a", "b", "c", "d", "e", "f"]
final_series = pd.Series(final_data, name="final series", index=final_index)

# Get access to basic information of the series
print("index:")
print(final_series.index)
print("data:")
print(final_series.values)
print("data type:")
print(final_series.dtype)
print("top 2 data:")
print(final_series.head(2))
print("series shape:")
print(final_series.shape)
print("")

# Calculate the cumulated sum to every single data
cumulated_sum = final_series.cumsum()
print("cumulated sum:")
print(cumulated_sum)
print("")

# Double each data by calling map method
# `lambda` is similar to the callback function in JavaScript
doubled_series = final_series.map(lambda x: x * 2)
print("doubled series:")
print(doubled_series)
print("")

# Select data by using location index
print("select single data:")
print(final_series.iloc[3])
print("select parts of data:")
print(final_series.iloc[2:4])
print("")

# Select data by using location
print(final_series.loc[3])

# Find missing value (no missing value here, so all `False`)
print("mission value:")
print(final_series.isnull())
print("")

# Sort values
sorted_series = final_series.sort_values()
print("series after being sorted:")
print(sorted_series)
