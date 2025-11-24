#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import plotly.express as px


# In[2]:


df = pd.read_excel("C:/Users/grawo/OneDrive/Desktop\Project/financial_loan.xlsx")

df.head()


# In[3]:


print("Total Rows:", df.shape[0])


# In[4]:


print("Total Column:", df.shape[1])


# In[5]:


df.info()


# In[6]:


df.describe()


# In[7]:


df.dtypes


# ### Total Loan Application

# In[8]:


total_loan_application = df['id'].count()
print("total_loan_application:", total_loan_application)


# ###  Month to Date Total Loan Application

# In[9]:


latest_issue_date = df['issue_date'].max()
latest_year = latest_issue_date.year
latest_month = latest_issue_date.month

mtd_data = df[(df['issue_date'].dt.year == latest_year) & (df['issue_date'].dt.month == latest_month)]

mtd_loan_application = mtd_data['id'].count()

print(f"MTD Loan Application (for {latest_issue_date.strftime('%B %Y')}):{mtd_loan_application}")


# ### Total Funded Amount

# In[10]:


total_funded_amount = df['loan_amount'].sum()

total_funded_amount_millions = total_funded_amount / 1000000

print("Total Funded Amount: £{:.2f}M" . format(total_funded_amount_millions))


# ### Month to Date Total Funded Amount

# In[11]:


latest_issue_date = df['issue_date'].max()
latest_year = latest_issue_date.year
latest_month = latest_issue_date.month

mtd_data = df[(df['issue_date'].dt.year == latest_year) & (df['issue_date'].dt.month == latest_month)]

mtd_total_funded_amount = mtd_data['loan_amount'].sum()
mtd_total_funded_amount_millions = mtd_total_funded_amount / 1000000

print("MTD Funded Amount: £{:.2f}M".format(mtd_total_funded_amount_millions))


# ### Total Amount Received

# In[12]:


total_amount_received = df['total_payment'].sum()

total_amount_received_millions = total_amount_received / 1000000

print("Total Amount Received: £{:.2f}M" . format(total_amount_received_millions))


# ### Month to Date Total Amount Received

# In[13]:


latest_issue_date = df['issue_date'].max()
latest_year = latest_issue_date.year
latest_month = latest_issue_date.month

mtd_data = df[(df['issue_date'].dt.year == latest_year) & (df['issue_date'].dt.month == latest_month)]

mtd_total_amount_received = mtd_data['total_payment'].sum()
mtd_total_amount_received_millions = mtd_total_amount_received / 1000000
print("MTD Amount Received: £{:.2f}M".format(mtd_total_amount_received_millions))


# ### Average Interest Rate

# In[14]:


average_interest_rate = df['int_rate'].mean()*100

print("Avg Int Rate: {:.2f}%".format(average_interest_rate) )


# ### Average Debt-to-Income Ratio (DTI)

# In[15]:


average_dti_rate = df['dti'].mean()*100

print("Avg DTI: {:.2f}%".format(average_dti_rate) )


# ### Good Loan Metrics

# In[16]:


good_loan = df[df['loan_status'].isin(["Fully Paid", "Current"])]

total_loan_appliction = df['id'].count()

good_loan_application = good_loan['id'].count()
good_loan_funded_amount = good_loan['loan_amount'].sum()
good_loan_received = good_loan['total_payment'].sum()

good_loan_funded_amount_millions = good_loan_funded_amount / 1000000
good_loan_received_millions = good_loan_received / 1000000

good_loan_percentage = (good_loan_application / total_loan_application) * 100

print("Good Loan Application:" , good_loan_application)
print("Good Loan Funded Amount (in Millions): £{:.2f}M".format(good_loan_funded_amount_millions))
print("Good Loan Total Received (in Millions): £{:.2f}M".format(good_loan_received_millions))
print("Percentage of Good Loan Application: {:.2f}%".format(good_loan_percentage))


# ###  Bad Loan Metrics

# In[17]:


bad_loan = df[df['loan_status'].isin(["Charged Off"])]

total_loan_appliction = df['id'].count()

bad_loan_application = bad_loan['id'].count()
bad_loan_funded_amount = bad_loan['loan_amount'].sum()
bad_loan_received = bad_loan['total_payment'].sum()

bad_loan_funded_amount_millions = bad_loan_funded_amount / 1000000
bad_loan_received_millions = bad_loan_received / 1000000

bad_loan_percentage = (bad_loan_application / total_loan_application) * 100

print("Bad Loan Application:" , bad_loan_application)
print("Bad Loan Funded Amount (in Millions): £{:.2f}M".format(bad_loan_funded_amount_millions))
print("Bad Loan Total Received (in Millions): £{:.2f}M".format(bad_loan_received_millions))
print("Percentage of Good Loan Application: {:.2f}%".format(bad_loan_percentage))


# ### Monthly Trend By Issue Date for Total Funded Amount

# In[18]:


monthly_funded = (
    df.sort_values('issue_date')
    .assign(month_name=lambda x: x['issue_date'].dt.strftime('%b %Y'))
    .groupby('month_name' , sort=False)['loan_amount']
    .sum()
    .div(1_000_000)
    .reset_index(name='loan_amount_millions')
)

plt.figure(figsize=(10 , 5))
plt.fill_between (monthly_funded['month_name'], monthly_funded['loan_amount_millions'], color='pink', alpha=0.5)
plt.plot(monthly_funded['month_name'],monthly_funded['loan_amount_millions'],color='red' , linewidth=2)

for i, row in monthly_funded.iterrows():
    plt.text(i, row['loan_amount_millions'] + 0.1, f"{row['loan_amount_millions']:.2f}",
             ha='center' , va='bottom' , fontsize=9, rotation=0, color='black')
    
plt.title('Total Funded Amount By Month', fontsize=14)
plt.xlabel('Month')
plt.ylabel('Funded Amount(£ Millions)')
plt.xticks(ticks=range(len(monthly_funded)), labels=monthly_funded['month_name'], rotation=45)
plt.grid(True, linestyle='--',alpha=0.6)
plt.tight_layout()
plt.show()


# ### Monthly Trend by Issue Date for Total Amount Received

# In[19]:


monthly_received = (
    df.sort_values('issue_date')
    .assign(month_name=lambda x: x['issue_date'].dt.strftime('%b %Y'))
    .groupby('month_name' , sort=False)['total_payment']
    .sum()
    .div(1_000_000)
    .reset_index(name='received_amount_millions')
)

plt.figure(figsize=(10 , 5))
plt.fill_between (monthly_funded['month_name'], monthly_funded['loan_amount_millions'], color='grey', alpha=0.5)
plt.plot(monthly_funded['month_name'],monthly_funded['loan_amount_millions'],color='black' , linewidth=2)

for i, row in monthly_received.iterrows():
    plt.text(i, row['received_amount_millions'] + 0.1, f"{row['received_amount_millions']:.2f}",
             ha='center' , va='bottom' , fontsize=9, rotation=0, color='black')
    
plt.title('Total Received Amount By Month', fontsize=14)
plt.xlabel('Month')
plt.ylabel('Received Amount(£ Millions)')
plt.xticks(ticks=range(len(monthly_funded)), labels=monthly_funded['month_name'], rotation=45)
plt.grid(True, linestyle='--',alpha=0.6)
plt.tight_layout()
plt.show()


# ### Monthly Trend by Issue Date for Total Loan Applicaton

# In[20]:


monthly_application = (
    df.sort_values('issue_date')
    .assign(month_name=lambda x: x['issue_date'].dt.strftime('%b %Y'))
    .groupby('month_name' , sort=False)['id']
    .count()
    .reset_index(name='loan_application_count')
)

plt.figure(figsize=(10 , 5))
plt.fill_between (monthly_application['month_name'], monthly_application['loan_application_count'], color='purple', alpha=0.5)
plt.plot(monthly_application['month_name'],monthly_application['loan_application_count'],color='black' , linewidth=2)

