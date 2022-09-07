#!/usr/bin/env python
# coding: utf-8

# In[126]:


import numpy as np
import pandas as pd





def mean_ret_A(data,duration):
    """
    Function returns tha annualized mean of the data
    Parameters:
    data: Time series of the return data
    duration: Frequency of the time series
    
    """
        
    if duration == "M":
        return 12*np.mean(data)
    elif duration == "D":
        return 252*np.mean(data)
    elif duration == "W":
        return 52*np.mean(data)
    elif duration == "Y":
        return np.mean(data)
        


# In[80]:


def sd_ret_A(data,duration):
    """
    Function returns tha annualized standard deviation of the data
    Parameters:
    data: Time series of the return data
    duration: Frequency of the time series
    
    """
    if duration == "M":
        return np.sqrt(12)*np.std(data)
    elif duration == "D":
        return np.sqrt(252)*np.std(data)
    elif duration == "W":
        return np.sqrt(52)*np.std(data)
    elif duration == "Y":
        return np.std(data)


# In[81]:


def sharpe_ratio_a(data,duration, rf=0):
    """
    Function returns tha annualized sharpe ratio of the data
    Parameters:
    data: Time series of the return data
    duration: Frequency of the time series
    rf: Risk free rate for the period
    
    """
    return (mean_ret_A(data,duration)-rf)/sd_ret_A(data,duration)


# In[105]:


def max_ddwn(data):
    
    """
    Function returns tha maximum drawdown of a strategy for a given time period
    Parameters:
    data: Time series of the return data    
    """
    
    wealth_indx = np.cumprod(1+data)
    previous_peaks = np.maximum.accumulate(wealth_indx)
    drawdown = (wealth_indx-previous_peaks)/previous_peaks
    return min(drawdown)


# In[50]:


def sd_ret_neg_A(data,duration):
    """
    Function returns tha annualized standard deviation of the negative returns in data
    Parameters:
    data: Time series of the return data
    duration: Frequency of the time series
    
    """
    ret_neg=[ x for x in data if x<0]
    
    if duration == "M":
        return np.sqrt(12)*np.std(ret_neg)
    elif duration == "D":
        return np.sqrt(252)*np.std(ret_neg)
    elif duration == "W":
        return np.sqrt(52)*np.std(ret_neg)
    elif duration == "Y":
        return np.std(ret_neg)


# In[115]:


def sortino_ratio(data,duration,rf=0):
    """
    Function returns tha annualized sortino ratio of the data
    Parameters:
    data: Time series of the return data
    duration: Frequency of the time series
    rf: Risk free rate for the period
    
    """
    return (mean_ret_A(data,duration)-rf)/sd_ret_neg_A(data,duration)


# In[ ]:

def holding_return(data):
    """
    Function returns the holding period retun of the data
    Parameters:
    data: Time series of the return data
    
    """
    return((1+data).cumprod()[-1]-1)  

def turnover(data):
    """
    Function returns the portfolio turnover
    Paramters:
    data: Time series of the return data
    """
    c=0
    turnover = []
    for each_date in sorted(set(data['date'])):
        if c==0:
            prev_data = data[data['date']==each_date]
            c=1
            continue
        else:
            curr_data = data[data['date']==each_date]
            each_turnover = min(len(set(curr_data['cusip'].astype('str'))-set(prev_data['cusip'].astype('str'))), len(set(prev_data['cusip'].astype('str'))-set(curr_data['cusip'].astype('str'))))/len(set(prev_data['cusip'].astype('str')))
            prev_data = data[data['date']==each_date]
        turnover.append(each_turnover)

    return sum(turnover)/len(turnover)
    

def tear_sheet(data,turnover_data,freq="M"):

    """
    
    Function returns a dataframe of tear sheet on an annual basis
    Parameters:
    data: Time series of the return data
    freq: Frequency of the time series. Default steup as Monthly. Use "M" for monthly
    
    
    """

    data.loc[:,"year"]=data.iloc[:,0].apply(lambda x : x.year)

    unique_years=data["year"].unique().tolist()

    tear_sheet=[]
    
    for x in unique_years:
        cumm_yrs_data = data[data["year"]<=x].iloc[:,1].values
        yrs_data=data[data["year"]==x].iloc[:,1].values
        trnovr_data=turnover_data[turnover_data["fyear"]==x]
        ## Assigning Variables to Components of tear sheet
        a = mean_ret_A(yrs_data, freq)
        b = sd_ret_A(yrs_data, freq )
        c = holding_return(yrs_data)
        d = holding_return(cumm_yrs_data)
        e = sharpe_ratio_a(yrs_data,freq, 0.02)
        f = sortino_ratio(yrs_data, freq, 0.02)
        g = max_ddwn(yrs_data)
        h = turnover(trnovr_data)

        tear_sheet.append([x,a,b,c,d,e,f,g,h])
    
    tear_sheet=np.array(tear_sheet)

    tear_sheet_disp=pd.DataFrame(data=tear_sheet, columns=["Year", "Mean Monthly Return", "Volatility", "Yearly Return", "Cummulative Return","Sharpe", "Sortino", "Max Drawdown", "Turnover"],)

    tear_sheet_disp["Year"]=tear_sheet_disp["Year"].astype("int64")

    return tear_sheet_disp
    


