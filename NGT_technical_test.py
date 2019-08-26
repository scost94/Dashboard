"Oussema Boujelben"
"boujelben.oussema@gmail.com"
"2019-2020"
"NGT Technical Test"

# In[    Libraries   ]

import warnings

warnings.filterwarnings('ignore')
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib import style
import datetime
import calendar

style.use('ggplot')
import firebase_admin
from firebase_admin import credentials, firestore

# In[    Directory   ]
file_path = ('C:/Users/Oussema/Desktop/test technique')  # Please specify your path here.
os.chdir(file_path)
os.listdir()
data = pd.read_csv("ngt_software_engineer_test_example_data.csv", sep=',')

# In[ Connect to FireBase ]

# Our Api is saved on our PC for security reasons, if you want to use this code on another PC,
# Comment the 2 following lines and uncomment line 41.

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)  # for better securtiy we used credentials.

# Use the following option if you are testing the code from another PC.
# firebase_admin.initialize_app(options={'databaseURL':'https://nextgatetech.firebaseio.com',})

db = firestore.client()

# Test our connection
# doc_ref = db.collection(u'users').document(u'aaaaaa')
# doc_ref.set({
#        u'username': u'oussema',
#        u'password': u'1234',
#        u'postalcode': 1471
#            })
# print('done')

# In[] ################ TASK 1 ################


# In[ ]
collection_name = 'NGT_Test'


def todate(date):
  day = datetime.datetime.strptime(date, '%d/%m/%Y').weekday()
  return (calendar.day_name[day])


# In[    Data Exploration    ]

description = data.dtypes

ref = db.collection(collection_name).document('Description')
ref.set((description.astype(str)).to_dict())

stat_det = (data.describe()).T

ref = db.collection('NGT_Test').document('Stats_Details')
ref.set(stat_det.to_dict(orient='index'))

# In[]
# In[Data Quality check(1):Missing Data(Date) & Missing Values]


# Choice: We cannot make proper analysis, statistical calculations, and even
#         predict prices if we lack data.

# Missing Dates
group_by_SubShare = data.groupby(['Subfund_ID', 'Shareclass_ID'])
missing_1 = group_by_SubShare.size()
missing_1.index = missing_1.index.map(str)
ref = db.collection(collection_name).document(u'Quality_1v11')
ref.set(missing_1.to_dict())

# missing_1.plot(kind='barh', stacked=True, figsize=[16,6], colormap='hot')

# Figure clearly shows that 2A lacks lot of data/dates.


### Missing values : nan Values
nan_res = data.isnull().values.any()

ref = db.collection(collection_name).document(u'Quality_1v2')
ref.set({"Missing values": str(nan_res)})

# msno.matrix(data)   #Uncomment to visualize on python
# msno.bar(data)      #Uncomment to visualize on python


# In[ Data Quality check (2) : Moving Average]


## Moving average, to understand the data behavior easier and analyze it.

data['coeff'] = data['NAV_Amount'] / data['NAV_Per_Share']
data['product'] = data['ISIN'].str[-2:]

# For 1 case
# plt.figure()
df = data.loc[(data['product'] == '1A')]
df['10ma'] = df['NAV_Amount'].rolling(window=10).mean()
# ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5,colspan=1)
# ax1.plot(df['Date'],df['NAV_Amount'])
# ax1.plot(df['Date'],df['10ma'])
# plt.title('Moving average for NAV_Amount per date 1A')
# plt.show()

# Moving Average to db
moving_average = df[['Date', '10ma', 'NAV_Amount']]
moving_average.index = moving_average.index.map(str)

ref = db.collection(collection_name).document(u'Quality_2')
ref.set(moving_average.to_dict('list'))

# In[Duplicated Data]


# Choice: Data can be computed twice by mistake,
#         by 2 different agents or same person ?
#         also duplicated observations can arise during data collection
#         (Combining or merging datasets from multiple sources).

dup_result = data.duplicated().values.any() == True  # No duplicated rows overall

ref = db.collection('NGT_Test').document(u'Quality_3')
ref.set({"Duplicated rows": str(dup_result)})

## check if there are duplicated values for some specific columns(NAV_Amount,
## NB_Share_Outstandings,NAV_Per_Share)


# for x in range(1,3):
#    col = data.iloc[:, x]
#    if (col.duplicated().values.any() == True):
#        duplicateRowsDF = col[col.duplicated()]
#        print("There are some duplicated values for col n° = %d"%x)
#        print("Duplicate values except first occurrence based on all columns are :")
##        print(duplicateRowsDF) #uncomment to show the duplicated values
#        break
#    print("No duplicated values found for column %d"%x)


# In[Coefficients of Similarity NAV_Amount/Nav_Per_Share]

data['coeff'] = data['NAV_Amount'] / data['NAV_Per_Share']
data['product'] = data['ISIN'].str[-2:]

temp = pd.DataFrame([data['coeff'], data['product'], data['Date']]).T

temp.set_index('Date', inplace=True)

# prod1A = temp[temp['product']=='1A']['coeff'].reset_index(drop=True)
# prod1B = temp[temp['product']=='1B']['coeff'].reset_index(drop=True)
prod1C = temp[temp['product'] == '1C']['coeff'].reset_index(drop=True)
prod1D = temp[temp['product'] == '1D']['coeff'].reset_index(drop=True)
# prod2A = temp[temp['product']=='2A']['coeff'].reset_index(drop=True)
prod2B = temp[temp['product'] == '2B']['coeff'].reset_index(drop=True)
# prod2C = temp[temp['product']=='2C']['coeff'].reset_index(drop=True)
# prod2D = temp[temp['product']=='2D']['coeff'].reset_index(drop=True)
# prod2E = temp[temp['product']=='2E']['coeff'].reset_index(drop=True)
# prod3A = temp[temp['product']=='3A']['coeff'].reset_index(drop=True)
# prod3B = temp[temp['product']=='3B']['coeff'].reset_index(drop=True)

# Finalprod = {'1A':prod1A,'1B':prod1B,'1C':prod1C,'1D':prod1D,'2A':prod2A,'2B':prod2B,'2C':prod2C,
#             '2D':prod2D,'2E':prod2E,'3A':prod3A,'3B':prod3B}

Finalprod = {'1C': prod1C, '1D': prod1D, '2B': prod2B}  # Example
df = pd.DataFrame(Finalprod)
df['Date'] = data['Date']

ref = db.collection('NGT_Test').document(u'Coeff_line')
ref.set(df.to_dict('list'))

############-----------------############
############-----------------############
############-----------------############

temp = pd.DataFrame([data['coeff'], data['product']]).T

prod1A = temp[temp['product'] == '1A']['coeff'].reset_index(drop=True)
prod1B = temp[temp['product'] == '1B']['coeff'].reset_index(drop=True)
prod1C = temp[temp['product'] == '1C']['coeff'].reset_index(drop=True)
prod1D = temp[temp['product'] == '1D']['coeff'].reset_index(drop=True)
prod2A = temp[temp['product'] == '2A']['coeff'].reset_index(drop=True)
prod2B = temp[temp['product'] == '2B']['coeff'].reset_index(drop=True)
prod2C = temp[temp['product'] == '2C']['coeff'].reset_index(drop=True)
prod2D = temp[temp['product'] == '2D']['coeff'].reset_index(drop=True)
prod2E = temp[temp['product'] == '2E']['coeff'].reset_index(drop=True)
prod3A = temp[temp['product'] == '3A']['coeff'].reset_index(drop=True)
prod3B = temp[temp['product'] == '3B']['coeff'].reset_index(drop=True)

Finalprod = {'1A': prod1A, '1B': prod1B, '1C': prod1C, '1D': prod1D, '2A': prod2A, '2B': prod2B, '2C': prod2C,
             '2D': prod2D, '2E': prod2E, '3A': prod3A, '3B': prod3B}

# Finalprod = {'1B':prod1B,'3A':prod1A}

df = pd.DataFrame(Finalprod)

ref = db.collection('NGT_Test').document(u'Coeff_box')
ref.set(df.to_dict('list'))

# plt.scatter(temp['product'],temp['coeff'],color = 'red') #Uncomment to plot

# Additional data quality checks: data format should be human/machine readable.


# In[]
# In[Data Quality check (3):Coefficients of Similarity NAV_Amount/Nav_Per_Share]

data['coeff'] = data['NAV_Amount'] / data['NAV_Per_Share']
data['product'] = data['ISIN'].str[-2:]

temp = pd.DataFrame([data['coeff'], data['product']]).T

# temp.set_index('product',inplace=True)


prod1A = temp[temp['product'] == '1A']['coeff'].reset_index(drop=True)
# prod1B = temp[temp['product']=='1B']['coeff'].reset_index(drop=True)
# prod1C = temp[temp['product']=='1C']['coeff'].reset_index(drop=True)
# prod1D = temp[temp['product']=='1D']['coeff'].reset_index(drop=True)
prod2A = temp[temp['product'] == '2A']['coeff'].reset_index(drop=True)
# prod2B = temp[temp['product']=='2B']['coeff'].reset_index(drop=True)
# prod2C = temp[temp['product']=='2C']['coeff'].reset_index(drop=True)
# prod2D = temp[temp['product']=='2D']['coeff'].reset_index(drop=True)
# prod2E = temp[temp['product']=='2E']['coeff'].reset_index(drop=True)
prod3A = temp[temp['product'] == '3A']['coeff'].reset_index(drop=True)
# prod3B = temp[temp['product']=='3B']['coeff'].reset_index(drop=True)

# Finalprod = {'1A':prod1A,'1B':prod1B,'1C':prod1C,'1D':prod1D,'2A':prod2A,'2B':prod2B,'2C':prod2C,
#             '2D':prod2D,'2E':prod2E,'3A':prod3A,'3B':prod3B}

Finalprod = {'1A': prod1A, '2A': prod2A, '3A': prod3A}

df = pd.DataFrame(Finalprod)
ref.set(df.to_dict('list'))

plt.scatter(temp.index, temp['coeff'], color='red')
temp.index = temp.index.map(str)

ref = db.collection('NGT_Test').document(u'ZZZ')
ref.set(temp.to_dict('list'))

# Additional data quality checks: data format should be human/machine readable.
# In[]

#### Data behiavor Analysis, for detecting suspicious values. (Maybe they are
#### in wrong structural, we don't have deep knowledge on the finance domain so
#### maybe the NAV value should be in some specific range for certain products.)
#### So if it is the case, we can fix its structural errors or put it in the right
#### format for a better "accuracy" !!!


# specify product for easier visualization and analysis based on the ISIN
data['Week'] = data.apply(lambda x: todate(x['Date']), axis=1)
data['product'] = data['ISIN'].str[-2:]

# Easier understanding and better manipulation of our data (Subfunds - ShareClass)
product = ['1A', '1B', '1C', '1D', '2A', '2B', '2C', '2D', '2E', '3A', '3B']  # We can optimize this
dataframe_collection = {}
for prod in product:
  dataframe_collection[prod] = pd.DataFrame(data.loc[(data['product'] == prod)])

# In[ Others:   Data Visualization   ]


## Data Analysis per day


# plot_num = 1
# for name in dataframe_collection:
#    plt.figure()
#    fig = pylab.gcf()
#    fig.canvas.set_window_title('NAV per Week for %s'%name)
#    t = time.sleep(0.3)
#    plt.scatter(dataframe_collection[name]['Week'],dataframe_collection[name]['NAV_Amount'],color = 'red')
#    plt.legend(loc=0,ncol=4)
#    plt.title('%d value captured for the product %s'%(dataframe_collection[name].shape[0],name), size=18)
#    plot_num += 1
##    if(plot_num == 3):
##        break
#    plt.xlabel('Day of the Week')
#    plt.ylabel('NAV_Amount')
#    t = time.sleep(0.3)


## Data Analysis per Date


# for name in dataframe_collection:
#    plt.figure()
#    fig = pylab.gcf()
#    fig.canvas.set_window_title('NAV per Date for %s'%name)
#    t = time.sleep(0.3)
#    plt.plot(dataframe_collection[name]['Date'],dataframe_collection[name]['NAV_Amount'],color = 'red')
#    plt.legend(loc=0,ncol=4)
#    plt.title('%d value captured for the product %s'%(dataframe_collection[name].shape[0],name), size=18)
#    plt.xlabel('Date')
#    plt.ylabel('NAV_Amount')
#    t = time.sleep(0.3)


# In[Moving average]


## Moving average for


# for name in dataframe_collection:
#    plt.figure()
#    fig = pylab.gcf()
#    fig.canvas.set_window_title('Moving Average for %s'%name)
#    t = time.sleep(0.3)
#    df1 = dataframe_collection[name]
#    df1['10ma'] = dataframe_collection[name]['NAV_Amount'].rolling(window=10).mean()
#    ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5,colspan=1)
#    ax1.plot(df1['Date'],df1['NAV_Amount'])
#    ax1.plot(df1['Date'],df1['10ma'])
#    plt.title(('Moving Average for %s'%name), size=18)
#    plt.xlabel('Date')
#    plt.ylabel('NAV_Amount')
#    plt.legend(loc=0,ncol=4)
#    t = time.sleep(0.3)


# In[ Others ]
### Boxplot to check NAV Range, if there are any suspicious values.

# boxplot per figure
# for name in dataframe_collection:
#    plt.figure()
#    fig = pylab.gcf()
#    fig.canvas.set_window_title('NAV_Amount Boxplot for %s'%name)
#
#    sns.boxplot(data=((data.loc[(data['product'] == name)]).reset_index())['NAV_Amount'])
#    plt.title(('Boxplot for %s'%name), size=18)
#    t = time.sleep(0.3)
#    break
#

# In[ Others  ]
### All boxplots same figure


# fig = pylab.gcf()
# fig.canvas.set_window_title('NAV Boxplot for every Subshare')
# plt.title('NAV Boxplot for every Subshare')
# fig = plt.figure(1, figsize=(9, 6))
# ax = fig.add_subplot(111)
# a1 =dataframe_collection['1A']['NAV_Amount']
# a2 =dataframe_collection['1B']['NAV_Amount']
# a3 =dataframe_collection['1C']['NAV_Amount']
# a4 =dataframe_collection['1D']['NAV_Amount']
# a5 =dataframe_collection['2A']['NAV_Amount']
# a6 =dataframe_collection['2B']['NAV_Amount']
# a7 =dataframe_collection['2C']['NAV_Amount']
# a8 =dataframe_collection['2D']['NAV_Amount']
# a9 =dataframe_collection['2E']['NAV_Amount']
# a10 =dataframe_collection['3A']['NAV_Amount']
# a11 =dataframe_collection['3B']['NAV_Amount']
# plt.boxplot([a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11])
# ax.set_xticklabels(['1A','1B','1C','1D','2A','2B','2C','2D','2E','3A','3B'])


# Note: we can add other analysis visualization figures, like histogram where
#       we can compare distribution of data, and more.

# In[] ################ TASK 2 ################


# To calculate the correlation, we need to understand which currency is used
# for each variable, so to really understand the correlation between variables,
# and discover any complex relation between them, we need to make sure that
# they are using the same currency or same measure unit.
# For our case, we do not have any idea on each variable currency as we are
# not specialized in finance, but we will do the simple correlation calculation
# supposing that all values are using same currency (else we just conver them
# by multiplying values by the appropriate factor and conver them all to EUR)


# In[]

######################### Dealing with Missing Data #########################
# Since we managed to identify some missing rows/data for 2A, we are going
# to add these values using the mean function of the available values.
# (if we had enough data we could use machine learning maybe to predict it)

# In[ Step 1]
#### Filling 2A

# Extract Datelist and merge data based on Data, then we refill nan values
datelist = dataframe_collection['1A']['Date']

dataframe_collection['2A'] = dataframe_collection['2A'].merge(datelist,
                                                              on='Date', how='outer')

# test=test.interpolate(method ='linear', limit_direction ='forward')
# test.fillna(test.mean(), inplace=True) # filling with mean


## filling a missing value with previous ones (faster and reasonable)
dataframe_collection['2A'] = dataframe_collection['2A'].fillna(method='pad')

# we picked the last filling method as we noticed that there have been a huge
# decrease in the NAV Value in the last days, so based on the hypothesis that
# the NAV will remain low or stable.

#### Filling 3A & 3B
dataframe_collection['3A'] = dataframe_collection['3A'].append(pd.Series(),
                                                               ignore_index=True)
dataframe_collection['3B'] = dataframe_collection['3B'].append(pd.Series(),
                                                               ignore_index=True)
dataframe_collection['3A'] = dataframe_collection['3A'].fillna(method='pad')
dataframe_collection['3B'] = dataframe_collection['3B'].fillna(method='pad')

# In[ Step 2]
#### Calculate Correlation between the 11 Shareclass for the NAV Amount.

NAV_corr = pd.DataFrame(index=datelist)
NAV_corr = pd.DataFrame()
NAV_corr['Date'] = datelist

NAV_corr['NAV_Per_Share_1A'] = (dataframe_collection['1A']['NAV_Per_Share']).values
NAV_corr['NAV_Per_Share_1B'] = (dataframe_collection['1B']['NAV_Per_Share']).values
NAV_corr['NAV_Per_Share_1C'] = (dataframe_collection['1C']['NAV_Per_Share']).values
NAV_corr['NAV_Per_Share_1D'] = (dataframe_collection['1D']['NAV_Per_Share']).values
NAV_corr['NAV_Per_Share_2A'] = (dataframe_collection['2A']['NAV_Per_Share']).values
NAV_corr['NAV_Per_Share_2B'] = (dataframe_collection['2B']['NAV_Per_Share']).values
NAV_corr['NAV_Per_Share_2AC'] = (dataframe_collection['2C']['NAV_Per_Share']).values
NAV_corr['NAV_Per_Share_2D'] = (dataframe_collection['2D']['NAV_Per_Share']).values
NAV_corr['NAV_Per_Share_2E'] = (dataframe_collection['2E']['NAV_Per_Share']).values
NAV_corr['NAV_Per_Share_3A'] = (dataframe_collection['3A']['NAV_Per_Share']).values
NAV_corr['NAV_Per_Share_3B'] = (dataframe_collection['3B']['NAV_Per_Share']).values

# Now we can run the correlation between each pair of equities
corr_df = NAV_corr.corr()
corr_df.head().reset_index()
del corr_df.index.name

ref = db.collection(collection_name).document(u'Correlatin_NAV_Per_Share')
ref.set(corr_df.to_dict('list'))

# heatmap for correlation visualization

# mask = np.zeros_like(corr_df)
# mask[np.triu_indices_from(mask)] = True
# sns.heatmap(corr_df, cmap='RdYlGn', vmax=1.0, vmin=-1.0 , mask = mask, linewidths=2.5)
# plt.yticks(rotation=0)
# plt.xticks(rotation=90)
# plt.show()


# Positive Correlation: both variables change in the same direction.
# Neutral Correlation: No relationship in the change of the variables.
# Negative Correlation: variables change in opposite directions.
# In[The end - 24/08/2019]
