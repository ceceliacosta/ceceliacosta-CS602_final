#GPA _ test seems like a good example
#add file name and description at top

import csv
import statistics
import matplotlib.pyplot as plt
import datetime
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import mapbox as mb
from pandas.tests.frame.test_sort_values_level_as_str import ascending
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFilter
from PIL import ImageFont
from mock.mock import inplace
import os 
from os import path 
from bokeh.layouts import column
from _pytest._version import version
import seaborn as sns


#intro to project
def intro():
    img = Image.open("main.jpg")
    st.image(img, width=600)
    st.title("California Fire Incidents")
    st.markdown("Welcome to an overview of some data gathered on California Fire Incidents by county for the years 2013 through 2019.")
    st.header("DISCLAIMER:")
    st.markdown("The following data is from Kaggle and contains various missing values.")
    st.markdown("Charts, graphs, etc are based off of that data and may not be exact due to the missing values")
intro()

#import data and clean
def datafile():
    pd.set_option('display.max_columns', 2000)
    pd.set_option('display.max_rows', 2000)
    pd.set_option('display.width', 2000)
    df_raw = pd.read_csv('California_Fire_Incidents.csv', index_col = 0)
    df_edit = df_raw.drop(columns= ['Active', 'CanonicalUrl', 'ConditionStatement', 'ControlStatement','Featured', 'Final','Public', 'Status','UniqueId', 'Updated'])
    return df_edit


#word cloud over search key words - top 10 most used words
def word_cloud():
    df_edit = datafile()
    df_edit.dropna(subset = ["SearchKeywords"], inplace = True)    
    text = df_edit.SearchKeywords.values
    # fire_mask = np.array(Image.open("fire2.jpg"))
    # print(fire_mask)
    wordcloud = WordCloud(
        max_words= 10,
        width= 500,
        height= 500,
        background_color = 'white',
        colormap = "Reds",
        # mask= fire_mask,
        # contour_width=2, 
        # contour_color='red',
        stopwords = STOPWORDS).generate(str(text))
    fig = plt.figure(figsize = [8, 8])
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.imshow(wordcloud, interpolation = 'bilinear')
    plt.show()
    
    st.header("Word Cloud")
    st.subheader("The data includes a column that identifies the frequently searched words keywords for each fire")
    st.write('Below is a word cloud of the top 10 most frequently searched words')
    st.pyplot(fig)

    return wordcloud

#df manipulated to get a list of each county without duplicates then sorted, dictionary created of total number of fires per county, avg found
def county_info():
    df_edit = datafile()
    counties_all = df_edit['Counties'].drop_duplicates(keep = 'first').sort_values(ascending = True)
    counties_all_list = counties_all.tolist()
    # for item in counties_all_list:
    #     print(item)
    county_data = {}
    for county in df_edit["Counties"]:
        if county not in county_data:
            county_data[county] = df_edit['Counties'].values.tolist().count(county)   
    dictionary_items = county_data.items()
    sorted_items = sorted(dictionary_items)
    sorted_df = pd.DataFrame(sorted_items, columns = ['County', 'Overall Frequency'])
    #county_list = list(county_data.keys())
    #print(county_list)
    # fire_total =  list(county_data.values())
    # fire_avg = [x / 7 for x in fire_total]
    # fire_avg = [round(x,0) for x in fire_avg]
    # print(fire_avg)
    fire_total =  sorted_df['Overall Frequency']
    fire_avg = [x / 7 for x in fire_total]
    fire_avg = [round(x,0) for x in fire_avg]

    return counties_all_list, county_data


#bar chart of number of fires per year
def firefreq_per_year():
    df_edit = datafile()
    counties_all_list, county_data = county_info()
    year_freq = {}
    for year in df_edit["ArchiveYear"]:
        if year not in year_freq:
            year_freq[year] = df_edit['ArchiveYear'].values.tolist().count(year)
 
    years_list = list(year_freq.keys())
    freq =  list(year_freq.values())
    
    years_list = list(year_freq.keys())
    freq =  list(year_freq.values())
    fig = plt.figure(figsize= (10,5))
    plt.bar(range(len(year_freq)), freq, tick_label=years_list)
    plt.show()
    st.header("Number of Fires Each Year")
    st.pyplot(fig)
#selectbox1
    choice = st.selectbox('Please select a year to view the exact amount of fires: ', (years_list))
    st.write("The number of fires for", choice, 'was', year_freq[choice])

#pivot table
    pivottable_df = df_edit[['Counties', 'ArchiveYear']]
    pivottable_df['Fires'] = 1
    pivot_table = pd.pivot_table(pivottable_df, index=["Counties", "ArchiveYear"], aggfunc='count', margins=True, margins_name="Total Fires")
    col1, col2, col3 = st.beta_columns([1, 1, 1])
    st.subheader("Number of Fires Per County Each Year")
    st.write(pivot_table)
    
#selectbox2
    choice2 = st.selectbox('Please select a county to view the total number of fires and the average over seven years: ', (counties_all_list))
    st.write("The total number of fires for", choice2, 'is', county_data[choice2])
    st.write("The average number of fires for", choice2, 'is', (county_data[choice2] / 7))
        
    return year_freq, years_list, freq   
    
    #pie chart
# def pie():
#     year_freq, years_list, freq = firefreq_per_year()
#
#     explode = []
#     for i in range(len(freq)):
#         if freq[i] == max(freq):
#             i = 0.2
#             explode.append(i)
#         else:
#             i = 0
#             explode.append(i)
#
#     plt.pie(freq, explode = explode, labels = years_list, shadow= True, autopct='%.2f%%')
#     plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
#     plt.title("Number of Fires Each Year", loc = "right")
#     plt.show() 
#     return year_freq, years_list, freq

def main():
    wordcloud = word_cloud()
    counties_all_list, county_data = county_info()
    year_freq, years_list, freq = firefreq_per_year()
    

main()