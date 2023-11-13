#%%
import pandas as pd
import re
import numpy as np
#%%
df = pd.read_csv("/Users/carriemagee/Desktop/NETWORKS/influence_edges.csv")


# %%
filtered_df = df.dropna(subset=['Target'])

# Display the filtered DataFrame
print(filtered_df)
# %%
len(filtered_df)
# %%

# Define a function to check for non-English characters
def contains_non_english(name):
    return not all(ord(char) < 128 for char in name)

# Remove rows with non-English names
filtered_df = df[~df['Source'].apply(contains_non_english)]

# %%
# Display the filtered DataFrame
data = filtered_df.dropna(subset=['Target'])

# %%
print(data.head(30))
# %%
website_patterns = ['http', 'www', '.com']

# Define a function to check for website patterns
def contains_website(target):
    for pattern in website_patterns:
        if pattern in target:
            return True
    return False

# Remove rows with websites in the 'target' column
filtered_df = data[~data['Target'].apply(contains_website)]

# Display the filtered DataFrame
print(filtered_df.head(30))
# %%
filtered_df.to_csv('cleaned_data.csv', index=False)
# %%
