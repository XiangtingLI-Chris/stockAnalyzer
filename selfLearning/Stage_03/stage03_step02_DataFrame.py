import pandas as pd

##### Three Methods to Create a DataFrame #####

#    Name    Age
# 0  Google  25
# 1  Chrome  30
# 2  Taobao  35

### Method 1: Use lists in a dict to create a DataFrame
data_list_dict = {
    # columns
    "Name": ["Google", "Chrome", "Taobao"],
    "Age": [25, 30, 35]
}

# `DataFrame` is a class in pandas (here called `pd`),
# `pd.DataFrame(obj)` is used to create an instance of the class `DataFrame`
df_list_dict = pd.DataFrame(data_list_dict)

print(df_list_dict, "\n")

### Method 2: Use dicts in a list to create a DataFrame
data_dict_list = [
    # rows
    {"Name": "Google", "Age": 25},
    {"Name": "Chrome", "Age": 30},
    {"Name": "Taobao", "Age": 35}
]
df_dict_list = pd.DataFrame(data_dict_list)
print(df_dict_list, "\n")

### Method 3: Use lists in a list to create a DataFrame
data_list = [
    # rows
    ["Google", 25],
    ["Chrome", 30],
    ["Taobao", 35]
]
columns = ["Name", "Age"]
df_list = pd.DataFrame(data_list, columns=columns)
print(df_list, "\n")

# Missing data in method 2 also works.
data_missing = [
    # rows
    {"Name": "Google", "Age": 25},
    {"Name": "Chrome"},     # missing data will be filled as `NaN`
    {"Name": "Taobao", "Age": 35}
]
df_missing = pd.DataFrame(data_missing)
print(df_missing, "\n")

##### Final Version #####
final_data = [
    ["Alice", 25, "New York"],
    ["Bob", 35, "Los Angeles"],
    ["Charlie", 30, "Chicago"],
    ["David", 40, "Houston"]
]
final_columns = ["Name", "Age", "City"]
final_df = pd.DataFrame(final_data, columns=final_columns)

# Check top two rows of data
print("top 2 rows:")
print(final_df.head(2))
print("")

# Check basic information
print("basic information:")
print(final_df.info())
print("")

# Check statistic information
print("statistic information:")
print(final_df.describe())
print("")

# Sort data by age
final_df_sorted = final_df.sort_values(by="Age", ascending=True)
print("sorted data:")
print(final_df_sorted)
print("")

# Choose rows according to index
print("iloc selection:")
print(final_df.iloc[1:3])
print("")

# Choose rows according to label
print("loc selection:")
print(final_df.loc[1:3])
print("")