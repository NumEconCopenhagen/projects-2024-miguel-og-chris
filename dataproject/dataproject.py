#We import the GDPData and DebtData and inspect the data
GDPData = pd.read_csv('GDPGrowthData-All.csv', delimiter=';')
DebtData = pd.read_csv('DebtData-All.csv', delimiter=';')
#The two datasets are identical in structure, so we will only display one of them in the data cleaning proces
# Get rid of empty rows
GDPData.dropna(how='all', inplace=True)
DebtData.dropna(how='all', inplace=True)
# Get rid of last row
# Get the index of the last row
last_row_index_GDP = GDPData.index[-1]
last_row_index_Debt = DebtData.index[-1]

# Drop the last row
GDPData.drop(last_row_index_GDP, inplace=True)
DebtData.drop(last_row_index_Debt, inplace=True)

# Transforming the data into a long format
GDP_panel_data = GDPData.melt(id_vars=['Real Per Capita GDP Growth (Annual percent change)'], 
                       var_name="Year", 
                       value_name="GDP Growth Rate")
Debt_panel_data = DebtData.melt(id_vars=['Government Debt (% of GDP) (Percent of GDP)'], 
                       var_name="Year", 
                       value_name="Government debt (Percent of GDP)")

# Defining the columns we want
GDP_panel_data.columns = ["Country name", "Year", "Real per capita GDP growth rate"]
Debt_panel_data.columns = ["Country name", "Year", "Government debt (Percent of GDP)"]

# Converting 'Year' to integer for proper sorting
GDP_panel_data['Year'] = GDP_panel_data['Year'].astype(int)
Debt_panel_data['Year'] = Debt_panel_data['Year'].astype(int)

# Sorting the data by country and year
GDP_panel_data = GDP_panel_data.sort_values(by=["Country name", "Year"])
Debt_panel_data = Debt_panel_data.sort_values(by=["Country name", "Year"])
GDP_panel_data.to_csv('Panel_data_print_GDP', index=False)

#Merge the data where collumns 'Country name' and 'Year' match
merged_data = pd.merge(GDP_panel_data, Debt_panel_data, on=['Country name', 'Year'], how = 'inner')
merged_data.to_csv('Merged_data_print', index=False)