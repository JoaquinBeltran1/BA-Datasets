from typing import List
from datetime import datetime
from dateutil.relativedelta import relativedelta

import pandas as pd
import numpy as np

# Quarterly user growth
QAURTERS = [ (120, 40, 28, 24), (45, 35, 36, 23), (27, 14, 7, 3)]

def monthly_growth(years: List):
    """
    For each quarter, divide its growth by 3,
    this new value to be assigned to each month

    Return a dict with month_number, growth_per_month
    """
    monthly_percentage = []
    for quarters in years:
        for quarter in quarters:
            each_month = (quarter / 3) / 100            
            monthly_percentage.append([each_month, each_month, each_month])
            
    growth_per_month = [i for sublist in monthly_percentage for i in sublist]
    
    months = []
    for i in enumerate(growth_per_month):
        months.append(f"month_{ i[0] + 1}")
        
    dict_from_list = dict(zip(months, growth_per_month))
    return dict_from_list

def monthly_users(data):
    """
    Create a DataFrame with 4 columns
    - Month_name
    - Monhtly growth
    - Accumulated users, 
    - New monthly users

    Users for the first month = 45
    """
    dataframe = pd.DataFrame(data.items(), columns=['Month', 'MonthlyGrowth'])
    dataframe["TotalUsers"] = 0
    dataframe["NewUsers"] = 0

    for i, val in enumerate(dataframe["TotalUsers"]):
        if i == 0:
            dataframe.iat[i, 2] = 45
            dataframe.iat[i, 3] = 45
        
        else:
            # Total users
            dataframe.iat[i,2] = int(dataframe.iloc[i-1][2] * dataframe.iloc[i-1][1] + dataframe.iloc[i-1][2])
            # New monthly users
            dataframe.iat[i,3] = int(dataframe.iloc[i][2] - dataframe.iloc[i-1][2])
    return(dataframe)

def add_date_column(dataframe):
    """
    Add a new column to the DataFrame.

    Give a real date to each row.
    Start time = July, 2018
    """
    months = dataframe["Month"]
    dates = []
    start = datetime(2018, 7, 1)
    one_more_month = relativedelta(months=1)

    for i, val in enumerate(months):
        if i == 0:
            dates.append(start)
        
        else:
            new_month = dates[i-1] + one_more_month
            dates.append(new_month)

    dataframe["Date"] = dates
    return dataframe

def new_users_per_day(dataframe):
    """
    Given real months, get business days for each one.

    Then, for each month assign a number of new customers per day,
    that follow a normal distribution:

    np.random.normal(mu, sigma, size)

    Where:
    - mu is the mean of new customer per day
    in a month.
    - sigma is the standard deviation.
    - size is the number of business day in each month

    Then flatten all months into a list, round them, and convert
    to 0 all negative numbers.
    """
    full = []
    for i in range(len(dataframe["NewUsers"])):
        if i <= 34:
            s = list(np.random.normal(
                dataframe["NewUsers"][i] / len(pd.bdate_range(start=dataframe["Date"][i], end=dataframe["Date"][i + 1], inclusive="left")), 1,
                len(pd.bdate_range(start=dataframe["Date"][i], end=dataframe["Date"][i + 1], inclusive="left"))))
        elif i == 35:
            s = list(np.random.normal(dataframe["NewUsers"][i] / len(pd.bdate_range(start=dataframe["Date"][i], end=dataframe["Date"][i] + pd.tseries.offsets.MonthEnd(1))), 1, 
                          len(pd.bdate_range(start=dataframe["Date"][i], end=dataframe["Date"][i] + pd.tseries.offsets.MonthEnd(1)))))
        full.append(s)
        flat_full = [i for sublist in full for i in sublist]
        rounded = [round(i) for i in flat_full]
        
        for i in range(len(rounded)):
            if rounded[i] < 0:
                rounded[i] = 0
    return rounded

def bdays_in_period(dataframe):
    """
    Get list of real dates for each busines day in our period.
    Do it by month.
    """
    days = []
    for i in range(len(dataframe)):
        if i <= 34:
            days.append(list(pd.bdate_range(start=dataframe["Date"][i], end=dataframe["Date"][i+1], inclusive="left")))
        else:
            days.append(list(pd.bdate_range(start=dataframe["Date"][i], end=dataframe["Date"][35] + pd.tseries.offsets.MonthEnd(1))))
            
    flat_list = [i for sublist in days for i in sublist]
    return flat_list

def conc_days_users(days: List, users: List):
    """"
    Create a DataFrame with two columns:
    - days
    - new users per day
    """
    dataset = pd.DataFrame(data = {"Date": days, "NewDailyUsers": users})
    return dataset

