# %%
import pandas as pd

# Load the data
file_path = "../data/movcont.xlsx"
df = pd.read_excel(file_path)

# Trim whitespaces on column names
df.columns = df.columns.str.strip()

# show df columns
print(df.columns)


# %%

# Function to process each group
def process_group(group):
    if len(group) == 2 and set(group['Tipo']) == {'C', 'D'}:
        return True
    return False

# Group by 'Conta' and 'Valor' and filter
groups = df.groupby(['Conta', 'Valor'])
filtered_groups = groups.filter(lambda x: process_group(x))

# Assigning IdentLan values
identlan_value = 1
for (conta, valor), group in filtered_groups.groupby(['Conta', 'Valor']):
    df.loc[group.index, 'IdentLan'] = identlan_value
    identlan_value += 1

# Display the modified DataFrame
print(df.head(10))

# %%

# create a new df removing all identlan Nan values
df2 = df[df['IdentLan'].notna()]

# order by identlan ascending
df2 = df2.sort_values(by=['IdentLan'])

# create a new df from df with only the rows that have identlan Nan values
df3 = df[df['IdentLan'].isna()]

# compare the two dfs
print(df2.shape)
print(df3.shape)

# Display the modified DataFrame
# print(df2.head(10))

# Sum 'Valor' column from df2 grouped by 'Tipo' and format as currency
df_total_encontrado = df2.groupby('Tipo')['Valor'].sum().map('${:,.2f}'.format)
print(df_total_encontrado)

# Do the same for df3
df_total_nao_encontrado = df3.groupby('Tipo')['Valor'].sum().map('${:,.2f}'.format)
print(df_total_nao_encontrado)

