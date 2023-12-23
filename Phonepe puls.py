#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import pandas as pd
import os
import pymysql
from sqlalchemy import create_engine 
from tabulate import tabulate
import streamlit as st
from PIL import Image
import plotly.express as px
from git.repo.base import Repo
import mysql.connector


# In[2]:


# agg transaction
path1 = "C:/phonepe/pulse/data/aggregated/transaction/country/india/state/"
agg_tran_list = os.listdir(path1)

columns1 ={"States":[], "Years":[], "Quarter":[], "Transaction_type":[], "Transaction_count":[],"Transaction_amount":[] }

for state in agg_tran_list:
    cur_states =path1+state+"/"
    agg_year_list = os.listdir(cur_states)
    
    for year in agg_year_list:
        cur_years = cur_states+year+"/"
        agg_file_list = os.listdir(cur_years)

        for file in agg_file_list:
            cur_files = cur_years+file
            data = open(cur_files,"r")
            A = json.load(data)

            for i in A["data"]["transactionData"]:
                name = i["name"]
                count = i["paymentInstruments"][0]["count"]
                amount = i["paymentInstruments"][0]["amount"]
                columns1["Transaction_type"].append(name)
                columns1["Transaction_count"].append(count)
                columns1["Transaction_amount"].append(amount)
                columns1["States"].append(state)
                columns1["Years"].append(year)
                columns1["Quarter"].append(int(file.strip(".json")))

aggre_transaction = pd.DataFrame(columns1)