def dataset_1_v1(dataset):
    """
    Extract dates in the right format.
    Store in a list.
    """
    dates = []
    for i in dataset["Date"]:
        dates.append(i.strftime('%d/%m/%Y'))
    
    """
    Create list of users.

    For each user, create a string user_i.
    Store in a list.
    """
    users = dataset["NewDailyUsers"].to_list()
    list_users = []
    for i in range(sum(users)):
        list_users.append("user_" + str(i))
    
    """
    For each user in list_users,
    i is the number of users for a particular day,
    so we append as many users from list_users,
    as that i says.

    Delete those used users, so that we
    use them all.
    """
    new_list = []
    for i in users:
        new_list.append(list_users[:i])
        del list_users[:i] # Super important, otherwise the names reset to person_1, at each date
    
    """
    Create a dict with the date, # of users for that date,
    and the user/s for that date.
    """
    final_dict= {}
    for i, (a, b, c) in enumerate(zip(dates, users, new_list)):
        final_dict[i] = (a, b, c)

    """
    Create a new dict with two columns.
    Each row is a user and a date.
    """
    keys = []
    values = []
    for key, value in final_dict.items():
        for item in value[2]:
            keys.append(item)
            values.append(value[0])
    final_final_dict = dict(zip(keys, values))

    return final_final_dict

def get_firstname(data, users_dict)->List:
    names_dataset = pd.read_csv(data, delimiter=";")

    m_prenoms = names_dataset[names_dataset.sexe == 1]
    f_prenoms = names_dataset[names_dataset.sexe == 2]

    # Selecting ages between 19 and 62
    mask_m = (m_prenoms['annais'] >= '1960') & (m_prenoms['annais'] <= '2003')
    mask_f = (f_prenoms['annais'] >= '1960') & (f_prenoms['annais'] <= '2003')
    m_prenoms_right_age = m_prenoms.loc[mask_m]
    f_prenoms_right_age = f_prenoms.loc[mask_f]

    # Dropping PRENOMS RARES
    m_prenoms_right_age = m_prenoms_right_age[m_prenoms_right_age['preusuel'] != '_PRENOMS_RARES']
    f_prenoms_right_age = f_prenoms_right_age[f_prenoms_right_age['preusuel'] != '_PRENOMS_RARES']

    ### Adding column with probability for each name
    total_m = sum(m_prenoms_right_age["nombre"])
    total_f = sum(f_prenoms_right_age["nombre"])

    probas_m = []
    for i in range(len(m_prenoms_right_age)):
        probas_m.append(m_prenoms_right_age.iat[i,3] / total_m)
    
    probas_f = []
    for i in range(len(f_prenoms_right_age)):
        probas_f.append(f_prenoms_right_age.iat[i,3] / total_f)

    m_prenoms_right_age["probas"] = probas_m
    f_prenoms_right_age["probas"] = probas_f

    ### Assigning FirstName

    m_f = [1, 2]
    m_f_probs = [0.6, 0.4]
    
    first_name = []
    for i in users_dict:
        user_m_f = np.random.choice(m_f, p = m_f_probs)
        if user_m_f == 1:
            first_name.append(np.random.choice(m_prenoms_right_age["preusuel"], p=probas_m))
        else:
            first_name.append(np.random.choice(f_prenoms_right_age["preusuel"], p=probas_f))
    
    return first_name

def get_lastname(data, list_first_name):
    """
    """
    noms = pd.read_csv(data, sep='\t')
    noms.drop(['_1891_1900',
           '_1901_1910',
           '_1911_1920',
           '_1921_1930',
           '_1931_1940',
           '_1941_1950',
           '_1951_1960']
          , axis=1
          , inplace=True
          )
    noms = noms.drop(218982) # AUTRES NOMS
    noms['Noms Total']= noms.iloc[:, 1:].sum(axis=1) # Total for all decades
    noms = noms[["NOM", "Noms Total"]] # Only keep LastName and Total

    ### Assign probability to each LastName
    total_noms = sum(noms["Noms Total"])
    probas_noms = []
    for i in range(len(noms)):
        probas_noms.append(noms.iat[i,1] / total_noms)
    
    noms["Probas Noms"] = probas_noms # Add column with probability

    ### Give LastName
    last_name = []
    for i in range(len(list_first_name)):
        last_name.append(np.random.choice(noms["NOM"], p=noms["Probas Noms"]))
    
    dataset = pd.DataFrame(list_first_name, columns=["FirstName"])
    dataset["LastName"] = last_name
    return dataset

def full_name_date(full_name, dates):
    full_name["Date"] = dates.values()
    return full_name
