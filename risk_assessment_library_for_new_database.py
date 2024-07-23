import math
import pandas as pd
import csv
import numpy as np
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import math
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import datetime,timedelta
# from numba import jit, cuda
import numpy as np
import yfinance as yf
from pandas_datareader import data as pdr
# from fake_useragent import UserAgent
from datetime import datetime
import requests
import urllib.parse
import requests 
import urllib

current_datetime = datetime.now().strftime("%Y-%m-%d")
print(current_datetime)


## use webdriver for firefox

class YFinance:
    user_agent_key = "User-Agent"
    user_agent_value = ("Mozilla/5.0 (Windows NT 6.1; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/58.0.3029.110 Safari/537.36")
    
    def __init__(self, ticker):
        self.yahoo_ticker = ticker

    def __str__(self):
        return self.yahoo_ticker

    def _get_yahoo_cookie(self):
        cookie = None

        headers = {self.user_agent_key: self.user_agent_value}
        response = requests.get("https://fc.yahoo.com",
                                headers=headers,
                                allow_redirects=True)

        if not response.cookies:
            raise Exception("Failed to obtain Yahoo auth cookie.")

        cookie = list(response.cookies)[0]

        return cookie

    def _get_yahoo_crumb(self, cookie):
        crumb = None

        headers = {self.user_agent_key: self.user_agent_value}

        crumb_response = requests.get(
            "https://query1.finance.yahoo.com/v1/test/getcrumb",
            headers=headers,
            cookies={cookie.name: cookie.value},
            allow_redirects=True,
        )
        crumb = crumb_response.text

        if crumb is None:
            raise Exception("Failed to retrieve Yahoo crumb.")

        return crumb

    @property
    def info(self):
        # Yahoo modules doc informations :
        # https://cryptocointracker.com/yahoo-finance/yahoo-finance-api
        cookie = self._get_yahoo_cookie()
        crumb = self._get_yahoo_crumb(cookie)
        info = {}
        ret = {}

        headers = {self.user_agent_key: self.user_agent_value}

        yahoo_modules = ("summaryDetail,"
                         "financialData,"
                         "indexTrend,"
                         "defaultKeyStatistics")

        url = ("https://query1.finance.yahoo.com/v10/finance/"
               f"quoteSummary/{self.yahoo_ticker}"
               f"?modules={urllib.parse.quote_plus(yahoo_modules)}"
               f"&ssl=true&crumb={urllib.parse.quote_plus(crumb)}")

        info_response = requests.get(url,
                                     headers=headers,
                                     cookies={cookie.name: cookie.value},
                                     allow_redirects=True)

        info = info_response.json()
        info = info['quoteSummary']['result'][0]

        for mainKeys in info.keys():
            for key in info[mainKeys].keys():
                if isinstance(info[mainKeys][key], dict):
                    try:
                        ret[key] = info[mainKeys][key]['raw']
                    except (KeyError, TypeError):
                        pass
                else:
                    ret[key] = info[mainKeys][key]

        return ret

class risk_assessment:
    alpha = 2/15
    ema_value=30
    price =0
    date =0
    date_14=0
    k_value = 50 
    list_of_date = []
    list_of_ending_price = []
    list_of_opening_price = []
    rsv_list=[]
    d_value = 50 
    k_list= []
    d_list = []
    MFI_list=[]
    list_of_maximum_price = [] 
    list_of_minimum_price = [] 
    sum_of_postive_ema_value =0
    sum_of_negative_ema_value =0
    list_of_volume_of_exchange=[]
    list_of_rate_of_change=[]
    list_after_editing = [] 
    list_of_volume_of_exchange_hand=[]
    list_of_rate_of_change_in_float=[]
    up = []
    down=[]
    ema_list= [] 
    ema_up =0 
    ema_down= 0
    rsi_list = []
    W_list=[]
    W_value = 0 
    a=0
    mfr=0
    comparing_date_purchase = []
    comparing_date_sell_off = []  
    strings=[]
    x=0
    actual_purchase = [] 
    actual_sell_off=[] 
    removal =0
    actual_actual_purchase =[]
    total_cost = []
    total_revenue =[]
    elasped_day = []
    number_of_trade = 0
    total_cost_value= 0
    total_revenue_value =0
    total_elasped_day= 0 
    ag = 0
    agpd=0
    revenue_per_year = 0
    buy_at_ending_price = []
    sell_at_ending_price =[]
    current_price =0 
    current_price_list = []
    list_of_reflection = []
    W_moderate_list_within_class=[]
    elasped_day_list = []
    

    def __init__(self,number,area=""):
        self.close()
        self.number= number
        if area != "":
            self.area= area
            stock_price_database = r"C:\Users\yiuki\Stockid_data\{}.{}.txt".format(self.number,self.area)
        else:
            self.area= "america"
            stock_price_database = r"/home/ricky/Documents/Stockid_data/{}.txt".format(self.number)

        f=open(stock_price_database,'r',encoding="utf8")
        self.strings = f.read().split("\n")
        self.strings = self.strings[:-1]
    def split_string(self):
        for string in self.strings:
            string = string.replace('"','')
            string12 = string.split(",", 5)
            # print(string12)
            string12[0]=string12[0][:10]
            # print(string12[0])
    
            self.list_of_date.append(string12[0])
            self.list_of_ending_price.append(string12[1])
            self.list_of_opening_price.append(string12[4])
            self.list_of_maximum_price.append(string12[2])
            self.list_of_minimum_price.append(string12[3])
            self.list_of_volume_of_exchange.append(string12[5])

        if (len(self.list_of_date)<28):
            return 10
        else: 
            return 1
            
            # self.list_of_rate_of_change.append(string12[6]) 
    def removing_million_and_thousands(self):
        for i in self.list_of_volume_of_exchange:
            x = len(i)
            string_remaining = i[0:x-1]
            # print(string_remaining)
            string_remaining=float(string_remaining)
            if (i[-1] == 'M'):
                string_remaining = string_remaining*1000000
            elif (i[-1]=="K"):
                string_remaining=string_remaining*1000000/1000
            # print(string_remaining)
            self.list_of_volume_of_exchange_hand +=[string_remaining]  
    def floating_list_of_volume_of_exchange_hand(self):
        self.list_of_volume_of_exchange_hand= [float(x) for x in self.list_of_volume_of_exchange]
    def reverse(self):
        self.list_of_date.reverse()
        self.list_of_ending_price.reverse()
        self.list_of_maximum_price.reverse()
        self.list_of_minimum_price.reverse()
        self.list_of_rate_of_change.reverse()
        self.list_of_volume_of_exchange_hand.reverse()
        self.list_of_opening_price.reverse()
    def get_date(self):
        x=13
        # date = input("What date")
        # self.date=date
        # print(date)
        # x=int(self.list_of_date.index(date))
        self.x=x
        # print(x)
        self.a=x
    def rate_of_range(self):
        for i in self.list_of_rate_of_change:
            x=len(i)
            string_remaining = i[0:x-1]
            string_remaining = float(string_remaining)/100
            # print(string_remaining)
            self.list_of_rate_of_change_in_float+=[string_remaining]

    def MFI(self):
        list_of_ending_price= [float(x) for x in self.list_of_ending_price]
        # list_of_opening_price=[float(x) for x in self.list_of_opening_price]
        # reference_point = list_of_ending_price[self.x-8]
        # postve_flow = []
        money_postive_flow = []
        # negative_flow = []
        money_negative_flow = []
        # max_value = (max((list_of_ending_price))) ## define error => should use maximum price instead
        # min_value = min((list_of_ending_price))
        for i in range(14): ### here is the bug
            max_value= float(self.list_of_maximum_price[i+self.x-13])
            min_value=float(self.list_of_minimum_price[i+self.x-13])
            #print("Maximum value: " + str(max_value))
            #print("Minimum value: " + str(min_value))
            # print("index  : "+ str(self.list_of_volume_of_exchange_hand))
            # print(self.list_of_ending_price[self.x+i-13])
            # print(self.list_of_ending_price[self.x+i-13+1])
            # print(len(list_of_ending_price))
            # print(self.a+i-13)
            if (float(self.list_of_ending_price[self.x+i-13])-float(self.list_of_ending_price[self.x+i-13-1] ) > 0):  ## for some reasons, it cannot detect postive and negative correctly /. should be 14 days // new it is changed 
                # postve_flow.append(list_of_ending_price[x+i])
                # print(len(list_of_ending_price))
                # print(self.x+i-13)
                typical_price = (max_value+min_value+list_of_ending_price[self.x+i-13])/3 ## smae error here 
                # print(typical_price)
                raw_money = typical_price*self.list_of_volume_of_exchange_hand[self.x+i-13]
                # print(list_of_volume_of_exchange_hand[x+i])
                # print("Positive flow: " +str(raw_money))
                money_postive_flow.append(raw_money)
            else:
                # negative_flow.append(list_of_ending_price[x+i])
                # print(self.list_of_ending_price[self.x+i-13])
                typical_price = (max_value+min_value+list_of_ending_price[self.x+i-13])/3
                # print("typical price: " +str(typical_price))
                # print(self.x+i-13)
                # print(self.list_of_volume_of_exchange_hand[self.x+i-13+1])
                raw_money = typical_price*self.list_of_volume_of_exchange_hand[self.x+i-13]
                # print(list_of_volume_of_exchange_hand[x+i])
                # print("negative flow: " + str(raw_money))
                money_negative_flow.append(raw_money)

        total_postive_flow = sum(money_postive_flow)
        # print("len " + str(len(money_negative_flow)+len(money_postive_flow)))
        # print("Postive flow " +str(total_postive_flow))
        total_negative_flow=sum(money_negative_flow)
        # print("Total negative flow " +str(total_negative_flow))
            
        if total_negative_flow ==0:
            mfr = 10000000
        else:
            mfr = total_postive_flow/total_negative_flow
            # print("mfr: " +str(mfr))
            # MFR=1/MFR
            # print(mfr)


        MFI_value = 100 *(1-1/(1+mfr))
        # print(MFI_value)
        return MFI_value   
    def MFI_list1(self):
        for i in range(len(self.list_of_ending_price)-13):
            y=self.MFI()
            self.MFI_list.append(y)
            self.x+=1 
    
        return self.MFI_list
    # @jit(target_backend='cuda')                         
    def ema(self): ##tick should have no error laters
        list_of_ending_price = [float(x) for x in self.list_of_ending_price]
        # print(list_of_ending_price)
        # print("Maximum: :" +str(list_of_maximum_price[x]))
        # print("Minimum : " + str(list_of_minimum_price[x]))
        # print("Starting: " + str(list_of_opening_price[x]))
        for i in range(len(list_of_ending_price)): #ofbinzl -14 ##-self.x
            if i ==0:
                continue
            else:
                if (list_of_ending_price[self.x-13+i-1] > list_of_ending_price[self.x-13+i+1-1] ):
                    self.down +=[ list_of_ending_price[self.x-13+i-1] - list_of_ending_price[self.x-13+i+1-1] ] # need to minus 1 for some reason
                    # print("1 down: " + str(list_of_ending_price[self.x-13+i-1]))
                    # print("2 down : " + str(list_of_ending_price[self.x-13+i]))
                    # print("result of down: " + str((list_of_ending_price[self.x-13+i-1] - list_of_ending_price[self.x-13+i] )))
                    # # print("down : " + str(down))
                    self.up.append(0)
                elif (list_of_ending_price[self.x-13+i+1-1] > list_of_ending_price[self.x-13+i-1]):
                    self.up += [list_of_ending_price[self.x-13+i+1-1]- list_of_ending_price[self.x-13+i-1]]
                    # print("1 up: " + str(list_of_ending_price[x-13+i]))
                    # print("2 up : " + str(list_of_ending_price[x-13+i-1]))
                    # print("result of up: " + str((list_of_ending_price[x-13+i] - list_of_ending_price[x-13+i-1] )))
                    self.down.append(0)
                    # print("up : " +str(up))
                else: 
                    self.up.append(0)
                    self.down.append(0)
        
        # print("up : "+str(self.up))
        ema_up = 0
        ema_down= 0 
        sum_ema_up_list = []
        sum_ema_down_list=[]

         ## calucating for volume of exchange  ##here 
        for i in range(14):
            ema_up += self.up[i]*(1-self.alpha) ** (i)
            sum_ema_up_list.append(ema_up)
            ema_down += self.down[i]*(1-self.alpha) ** (i)
            sum_ema_down_list.append(ema_down)

        ##############################################################

        ema_up=ema_up/14
        ema_down=ema_down/14
        # print(ema_up)
        # print(ema_down)
        
        for i in range(len(self.up)-self.x-1): #currently, 7 days  => 14 days  len(list_of_ending_price)-14+x ##-self.x+1
            # print("up value: " + str(up[x+i+1]))
            ema_up = self.alpha*self.up[self.x+i+1] +(1-self.alpha)*ema_up  #orginally i+12
            # print("ema up : "+ str(ema_up))
            ema_down = self.alpha*self.down[self.x+i+1] +(1-self.alpha)*ema_down
            
            # print("ema down : "+ str(ema_down))   
            if ema_down == 0:
                ema_down= 1/1000
                rs =ema_up/ ema_down
            else:
                rs =ema_up/ ema_down
            # print("rs" + str(rs))
            rsi = (1-(1/(1+rs)))*100
            self.rsi_list.append(rsi)
        
        return self.rsi_list
    def RSV(self): ## should have no error --------the value will vary if the date is inputted at a wrong order -- now no error
        list_of_ending_price= [float(x) for x in self.list_of_ending_price]
        list_of_maximum_price= [float(x) for x in self.list_of_maximum_price]  
        list_of_minimum_price= [float(x) for x in self.list_of_minimum_price]  
        for i in range(len(self.list_of_date)): #orginally 7 days 
            if i < 13: 
                continue
            else: 
                max_value = max(list_of_maximum_price[i-13:i+1]) # use the maximum value of stock for today --> index is [x-13+i:x+i+1]
                # print("max value: " + str(max_value))
                min_value = min(list_of_minimum_price[i-13:i+1]) # use the maximum value of the stock for today  --[x-13+i+1:x+i+1]
                # print("min_value: "+str(min_value))
                # print(self.list_of_date[i])
                value = float(list_of_ending_price[i]) # use the stock price at that moment 
                # index out of range at that moment 
                # print("value" + str(value))
                
                if (max_value-min_value) ==0:
                    self.rsv_list.append(-1000000000000000)
                else:
                    self.rsv_list.append((value-min_value)/(max_value-min_value)*100)

        return self.rsv_list
    def K(self): ## should not have error
        for i in range(len(self.rsv_list)):
            self.k_value *=2/3
            self.k_value +=  1/3*self.rsv_list[i]
            # print(self.k_value)
            self.k_list.append(self.k_value)
    def D(self): # should not have error 
        # print(len(self.rsv_list))
        # print("k_list" + str(len(self.k_list)))
        for i in range(len(self.rsv_list)):
            self.d_value *= 2/3
            self.d_value += 1/3 * self.k_list[i]
            self.d_list.append(self.d_value)
        
        return self.d_list
    def W(self):
        print("Hello World")
        # print(len(MFI_list))

        # print(len(rsv_list))
        # print(len(self.d_list))
        # print(len(self.list_of_ending_price)-14-self.a+1)
        for i in range(len(self.list_of_ending_price)-14-self.a-1-14-14):  #len(list_of_ending_price)-14-a-1
            # print(i+a-11)
            # # print(type(MFI_list[i]))
            # print("MFI: " +str(MFI_list[i]))
            # print(rsi_list[i])
            # print(d_list[i+3])
            # print(d_list[i])
            W_value = (self.MFI_list[i]+self.rsi_list[i]+self.d_list[i+3])/3
            # print(W_value)
            self.W_list.append(W_value)
    # @jit(target_backend='cuda')                         
    def W_moderate(self):
        # print("Hello World")
        # print(len(MFI_list))
        # print(self.list_of_ending_price[-1])
        W_moderate_list=[]
        W_sell_list=[]

        # print(len(rsv_list))
        # print(len(self.rsi_list))
        # print(len(self.list_of_ending_price)-1-self.a-3)
        for i in range(len(self.list_of_ending_price)-self.a):  #len(list_of_ending_price)-14-a-1 #may cause bug => need to fix some bug arised from there
            # list_2=[]
            # print(i+a-11)
            # # print(type(MFI_list[i]))
            # print("MFI: " +str(self.MFI_list[i]))
            # print("rsi " + str(self.rsi_list[i-2]))
            # print("d: "+str(self.d_list[i]))
            # print(rsi_list[i-2])
            # print(d_list[i])
            # print(d_list[i])
            list_1= []
            list_1.append(self.MFI_list[i])
            list_1.append(self.rsi_list[i-2])
            list_1.append(self.d_list[i])
            W_moderate = 1/2*0.618**2*max(list_1)+1/2*min(list_1)+1/2*0.618*(self.MFI_list[i]+self.rsi_list[i-2]+self.d_list[i]-max(list_1)-min(list_1))
            # W_buy = 1/2*0.618**2*max(list_1)+1/2*min(list_1)+1/2*0.618*(self.MFI_list[i]+self.rsi_list[i-2]+self.d_list[i]-max(list_1)-min(list_1))
            W_sell = 1/2*0.618**2*min(list_1)+1/2*max(list_1)+1/2*0.618*(self.MFI_list[i]+self.rsi_list[i-2]+self.d_list[i]-max(list_1)-min(list_1))
            # print(W_moderate)
            W_moderate_list.append(W_moderate)
            W_sell_list.append(W_sell)
            self.W_moderate_list_within_class.append(W_moderate)


            # W_value = (MFI_list[i]+rsi_list[i]+d_list[i+3])/3
            if W_moderate < 17:  #### 25
                # print("Time to purcharse as the W's value hits " + str(W_moderate)+ " Date:" + self.list_of_date[i+self.a] + " Price: " +str(self.list_of_ending_price[self.a+i]))
                self.comparing_date_purchase.append(i+self.a)
                self.list_of_reflection.append(i)
                # print("rsi : " +str(rsi_list[i-2]))
                # print("MFI: " +str(MFI_list[i]))
                # print("D value: " + str(d_list[i]))
            if W_sell> 45:
                # print("Time to sell off as W's value hits"+ str(W_moderate)+" Date" +self.list_of_date[i+self.a]+ " Price : " + str(self.list_of_ending_price[self.a+i]))
                self.comparing_date_sell_off.append(i+self.a)

        return W_moderate_list,W_sell_list
    def convert_weekdays_to_days(self,elapsed_weekdays):
        complete_weeks = elapsed_weekdays // 5
        weekend_days = complete_weeks * 2
        remaining_weekdays = elapsed_weekdays % 5
        total_days = weekend_days + remaining_weekdays
        return total_days
    def calculate_elapsed_days(self,start_date, end_date):
        date_format = "%Y-%m-%d"
        start_datetime = datetime.strptime(start_date, date_format)
        end_datetime = datetime.strptime(end_date, date_format)

        elapsed_days = (end_datetime - start_datetime).days

        return elapsed_days
    # @jit(target_backend='cuda')                         
    def income(self):
        # print(self.comparing_date_purchase)
        # print(self.comparing_date_sell_off)
        buying_date=[]
        selling_date=[]
        for i in self.comparing_date_purchase:
            # print("Now that we are buying at that date:" + str(self.list_of_date[i]) + "at a price of " +str(self.list_of_ending_price[i]))
            self.buy_at_ending_price.append(self.list_of_ending_price[i])
            for j in self.comparing_date_sell_off:
                if j - i>=0:
                    # print("Now we are selling off at that date"+str(self.list_of_date[j])+ " at a price of " +str(self.list_of_ending_price[j]))
                    self.actual_purchase.append(i)
                    self.sell_at_ending_price.append(self.list_of_ending_price[j])
                    # print(self.actual_purchase)
                    # print(self.actual_sell_off)
                    # cost, difference = self.calucation_profit(float(self.list_of_ending_price[i]),float(self.list_of_ending_price[j]))
                    # self.total_cost.append(cost)
                    # self.total_revenue.append(difference)
                    # print(self.list_of_date[i])
                    # print(self.list_of_date[j])
                    buying_date.append(self.list_of_date[i])
                    selling_date.append(self.list_of_date[j])
                    # days = self.calculate_elapsed_days(self.list_of_date[i],self.list_of_date[j])
                    # self.elasped_day.append(days)
                    # self.actual_sell_off.append(j)
                    # self.number_of_trade+=1
                    break

        # print(self.actual_purchase)
        # print("elasped day: " +str((self.elasped_day)))

        # print("Buy now "+ str(buying_date))
        # print("Sell now " +str(selling_date))
        # print(self.buy_at_ending_price)
        # print(self.sell_at_ending_price)
        self.buy_at_ending_price, self.sell_at_ending_price=self.removing_stuff_from_the_list(self.buy_at_ending_price,self.sell_at_ending_price) ## skipping dates
        # print(self.buy_at_ending_price)
        # print(self.sell_at_ending_price)
        ##Have errors still => For some reasons it cannot coordinate with 300003 => need some hotfix => But don't have time => May need to do it later
        result_list_for_selling_dates , indices, unique_indeices_for_buying_list = self.remove_duplicates_with_indices(buying_date,selling_date) ## removing dates

        for i in range(len(unique_indeices_for_buying_list)):
            self.elasped_day.append(self.calculate_elapsed_days(unique_indeices_for_buying_list[i],result_list_for_selling_dates[i]))

        # print(self.elasped_day)
        self.total_elasped_day=sum(self.elasped_day)

        if (len(self.elasped_day)!=0):
            average_day = self.total_elasped_day/len(self.elasped_day)
            day_std_deviation=np.std(self.elasped_day)
        else:
            average_day=0
            day_std_deviation=0
        # print(average_day)
        # print(self.sell_at_ending_price)
        # print(len(self.buy_at_ending_price))
        for i in range(len(self.sell_at_ending_price)):
            # print(i)
            cost, difference = self.calucation_profit(float(self.buy_at_ending_price[i]),float(self.sell_at_ending_price[i]))
            self.total_cost.append(cost)
            self.total_revenue.append(difference)

        # for j in range(len(selling_date)):
        #     if (selling_date[j] == selling_date[j-1]):
        # print(self.elasped_day)
        self.total_cost_value=sum(self.total_cost)
        # print(self.total_cost_value)
        # print(self.total_revenue)
        self.total_revenue_value  = sum(self.total_revenue)
        # print(self.total_revenue_value)
        if self.total_cost_value ==0:
            ag= - 10
        else:
            ag = self.total_revenue_value/self.total_cost_value

        print("ag: " + str(ag))
        if len(self.elasped_day) ==0:
            agpd = -10
        else:
            agpd = self.total_elasped_day/len(self.elasped_day)
        agpd = ag/agpd 
        print("agpd : " +str(agpd))
        revenue_per_year = (agpd+1)**(261) 
        print("revenue per year"+ str(revenue_per_year))
        ####### elasped day part => if two same day => Will get deleted ##############
        # self.checking(self.elasped_day)
        # print(self.elasped_day)

        ############################

        #Below are modification when the price goes up and we stopped buying ##############################################
        
        # for i in range(len(self.actual_purchase)):
        #     # print("Number that we are doin"+str(self.actual_purchase[i]) + "Id number is: " + str(i))
        #     if i+1 >= len(self.actual_purchase):
        #         continue
        #     else:
        #         # self.removal +=1
        #         if self.actual_purchase[i] - self.actual_purchase[i-1] > 2:
        #             if float(self.list_of_ending_price[self.actual_purchase[i]])-float(self.list_of_ending_price[self.actual_purchase[i-1]]) >0:
        #                 print("Today" + self.list_of_ending_price[self.actual_purchase[i]] )
        #                 # print("Yesterday: "  +self.list_of_ending_price[self.actual_purchase[i-1]])
        #                 # print("difference : " + str(float(self.list_of_ending_price[self.actual_purchase[i]])-float(self.list_of_ending_price[self.actual_purchase[i-1]])))
        #                 # # self.actual_actual_purchase.remove(self.actual_purchase[i])
        #             else:
        #                 self.actual_actual_purchase.append(self.actual_purchase[i])
        #         else:
        #             self.actual_actual_purchase.append(self.actual_purchase[i])


        ##########################################################################################
        
        # print("Ideas" + str(self.actual_actual_purchase))
        # print("Actual purchase price" + str(list))

        # print(self.actual_purchase)
        # print(self.actual_sell_off)

        # for i in self.actual_actual_purchase:
        #     print(self.list_of_ending_price[i])

        return agpd,len(self.elasped_day),average_day,day_std_deviation
    def removing_stuff_from_the_list(self,buy_list,sell_list):
        buy_list = [float(x) for x in buy_list]
        sell_list = [float(x) for x in sell_list]
        removal_list_in_buy_list= []
        removal_list_in_sell_list=[]
        for j in range(len(sell_list)): 
    # print("j" +str(j))
    # print("Second index" +str(j))
            if (j) > int(len(buy_list)):
                break
            else:
                if sell_list[j]==sell_list[j-1]:
                    if (buy_list[j]>buy_list[j-1]):
                        # print("index"+str(j))
                        # print("Too high" + str(buy_list[j]))
                        # print("Yesterday " +str(buy_list[j-1]))
                        # print("Where are we selling it to" + str(sell_list[j]))
                        # print("Are you sure about that" + str(sell_list[j-1]))
                        removal_list_in_buy_list.append(buy_list[j])
                        removal_list_in_sell_list.append(sell_list[j])
                        
        for i in removal_list_in_buy_list:
            buy_list.remove(i)
            
        for j in removal_list_in_sell_list:
            sell_list.remove(j)
        
        return buy_list,sell_list
    def remove_duplicates_with_indices(self,buying_date,selling_date):

        unique_list = []
        unique_indices = []
        unique_indices_for_buying_list = [] 
        seen = set()

        for index, item in enumerate(selling_date):
            if item not in seen:
                unique_list.append(item)
                unique_indices.append(index)
                unique_indices_for_buying_list.append(buying_date[index])
                seen.add(item)

        return unique_list, unique_indices, unique_indices_for_buying_list
    def calucation_profit(self,buy_price, sell_price):
        if self.area == "america":
            quantity = 10000000/(buy_price)
            quantity = round(quantity,0)
            # print(quantity)
            cost = quantity * buy_price*1.0028
            # print(cost)
            sell = quantity * sell_price
            # print(sell)
            difference = sell-cost
        else:
            quantity = 10000/buy_price
            quantity = round(quantity,-2)
            # print(quantity)
            cost = quantity * buy_price*1.0028
            # print(cost)
            sell = quantity * sell_price
            # print(sell)
            difference = sell-cost
        return cost,difference
    def checking(self,list):    
        for i,val in enumerate(list):
            if abs(list[i]-list[i-1])<2:
                print(list[i])
                list.remove(list[i])
                self.checking(list)
        return list
    def monitoring_website(self):
        url = "https://quote.eastmoney.com/f1.html?newcode=0.{}".format(self.number)
        browser = webdriver.Chrome()
        browser.get(url)

        now = datetime.now() # current date and time

        list = []
        current_datetime = datetime.now().strftime("%Y-%m-%d")
        print(current_datetime)
        str_current_datetime = current_datetime
        filename = str_current_datetime+"stock_price.txt"
        time.sleep(7)  
        while True:
            now = datetime.now()
            time1 = now.strftime("%H:%M:%S")
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            prices = soup.find_all('div',{'class': 'zxj'})
        
            for price in prices:
                price = price.find('span').get_text()
                print(price)

            with open(filename,'a') as f:
                f.write(str(current_datetime) + " " + time1 + " "+ price+ "\n" + " " ) 

            time.sleep(1)
    def getting_current_price(self):
        # stock_id = "{}.{}".format(self.number,self.area)
        # while True:
        # a= YFinance(stock_id)
        # YFinance.info(a)
        # print(stock)
        # stock = yf.Ticker(stock_id)
        # self.current_price = stock.info["currentPrice"]

        self.current_price = float (self.list_of_ending_price[-1])

        # self.current_price = float (self.list_of_ending_price[-1])
        self.current_price_list.append(self.current_price)
        print("Now Price" +str(self.current_price))
        # time.sleep(30)
    def persumable_price(self,price):
        self.current_price=float(price)
        self.current_price_list.append(self.current_price)
    def getting_predictive_price(self,percentage):
        # stock_id = "{}.{}".format(self.number,self.area)
        # while True:
        # stock = yf.Ticker(stock_id)
        # self.current_price = stock.info["currentPrice"]
        self.current_price = percentage*float (self.list_of_ending_price[-1])
        self.current_price_list.append(self.current_price)
        print("Now Price" +str(self.current_price))
    def predictiing_volume_of_exchange_using_ema(self):
        list_of_volume_of_exchange_hand = [float(x) for x in self.list_of_volume_of_exchange_hand]
        ema_up = 0
        # ema_down= 0 
        # sum_ema_up_list = []
        # sum_ema_down_list=[]
        # rsi_list_for_volume =[]

        for i in range(13):
            # print(ema_up)
            ema_up += list_of_volume_of_exchange_hand[-14+i]*(1-self.alpha) ** (i)
            # rsi_list_for_volume.append(ema_up)

        print(ema_up)  
        return list_of_volume_of_exchange_hand[-1]
    def predicting_MFI(self,volume): ## we need to make sure it can slice before it works
        self.x = len(self.list_of_ending_price)-14
        # print("self.x: " +str(self.x))
        # print("item: " +str(len(self.list_of_ending_price)))
        list_of_ending_price= [float(x) for x in self.list_of_ending_price]
        list_of_ending_price.append(self.current_price)
        list_of_maximum_price= [float(x) for x in self.list_of_maximum_price] 
        list_of_maximum_price.append(max(self.current_price_list))
        # print(list_of_maximum_price[-1])
        list_of_minimum_price= [float(x) for x in self.list_of_minimum_price] 
        list_of_minimum_price.append(min(self.current_price_list)) 
        list_of_volume_of_exchange_hand= [float(x) for x in self.list_of_volume_of_exchange_hand] 
        list_of_volume_of_exchange_hand.append(volume)
        # print("volume length: "+str(len(list_of_volume_of_exchange_hand)))

        # self.list_of_volume_of_exchange_hand[self.x+i]
        # list_of_opening_price=[float(x) for x in self.list_of_opening_price]
        # reference_point = list_of_ending_price[self.x-8]
        # postve_flow = []
        money_postive_flow = []
        # negative_flow = []
        money_negative_flow = []
        # max_value = (max((list_of_ending_price))) ## define error => should use maximum price instead
        # min_value = min((list_of_ending_price))
        for i in range(14): ### here is the bug
            max_value= float(list_of_maximum_price[i+self.x])
            min_value=float(list_of_minimum_price[i+self.x])
            # print("Maximum value: " + str(max_value))
            # print("Minimum value: " + str(min_value))
            # print("index  : "+ str(len(self.list_of_volume_of_exchange_hand)))
            # print(self.list_of_ending_price[self.x+i-13])
            # print(self.list_of_ending_price[self.x+i-13+1])
            # print(len(list_of_ending_price))
            # print(self.a+i-13)
            if (float(list_of_ending_price[self.x+i])-float(list_of_ending_price[self.x+i-1] ) > 0):  ## for some reasons, it cannot detect postive and negative correctly /. should be 14 days // new it is changed 
                # postve_flow.append(list_of_ending_price[x+i])
                # print(len(list_of_ending_price))
                # print(self.x+i)
                typical_price = (max_value+min_value+list_of_ending_price[self.x+i])/3 ## smae error here 
                # print(typical_price)
                raw_money = typical_price*list_of_volume_of_exchange_hand[self.x+i]
                # print(list_of_volume_of_exchange_hand[x+i])
                # print("Positive flow: " +str(raw_money))
                # print(self.list_of_volume_of_exchange_hand[self.x+i])

                money_postive_flow.append(raw_money)
            else:
                # negative_flow.append(list_of_ending_price[x+i])
                # print(self.list_of_ending_price[self.x+i-13])
                typical_price = (max_value+min_value+list_of_ending_price[self.x+i])/3
                # print("typical price: " +str(typical_price))
                # print(self.x+i-13)
                # print(self.list_of_volume_of_exchange_hand[self.x+i])
                raw_money = typical_price*self.list_of_volume_of_exchange_hand[self.x+i]
                # print(list_of_volume_of_exchange_hand[x+i])
                # print("negative flow: " + str(raw_money))
                money_negative_flow.append(raw_money)

        total_postive_flow = sum(money_postive_flow)
        # print(total_postive_flow)
        total_negative_flow=sum(money_negative_flow)
            
        if total_negative_flow ==0:
            mfr = 10000000
        else:
            mfr = total_postive_flow/total_negative_flow
            
            # print("mfr: " +str(mfr))
            # MFR=1/MFR
            # print(mfr)


        MFI_value = 100 *(1-1/(1+mfr))
        # print(MFI_value)
        return MFI_value     
    def predicting_MFI_list1(self,volume):
        MFI_list=[]
        for i in range(1):
            y=self.predicting_MFI(volume)
            MFI_list.append(y)
            # print(y)
        
        return MFI_list
            # self.x+=1 
    def prediciting_RSV(self): ###tick => can be used
        list_of_ending_price= [float(x) for x in self.list_of_ending_price]
        list_of_ending_price.append(self.current_price)
        list_of_maximum_price= [float(x) for x in self.list_of_maximum_price] 
        list_of_maximum_price.append(max(self.current_price_list))
        list_of_minimum_price= [float(x) for x in self.list_of_minimum_price] 
        list_of_minimum_price.append(min(self.current_price_list)) 
        # print(self.current_price)
        # print(list_of_minimum_price[-1])
        predicting_rsv_list=[]
        for i in range(14): #orginally 7 days 
            # if i < 13: 
            #     continue
            # else: 
            # print(list_of_minimum_price[-1])
            max_value = max(list_of_maximum_price[i-14-13-2+2:i-16+1+2-1]) # use the maximum value of stock for today --> index is [x-13+i:x+i+1]
            # print("max value: " + str(max_value))
            min_value = min(list_of_minimum_price[i-14-13-2+2:i-14+1-1-1+2-1]) # use the maximum value of the stock for today  --[x-13+i+1:x+i+1]
            # print("min_value: "+str(min_value))
            # print(self.list_of_date[-15+i+2])
            value = float(list_of_ending_price[i-16+2]) # use the stock price at that moment 
            # index out of range at that moment 
            # print("value" + str(value))
            
            if (max_value-min_value) ==0:
                predicting_rsv_list.append(-1000000000000000)
            else:
                predicting_rsv_list.append((value-min_value)/(max_value-min_value)*100)

        return predicting_rsv_list

    def prediciting_k(self,predicting_rsv_list): #done
        k_list=[]
        # print("K_value" +str(self.k_value))
        k = self.k_value
        for i in range(1):
            k *=2/3
            k +=  1/3*predicting_rsv_list[-1]
            # print("K_vlaue: " +str(self.k_value))
            k_list.append(k)
        return k_list
    
    def predicitng_d(self,predicitng_rsv_list,k_list): #done
        d_list=[]
        d= self.d_value
        for i in range(1):
            d *= 2/3
            d += 1/3 * k_list[0]
            d_list.append(d)
        
        return d_list

    def prediciting_ema(self): ## think / should we just straight up call the list of ema first/ Can we reuse it
        self.x = 13
        list_of_ending_price = [float(x) for x in self.list_of_ending_price]
        list_of_ending_price.append(self.current_price)
        # up=[]
        # down= [] 
        # print(list_of_ending_price)
        # print("Maximum: :" +str(list_of_maximum_price[x]))
        # print("Minimum : " + str(list_of_minimum_price[x]))
        # print("Starting: " + str(list_of_opening_price[x]))
        for i in range(len(list_of_ending_price)+14): #ofbinzl -14
            if i <13:
                continue
            else:
                # print(self.list_of_ending_price[i])
                if (list_of_ending_price[-13+i-1-1] > list_of_ending_price[-13+i+1-1-1] ):
                    self.down +=[ list_of_ending_price[-13+i-1-1] - list_of_ending_price[-13+i+1-1-1] ] # need to minus 1 for some reason
                    # print("1 down: " + str(list_of_ending_price[-13+i-1]))
                    # print("2 down : " + str(list_of_ending_price[-13+i]))
                    # print("result of down: " + str((list_of_ending_price[self.x-13+i-1] - list_of_ending_price[self.x-13+i] )))
                    # # print("down : " + str(down))
                    self.up.append(0)
                elif (list_of_ending_price[-13+i+1-1-1] > list_of_ending_price[-13+i-1-1]):
                    self.up += [list_of_ending_price[-13+i+1-1-1]- list_of_ending_price[-13+i-1-1]]
                    # print("1 up: " + str(list_of_ending_price[-13+i]))
                    # print("2 up : " + str(list_of_ending_price[-13+i-1]))
                    # print("result of up: " + str((list_of_ending_price[x-13+i] - list_of_ending_price[x-13+i-1] )))
                    self.down.append(0)
                    # print("up : " +str(up))
                else: 
                    self.up.append(0)
                    self.down.append(0)
        
        # print("up : "+str(self.up))
        ema_up = 0
        ema_down= 0 
        sum_ema_up_list = []
        sum_ema_down_list=[]

         ## calucating for volume of exchange  ##here 
        for i in range(14):
            ema_up += self.up[i]*(1-self.alpha) ** (i)
            sum_ema_up_list.append(ema_up)
            ema_down += self.down[i]*(1-self.alpha) ** (i)
            sum_ema_down_list.append(ema_down)

        ##############################################################

        ema_up=ema_up/14
        ema_down=ema_down/14
        # print(ema_up)
        # print(ema_down)

        ######################################################################
        #Not sure about this part afterward => Good luck => Don't know what am I doing exactly
        # print(len(self.up))
        
        for i in range(len(self.up)): #currently, 7 days  => 14 days  len(list_of_ending_price)-14+x
            # print("up value: " + str(up[x+i+1]))
            ema_up = self.alpha*self.up[i] +(1-self.alpha)*ema_up  #orginally i+12
            # print("ema up : "+ str(ema_up))
            ema_down = self.alpha*self.down[i] +(1-self.alpha)*ema_down
            
            # print("ema down : "+ str(ema_down))   
            if ema_down == 0:
                ema_down= 1/1000
                rs =ema_up/ ema_down
            else:
                rs =ema_up/ ema_down
            # print("rs" + str(rs))
            rsi = (1-(1/(1+rs)))*100
            # print("rsi: " +str(rsi))
            self.rsi_list.append(rsi)
        
        return self.rsi_list

    def prediciting_W_moderate(self,MFI_list,rsi_list,d_list):
        # for i in range(len(d_list)):  #len(list_of_ending_price)-14-a-1 #may cause bug => need to fix some bug arised from there
            # list_2=[]
            # print(i+a-11)
            # # print(type(MFI_list[i]))
            # print("MFI: " +str(MFI_list[i]))
            # print(rsi_list[i-2])
            # print(d_list[i])
            # print(d_list[i])
        list_1= []
        list_1.append(MFI_list[-1])
        list_1.append(rsi_list[-1])
        list_1.append(d_list[-1])
        W_moderate = 1/2*0.618**2*max(list_1)+1/2*min(list_1)+1/2*0.618*(MFI_list[-1]+rsi_list[-1]+d_list[-1]-max(list_1)-min(list_1))
        # W_buy = 1/2*0.618**2*max(list_1)+1/2*min(list_1)+1/2*0.618*(self.MFI_list[i]+self.rsi_list[i-2]+self.d_list[i]-max(list_1)-min(list_1))
        W_sell = 1/2*0.618**2*min(list_1)+1/2*max(list_1)+1/2*0.618*(MFI_list[-1]+rsi_list[-1]+d_list[-1]-max(list_1)-min(list_1))
        # print("W buy at " +str(W_moderate))
        # print("W sell at: " +str(W_sell))
        return W_moderate,W_sell

        # W_value = (MFI_list[i]+rsi_list[i]+d_list[i+3])/3
        # if W_moderate < 17:  #### 25
        #     # print("Time to purcharse as the W's value hits " + str(W_moderate)+ " Price: " +str(self.list_of_ending_price[-1]))
        #     # self.comparing_date_purchase.append(i+self.a)
        #     # print("rsi : " +str(rsi_list[i-2]))
        #     # print("MFI: " +str(MFI_list[i]))
        #     # print("D value: " + str(d_list[i]))
        # if W_sell> 45:
        #     print("Time to sell off as W's value hits"+ str(W_moderate)+ " Price : " + str(self.list_of_ending_price[-1]))
            # self.comparing_date_sell_off.append(i+self.a)

    def check_if_update(self):
        yf.pdr_override()
        # print("hellow world")
        indexes = self.number
        # print(indexes)
        place = self.area
        current_datetime = datetime.now().strftime("%Y-%m-%d")
        date= self.list_of_date[-1]
        
        print(('0'*(6-len(indexes))+indexes+ "." + place))

        # print(date)
        if (date!=current_datetime):
            # print("hello world")
            try:
                # print(str('0'*(6-len(str(indexes+1)))+str(indexes+1)+ "." + place))
                df = pdr.get_data_yahoo('0'*(6-len(indexes))+indexes+ "." + place, start=date, end=current_datetime)
                print("Hello wolrd")
            except:
                pass
            else:
                if len(df) != 0:
                    df.drop(['Adj Close'],axis = 1)

                    df = df[['Close','High','Low','Open','Volume']]

                    for i in df.index:
                        for j in df:
                            df.loc[i,j] = round(df.loc[i,j],2)

                    df = df.astype(str)


                    with open(str(indexes)+'.'+str(place), 'a') as f_object:
                        f_object.write(str(df))

                    # # Pass this file object to csv.writer()
                    # # and get a writer object
                    # writer_object = writer(f_object)
                
                    # # Pass the list as an argument into
                    # # the writerow()
                    # writer_object.writerow(List)
                
                    # # Close the file object
                    # f_object.close()
                    # df.to_csv('C:\\Users\\yiuki\\Stockid_data\\'+'0'*(6-len(str(indexes+1)))+str(indexes+1)+"." + place+'.txt', header = False, quoting=csv.QUOTE_NONNUMERIC)
    def predicting_reflection(self):
        ### intializing the parameter
        list_of_5_days=[]
        number_of_5_days = 0
        list_of_10_days=[]
        number_of_10_days = 0
        list_of_15_days=[]
        number_of_15_days = 0
        reference_point=0
        ready_to_delete=0
        list_of_reflection2=[]
        j_list=[]
        average_day_list=[]

        # list_of_reflection2 = self.list_of_reflection
        print(self.list_of_reflection)

        ### Sorting alrogithms I mean that is a better way for checking the W_moderate value but like for now I cannot write it yet
        ### Just check for the rise of W_moderate value
        for i in self.list_of_reflection:
            if(i+1 >= len(self.W_moderate_list_within_class)):
                    list_of_reflection2.append(i)
                    break
            
            if (self.W_moderate_list_within_class[i+1]>=17):
                # print(self.W_moderate_list_within_class[i+1])
                list_of_reflection2.append(i)
        
        # print(list_of_reflection2)
        # print("list gone")

        ## finding the point of interest
        for i in list_of_reflection2:
            for j in range(15):
                if (i+j >= len(self.W_moderate_list_within_class)):
                    print("Gone")
                    break
                if (self.W_moderate_list_within_class[i+j] - self.W_moderate_list_within_class[i]>7.5 and (j)<=5):
                    print("5 days result")
                    print("Date taken: "+str(j))
                    print("The previous days W_moderate")
                    for k in range(j):
                        print(self.W_moderate_list_within_class[i+k])
                    print("Ending point W_moderate: " +str(self.W_moderate_list_within_class[i+j]))
                    print("Ending date: "+str(self.list_of_date[i+j+self.a]))
                    j_list.append(j)
                    if ( i - reference_point<=5):
                        reference_point = i 
                        break 
                    list_of_5_days.append(i)
                    number_of_5_days+=1
                    break
                elif (self.W_moderate_list_within_class[i+j] - self.W_moderate_list_within_class[i]>7.5 and (j)<=10):
                    print("10 days result")
                    print("Date taken: "+str(j))
                    print("The previous days W_moderate")
                    for k in range(j):
                        print(self.W_moderate_list_within_class[i+k])
                    print("Ending point W_moderate: " +str(self.W_moderate_list_within_class[i+j]))
                    print("Ending date: "+str(self.list_of_date[i+j+self.a]))
                    j_list.append(j)
                    if ( i - reference_point<=10):
                        reference_point = i 
                        break 
                    list_of_10_days.append(i)
                    number_of_10_days+=1
                    break
                elif ((self.W_moderate_list_within_class[i+j] - self.W_moderate_list_within_class[i]>7.5 and (j)<=15)):
                    print("15 days result")
                    print("Date taken: " +str(j))
                    print("The previous days W_moderate")
                    for k in range(j):
                        print(self.W_moderate_list_within_class[i+k])
                    print("Ending W_moderate"+str(self.W_moderate_list_within_class[i+j]))
                    print("Ending date need" +str(self.list_of_date[i+j+self.a]))
                    j_list.append(j)
                    if ( i - reference_point<=15):
                        reference_point = i 
                        break
                    list_of_15_days.append(i)
                    number_of_15_days+=1
                    break

        #### Printing results after sorting 
        for i in range(len(list_of_reflection2)):
            if i+1 == len(list_of_reflection2):
                break
            
            average_day_list.append(self.calculate_elapsed_days(self.list_of_date[list_of_reflection2[i]+self.a],self.list_of_date[list_of_reflection2[i+1]+self.a]))
        
        print(average_day_list)

        self.elasped_day_list=j_list

        print("5 days")
        print(list_of_5_days)
        for i in list_of_5_days:
            print(self.list_of_date[i+self.a])
        print(number_of_5_days)
        print("10 days")
        print(list_of_10_days)
        for i in list_of_10_days:
            print(self.list_of_date[i+self.a])
        print(number_of_10_days)
        print("15 days")
        print(list_of_15_days)
        for i in list_of_15_days:
            print(self.list_of_date[i+self.a])
        print(number_of_15_days)
        print("On average:")
        print("We need " +str(np.average(j_list))+" days to see a rebound")
        print("Between each reflection, there is a " +str(np.average(average_day_list))+ " day gap between")
        print(" and " +str(np.std(average_day_list)) +" as standard deviation")

    def price_return(self):
        return float(self.list_of_ending_price[-1])

    def close(self):
        # print("Hello")
        self.alpha = 2/15
        self.ema_value=30
        self.price =0
        self.date =0
        self.date_14=0
        self.k_value = 50 
        self.list_of_date = []
        self.list_of_ending_price = []
        self.list_of_opening_price = []
        self.rsv_list=[]
        self.d_value = 50 
        self.k_list= []
        self.d_list = []
        self.MFI_list=[]
        self.list_of_maximum_price = [] 
        self.list_of_minimum_price = [] 
        self.sum_of_postive_ema_value =0
        self.sum_of_negative_ema_value =0
        self.list_of_volume_of_exchange=[]
        self.list_of_rate_of_change=[]
        self.list_after_editing = [] 
        self.list_of_volume_of_exchange_hand=[]
        self.list_of_rate_of_change_in_float=[]
        self.up = []
        self.down=[]
        self.ema_list= [] 
        self.ema_up =0 
        self.ema_down= 0
        self.rsi_list = []
        self.W_list=[]
        self.W_value = 0 
        self.a=0
        self.mfr=0
        self.comparing_date_purchase = []
        self.comparing_date_sell_off = []  
        self.strings=[]
        self.x=0
        self.actual_purchase = [] 
        self.actual_sell_off=[] 
        self.removal =0
        self.actual_actual_purchase =[]
        self.total_cost = []
        self.total_revenue =[]
        self.elasped_day = []
        self.number_of_trade = 0
        self.total_cost_value= 0
        self.total_revenue_value =0
        self.total_elasped_day= 0 
        self.ag = 0
        self.agpd=0
        self.revenue_per_year = 0
        self.buy_at_ending_price = []
        self.sell_at_ending_price =[]
        self.strings =[]
        # self.number= 0
        # self.area = ""
        # print("clear")
        # self.__init__(self.number,self.area)
        # print(self.list_of_ending_price)
        # cache.clear()

    def W_moderate_at_last_day(self,MFI_list,rsi_list,d_list):
        # for i in range(len(d_list)):  #len(list_of_ending_price)-14-a-1 #may cause bug => need to fix some bug arised from there
            # list_2=[]
            # print(i+a-11)
            # # print(type(MFI_list[i]))
            # print("MFI: " +str(MFI_list[i]))
            # print(rsi_list[i-2])
            # print(d_list[i])
            # print(d_list[i])
        w_moderate_list=[]
        W_sell_list=[]

        list_1= []
        list_1.append(MFI_list[-1])
        list_1.append(rsi_list[-1])
        list_1.append(d_list[-1])
        # for i in range(20):
        #     print("MFI" +str(MFI_list[-i]))
        # print("Vaianace")
        # print("MFI" +str(MFI_list[-1]))
        # print("rsi"+str(rsi_list[-1]))
        # print("d_list"+str(d_list[-1]) )
        W_moderate = 1/2*0.618**2*max(list_1)+1/2*min(list_1)+1/2*0.618*(MFI_list[-1]+rsi_list[-1]+d_list[-1]-max(list_1)-min(list_1))
        # W_buy = 1/2*0.618**2*max(list_1)+1/2*min(list_1)+1/2*0.618*(self.MFI_list[i]+self.rsi_list[i-2]+self.d_list[i]-max(list_1)-min(list_1))
        W_sell = 1/2*0.618**2*min(list_1)+1/2*max(list_1)+1/2*0.618*(MFI_list[-1]+rsi_list[-1]+d_list[-1]-max(list_1)-min(list_1))
        # print("W buy at: " +str(W_moderate))

        list_yesterday= []
        list_yesterday.append(MFI_list[-2])
        list_yesterday.append(rsi_list[-2])
        list_yesterday.append(d_list[-2])
        # for i in range(20):
        #     print("MFI" +str(MFI_list[-i]))
        # print("MFI" +str(MFI_list[-2]))
        # print("rsi"+str(rsi_list[-2]))
        # print(d_list[-2]) 
        W_moderate_yesterday = 1/2*0.618**2*max(list_yesterday)+1/2*min(list_yesterday)+1/2*0.618*(MFI_list[-2]+rsi_list[-2]+d_list[-2]-max(list_yesterday)-min(list_yesterday))
        # W_buy = 1/2*0.618**2*max(list_1)+1/2*min(list_1)+1/2*0.618*(self.MFI_list[i]+self.rsi_list[i-2]+self.d_list[i]-max(list_1)-min(list_1))
        W_sell_yesterday = 1/2*0.618**2*min(list_yesterday)+1/2*max(list_yesterday)+1/2*0.618*(MFI_list[-2]+rsi_list[-2]+d_list[-2]-max(list_yesterday)-min(list_yesterday))

        # W_value = (MFI_list[i]+rsi_list[i]+d_list[i+3])/3
        # if W_moderate < 17:  #### 25
        #     print("Time to purcharse as the W's value hits " + str(W_moderate)+ " Price: " +str(self.list_of_ending_price[-1]))
        #     # self.comparing_date_purchase.append(i+self.a)
        #     # print("rsi : " +str(rsi_list[i-2]))
        #     # print("MFI: " +str(MFI_list[i]))
        #     # print("D value: " + str(d_list[i]))
        # if W_sell> 45:
        #     print("Time to sell off as W's value hits"+ str(W_moderate)+ " Price : " + str(self.list_of_ending_price[-1]))
        #     # self.comparing_date_sell_off.append(i+self.a)

        return W_moderate,W_sell,W_moderate_yesterday,W_sell_yesterday

    def date_return(self):
        return self.list_of_date[-1]
    def ema_for_price_for_the_last_five_days(self):
        list_of_ending_price = [float(x) for x in self.list_of_ending_price]
        ema_value=0
        ema_15_list = []
        ema_5_list = []
        Z_5_list=[]
        Z_15_list=[]
        list_of_reflection2=[]

        for i in range(len(list_of_ending_price)): #currently, 7 days  => 14 days  len(list_of_ending_price)-14+x ##-self.x+1
            if i ==0:
                ema_value = list_of_ending_price[0]
                ema_15_list.append(ema_value)
            else:
                ema_value = (2/16)*list_of_ending_price[i] + ema_value* (1-2/16)
                ema_15_list.append(ema_value)
        
        ema_value= 0

        for i in range(len(list_of_ending_price)): #currently, 7 days  => 14 days  len(list_of_ending_price)-14+x ##-self.x+1
            if i ==0:
                ema_value = list_of_ending_price[0]
                ema_5_list.append(ema_value)
            else:
                ema_value = (2/6)*list_of_ending_price[i] + ema_value* (1-2/6)
                ema_5_list.append(ema_value)

        for i in range(len(list_of_ending_price)-5):
            a = len(list_of_ending_price)
            if i < 5:
                continue
            else:
                Z_5 = (list_of_ending_price[i] - np.average(ema_5_list[i-4:i]) )/ np.std(ema_5_list[i-4:i])
                Z_5_list.append(Z_5)
                # print(self.list_of_date[i+4])
                # print(self.list_of_ending_price[i+4])
                # print(Z_5)
        
        for i in range(len(list_of_ending_price)-15):
            a = len(list_of_ending_price)
            if i < 15:
                continue
            else:
                Z_15 = (list_of_ending_price[i] - np.average(ema_5_list[i-14:i]) )/ np.std(ema_5_list[i-14:i])
                Z_15_list.append(Z_15)
                # print(self.list_of_date[i+14])
                # print(self.list_of_ending_price[i+14])
                # print(Z_15)

        print("For Z_5 days")

        for i in self.list_of_reflection:
            if(i+1 >= len(self.W_moderate_list_within_class)):
                    list_of_reflection2.append(i)
                    break
            
            if (self.W_moderate_list_within_class[i+1]>=17):
                # print(self.W_moderate_list_within_class[i+1])
                list_of_reflection2.append(i)

        j = 0
        a=0
        for i in self.list_of_reflection:
            print(self.list_of_date[i+14])
            if float in Z_15_list:
                print(Z_15_list[i])
            else:
                break
            # print(i)
            # print(list_of_reflection2[j])
            if ( int(i) == int(list_of_reflection2[j])):
                # print("Good morning")
                for _ in range(self.elasped_day_list[a]):
                    if _ !=0:
                        print(self.list_of_date[i+14+_])
                        print(Z_15_list[i+_])
                a=a+1
                j= j+1
            print("Next one")

        print("As for Z_5")
        j=0
        a=0

        for i in self.list_of_reflection:
            print(self.list_of_date[i+14])
            print(Z_5_list[i])
            if ( int(i) == int(list_of_reflection2[j])):
                # print("Good morning")
                if int in self.elasped_day_list:      
                    for _ in range(self.elasped_day_list[a]):
                        if _ !=0:
                            print(self.list_of_date[i+14+_])
                            print(Z_15_list[i+_])
                else:
                    break
                a=a+1
                j= j+1
            print("Next one")


        return Z_15_list,Z_5_list
    
    def days_has_been_below_17(self):
        counter= 0
        i = 1
        # print(self.W_moderate_list_within_class)
        while (self.W_moderate_list_within_class[-i])<=17:
            # print("Hello World")
            # print(self.W_moderate_list_within_class[-i])
            i +=1
            counter +=1
        
        return counter