aggre_transaction["States"] = aggre_transaction["States"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
aggre_transaction["States"] = aggre_transaction["States"].str.replace("-"," ")
aggre_transaction["States"] = aggre_transaction["States"].str.title()
aggre_transaction['States'] = aggre_transaction['States'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")


# In[3]:


#agg_user
path2 ="C:/phonepe/pulse/data/aggregated/user/country/india/state/"
agg_user_list = os.listdir(path2)

columns2 = {"States":[], "Years":[], "Quarter":[], "Brands":[],"Transaction_count":[], "Percentage":[]}

for state in agg_user_list:
    cur_states = path2+state+"/"
    agg_year_list = os.listdir(cur_states)
    
    for year in agg_year_list:
        cur_years = cur_states+year+"/"
        agg_file_list = os.listdir(cur_years)
        
        for file in agg_file_list:
            cur_files = cur_years+file
            data = open(cur_files,"r")
            B = json.load(data)

            try:

                for i in B["data"]["usersByDevice"]:
                    brand = i["brand"]
                    count = i["count"]
                    percentage = i["percentage"]
                    columns2["Brands"].append(brand)
                    columns2["Transaction_count"].append(count)
                    columns2["Percentage"].append(percentage)
                    columns2["States"].append(state)
                    columns2["Years"].append(year)
                    columns2["Quarter"].append(int(file.strip(".json")))
            
            except:
                pass

aggre_user = pd.DataFrame(columns2)

aggre_user["States"] = aggre_user["States"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
aggre_user["States"] = aggre_user["States"].str.replace("-"," ")
aggre_user["States"] = aggre_user["States"].str.title()
aggre_user['States'] = aggre_user['States'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")



# In[4]:


#map transactin
path3= "C:/phonepe/pulse/data/map/transaction/hover/country/india/state/"
map_tran_list = os.listdir(path3)

columns3 = {"States":[], "Years":[], "Quarter":[],"District":[], "Transaction_count":[],"Transaction_amount":[]}

for state in map_tran_list:
    cur_states = path3+state+"/"
    map_year_list = os.listdir(cur_states)
    
    for year in map_year_list:
        cur_years = cur_states+year+"/"
        map_file_list = os.listdir(cur_years)
        
        for file in map_file_list:
            cur_files = cur_years+file
            data = open(cur_files,"r")
            C = json.load(data)

            for i in C['data']["hoverDataList"]:
                name = i["name"]
                count = i["metric"][0]["count"]
                amount = i["metric"][0]["amount"]
                columns3["District"].append(name)
                columns3["Transaction_count"].append(count)
                columns3["Transaction_amount"].append(amount)
                columns3["States"].append(state)
                columns3["Years"].append(year)
                columns3["Quarter"].append(int(file.strip(".json")))

map_transaction = pd.DataFrame(columns3)

map_transaction["States"] = map_transaction["States"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
map_transaction["States"] = map_transaction["States"].str.replace("-"," ")
map_transaction["States"] = map_transaction["States"].str.title()
map_transaction['States'] = map_transaction['States'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")


# In[5]:


#map user
path4 = "C:/phonepe/pulse/data/map/user/hover/country/india/state/"
map_user_list = os.listdir(path4)

columns4 = {"States":[], "Years":[], "Quarter":[], "Districts":[], "RegisteredUser":[], "AppOpens":[]}

for state in map_user_list:
    cur_states = path4+state+"/"
    map_year_list = os.listdir(cur_states)
    
    for year in map_year_list:
        cur_years = cur_states+year+"/"
        map_file_list = os.listdir(cur_years)
        
        for file in map_file_list:
            cur_files = cur_years+file
            data = open(cur_files,"r")
            D = json.load(data)

            for i in D["data"]["hoverData"].items():
                district = i[0]
                registereduser = i[1]["registeredUsers"]
                appopens = i[1]["appOpens"]
                columns4["Districts"].append(district)
                columns4["RegisteredUser"].append(registereduser)
                columns4["AppOpens"].append(appopens)
                columns4["States"].append(state)
                columns4["Years"].append(year)
                columns4["Quarter"].append(int(file.strip(".json")))

map_user = pd.DataFrame(columns4)

map_user["States"] = map_user["States"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
map_user["States"] = map_user["States"].str.replace("-"," ")
map_user["States"] = map_user["States"].str.title()
map_user['States'] = map_user['States'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")


# In[6]:


#top transaction
path5 = "C:/phonepe/pulse/data/top/transaction/country/india/state/"
top_tran_list = os.listdir(path5)

columns5 = {"States":[], "Years":[], "Quarter":[], "Pincodes":[], "Transaction_count":[], "Transaction_amount":[]}

for state in top_tran_list:
    cur_states = path5+state+"/"
    top_year_list = os.listdir(cur_states)
    
    for year in top_year_list:
        cur_years = cur_states+year+"/"
        top_file_list = os.listdir(cur_years)
        
        for file in top_file_list:
            cur_files = cur_years+file
            data = open(cur_files,"r")
            E = json.load(data)

            for i in E["data"]["pincodes"]:
                entityName = i["entityName"]
                count = i["metric"]["count"]
                amount = i["metric"]["amount"]
                columns5["Pincodes"].append(entityName)
                columns5["Transaction_count"].append(count)
                columns5["Transaction_amount"].append(amount)
                columns5["States"].append(state)
                columns5["Years"].append(year)
                columns5["Quarter"].append(int(file.strip(".json")))

top_transaction = pd.DataFrame(columns5)

top_transaction["States"] = top_transaction["States"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
top_transaction["States"] = top_transaction["States"].str.replace("-"," ")
top_transaction["States"] = top_transaction["States"].str.title()
top_transaction['States'] = top_transaction['States'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")



# In[7]:


# top user
path6 = "C:/phonepe/pulse/data/top/user/country/india/state/"
top_user_list = os.listdir(path6)

columns6 = {"States":[], "Years":[], "Quarter":[], "Pincodes":[], "RegisteredUser":[]}

for state in top_user_list:
    cur_states = path6+state+"/"
    top_year_list = os.listdir(cur_states)

    for year in top_year_list:
        cur_years = cur_states+year+"/"
        top_file_list = os.listdir(cur_years)

        for file in top_file_list:
            cur_files = cur_years+file
            data = open(cur_files,"r")
            F = json.load(data)

            for i in F["data"]["pincodes"]:
                name = i["name"]
                registeredusers = i["registeredUsers"]
                columns6["Pincodes"].append(name)
                columns6["RegisteredUser"].append(registereduser)
                columns6["States"].append(state)
                columns6["Years"].append(year)
                columns6["Quarter"].append(int(file.strip(".json")))

top_user = pd.DataFrame(columns6)

top_user["States"] = top_user["States"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
top_user["States"] = top_user["States"].str.replace("-"," ")
top_user["States"] = top_user["States"].str.title()
top_user['States'] = top_user['States'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")



# In[8]:


#ntable creation
# mysql connection

import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Malar", 
)
mycursor = mydb.cursor(buffered=True)


# In[9]:


Engine=create_engine("mysql+pymysql://root:Malar@localhost/phonepe")


# In[10]:


create_query1 = '''CREATE TABLE if not exists aggregated_transaction (States varchar(50),
                                                                      Years int,
                                                                      Quarter int,
                                                                      Transaction_type varchar(50),
                                                                      Transaction_count bigint,
                                                                      Transaction_amount bigint
                                                                     )'''
mycursor.execute('use phonepe') 
mycursor.execute(create_query1)
mydb.commit()

for index,row in aggre_transaction.iterrows():
    insert_query1 = '''INSERT INTO aggregated_transaction (States, Years, Quarter, Transaction_type, Transaction_count, Transaction_amount)
                                                        values(%s,%s,%s,%s,%s,%s)'''
    values = (row["States"],
              row["Years"],
              row["Quarter"],
              row["Transaction_type"],
              row["Transaction_count"],
              row["Transaction_amount"]
              )
    mycursor.execute(insert_query1,values)
    mydb.commit()
  


# In[11]:


create_query2 = '''CREATE TABLE if not exists aggregated_user (States varchar(50),
                                                                Years int,
                                                                Quarter int,
                                                                Brands varchar(50),
                                                                Transaction_count bigint,
                                                                Percentage float)'''
mycursor.execute('use phonepe')
mycursor.execute(create_query2)
mydb.commit()

for index,row in aggre_user.iterrows():
    insert_query2 = '''INSERT INTO aggregated_user (States, Years, Quarter, Brands, Transaction_count, Percentage)
                                                    values(%s,%s,%s,%s,%s,%s)'''
    values = (row["States"],
              row["Years"],
              row["Quarter"],
              row["Brands"],
              row["Transaction_count"],
              row["Percentage"])
    mycursor.execute(insert_query2,values)
    mydb.commit()


# In[12]:


create_query3 = '''CREATE TABLE if not exists map_transaction (States varchar(50),
                                                                Years int,
                                                                Quarter int,
                                                                District varchar(50),
                                                                Transaction_count bigint,
                                                                Transaction_amount float)'''
mycursor.execute('use phonepe')
mycursor.execute(create_query3)
mydb.commit()

for index,row in map_transaction.iterrows():
            insert_query3 = '''
                INSERT INTO map_Transaction (States, Years, Quarter, District, Transaction_count, Transaction_amount)
                VALUES (%s, %s, %s, %s, %s, %s)

            '''
            values = (
                row['States'],
                row['Years'],
                row['Quarter'],
                row['District'],
                row['Transaction_count'],
                row['Transaction_amount']
            )
            mycursor.execute(insert_query3,values)
            mydb.commit() 


# In[13]:


#map_user_table
create_query4 = '''CREATE TABLE if not exists map_user (States varchar(50),
                                                        Years int,
                                                        Quarter int,
                                                        Districts varchar(50),
                                                        RegisteredUser bigint,
                                                        AppOpens bigint)'''
mycursor.execute('use phonepe')
mycursor.execute(create_query4)
mydb.commit()

for index,row in map_user.iterrows():
    insert_query4 = '''INSERT INTO map_user (States, Years, Quarter, Districts, RegisteredUser, AppOpens)
                        values(%s,%s,%s,%s,%s,%s)'''
    values = (row["States"],
              row["Years"],
              row["Quarter"],
              row["Districts"],
              row["RegisteredUser"],
              row["AppOpens"])
    mycursor.execute(insert_query4,values)
    mydb.commit()


# In[14]:


#top_transaction_table
create_query5 = '''CREATE TABLE if not exists top_transaction (States varchar(50),
                                                                Years int,
                                                                Quarter int,
                                                                pincodes int,
                                                                Transaction_count bigint,
                                                                Transaction_amount bigint)'''
mycursor.execute('use phonepe')
mycursor.execute(create_query5)
mydb.commit()

for index,row in top_transaction.iterrows():
    insert_query5 = '''INSERT INTO top_transaction (States, Years, Quarter, Pincodes, Transaction_count, Transaction_amount)
                                                    values(%s,%s,%s,%s,%s,%s)'''
    values = (row["States"],
              row["Years"],
              row["Quarter"],
              row["Pincodes"],
              row["Transaction_count"],
              row["Transaction_amount"])
    mycursor.execute(insert_query5,values)
    mydb.commit()


# In[15]:


#top_user_table
create_query = '''CREATE TABLE if not exists top_user (States varchar(50),
                                                        Years int,
                                                        Quarter int,
                                                        Pincodes int,
                                                        RegisteredUser bigint
                                                        )'''
mycursor.execute('use phonepe')
mycursor.execute(create_query)
mydb.commit()

for index,row in top_user.iterrows():
    insert_query6 = '''INSERT INTO top_user (States, Years, Quarter, Pincodes, RegisteredUser)
                                            values(%s,%s,%s,%s,%s)'''
    values = (row["States"],
              row["Years"],
              row["Quarter"],
              row["Pincodes"],
              row["RegisteredUser"])
    mycursor.execute(insert_query6,values)
    mydb.commit()


# In[16]:


import json
import streamlit as st
import pandas as pd
import requests
import psycopg2
import plotly.express as px
import plotly.graph_objects as go


# In[17]:


#CREATE DATAFRAMES FROM SQL
#sql connection
import mysql.connector


# In[18]:


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Malar", 
)
mycursor = mydb.cursor(buffered=True)


# In[19]:


#Aggregated_transsaction
mycursor.execute('use phonepe')
mycursor.execute("select * from aggregated_transaction;")
mydb.commit()
table1 = mycursor.fetchall()
aggre_trans = pd.DataFrame(table1,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))


# In[20]:


#Aggregated_transsaction
mycursor.execute('use phonepe')
mycursor.execute("select * from aggregated_transaction;")
mydb.commit()
table1 =mycursor.fetchall()
aggre_trans = pd.DataFrame(table1,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))


# In[21]:


#Map_transaction
mycursor.execute('use phonepe')
mycursor.execute("select * from map_transaction")
mydb.commit()
table3 = mycursor.fetchall()
Map_trans = pd.DataFrame(table3,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"))


# In[22]:


#Map_user
mycursor.execute('use phonepe')
mycursor.execute("select * from map_user")
mydb.commit()
table4 = mycursor.fetchall()
Map_user = pd.DataFrame(table4,columns = ("States", "Years", "Quarter", "Districts", "RegisteredUser", "AppOpens"))


# In[23]:


#Top_transaction
mycursor.execute('use phonepe')
mycursor.execute("select * from top_transaction")
mydb.commit()
table5 = mycursor.fetchall()
Top_trans = pd.DataFrame(table5,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))


# In[24]:


#Top_user
mycursor.execute('use phonepe')
mycursor.execute("select * from top_user")
mydb.commit()
table6 = mycursor.fetchall()
Top_user = pd.DataFrame(table6, columns = ("States", "Years", "Quarter", "Pincodes", "RegisteredUser"))


# In[ ]:




