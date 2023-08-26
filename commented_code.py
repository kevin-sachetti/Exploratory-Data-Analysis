# Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

# Load the Dataset
my_data = pd.read_csv('dataset/dataset.csv')

# Shape
my_data.shape

# Data Sample, the first lines
my_data.head()

# Data Sample, the last lines
my_data.tail()

### Data Analysis:

# Columns
my_data.columns

# Check the data type
my_data.dtypes

# Sales statistics summary
my_data['Sales_Value'].describe()

# Checks for duplicate records
my_data[my_data.duplicated()]

# Checks for null values
my_data.isnull().sum()



### Insight 1º:
### Which city has the highest sales value for the 'Office Supplies' category?

# Filter the dataframe with the records of the category we want
insight_1 = my_data[my_data['Category'] == 'Office Supplies']

# Agroup by city and calculate the total Sales_Value
insight_1_total = insight_1.groupby('City')['Sales_Value'].sum()

# Finds the city with the highest sales value
highest_sales_value = insight_1_total.idxmax()
print("City with highest sales value for 'Office Supplies':", highest_sales_value)

# Checks the result
insight_1_total.sort_values(ascending = False)



### Insight 2º:
### What is the Total Sales by Order Date?

# The total sales for each order date
insight_2 = my_data.groupby('Data_Order')['Sales_Value'].sum()
insight_2.head()

# Plot
plt.figure(figsize = (20, 6))
insight_2.plot(x = 'Data_Order', y = 'Sales_Value', color = 'blue')
plt.title('Total Sales by Order Date')
plt.show()



### Insight 3º:
### What is the Total Sales by State?

# Agroup by state and calculate the sales total
insight_3 = my_data.groupby('State')['Sales_Value'].sum().reset_index()

# Plot
plt.figure(figsize = (16, 6))
sns.barplot(data = insight_3, y = 'Sales_Value', x = 'State').set(title = 'Sales by State')
plt.xticks(rotation = 80)
plt.show()



### Insight 4º:
### What are the top 10 cities with the highest total sales?
insight_4 = my_data.groupby('City')['Sales_Value'].sum().reset_index().sort_values(by = 'Sales_Value', ascending = False).head(10)
insight_4.head(10)

# Plot
plt.figure(figsize = (16, 6))
sns.set_palette('coolwarm')
sns.barplot(data = insight_4, y = 'Sales_Value', x = 'City').set(title = 'Top 10 cities with the highest total sales')
plt.show()



### Insight 5º:
### Which segment had the highest total sales?

# Agroup by segment and calculate the sales total
insight_5 = my_data.groupby('Segment')['Sales_Value'].sum().reset_index().sort_values(by = 'Sales_Value', ascending = False)
insight_5.head()

# Function to convert data to absolute value
def autopct_format(values): 
    def my_format(pct): 
        total = sum(values) 
        val = int(round(pct * total / 100.0))
        return ' $ {v:d}'.format(v = val)
    return my_format

# Plot
plt.figure(figsize = (16, 6))
plt.pie(insight_5['Sales_Value'], labels = insight_5['Segment'], autopct = autopct_format(insight_5['Sales_Value']), startangle = 90)
centre_circle = plt.Circle((0, 0), 0.82, fc = 'white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

# Labels
plt.annotate(text = 'Sales Total: ' + '$ ' + str(int(sum(insight_5['Sales_Value']))), xy = (-0.25, 0))
plt.title('Sales Total by Segment')
plt.show()



### Insight 6º:
### What is the Total Sales per Segment and per Year?

my_data.head()

# Convert date column to datetime type to get proper format
my_data['Data_Order'] = pd.to_datetime(my_data['Data_Order'], dayfirst = True)
my_data.dtypes

# Extract the year into a new variable
my_data['Year'] = my_data['Data_Order'].dt.year
my_data.head()

# The Total Sales per Segment and per Year
insight_6 = my_data.groupby(['Year','Segment'])['Sales_Value'].sum()
insight_6



### Insight 7º:
### The company's managers are considering offering different discount tiers and would like to simulate based, on the following rule: If the Sales_Value is greater than 1000, a 15%% discount is given. If the Sales_Value is less than 1000, a 10%% discount is given.")
### How many sales would receive a 15% discount?

# Creates a new column according to the rule defined above
my_data['Discount'] = np.where(my_data['Sales_Value'] > 1000, 0.15, 0.10)
my_data.head()

# Total by variable values
disc = my_data['Discount'].value_counts()
print("15%% discount was given to:", disc)



### Insight 8º:
### Assuming the company decides to grant the 15% discount from the previous item. 
### What would be the average Sales_Value before and after the discount?

# Column calculating the sale value minus the discount
my_data['Sales_Value_Discount'] = my_data['Sales_Value'] - (my_data['Sales_Value'] * my_data['Discount']) 
my_data.head()

# Filtering the sales before the 15% discount
insight_8_before = my_data.loc[my_data['Discount'] == 0.15, 'Sales_Value']

# Filtering the sales after the 15% discount
insight_8_after = my_data.loc[my_data['Discount'] == 0.15, 'Sales_Value_Discount']

# Calculate the average sales before the 15% discount
mean_before = insight_8_before.mean()
print("Average sales before 15%% discount:", round(mean_before, 2))

# Calculate the average sales after the 15% discount
mean_after = insight_8_after.mean()
print("Average sales after 15%% discount:", round(mean_after, 2))



### Insight 9º:
### What is the Average Sales per Segment, per Year, and per Month?

# Extract the month into a new variable
my_data['Month'] = my_data['Data_Order'].dt.month
my_data.head()

# Agroup by year, month and segment and calculate aggregation statistics
insight_9 = my_data.groupby(['Year', 'Month', 'Segment'])['Sales_Value'].agg([np.sum, np.mean, np.median])
insight_9

# Extract the nivels
years = insight_9.index.get_level_values(0)
months = insight_9.index.get_level_values(1)
segments = insight_9.index.get_level_values(2)

# Plot
plt.figure(figsize = (12, 6))
sns.set()
fig1 = sns.relplot(kind = 'line', data =insight_9, y = 'mean', x = months, hue = segments, col = years, col_wrap = 4)
plt.show()



### Insight 10º:
### What is the Total Sales by Category and Subcategory, considering only the top 12 Subcategories?

# Agroup by category and subcategory and calculate the sum for numeric variables
insight_10 = my_data.groupby(['Category','Subcategory']).sum(numeric_only = True).sort_values('Sales_Value', ascending = False).head(12)
insight_10 = insight_10[['Sales_Value']].astype(int).sort_values(by= 'Category').reset_index()
insight_10

# Dataframe with totals by category
insight_10_cat = insight_10.groupby('Category').sum(numeric_only= True).reset_index()
insight_10_cat

# Colors for categories
category_colors = ['#5d00de', '#0ee84f', '#e80e27']

# Colors for subcategories
subcategory_colors = ['#aa8cd4', '#aa8cd5','#aa8cd6', '#aa8cd7', '#26c957', '#26c958', '#26c959', '#26c960','#e65e65', '#e65e66', '#e65e67', '#e65e68']

# Plot
fig, ax = plt.subplots(figsize = (18,12))
p1 = ax.pie(insight_10_cat['Sales_Value'], radius = 1, labels = insight_10_cat['Category'], wedgeprops = dict(edgecolor = 'white'), colors = category_colors)
p2 = ax.pie(insight_10['Sales_Value'], radius = 0.9, labels = insight_10['Subcategory'], autopct = autopct_format(insight_10['Sales_Value']), colors = subcategory_colors, labeldistance = 0.7, wedgeprops = dict(edgecolor = 'white'), pctdistance = 0.53, rotatelabels = True)
centre_circle = plt.Circle((0, 0), 0.6, fc = 'white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.annotate(text = 'Sales Total: ' + '$ ' + str(int(sum(insight_10['Sales_Value']))), xy = (-0.2, 0))
plt.title('Total Sales by Category and Top 12 Subcategories')
plt.show()