class using_risk_assessment():
    def __init__(self) -> None:
        pass

    def finding_one_agpd(self,id,place=None):
        a= risk_assessment(id,place)
        # a= risk_assessment("300002","SZ")
        risk_assessment.split_string(a)
        # risk_assessment.removing_million_and_thousands(a)
        risk_assessment.floating_list_of_volume_of_exchange_hand(a)
        # risk_assessment.reverse(a)
        risk_assessment.get_date(a)
        # risk_assessment.rate_of_range(a)
        risk_assessment.RSV(a)
        rsi_list =risk_assessment.ema(a)
        risk_assessment.K(a)
        d_list=risk_assessment.D(a)
        MFI_list=risk_assessment.MFI_list1(a)
        # print(MFI_list[-3])
        W_moderate_list,W_sell_list=risk_assessment.W_moderate(a)
        # risk_assessment.W_moderate(a)
        W_moderate,W_sell,W_moderate_yesterday,W_sell_yesterday= risk_assessment.W_moderate_at_last_day(a,MFI_list,rsi_list,d_list)
        date = risk_assessment.date_return(a)
        print(date)
        print("W_b" +str(W_moderate))
        print("W_sell" +str(W_sell))
        print("The other one")
        # for _ in range(len(W_moderate_list)):
        #     print(W_moderate_list[_])

        # print("W_B yesterday" + str(W_moderate_yesterday))
        agpd,length_of_the_buying_date,average_day,day_std_deviation = risk_assessment.income(a)
        risk_assessment.predicting_reflection(a)
        Z_15_list, Z_5_list = risk_assessment.ema_for_price_for_the_last_five_days(a)
        counter=risk_assessment.days_has_been_below_17(a)
        risk_assessment.close(a)
    
    def real_time_monitoring(self,id,place=None):
        a= risk_assessment(id,place)
        # # a= risk_assessment("300002","SZ")
        risk_assessment.split_string(a)
        # risk_assessment.check_if_update(a)
        # # risk_assessment.removing_million_and_thousands(a)
        risk_assessment.floating_list_of_volume_of_exchange_hand(a)
        # # risk_assessment.reverse(a)
        risk_assessment.get_date(a)
        # # risk_assessment.rate_of_range(a)
        rsv_list = risk_assessment.RSV(a)
        # # print(rsv_list[-1])
        risk_assessment.ema(a)
        risk_assessment.K(a)
        risk_assessment.D(a)
        risk_assessment.MFI_list1(a)
        # risk_assessment.W_moderate(a)
        # agpd = risk_assessment.income(a)
        # risk_assessment.monitoring_website(a)
        volume=risk_assessment.predictiing_volume_of_exchange_using_ema(a)

        for i in range(660):
            risk_assessment.getting_current_price(a)
            # print(volume)
            rsv_list = risk_assessment.prediciting_RSV(a)
            # print("rsv" +str(rsv_list))
            k_value=risk_assessment.prediciting_k(a,rsv_list)
            # print("k" +str(k_value))
            d_list = risk_assessment.predicitng_d(a,rsv_list,k_value)
            # print("d"+str(d_list))
            mfi_list=risk_assessment.predicting_MFI_list1(a,volume)
            # print("mfi_list" +str(mfi_list[-1]))
            rsi_list=risk_assessment.prediciting_ema(a)
            # print("rsi_list"+str(rsi_list[-1]))
            risk_assessment.prediciting_W_moderate(a,mfi_list,rsi_list,d_list)
            
            # risk_assessment.close(a)
            # risk_assessment.close(a)
            time.sleep(30)

    def what_is_price_when_w_is_fallen_to_20(self,id,place):
        # id = input("Which ID")
        # place = input("Which place")
        try:
            a= risk_assessment(id,place)

        except FileNotFoundError:
            print("Wrong code")
            return FileNotFoundError

        # # a= risk_assessment("300002","SZ")
        risk_assessment.split_string(a)
        # risk_assessment.check_if_update(a)
        # # risk_assessment.removing_million_and_thousands(a)
        risk_assessment.floating_list_of_volume_of_exchange_hand(a)
        # # risk_assessment.reverse(a)
        risk_assessment.get_date(a)
        # # risk_assessment.rate_of_range(a)
        rsv_list = risk_assessment.RSV(a)
        # # print(rsv_list[-1])
        risk_assessment.ema(a)
        risk_assessment.K(a)
        risk_assessment.D(a)
        risk_assessment.MFI_list1(a)
        # risk_assessment.W_moderate(a)
        # agpd = risk_assessment.income(a)
        # risk_assessment.monitoring_website(a)
        volume=risk_assessment.predictiing_volume_of_exchange_using_ema(a)
        W_moderate_trying =0
        W_sell_trying =0

        for i in range(1):
            risk_assessment.getting_current_price(a)
                # print(volume)
            rsv_list = risk_assessment.prediciting_RSV(a)
            # print("rsv" +str(rsv_list))
            k_value=risk_assessment.prediciting_k(a,rsv_list)
            # print("k" +str(k_value))
            d_list = risk_assessment.predicitng_d(a,rsv_list,k_value)
            # print("d"+str(d_list))
            mfi_list=risk_assessment.predicting_MFI_list1(a,volume)
            # print("mfi_list" +str(mfi_list[-1]))
            rsi_list=risk_assessment.prediciting_ema(a)
            # print("rsi_list"+str(rsi_list[-1]))
            W_moderate,W_sell = risk_assessment.prediciting_W_moderate(a,mfi_list,rsi_list,d_list)
            W_sell_trying=W_sell

            # print(type(W_moderate))
            W_moderate_trying= W_moderate

        percentage = 1

        while (W_moderate_trying > 17) :

            risk_assessment.getting_predictive_price(a,percentage)
            # print(volume)
            rsv_list = risk_assessment.prediciting_RSV(a)
            # print("rsv" +str(rsv_list))
            k_value=risk_assessment.prediciting_k(a,rsv_list)
            # print("k" +str(k_value))
            d_list = risk_assessment.predicitng_d(a,rsv_list,k_value)
            # print("d"+str(d_list))
            mfi_list=risk_assessment.predicting_MFI_list1(a,volume)
            # print("mfi_list" +str(mfi_list[-1]))
            rsi_list=risk_assessment.prediciting_ema(a)
            # print("rsi_list"+str(rsi_list[-1]))
            W_moderate_trying,W_sell  = risk_assessment.prediciting_W_moderate(a,mfi_list,rsi_list,d_list)
            percentage-=0.01
        else:
            return W_moderate_trying

    def what_is_price_when_w_sell_is_risen_to_40(self,id,place) -> str:
        # id = input("Which ID")
        # place = input("Which place")
        a= risk_assessment(id,place)
        # # a= risk_assessment("300002","SZ")
        risk_assessment.split_string(a)
        # risk_assessment.check_if_update(a)
        # # risk_assessment.removing_million_and_thousands(a)
        risk_assessment.floating_list_of_volume_of_exchange_hand(a)
        # # risk_assessment.reverse(a)
        risk_assessment.get_date(a)
        # # risk_assessment.rate_of_range(a)
        rsv_list = risk_assessment.RSV(a)
        # # print(rsv_list[-1])
        risk_assessment.ema(a)
        risk_assessment.K(a)
        risk_assessment.D(a)
        risk_assessment.MFI_list1(a)
        # risk_assessment.W_moderate(a)
        # agpd = risk_assessment.income(a)
        # risk_assessment.monitoring_website(a)
        volume=risk_assessment.predictiing_volume_of_exchange_using_ema(a)
        W_sell_trying =0

        for i in range(1):
            risk_assessment.getting_current_price(a)
                # print(volume)
            rsv_list = risk_assessment.prediciting_RSV(a)
            # print("rsv" +str(rsv_list))
            k_value=risk_assessment.prediciting_k(a,rsv_list)
            # print("k" +str(k_value))
            d_list = risk_assessment.predicitng_d(a,rsv_list,k_value)
            # print("d"+str(d_list))
            mfi_list=risk_assessment.predicting_MFI_list1(a,volume)
            # print("mfi_list" +str(mfi_list[-1]))
            rsi_list=risk_assessment.prediciting_ema(a)
            # print("rsi_list"+str(rsi_list[-1]))
            W_moderate,W_sell = risk_assessment.prediciting_W_moderate(a,mfi_list,rsi_list,d_list)
            W_sell_trying= W_sell

        percentage = 1

        while (W_sell_trying <=40.2) :

            risk_assessment.getting_predictive_price(a,percentage)
            # print(volume)
            rsv_list = risk_assessment.prediciting_RSV(a)
            # print("rsv" +str(rsv_list))
            k_value=risk_assessment.prediciting_k(a,rsv_list)
            # print("k" +str(k_value))
            d_list = risk_assessment.predicitng_d(a,rsv_list,k_value)
            # print("d"+str(d_list))
            mfi_list=risk_assessment.predicting_MFI_list1(a,volume)
            # print("mfi_list" +str(mfi_list[-1]))
            rsi_list=risk_assessment.prediciting_ema(a)
            # print("rsi_list"+str(rsi_list[-1]))
            W_moderate_trying,W_sell_trying  = risk_assessment.prediciting_W_moderate(a,mfi_list,rsi_list,d_list)
            percentage+= 0.01
        else:
            longstring = f"When W rise to 40 : {W_sell_trying} "
            print(longstring)

        a= risk_assessment(id,place)
        # # a= risk_assessment("300002","SZ")
        risk_assessment.split_string(a)
        # risk_assessment.check_if_update(a)
        # # risk_assessment.removing_million_and_thousands(a)
        risk_assessment.floating_list_of_volume_of_exchange_hand(a)
        # # risk_assessment.reverse(a)
        risk_assessment.get_date(a)
        # # risk_assessment.rate_of_range(a)
        rsv_list = risk_assessment.RSV(a)
        # # print(rsv_list[-1])
        risk_assessment.ema(a)
        risk_assessment.K(a)
        risk_assessment.D(a)
        risk_assessment.MFI_list1(a)
        # risk_assessment.W_moderate(a)
        # agpd = risk_assessment.income(a)
        # risk_assessment.monitoring_website(a)
        volume=risk_assessment.predictiing_volume_of_exchange_using_ema(a)
        W_sell_trying =0

        for i in range(1):
            risk_assessment.getting_current_price(a)
                # print(volume)
            rsv_list = risk_assessment.prediciting_RSV(a)
            # print("rsv" +str(rsv_list))
            k_value=risk_assessment.prediciting_k(a,rsv_list)
            # print("k" +str(k_value))
            d_list = risk_assessment.predicitng_d(a,rsv_list,k_value)
            # print("d"+str(d_list))
            mfi_list=risk_assessment.predicting_MFI_list1(a,volume)
            # print("mfi_list" +str(mfi_list[-1]))
            rsi_list=risk_assessment.prediciting_ema(a)
            # print("rsi_list"+str(rsi_list[-1]))
            W_moderate,W_sell = risk_assessment.prediciting_W_moderate(a,mfi_list,rsi_list,d_list)
            W_sell_trying= W_sell

        percentage = 1

        while (W_sell_trying >=W_sell+10.5 or W_sell_trying<= W_sell+9.5) :
            if (W_sell_trying<= W_sell+9.5):
                risk_assessment.getting_predictive_price(a,percentage)
                # print(volume)
                rsv_list = risk_assessment.prediciting_RSV(a)
                # print("rsv" +str(rsv_list))
                k_value=risk_assessment.prediciting_k(a,rsv_list)
                # print("k" +str(k_value))
                d_list = risk_assessment.predicitng_d(a,rsv_list,k_value)
                # print("d"+str(d_list))
                mfi_list=risk_assessment.predicting_MFI_list1(a,volume)
                # print("mfi_list" +str(mfi_list[-1]))
                rsi_list=risk_assessment.prediciting_ema(a)
                # print("rsi_list"+str(rsi_list[-1]))
                W_moderate_trying,W_sell_trying  = risk_assessment.prediciting_W_moderate(a,mfi_list,rsi_list,d_list)
                percentage+= 0.001
            elif(W_sell_trying >=W_sell+10.5):
                risk_assessment.getting_predictive_price(a,percentage)
            # print(volume)
                rsv_list = risk_assessment.prediciting_RSV(a)
                # print("rsv" +str(rsv_list))
                k_value=risk_assessment.prediciting_k(a,rsv_list)
                # print("k" +str(k_value))
                d_list = risk_assessment.predicitng_d(a,rsv_list,k_value)
                # print("d"+str(d_list))
                mfi_list=risk_assessment.predicting_MFI_list1(a,volume)
                # print("mfi_list" +str(mfi_list[-1]))
                rsi_list=risk_assessment.prediciting_ema(a)
                # print("rsi_list"+str(rsi_list[-1]))
                W_moderate_trying,W_sell_trying = risk_assessment.prediciting_W_moderate(a,mfi_list,rsi_list,d_list)
                percentage-=0.001
        else:
            longstring2 = f"When W rise plus 10 {W_sell_trying}" 
            print( longstring2)
            print("Why2")
            return str(longstring),str(longstring2)

    def reflective_price(self,id,place,price):
        # id = input("Which ID")
        # place = input("Which place")
        # price = input("Which price")
        a= risk_assessment(id,place)
        # # a= risk_assessment("300002","SZ")
        risk_assessment.split_string(a)
        # risk_assessment.check_if_update(a)
        # # risk_assessment.removing_million_and_thousands(a)
        risk_assessment.floating_list_of_volume_of_exchange_hand(a)
        # # risk_assessment.reverse(a)
        risk_assessment.get_date(a)
        # # risk_assessment.rate_of_range(a)
        rsv_list = risk_assessment.RSV(a)
        # # print(rsv_list[-1])
        risk_assessment.ema(a)
        risk_assessment.K(a)
        risk_assessment.D(a)
        risk_assessment.MFI_list1(a)
        # risk_assessment.W_moderate(a)
        # agpd = risk_assessment.income(a)
        # risk_assessment.monitoring_website(a)
        volume=risk_assessment.predictiing_volume_of_exchange_using_ema(a)
        W_sell_trying =0

        for i in range(1):
            risk_assessment.persumable_price(a,price)
                # print(volume)
            rsv_list = risk_assessment.prediciting_RSV(a)
            # print("rsv" +str(rsv_list))
            k_value=risk_assessment.prediciting_k(a,rsv_list)
            # print("k" +str(k_value))
            d_list = risk_assessment.predicitng_d(a,rsv_list,k_value)
            # print("d"+str(d_list))
            mfi_list=risk_assessment.predicting_MFI_list1(a,volume)
            # print("mfi_list" +str(mfi_list[-1]))
            rsi_list=risk_assessment.prediciting_ema(a)
            # print("rsi_list"+str(rsi_list[-1]))
            W_moderate,W_sell = risk_assessment.prediciting_W_moderate(a,mfi_list,rsi_list,d_list)
            W_sell_trying= W_sell
        
        return W_sell

        # percentage = 1

    def what_is_price_when_w_sell_is_risen_to_10_plus_current(self,id,place,w_sell_diff):
        # id = input("Which ID")
        # place = input("Which place")
        w_sell_diff=float(w_sell_diff)
        
        a= risk_assessment(id,place)
        # # a= risk_assessment("300002","SZ")
        risk_assessment.split_string(a)
        # risk_assessment.check_if_update(a)
        # # risk_assessment.removing_million_and_thousands(a)
        risk_assessment.floating_list_of_volume_of_exchange_hand(a)
        # # risk_assessment.reverse(a)
        risk_assessment.get_date(a)
        # # risk_assessment.rate_of_range(a)
        rsv_list = risk_assessment.RSV(a)
        # # print(rsv_list[-1])
        risk_assessment.ema(a)
        risk_assessment.K(a)
        risk_assessment.D(a)
        risk_assessment.MFI_list1(a)
        # risk_assessment.W_moderate(a)
        # agpd = risk_assessment.income(a)
        # risk_assessment.monitoring_website(a)
        volume=risk_assessment.predictiing_volume_of_exchange_using_ema(a)
        W_sell_trying =0

        for i in range(1):
            risk_assessment.getting_current_price(a)
                # print(volume)
            rsv_list = risk_assessment.prediciting_RSV(a)
            # print("rsv" +str(rsv_list))
            k_value=risk_assessment.prediciting_k(a,rsv_list)
            # print("k" +str(k_value))
            d_list = risk_assessment.predicitng_d(a,rsv_list,k_value)
            # print("d"+str(d_list))
            mfi_list=risk_assessment.predicting_MFI_list1(a,volume)
            # print("mfi_list" +str(mfi_list[-1]))
            rsi_list=risk_assessment.prediciting_ema(a)
            # print("rsi_list"+str(rsi_list[-1]))
            W_moderate,W_sell = risk_assessment.prediciting_W_moderate(a,mfi_list,rsi_list,d_list)
            W_sell_trying= W_sell

        percentage = 1

        while (W_sell_trying >=W_sell+(w_sell_diff+0.5) or W_sell_trying<= W_sell+(w_sell_diff-0.5)) :
            if (W_sell_trying<= W_sell+w_sell_diff-0.5):
                risk_assessment.getting_predictive_price(a,percentage)
                # print(volume)
                rsv_list = risk_assessment.prediciting_RSV(a)
                # print("rsv" +str(rsv_list))
                k_value=risk_assessment.prediciting_k(a,rsv_list)
                # print("k" +str(k_value))
                d_list = risk_assessment.predicitng_d(a,rsv_list,k_value)
                # print("d"+str(d_list))
                mfi_list=risk_assessment.predicting_MFI_list1(a,volume)
                # print("mfi_list" +str(mfi_list[-1]))
                rsi_list=risk_assessment.prediciting_ema(a)
                # print("rsi_list"+str(rsi_list[-1]))
                W_moderate_trying,W_sell_trying  = risk_assessment.prediciting_W_moderate(a,mfi_list,rsi_list,d_list)
                percentage+= 0.001
            elif(W_sell_trying >=W_sell+w_sell_diff+0.5):
                risk_assessment.getting_predictive_price(a,percentage)
            # print(volume)
                rsv_list = risk_assessment.prediciting_RSV(a)
                # print("rsv" +str(rsv_list))
                k_value=risk_assessment.prediciting_k(a,rsv_list)
                # print("k" +str(k_value))
                d_list = risk_assessment.predicitng_d(a,rsv_list,k_value)
                # print("d"+str(d_list))
                mfi_list=risk_assessment.predicting_MFI_list1(a,volume)
                # print("mfi_list" +str(mfi_list[-1]))
                rsi_list=risk_assessment.prediciting_ema(a)
                # print("rsi_list"+str(rsi_list[-1]))
                W_moderate_trying,W_sell_trying = risk_assessment.prediciting_W_moderate(a,mfi_list,rsi_list,d_list)
                percentage-=0.001
        else:
            return (W_sell_trying)
    def checking_everything_at_night_for_agpd_for_America(self):
        stock_price_shenzhen = r"/home/ricky/Documents/Stockid_data/list_of_shenzhen.txt"
        stock_price_shanghai = r"/home/ricky/Documents/Stockid_data/list_of_shanghai.txt"
        stock_price_america = r"/home/ricky/Documents/agpd_america_2024-04-03_all_0.001.txt"

        filename = "agpd_america_" + str(current_datetime)+"_all_0.001.txt"

        list_for_shanghai =[]
        list_for_shenzhen =[]
        list_for_america = []
        f=open(stock_price_america,'r',encoding="utf8")
        strings = f.read().split("\n")
        strings=strings[1:-1]
        # print(strings)
        for string in strings:
            string= string.split(" ",1)[0]
            # print(string)
            list_for_america.append(string)
            # print(strings123)



        list1 = ['']
        agpd_list = []
        # date = "2019-01-21"
        agpd_1  = 0
        stock_id_list = []
        number_of_trade_list = []
        W_moderate_list=[]
        W_sell_list=[]
        date_list = []
        average_day_list=[]
        day_std_deviation_list=[]
        W_sell_yesterday_list=[]
        W_moderate_yesterday_list=[]
        percentage_difference_in_W_moderate_list=[]
        five_day_average_of_W_buy_list=[]
        ending_price_list = []

        for i in list_for_america:
            try:
                
                # i = str(i).zfill(6)
                # # i =str(i)
                print(i)
                if (i=="NCPL" or i == "NUKK" or i == "XBIOW" or i == "WTER"):
                    continue
                # print(list)
                # instance = risk_assessment()
                # instance.close()
                # a=a+str(i)
                a= risk_assessment(i,"")

            except IndexError: 
                print("Index Error")
                pass
            except FileNotFoundError:
                # print(filename)
                print("File Not found error")
                pass

            except ZeroDivisionError:
                print("Zero ")

            else:
                # print("Hello world")
                digit = risk_assessment.split_string(a)
                # risk_assessment.removing_million_and_thousands(a)
                # print(list_of_ending_price)
                if digit ==10:
                    agpd_1 =-100
                    print(agpd_1)
                    agpd_list.append(agpd_1)
                else:
                    risk_assessment.floating_list_of_volume_of_exchange_hand(a)
                    # risk_assessment.reverse(a)
                    risk_assessment.get_date(a)
                    # risk_assessment.rate_of_range(a)
                    risk_assessment.RSV(a)
                    rsi_list =risk_assessment.ema(a)
                    risk_assessment.K(a)
                    d_list=risk_assessment.D(a)
                    MFI_list=risk_assessment.MFI_list1(a)
                    W_moderate123_list,W_sell123_list=risk_assessment.W_moderate(a)
                    # risk_assessment.W_moderate(a)
                    W_moderate,W_sell,W_moderate_yesterday,W_sell_yesterday= risk_assessment.W_moderate_at_last_day(a,MFI_list,rsi_list,d_list)
                    W_moderate_list.append(W_moderate)
                    W_moderate_yesterday_list.append(W_moderate_yesterday)
                    W_sell_yesterday_list.append(W_sell_yesterday)
                    W_sell_list.append(W_sell)
                    five_days_of_W_buy=np.array(W_moderate123_list[-6:-1])
                    average_five_days_W_buy=np.mean(five_days_of_W_buy)
                    five_day_average_of_W_buy_list.append(average_five_days_W_buy)
                    percentage_difference_in_W_moderate=(W_moderate-W_moderate_yesterday)/W_moderate_yesterday*100
                    percentage_difference_in_W_moderate_list.append(percentage_difference_in_W_moderate)
                    agpd_1,day,average_day,day_std_deviation = risk_assessment.income(a)
                    average_day_list.append(average_day)
                    day_std_deviation_list.append(day_std_deviation)
                    number_of_trade_list.append(day)
                    date = risk_assessment.date_return(a)
                    date_list.append(date)
                    # print(agpd_1)
                    agpd_list.append(agpd_1)
                    stock_id_list.append(i)
                    ending_price = risk_assessment.price_return(a)
                    ending_price_list.append(ending_price)
                    risk_assessment.close(a)

                # except:
                #     print("pass")

        # print(agpd_list)
        with open(filename,'a+') as f:
            f.write("Stock_ID" + " " + "AGPD_value" + " "+ "Current_Price"+" "+ "Number_of_Trade"+ " "+"W_buy_value_now" + " " + "W_sell_value"+ " "+"day_last_update" + " "+"Average_day"+ " " + "Day_standard_deviation " +"W_moderate_%_diff"+" "+"five_day_average_of_W_buy"+"\n") 

            for i in range(len(agpd_list)-5):
            #     print("List of agpd_list" +str(len(agpd_list)))
            #     print("List of number_of_trade_list" +str(len(number_of_trade_list)))
            #     print("List of W_moderate_list" +str(len(W_moderate_list)))
            #     print("List of five_day_average_list" +str(len(five_day_average_of_W_buy_list)))
            #     print("List of percentage_difference_list" +str(len(percentage_difference_in_W_moderate_list)))
            #     print("List of average_day_list" +str(len(average_day_list)))
            #     print("List of day_list" +str(len(date_list)))
            #     print("List of stockid_list" +str(len(stock_id_list)))
            #     print("List of W_sell_list" +str(len(W_sell_list)))



                # print("List of date_standard deviation_list" +str(len(day_std_deviation_list)))


                # with open(filename,'a+') as f:
                # if (agpd_list[i] != 1):
                if (agpd_list[i] > 0.001 and number_of_trade_list[i]>=4 and agpd_list[i]!=1 and float(ending_price_list[i])>=2 and W_moderate_list[i]>0):
                    # index = agpd_list.index(i)
                    # with open(filename,'a+') as f:
                    f.write(str(stock_id_list[i]) + " " + str(agpd_list[i])+" " +str(ending_price_list[i]) + " "+ str(number_of_trade_list[i])+ " "+str(W_moderate_list[i]) + " " + str(W_sell_list[i])+ " "+str(date_list[i]) + " "+str(average_day_list[i])+ " "+str(day_std_deviation_list[i])+" "+ str(percentage_difference_in_W_moderate_list[i])+" "+str(five_day_average_of_W_buy_list[i])+"\n") 
                    print("Stock id: " + str(stock_id_list[i]))
                    print("agpd: " +str(agpd_list[i]))

    def checking_everything_at_night_for_agpd_for_SS(self):
        stock_price_shenzhen = r"/home/ricky/Documents/Stockid_data/list_of_shenzhen.txt"
        stock_price_shanghai = r"/home/ricky/Documents/Stockid_data/list_of_shanghai.txt"

        filename = "agpd_china_" + str(current_datetime)+"_all_0.001.txt"

        list_for_shanghai =[]
        list_for_shenzhen =[]
        f=open(stock_price_shanghai,'r',encoding="utf8")
        strings = f.read().split("\n")
        strings=strings[1:-1]
        for string in strings:
            # print(string[:6])
            list_for_shanghai.append(int(string[:6]))
            # print(int(string[:6]))

        s=open(stock_price_shenzhen,'r',encoding="utf8")
        strings123 = s.read().split("\n")
        strings123=strings123[1:-2]
        # print(strings123)
        for string in strings123:
            # print(string[:6])
            if (string[:6] == "301408"):
                # print("Je")
                break 
            
            # print(string[:6])
            list_for_shenzhen.append(int(string[:6]))


        list1 = ['SS']
        agpd_list = []
        # date = "2019-01-21"
        agpd_1  = 0
        stock_id_list = []
        number_of_trade_list = []
        W_moderate_list=[]
        W_sell_list=[]
        date_list = []
        average_day_list=[]
        day_std_deviation_list=[]
        W_sell_yesterday_list=[]
        W_moderate_yesterday_list=[]
        percentage_difference_in_W_moderate_list=[]
        five_day_average_of_W_buy_list=[]
        days_have_been=[]

        for list in list1:
            for i in list_for_shanghai:
                try:
                    
                    i = str(i).zfill(6)
                    # i =str(i)
                    print(i)
                    # print(list)
                    # instance = risk_assessment()
                    # instance.close()
                    # a=a+str(i)
                    a= risk_assessment(i,list)

                except IndexError: 
                    print("Index Error")
                    pass
                except FileNotFoundError:
                    print("File Not found error")
                    pass

                except ZeroDivisionError:
                    print("Zero ")

                else:
                    # print("Hello world")
                    digit = risk_assessment.split_string(a)
                    # risk_assessment.removing_million_and_thousands(a)
                    # print(list_of_ending_price)
                    if digit ==10:
                        agpd_1 =-100
                        print(agpd_1)
                        agpd_list.append(agpd_1)
                    else:
                        risk_assessment.floating_list_of_volume_of_exchange_hand(a)
                        # risk_assessment.reverse(a)
                        risk_assessment.get_date(a)
                        # risk_assessment.rate_of_range(a)
                        risk_assessment.RSV(a)
                        rsi_list =risk_assessment.ema(a)
                        risk_assessment.K(a)
                        d_list=risk_assessment.D(a)
                        MFI_list=risk_assessment.MFI_list1(a)
                        W_moderate123_list,W_sell123_list=risk_assessment.W_moderate(a)
                        # risk_assessment.W_moderate(a)
                        W_moderate,W_sell,W_moderate_yesterday,W_sell_yesterday= risk_assessment.W_moderate_at_last_day(a,MFI_list,rsi_list,d_list)
                        W_moderate_list.append(W_moderate)

                        W_moderate_yesterday_list.append(W_moderate_yesterday)
                        W_sell_yesterday_list.append(W_sell_yesterday)
                        W_sell_list.append(W_sell)
                        five_days_of_W_buy=np.array(W_moderate123_list[-6:-1])
                        average_five_days_W_buy=np.mean(five_days_of_W_buy)
                        five_day_average_of_W_buy_list.append(average_five_days_W_buy)
                        percentage_difference_in_W_moderate=(W_moderate-W_moderate_yesterday)/W_moderate_yesterday*100
                        percentage_difference_in_W_moderate_list.append(percentage_difference_in_W_moderate)
                        agpd_1,day,average_day,day_std_deviation = risk_assessment.income(a)
                        average_day_list.append(average_day)
                        day_std_deviation_list.append(day_std_deviation)
                        number_of_trade_list.append(day)
                        date = risk_assessment.date_return(a)
                        date_list.append(date)
                        # print(agpd_1)
                        agpd_list.append(agpd_1)
                        stock_id_list.append(i)
                        counter = risk_assessment.days_has_been_below_17(a)
                        days_have_been.append(counter)
                        risk_assessment.close(a)

                # except:
                #     print("pass")

        # print(agpd_list)
        with open(filename,'a+') as f:
            f.write("Stock_ID" + " " + "AGPD_value" + " "+ "Number_of_Trade"+ " "+"W_buy_value_now" + " " + "W_sell_value"+ " "+"day_last_update" + " "+"Average_day"+ " " + "Day_standard_deviation " +"W_moderate_%_diff"+" "+"five_day_average_of_W_buy"+ " "+"Days_have_been_below_17"+"\n") 

            for i in range(len(agpd_list)-5):
            #     print("List of agpd_list" +str(len(agpd_list)))
            #     print("List of number_of_trade_list" +str(len(number_of_trade_list)))
            #     print("List of W_moderate_list" +str(len(W_moderate_list)))
            #     print("List of five_day_average_list" +str(len(five_day_average_of_W_buy_list)))
            #     print("List of percentage_difference_list" +str(len(percentage_difference_in_W_moderate_list)))
            #     print("List of average_day_list" +str(len(average_day_list)))
            #     print("List of day_list" +str(len(date_list)))
            #     print("List of stockid_list" +str(len(stock_id_list)))
            #     print("List of W_sell_list" +str(len(W_sell_list)))



                # print("List of date_standard deviation_list" +str(len(day_std_deviation_list)))


                # with open(filename,'a+') as f:
                # if (agpd_list[i] != 1):
                if (agpd_list[i] > 0.001 and number_of_trade_list[i]>=4 and agpd_list[i]!=1):
                    # index = agpd_list.index(i)
                    # with open(filename,'a+') as f:
                    f.write(str(stock_id_list[i]) + " " + str(agpd_list[i]) + " "+ str(number_of_trade_list[i])+ " "+str(W_moderate_list[i]) + " " + str(W_sell_list[i])+ " "+str(date_list[i]) + " "+str(average_day_list[i])+ " "+str(day_std_deviation_list[i])+" "+ str(percentage_difference_in_W_moderate_list[i])+" "+str(five_day_average_of_W_buy_list[i])+" "+str(days_have_been[i])+"\n") 
                    print("Stock id: " + str(stock_id_list[i]))
                    print("agpd: " +str(agpd_list[i]))
        # for i in range(len(agpd_list)-5):
        #     print(len(agpd_list))
        #     print(len(number_of_trade_list))
        #     # if (agpd_list[i] != 1):
        #     if (agpd_list[i] > 0.001 and number_of_trade_list[i]>=4 and agpd_list[i]!=1):
        #         # index = agpd_list.index(i)
        #         with open(filename,'a+') as f:
        #             f.write(str(stock_id_list[i]) + " " + str(agpd_list[i]) + " "+ str(number_of_trade_list[i])+ " "+str(W_moderate_list[i]) + " " + str(W_sell_list[i])+ " "+str(date_list[i])+" "+str(average_day_list[i]) +"\n") 
        #         print("Stock id: " + str(stock_id_list[i]))
        #         print("agpd: " +str(agpd_list[i]))
    def checking_everything_at_night_for_agpd_for_SZ(self):
        stock_price_shenzhen = r"/home/ricky/Documents/Stockid_data/list_of_shenzhen.txt"
        stock_price_shanghai = r"/home/ricky/Documents/Stockid_data/list_of_shanghai.txt"

        filename = "agpd_china_" + str(current_datetime)+"_all_0.001.txt"

        list_for_shanghai =[]
        list_for_shenzhen =[]
        f=open(stock_price_shanghai,'r',encoding="utf8")
        strings = f.read().split("\n")
        strings=strings[1:-1]
        for string in strings:
            # print(string[:6])
            list_for_shanghai.append(int(string[:6]))
            # print(int(string[:6]))

        s=open(stock_price_shenzhen,'r',encoding="utf8")
        strings123 = s.read().split("\n")
        strings123=strings123[1:-2]
        # print(strings123)
        for string in strings123:
            # print(string[:6])
            if (string[:6] == "301408"):
                # print("Je")
                break 
            
            # print(string[:6])
            list_for_shenzhen.append(int(string[:6]))


        list1 = ['SZ']
        agpd_list = []
        # date = "2019-01-21"
        agpd_1  = 0
        stock_id_list = []
        number_of_trade_list = []
        W_moderate_list=[]
        W_sell_list=[]
        date_list = []
        average_day_list=[]
        day_std_deviation_list=[]
        W_sell_yesterday_list=[]
        W_moderate_yesterday_list=[]
        percentage_difference_in_W_moderate_list=[]
        five_day_average_of_W_buy_list=[]
        days_have_been=[]

        for list in list1:
            for i in list_for_shenzhen:
                try:
                    
                    i = str(i).zfill(6)
                    # i =str(i)
                    print(i)
                    # print(list)
                    # instance = risk_assessment()
                    # instance.close()
                    # a=a+str(i)
                    a= risk_assessment(i,list)

                except IndexError: 
                    print("Index Error")
                    pass
                except FileNotFoundError:
                    print("File Not found error")
                    pass

                except ZeroDivisionError:
                    print("Zero ")

                else:
                    # print("Hello world")
                    digit = risk_assessment.split_string(a)
                    # risk_assessment.removing_million_and_thousands(a)
                    # print(list_of_ending_price)
                    if digit ==10:
                        agpd_1 =-100
                        print(agpd_1)
                        agpd_list.append(agpd_1)
                    else:
                        risk_assessment.floating_list_of_volume_of_exchange_hand(a)
                        # risk_assessment.reverse(a)
                        risk_assessment.get_date(a)
                        # risk_assessment.rate_of_range(a)
                        risk_assessment.RSV(a)
                        rsi_list =risk_assessment.ema(a)
                        risk_assessment.K(a)
                        d_list=risk_assessment.D(a)
                        MFI_list=risk_assessment.MFI_list1(a)
                        W_moderate123_list,W_sell123_list=risk_assessment.W_moderate(a)
                        five_days_of_W_buy=np.array(W_moderate123_list[-6:-1])
                        average_five_days_W_buy=np.mean(five_days_of_W_buy)
                        five_day_average_of_W_buy_list.append(average_five_days_W_buy)
                        # risk_assessment.W_moderate(a)
                        W_moderate,W_sell,W_moderate_yesterday,W_sell_yesterday= risk_assessment.W_moderate_at_last_day(a,MFI_list,rsi_list,d_list)
                        W_moderate_list.append(W_moderate)
                        W_moderate_yesterday_list.append(W_moderate_yesterday)
                        W_sell_yesterday_list.append(W_sell_yesterday)
                        W_sell_list.append(W_sell)
                        percentage_difference_in_W_moderate=(W_moderate-W_moderate_yesterday)/W_moderate_yesterday*100
                        percentage_difference_in_W_moderate_list.append(percentage_difference_in_W_moderate)
                        agpd_1,day,average_day,day_std_deviation = risk_assessment.income(a)
                        day_std_deviation_list.append(day_std_deviation)
                        average_day_list.append(average_day)
                        number_of_trade_list.append(day)
                        date = risk_assessment.date_return(a)
                        date_list.append(date)
                        # print(agpd_1)
                        agpd_list.append(agpd_1)
                        stock_id_list.append(i)
                        counter = risk_assessment.days_has_been_below_17(a)
                        days_have_been.append(counter)
                        risk_assessment.close(a)

                # except:
                #     print("pass")

        # print(agpd_list)
        with open(filename,'a+') as f:
            # f.write("Stock_ID" + " " + "AGPD_value" + " "+ "Number_of_Trade"+ " "+"W_moderate_value_now" + " " + "W_sell_value"+ " "+"day_last_update" + " "+"Average_day"+ " " + "Day_standard_deviation " +"W_moderate_%_diff"+" "+"five_day_average_of_W_buy"+"\n") 

            for i in range(len(agpd_list)-1):
                print(len(agpd_list))
                print(len(number_of_trade_list))

                # with open(filename,'a+') as f:
                # if (agpd_list[i] != 1):
                if (agpd_list[i] > 0.001 and number_of_trade_list[i]>=4 and agpd_list[i]!=1):
                    # index = agpd_list.index(i)
                    # with open(filename,'a+') as f:
                    f.write(str(stock_id_list[i]) + " " + str(agpd_list[i]) + " "+ str(number_of_trade_list[i])+ " "+str(W_moderate_list[i]) + " " + str(W_sell_list[i])+ " "+str(date_list[i]) + " "+str(average_day_list[i])+ " "+str(day_std_deviation_list[i])+" "+ str(percentage_difference_in_W_moderate_list[i])+" "+str(five_day_average_of_W_buy_list[i])+" "+str(days_have_been[i])+"\n") 
                    print("Stock id: " + str(stock_id_list[i]))
                    print("agpd: " +str(agpd_list[i]))
    def checking_everything_at_night_for_agpd_for_CHINA(self):
        using_risk_assessment.checking_everything_at_night_for_agpd_for_SS(self)
        using_risk_assessment.checking_everything_at_night_for_agpd_for_SZ(self)

    def checking_everything_at_night_for_agpd_for_bought(self):
        temp_list=[]
        while True:
            temp = input("What did we buy")
            if temp == " " or temp== "":
                break
            else: 
                temp=int(temp)
                temp_list.append(temp)


        stock_price_shenzhen = r"/home/ricky/Documents/Stockid_data/list_of_shenzhen.txt"
        stock_price_shanghai = r"/home/ricky/Documents/Stockid_data/list_of_shanghai.txt"

        filename = "agpd_bought_" + str(current_datetime)+"_all_0.001.txt"

        list_for_shanghai =[]
        list_for_shenzhen =[]
        f=open(stock_price_shanghai,'r',encoding="utf8")
        strings = f.read().split("\n")
        strings=strings[1:-1]
        for string in strings:
            # print(string[:6])
            list_for_shanghai.append(int(string[:6]))
            # print(int(string[:6]))

        s=open(stock_price_shenzhen,'r',encoding="utf8")
        strings123 = s.read().split("\n")
        strings123=strings123[1:-2]
        # print(strings123)
        for string in strings123:
            # print(string[:6])
            if (string[:6] == "301408"):
                # print("Je")
                break 
            
            # print(string[:6])
            list_for_shenzhen.append(int(string[:6]))


        list1 = ['SZ','SS']
        agpd_list = []
        # date = "2019-01-21"
        agpd_1  = 0
        stock_id_list = []
        number_of_trade_list = []
        W_moderate_list=[]
        W_sell_list=[]
        date_list = []
        # temp_list=[2595,2319]
        print(temp_list)

        for list in list1:
            for i in temp_list:
                try:
                    
                    i = str(i).zfill(6)
                    # i =str(i)
                    # print("\n")
                    # print(i)
                    # print(list)
                    # instance = risk_assessment()
                    # instance.close()
                    # a=a+str(i)
                    a= risk_assessment(i,list)

                except IndexError: 
                    print("Index Error")
                    pass
                except FileNotFoundError:
                    # print("File Not found error")
                    pass

                except ZeroDivisionError:
                    print("Zero ")

                else:
                    # print("Hello world")
                    print("\n")
                    print(i)
                    digit = risk_assessment.split_string(a)
                    # risk_assessment.removing_million_and_thousands(a)
                    # print(list_of_ending_price)
                    if digit ==10:
                        agpd_1 =-100
                        print(agpd_1)
                        agpd_list.append(agpd_1)
                    else:
                        risk_assessment.floating_list_of_volume_of_exchange_hand(a)
                        # risk_assessment.reverse(a)
                        risk_assessment.get_date(a)
                        # risk_assessment.rate_of_range(a)
                        risk_assessment.RSV(a)
                        rsi_list =risk_assessment.ema(a)
                        risk_assessment.K(a)
                        d_list=risk_assessment.D(a)
                        MFI_list=risk_assessment.MFI_list1(a)
                        W_moderate_list,W_sell_list=risk_assessment.W_moderate(a)
                        # risk_assessment.W_moderate(a)
                        W_moderate,W_sell,W_moderate_yesterday,W_sell_yesterday= risk_assessment.W_moderate_at_last_day(a,MFI_list,rsi_list,d_list)
                        W_moderate=round(W_moderate,2)
                        W_sell=round(W_sell,2)
                        W_moderate=round(W_moderate_yesterday,2)
                        W_sell_yesterday=round(W_sell_yesterday,2)
                        print("W_ buy_now :" +str(W_moderate))
                        print("W_Sell_now : "+str(W_sell))
                        print("The change in W_buy is " +str(round((W_moderate-W_moderate_yesterday)/W_moderate_yesterday*100,4))+"%")
                        print("The change in W_sell is " +str(round((W_sell-W_sell_yesterday)/W_sell_yesterday*100,4))+"%")
                        five_days_of_W_buy=np.array(W_moderate_list[-5:])
                        average_five_days_W_buy=np.mean(five_days_of_W_buy)
                        five_days_of_W_sell=np.array(W_sell_list[-5:])
                        average_five_days_W_sell=np.mean(five_days_of_W_sell)

                        print("The last 5 day average of W_buy: "+str(round(average_five_days_W_buy,4)))
                        print("The last 5 day average of W_sell: "+str(round(average_five_days_W_sell,4)))


                        W_moderate_list.append(W_moderate)
                        W_sell_list.append(W_sell)
                        agpd_1,day,average_day,day_std_deviation = risk_assessment.income(a)
                        number_of_trade_list.append(day)
                        date = risk_assessment.date_return(a)
                        date_list.append(date)
                        # print(agpd_1)
                        agpd_list.append(agpd_1)
                        stock_id_list.append(i)
                        # print("\n")
                        risk_assessment.close(a)

                # except:
                #     print("pass")

        # print(agpd_list)
        # for i in range(len(agpd_list)-5):
        #     print(len(agpd_list))
        #     print(len(number_of_trade_list))
        #     # if (agpd_list[i] != 1):
        #     if (agpd_list[i] > 0.001 and number_of_trade_list[i]>=4 and agpd_list[i]!=1):
        #         # index = agpd_list.index(i)
        #         with open(filename,'a+') as f:
        #             f.write(str(stock_id_list[i]) + " " + str(agpd_list[i]) + " "+ str(number_of_trade_list[i])+ " "+str(W_moderate_list[i]) + " " + str(W_sell_list[i])+ " "+str(date_list[i]) +"\n") 
        #         print("Stock id: " + str(stock_id_list[i]))
        #         print("agpd: " +str(agpd_list[i]))
    
    def getting_latest_date(self,id,place=None):
        a= risk_assessment(id,place)
        # a= risk_assessment("300002","SZ")
        risk_assessment.split_string(a)
        # risk_assessment.removing_million_and_thousands(a)
        risk_assessment.floating_list_of_volume_of_exchange_hand(a)
        # risk_assessment.reverse(a)
        risk_assessment.get_date(a)
        return risk_assessment.date_return(a)

    
## checking a particular stock for its agpd

if __name__=='__main__': 
    a=using_risk_assessment()
    using_risk_assessment.finding_one_agpd(a,"301039","SZ")
    # using_risk_assessment.what_is_price_when_w_is_fallen_to_20(a)
# a= risk_assessment("301039","SZ")
# # a= risk_assessment("300002","SZ")
# risk_assessment.split_string(a)
# # risk_assessment.removing_million_and_thousands(a)
# risk_assessment.floating_list_of_volume_of_exchange_hand(a)
# # risk_assessment.reverse(a)
# risk_assessment.get_date(a)
# # risk_assessment.rate_of_range(a)
# risk_assessment.RSV(a)
# rsi_list =risk_assessment.ema(a)
# risk_assessment.K(a)
# d_list=risk_assessment.D(a)
# MFI_list=risk_assessment.MFI_list1(a)
# risk_assessment.W_moderate(a)
# W_moderate,W_sell= risk_assessment.W_moderate_at_last_day(a,MFI_list,rsi_list,d_list)
# print("W_moderate"+str(W_moderate))
# agpd = risk_assessment.income(a)
# risk_assessment.close(a)

# a=using_risk_assessment()
# using_risk_assessment.checking_everything_at_night_for_agpd(a)

# ## real-time montiroing

# a= risk_assessment("002323","SZ")
# a= risk_assessment("600600","SS")
# risk_assessment.split_string(a)
# # risk_assessment.check_if_update(a)
# # # risk_assessment.removing_million_and_thousands(a)
# risk_assessment.floating_list_of_volume_of_exchange_hand(a)
# # # risk_assessment.reverse(a)
# risk_assessment.get_date(a)
# # # risk_assessment.rate_of_range(a)
# rsv_list = risk_assessment.RSV(a)
# # # print(rsv_list[-1])
# risk_assessment.ema(a)
# risk_assessment.K(a)
# risk_assessment.D(a)
# risk_assessment.MFI_list1(a)
# # risk_assessment.W_moderate(a)
# # agpd = risk_assessment.income(a)
# # risk_assessment.monitoring_website(a)
# volume=risk_assessment.predictiing_volume_of_exchange_using_ema(a)

# for i in range(660):
#     risk_assessment.getting_current_price(a)
#     # print(volume)
#     rsv_list = risk_assessment.prediciting_RSV(a)
#     # print("rsv" +str(rsv_list))
#     k_value=risk_assessment.prediciting_k(a,rsv_list)
#     # print("k" +str(k_value))
#     d_list = risk_assessment.predicitng_d(a,rsv_list,k_value)
#     # print("d"+str(d_list))
#     mfi_list=risk_assessment.predicting_MFI_list1(a,volume)
#     # print("mfi_list" +str(mfi_list[-1]))
#     rsi_list=risk_assessment.prediciting_ema(a)
#     # print("rsi_list"+str(rsi_list[-1]))
#     risk_assessment.prediciting_W_moderate(a,mfi_list,rsi_list,d_list)
    
#     # risk_assessment.close(a)
#     # risk_assessment.close(a)
#     time.sleep(30)

#### feedback loop for when W-moderate is fallen to 20

# a= risk_assessment("002323","SZ")
# # # a= risk_assessment("300002","SZ")
# risk_assessment.split_string(a)
# # risk_assessment.check_if_update(a)
# # # risk_assessment.removing_million_and_thousands(a)
# risk_assessment.floating_list_of_volume_of_exchange_hand(a)
# # # risk_assessment.reverse(a)
# risk_assessment.get_date(a)
# # # risk_assessment.rate_of_range(a)
# rsv_list = risk_assessment.RSV(a)
# # # print(rsv_list[-1])
# risk_assessment.ema(a)
# risk_assessment.K(a)
# risk_assessment.D(a)
# risk_assessment.MFI_list1(a)
# # risk_assessment.W_moderate(a)
# # agpd = risk_assessment.income(a)
# # risk_assessment.monitoring_website(a)
# volume=risk_assessment.predictiing_volume_of_exchange_using_ema(a)
# W_moderate_trying =0

# for i in range(1):
#     risk_assessment.getting_current_price(a)
#         # print(volume)
#     rsv_list = risk_assessment.prediciting_RSV(a)
#     # print("rsv" +str(rsv_list))
#     k_value=risk_assessment.prediciting_k(a,rsv_list)
#     # print("k" +str(k_value))
#     d_list = risk_assessment.predicitng_d(a,rsv_list,k_value)
#     # print("d"+str(d_list))
#     mfi_list=risk_assessment.predicting_MFI_list1(a,volume)
#     # print("mfi_list" +str(mfi_list[-1]))
#     rsi_list=risk_assessment.prediciting_ema(a)
#     # print("rsi_list"+str(rsi_list[-1]))
#     W_moderate = risk_assessment.prediciting_W_moderate(a,mfi_list,rsi_list,d_list)
#     W_moderate_trying= W_moderate

# percentage = 1

# while (W_moderate_trying >20) :

#     risk_assessment.getting_predictive_price(a,percentage)
#     # print(volume)
#     rsv_list = risk_assessment.prediciting_RSV(a)
#     # print("rsv" +str(rsv_list))
#     k_value=risk_assessment.prediciting_k(a,rsv_list)
#     # print("k" +str(k_value))
#     d_list = risk_assessment.predicitng_d(a,rsv_list,k_value)
#     # print("d"+str(d_list))
#     mfi_list=risk_assessment.predicting_MFI_list1(a,volume)
#     # print("mfi_list" +str(mfi_list[-1]))
#     rsi_list=risk_assessment.prediciting_ema(a)
#     # print("rsi_list"+str(rsi_list[-1]))
#     W_moderate_trying  = risk_assessment.prediciting_W_moderate(a,mfi_list,rsi_list,d_list)
#     percentage-=0.01
# else:
#     print(W_moderate_trying)
    
    # risk_assessment.close(a)
    # risk_assessment.close(a)



##checking agpd at the end of day 

# stock_price_shenzhen = r"C:\Users\yiuki\Stockid_data\list_of_shenzhen.txt"
# stock_price_shanghai = r"C:\Users\yiuki\Stockid_data\list_of_shanghai.txt"
# list_for_shanghai =[]
# list_for_shenzhen =[]
# f=open(stock_price_shanghai,'r',encoding="utf8")
# strings = f.read().split("\n")
# strings=strings[1:-1]
# for string in strings:
#     # print(string[:6])
#     list_for_shanghai.append(int(string[:6]))
#     # print(int(string[:6]))

# s=open(stock_price_shenzhen,'r',encoding="utf8")
# strings123 = s.read().split("\n")
# strings123=strings123[1:-2]
# # print(strings123)
# for string in strings123:
#     # print(string[:6])
#     if (string[:6] == "301408"):
#         # print("Je")
#         break 
    
#     print(string[:6])
#     list_for_shenzhen.append(int(string[:6]))


# list1 = ['SZ']
# agpd_list = []
# # date = "2019-01-21"
# agpd_1  = 0
# stock_id_list = []
# number_of_trade_list = []
# W_moderate_list=[]

# for list in list1:
#     for i in list_for_shenzhen:
#         try:
            
#             i = str(i).zfill(6)
#             # i =str(i)
#             print(i)
#             # print(list)
#             # instance = risk_assessment()
#             # instance.close()
#             # a=a+str(i)
#             a= risk_assessment(i,list)

#         except IndexError: 
#             print("Index Error")
#             pass
#         except FileNotFoundError:
#             print("File Not found error")
#             pass

#         except ZeroDivisionError:
#             print("Zero ")

#         else:
#             # print("Hello world")
#             digit = risk_assessment.split_string(a)
#             # risk_assessment.removing_million_and_thousands(a)
#             # print(list_of_ending_price)
#             if digit ==10:
#                 agpd_1 =-100
#                 print(agpd_1)
#                 agpd_list.append(agpd_1)
#             else:
#                 risk_assessment.floating_list_of_volume_of_exchange_hand(a)
#                 # risk_assessment.reverse(a)
#                 risk_assessment.get_date(a)
#                 # risk_assessment.rate_of_range(a)
#                 risk_assessment.RSV(a)
#                 rsi_list =risk_assessment.ema(a)
#                 risk_assessment.K(a)
#                 d_list=risk_assessment.D(a)
#                 MFI_list=risk_assessment.MFI_list1(a)
#                 risk_assessment.W_moderate(a)
#                 W_moderate= risk_assessment.W_moderate_at_last_day(a,MFI_list,rsi_list,d_list)
#                 W_moderate_list.append(W_moderate)
#                 agpd_1,day = risk_assessment.income(a)
#                 number_of_trade_list.append(day)
#                 # print(agpd_1)
#                 agpd_list.append(agpd_1)
#                 stock_id_list.append(i)
#                 risk_assessment.close(a)

#         # except:
#         #     print("pass")

# # print(agpd_list)
# for i in range(len(agpd_list)-1):
#     if (agpd_list[i] > 0.004 ):
#         # index = agpd_list.index(i)
#         with open(filename,'a+') as f:
#             f.write(str(stock_id_list[i]) + " " + str(agpd_list[i]) + " "+ str(number_of_trade_list[i])+ " "+str(W_moderate_list[i]) +"\n") 
#         print("Stock id: " + str(stock_id_list[i]))
#         print("agpd: " +str(agpd_list[i]))
 


