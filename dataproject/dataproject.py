import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display
gdp_file = 'GDPGrowthData-All.csv'
debt_file = 'DebtData-All.csv'

def clean_data(gdp_file, debt_file):
    # Load the datasets
    GDPData = pd.read_csv(gdp_file, delimiter=';')
    DebtData = pd.read_csv(debt_file, delimiter=';')
    
    # Get rid of empty rows
    GDPData.dropna(how='all', inplace=True)
    DebtData.dropna(how='all', inplace=True)
    
    # Get rid of the last row
    GDPData.drop(GDPData.index[-1], inplace=True)
    DebtData.drop(DebtData.index[-1], inplace=True)
    
    return GDPData, DebtData

def clean_and_transform_data(gdp_file, debt_file):
     # Load the datasets
    GDPData = pd.read_csv(gdp_file, delimiter=';')
    DebtData = pd.read_csv(debt_file, delimiter=';')
    
    # Get rid of empty rows
    GDPData.dropna(how='all', inplace=True)
    DebtData.dropna(how='all', inplace=True)
    
    # Get rid of the last row
    GDPData.drop(GDPData.index[-1], inplace=True)
    DebtData.drop(DebtData.index[-1], inplace=True)
    # Transform the data into a long format
    GDP_panel_data = GDPData.melt(id_vars=['Real Per Capita GDP Growth (Annual percent change)'], 
                                  var_name="Year", 
                                  value_name="GDP Growth Rate")
    Debt_panel_data = DebtData.melt(id_vars=['Government Debt (% of GDP) (Percent of GDP)'], 
                                    var_name="Year", 
                                    value_name="Government debt (Percent of GDP)")
    
    # Define the columns we want
    GDP_panel_data.columns = ["Country name", "Year", "Real per capita GDP growth rate"]
    Debt_panel_data.columns = ["Country name", "Year", "Government debt (Percent of GDP)"]
    
    # Convert 'Year' to integer for proper sorting
    GDP_panel_data['Year'] = GDP_panel_data['Year'].astype(int)
    Debt_panel_data['Year'] = Debt_panel_data['Year'].astype(int)
    
    # Sort the data by country and year
    GDP_panel_data = GDP_panel_data.sort_values(by=["Country name", "Year"])
    Debt_panel_data = Debt_panel_data.sort_values(by=["Country name", "Year"])
    
    # Save the transformed GDP data to a CSV file
    GDP_panel_data.to_csv('Panel_data_print_GDP.csv', index=False)
    
    return GDP_panel_data, Debt_panel_data


# Function to clean, transform, and merge the data
def clean_transform_merge_data(gdp_file, debt_file):
    # Load and clean the data
    GDPData, DebtData = clean_and_transform_data(gdp_file, debt_file)
    
    # Merge the datasets
    merged_data = pd.merge(GDPData, DebtData, on=['Country name', 'Year'], how='inner')
    
    # Ensure all data in the columns is treated as strings, then replace commas
    merged_data['Real per capita GDP growth rate'] = merged_data['Real per capita GDP growth rate']\
        .astype(str).str.replace(',', '.').replace('no data', np.nan).astype(float)
    merged_data['Government debt (Percent of GDP)'] = merged_data['Government debt (Percent of GDP)']\
        .astype(str).str.replace(',', '.').replace('no data', np.nan).astype(float)
    
    return merged_data

def calculate_summary_statistics(merged_data):
    # Split the data
    grouped_data = merged_data.groupby('Country name')
    
    # Use aggregation function to calculate means
    summary = grouped_data.agg({
        'Real per capita GDP growth rate': 'mean',
        'Government debt (Percent of GDP)': 'mean'
    }).reset_index()
    
    # Combine results
    summary.columns = ['Country name', 'Average GDP Growth Rate', 'Average Government Debt']
    
    return summary

def plot_summary_statistics(summary):
    # Plotting
    fig, ax1 = plt.subplots(figsize=(12, 8))
    
    # Plot average GDP growth rate
    ax1.bar(summary['Country name'], summary['Average GDP Growth Rate'], color='b', label='Average GDP Growth Rate')
    ax1.set_xlabel('Country')
    ax1.set_ylabel('Average GDP Growth Rate', color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    plt.xticks(rotation=90)
    
    # Create a second y-axis to plot the average government debt
    ax2 = ax1.twinx()
    ax2.plot(summary['Country name'], summary['Average Government Debt'], color='r', label='Average Government Debt')
    ax2.set_ylabel('Average Government Debt', color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    
    fig.tight_layout()
    plt.title('Average GDP Growth Rate and Government Debt by Country')
    plt.show()

# Function to create the interactive plot
def create_interactive_plot(merged_data):
    # Dropdown menu for selecting the country
    country_dropdown = widgets.Dropdown(
        options=sorted(merged_data['Country name'].unique()),
        value='Angola',
        description='Country:',
        disabled=False,
    )

    # Function to update the plot
    def update_plot(country):
        country_data = merged_data[merged_data['Country name'] == country]

        # Ensure 'Year' is integer
        country_data['Year'] = country_data['Year'].astype(int)

        # Create the plot
        plt.figure(figsize=(10, 5))
        plt.bar(country_data['Year'], country_data['Real per capita GDP growth rate'], label='Real per capita GDP growth rate (%)')
        plt.plot(country_data['Year'], country_data['Government debt (Percent of GDP)'], label='Government debt (% of GDP)')
        plt.axhline(0, color='green', linewidth=0.8)  # Adding a horizontal line at y=0
        plt.title(f'GDP Growth and Public Debt for {country}')
        plt.xlabel('Year')
        plt.ylabel('Percent (%)')
        plt.xticks(country_data['Year'].unique(), fontsize=8)
        plt.legend()
        plt.grid(True)
        plt.show()

    # Display the interactive widget
    display(widgets.interactive(update_plot, country=country_dropdown))

def filter_country_data(merged_data, country_name):
    # Defining which country we want to include
    country_data = merged_data[merged_data['Country name'] == country_name]

    # Ensure all data in the columns is treated as strings, then replace commas
    country_data['Real per capita GDP growth rate'] = country_data['Real per capita GDP growth rate']\
        .astype(str).str.replace(',', '.').astype(float)
    country_data['Government debt (Percent of GDP)'] = country_data['Government debt (Percent of GDP)']\
        .astype(str).str.replace(',', '.').astype(float)
    
    # Ensure 'Year' is integer
    country_data['Year'] = country_data['Year'].astype(int)
    
    return country_data

def plot_country_data(country_data, country_name):
    # Plotting
    plt.figure(figsize=(10, 5))
    plt.bar(country_data['Year'], country_data['Real per capita GDP growth rate'], label='Real per capita GDP growth rate (%)')
    plt.plot(country_data['Year'], country_data['Government debt (Percent of GDP)'], label='Government debt (% of GDP)', linestyle='-')
    plt.axhline(0, color='green', linewidth=0.8)  # Adding a horizontal line at y=0
    plt.title(f'GDP Growth and Public Debt for {country_name}')
    plt.xlabel('Year')
    plt.ylabel('Percent (%)')
    plt.xticks(country_data['Year'].unique(), fontsize=8)
    plt.legend()
    plt.grid(True)
    plt.show()

def calculate_correlation(merged_data, country_name):
    # Filter data for the specified country
    country_data = merged_data[merged_data['Country name'] == country_name]

    # Ensure all data in the columns is treated as strings, then replace commas
    country_data['Real per capita GDP growth rate'] = country_data['Real per capita GDP growth rate']\
        .astype(str).str.replace(',', '.').astype(float)
    country_data['Government debt (Percent of GDP)'] = country_data['Government debt (Percent of GDP)']\
        .astype(str).str.replace(',', '.').astype(float)
    
    # Calculate the correlation
    correlation = country_data['Real per capita GDP growth rate'].corr(country_data['Government debt (Percent of GDP)'])
    print(f'Correlation between GDP Growth and Public Debt for {country_name}: {correlation}')
    
    return correlation

def plot_selected_countries(merged_data, countries):
    # Ensuring 'Year' is integer
    merged_data['Year'] = merged_data['Year'].astype(int)
    merged_data = merged_data.sort_values('Year')
    
    # Plotting
    plt.figure(figsize=(12, 6))
    
    # Setting an index for the bars
    index = np.arange(len(merged_data['Year'].unique()))
    bar_width = 0.2
    
    # Plotting bars and lines for each country
    for i, country in enumerate(countries):
        country_data = merged_data[merged_data['Country name'] == country]
        country_data = country_data.sort_values('Year')  
        
        # Plotting GDP Growth Rate as bars
        plt.bar(index + i*bar_width, country_data['Real per capita GDP growth rate'], bar_width, label=f'GDP Growth Rate {country} (%)')
        
        # Plotting Government Debt as line
        plt.plot(index + i*bar_width, country_data['Government debt (Percent of GDP)'], label=f'Government Debt {country} (% of GDP)', linestyle='-', marker='o')
    
    plt.axhline(0, color='gray', linewidth=0.8)
    plt.title('GDP Growth and Public Debt')
    plt.xlabel('Year')
    plt.ylabel('Percent (%)')
    plt.xticks(index + bar_width/2, merged_data['Year'].unique(), fontsize=8, rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def calculate_correlations(merged_data):
    # Define the countries in which we want to calculate the correlation
    Oil_data = merged_data[merged_data['Country name'] == 'Oil-exporting countries']
    Intensive_data = merged_data[merged_data['Country name'] == 'Resource-intensive countries  ']
    NonIntensive_data = merged_data[merged_data['Country name'] == 'Non-resource-intensive countires  ']
    
    # Ensuring all data in the columns is treated as strings, then replacing commas
    Oil_data['Real per capita GDP growth rate'] = Oil_data['Real per capita GDP growth rate'].astype(str).str.replace(',', '.').astype(float)
    Oil_data['Government debt (Percent of GDP)'] = Oil_data['Government debt (Percent of GDP)'].astype(str).str.replace(',', '.').astype(float)
    Intensive_data['Real per capita GDP growth rate'] = Intensive_data['Real per capita GDP growth rate'].astype(str).str.replace(',', '.').astype(float)
    Intensive_data['Government debt (Percent of GDP)'] = Intensive_data['Government debt (Percent of GDP)'].astype(str).str.replace(',', '.').astype(float)
    NonIntensive_data['Real per capita GDP growth rate'] = NonIntensive_data['Real per capita GDP growth rate'].astype(str).str.replace(',', '.').astype(float)
    NonIntensive_data['Government debt (Percent of GDP)'] = NonIntensive_data['Government debt (Percent of GDP)'].astype(str).str.replace(',', '.').astype(float)
    
    # Calculating the correlation between 'Real per capita GDP growth rate' and 'Government debt (Percent of GDP)'
    correlation_oil = Oil_data['Real per capita GDP growth rate'].corr(Oil_data['Government debt (Percent of GDP)'])
    correlation_intensive = Intensive_data['Real per capita GDP growth rate'].corr(Intensive_data['Government debt (Percent of GDP)'])
    correlation_Nonintensive = NonIntensive_data['Real per capita GDP growth rate'].corr(NonIntensive_data['Government debt (Percent of GDP)'])
    
    # Print the correlations
    print('Correlation between GDP Growth and Public Debt for Oil exporting countries:')
    print(correlation_oil)
    
    print('Correlation between GDP Growth and Public Debt for Resource-intensive countries:')
    print(correlation_intensive)
    
    print('Correlation between GDP Growth and Public Debt for Non-resource-intensive countries:')
    print(correlation_Nonintensive)