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
#import streamlit_wordcloud as wordcloud
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFilter
from PIL import ImageFont
from mock.mock import inplace
import os 
from os import path 

#import nltk 
#nltk.download('stopwords')
#from nltk.corpus import stopwords 

#from set import Set 

#intro to project
def intro():
    st.title("California Fires")
    st.markdown("Welcome to an overview of some data gathered on California fires by county from 2013 to 2019.")
    st.header("DISCLAIMER:")
    st.markdown("The following data is from Kaggle and contains various missing values.")
    st.markdown("Charts, graphs, etc are based off of that data and may not be exact due to the missing values")
intro()
#disclaimer on data
# def disclaimer():
#     st.markdown('DISCLAIMER: _The following data is from Kaggle and contains various missing values. Charts, graphs, etc are based off of that data and may not be exact due to the missing values_')
# disclaimer()


#import data and clean
def datafile():
    df_raw = pd.read_csv('California_Fire_Incidents.csv')
    #print(df_raw)
    #print(list(df_raw.columns))
    df_edit = df_raw.drop(columns= ['Active', 'CanonicalUrl', 'ConditionStatement', 'ControlStatement','Featured', 'Final','Public', 'Status','UniqueId', 'Updated'])
    #print(df_edit)
    #print(list(df_edit.columns))
    st.dataframe(df_edit)
    return df_edit

#list of counties on a map, number of fires, latitude, longitude, print user input- show all counties in ascending order 
def county_info():
    df_edit = datafile()
    counties_all = df_edit['Counties'].drop_duplicates(keep = 'first').sort_values(ascending = True)
    counties_all_list = counties_all.tolist()
    for item in counties_all_list:
        print(item)
    print(counties_all_list)
    
    county_data = {}
    for county in df_edit["Counties"]:
        if county not in county_data:
            county_data[county] = df_edit['Counties'].values.tolist().count(county)
    dictionary_items = county_data.items()
    sorted_items = sorted(dictionary_items)
  #  sorted_items = sorted_items.strip(" ' ")
    print(sorted_items)
    
    sorted_df = pd.DataFrame(sorted_items)
    #print(sorted_df[0][0])
    #sorted_df = sorted_df.reset_index(drop= True)
    print(sorted_df)
    print('County followed by the number of fires from 2013-2019:')
    #print()
    # print(sorted_items[1][1])
    # for i in range(len(counties_all_list)):
    #     if sorted_items[i][0] == counties_all_list[i]:
    #         print(i)
    # for i in range(len(sorted_items[:
    #     print(i)
    #print(counties_all_list)
    # print(county_data)

    
    county_list = list(county_data.keys())
    print(county_list)
    fire_total =  list(county_data.values())
    fire_avg = [f'{(x / 7): .2f}' for x in fire_total]
    print(fire_avg)
    
    # plt.scatter(county_list, fire_avg, label = county_list, color = "green")
    # plt.xlabel("County")
    # plt.xticks(rotation= 45)
    # plt.yticks(rotation= 45)
    # plt.ylabel("Average Number of Fires")
    # plt.title("Average Number of Fires per County from 2013-2019")
    # plt.tight_layout()
    # plt.show()
    
    #st.markdown('Here is a list of all of the counties in California that we will be looking at:', counties_all_list)
    
    
    
    return counties_all



#bar chart of number of fires per year
def firefreq_per_year():
    df_edit = datafile()
    year_freq = {}
    for year in df_edit["ArchiveYear"]:
        if year not in year_freq:
            year_freq[year] = df_edit['ArchiveYear'].values.tolist().count(year)
   # print(year_freq)
    years_list = list(year_freq.keys())
    freq =  list(year_freq.values())
    # print(years_list)
    # print(freq)
    #bar chart
    plt.bar(range(len(year_freq)), freq, tick_label=years_list)
    plt.show()
    #pie chart
    # explode = []
    # for i in range(len(freq)):
    #     if freq[i] == max(freq):
    #         i = 0.2
    #         explode.append(i)
    #     else:
    #         i = 0
    #         explode.append(i)
    #
    # plt.pie(freq, explode = explode, labels = years_list, shadow= True, autopct='%.2f%%')
    # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    # plt.title("Number of Fires Each Year", loc = "right")
    # plt.show() 
    return year_freq, years_list, freq


#word cloud over search key words - top 10 most used words
#add fire mask? words red / orange see colab
def word_cloud():
    df_edit = datafile()
    df_edit.dropna(subset = ["SearchKeywords"], inplace = True)
    
    # fire_mask = np.array(Image.open("fire.jpg"))
    # print(fire_mask)
    
    text = df_edit.SearchKeywords.values
    wordcloud = WordCloud(
        max_words= 10,
        width= 500,
        height= 500,
        background_color = 'black',
        stopwords = STOPWORDS).generate(str(text))
    plt.figure(figsize = [8, 8])

    plt.imshow(wordcloud, interpolation = 'bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()
      
    return wordcloud


def main():
    #df_edit = datafile()
    counties_all = county_info()
    year_freq, years_list, freq = firefreq_per_year()
    wordcloud = word_cloud()
    
#test
    # ax = df_edit.plot.bar(x = 'Counties', y='CrewsInvolved', rot=0)
    # plt.show()

    
    

    
    
main()