for i, row in monthly_application.iterrows():
    plt.text(i, row['loan_application_count'] + 0.1, f"{row['loan_application_count']:.2f}",
             ha='center' , va='bottom' , fontsize=9, rotation=0, color='black')
    
plt.title('Total Loan Application By Month', fontsize=14)
plt.xlabel('Month')
plt.ylabel('Number of Applications')
plt.xticks(ticks=range(len(monthly_application)), labels=monthly_application['month_name'], rotation=45)
plt.grid(True, linestyle='--',alpha=0.6)
plt.tight_layout()
plt.show()


# ### Regional Analysis by State for Total Funded Amount

# In[21]:


state_funding = df.groupby('address_state')['loan_amount'].sum().sort_values(ascending=True)
state_funding_thousands = state_funding / 1000

plt.figure(figsize=(10 , 8))
bars = plt.barh(state_funding_thousands.index, state_funding_thousands.values, color='skyblue')

for bar in bars:
    width = bar.get_width()
    plt.text(width + 10, bar.get_y() + bar.get_height() / 2,
            f'{width:,.0f}k', va='center', fontsize=9)
    
plt.title('Total Funded Amount by State (in £ Thousand)')
plt.xlabel('Funded Amount (in £ Thousands)')
plt.ylabel('State')
plt.tight_layout()
plt.show()


# ### Loan Term Analysis by Total Funded Amount

# In[22]:


term_funding_millions = df.groupby('term')['loan_amount'].sum() / 1000000

plt.figure(figsize=(5,5))

plt.pie(
    term_funding_millions,
    labels=term_funding_millions.index,
    autopct=lambda p: f"{p:.1f}%\n${p*sum(term_funding_millions)/100:.1f}M",
    startangle=90,
    wedgeprops={'width' : 0.4}
)

plt.gca().add_artist(plt.Circle((0, 0), 0.70, color='white'))
plt.title("Total Funded Amount By Term (in £ Millions)")
plt.show()


# ### Employee Length by Total Funded Amount

# In[29]:


emp_funding = df.groupby('emp_length')['loan_amount'].sum().sort_values()/1000

plt.figure(figsize=(10,6))
bars = plt.barh(emp_funding.index, emp_funding, color='darkorange')

for bar in bars:
    width = bar.get_width()
    plt.text(width + 5, bar.get_y() + bar.get_height() / 2,
            f"£{width:,.0f}k", va='center' , fontsize=9)
    
plt.xlabel("Funded Amount (£ Thousands)")
plt.title("Total Funded Amount by Employment Lenght")
plt.grid(axis='x', linestyle='--' , alpha=0.5)
plt.tight_layout()
plt.show()


# ### Loan Purpose by Total Funded Amount

# In[34]:


purpose_funding = df.groupby('purpose')['loan_amount'].sum().sort_values()/1000000

plt.figure(figsize=(10,6))
bars = plt.barh(purpose_funding.index, purpose_funding, color='green')

for bar in bars:
    width = bar.get_width()
    plt.text(width + 5, bar.get_y() + bar.get_height() / 2,
            f"£{width:,.0f}M", va='center' , fontsize=9)
    
plt.xlabel("Funded Amount (£ Millions)")
plt.title("Total Funded Amount by Loan Purpose")
plt.grid(axis='x', linestyle='--' , alpha=0.5)
plt.tight_layout()
plt.show()


# ### Home ownership by Total Funded Amount

# In[39]:


home_funding = df.groupby('home_ownership')['loan_amount'].sum().reset_index()
home_funding['loan_amount_millions'] = home_funding['loan_amount'] / 1000000

fig = px.treemap(
    home_funding,
    path=['home_ownership'],
    values='loan_amount_millions',
    color='loan_amount_millions',
    color_continuous_scale='Blues',
    title='Total Funded Amount by Home Ownership (£ Millions)'
)

fig.show()


# In[ ]:





# In[ ]:




