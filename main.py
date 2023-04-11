import operator

import numpy as np
import pandas as pd

import streamlit as st
import os
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt

clean_ = []
footpath_ = []
road_ = []
water_ = []
cl_benchmark = 0
fp_benchmark = 0
rd_benchmark = 0
wt_benchmark = 0
dict_cl = {}
dict_fp = {}
dict_rd = {}
dict_wt = {}
menu = ["Singular", "Comparision_top3", "Comparision_All_Cleanliness","Comparision_All_Footpath","Comparision_All_Road","Comparision_All_Water"]
choice = st.sidebar.selectbox("Select an option", menu)

# load the dataset into a pandas dataframe
df = pd.read_csv("bmc.csv")
wards = ["KarveNagar", "Ghole Road", "Kasaba", "Wanowrie Ramtekdi", "Dhankawadi", "Sinhgad Road",
         "Hadapsar", "Bhavani Peth", "Kondhwa", "Yerawada"]

for i in wards:
    location = i
    level = 'negative'
    df_particular = df.loc[df['location'] == i]
    # print(df_particular)
    # print(df_particular.head())
    negative = 0
    total = 0

    parameters_df = pd.DataFrame(columns=['cleanliness', 'footpath', 'water', 'road'])

    Cleanliness = "cleanliness"
    parameters_df['cleanliness'] = (df_particular['complaint'] == Cleanliness)
    count1 = (df_particular[df_particular['complaint'] == Cleanliness]['level'] == 'negative').sum()

    footpath = "footpath"
    parameters_df['footpath'] = (df_particular['complaint'] == footpath)
    count2 = (df_particular[df_particular['complaint'] == footpath]['level'] == 'negative').sum()

    water = "water"
    parameters_df['water'] = (df_particular['complaint'] == water)
    count3 = (df_particular[df_particular['complaint'] == water]['level'] == 'negative').sum()

    road = "road"
    parameters_df['road'] = (df_particular['complaint'] == road)
    count4 = (df_particular[df_particular['complaint'] == road]['level'] == 'negative').sum()

    total = len(df_particular['complaint'])
    # print("Total number of complaints for ward", i, ":", total)
    prob_neg_clean = count1 / total
    prob_neg_foot = count2 / total
    prob_neg_water = count3 / total
    prob_neg_road = count4 / total

    clean_.append(prob_neg_clean)
    footpath_.append(prob_neg_foot)
    water_.append(prob_neg_water)
    road_.append(prob_neg_road)

    dict_cl[i] = prob_neg_clean

    dict_fp[i] = prob_neg_foot

    dict_rd[i] = prob_neg_road

    dict_wt[i] = prob_neg_water

cl_benchmark = np.mean(clean_)
fp_benchmark = np.mean(footpath_)
rd_benchmark = np.mean(road_)
wt_benchmark = np.mean(water_)
sorted_dicdata = sorted(dict_cl.items(), key=operator.itemgetter(1), reverse=False)
sorted_dicdata2 = sorted(dict_fp.items(), key=operator.itemgetter(1), reverse=False)
sorted_dicdata3 = sorted(dict_rd.items(), key=operator.itemgetter(1), reverse=False)
sorted_dicdata4 = sorted(dict_wt.items(), key=operator.itemgetter(1), reverse=False)

if choice == "Singular":
    # load the dataset into a pandas dataframe
    df = pd.read_csv("bmc.csv")

    # Get the unique values in the 'location' column as a NumPy array
    unique_locations = np.unique(df['location'])

    st.title('Wards')
    prod_selected = st.selectbox("Select product", options=unique_locations)

    location = prod_selected
    df.head()
    df_particular = df.loc[df['location'] == location]
    negative = 0
    total = 0
    Cleanliness = "cleanliness"
    parameters_df['cleanliness'] = (df_particular['complaint'] == Cleanliness)
    count1 = (df_particular[df_particular['complaint'] == Cleanliness]['level'] == 'negative').sum()
    count_1 = (df_particular[df_particular['complaint'] == Cleanliness]['level'] == 'positive').sum()

    footpath = "footpath"
    parameters_df['footpath'] = (df_particular['complaint'] == footpath)
    count2 = (df_particular[df_particular['complaint'] == footpath]['level'] == 'negative').sum()
    count_2 = (df_particular[df_particular['complaint'] == Cleanliness]['level'] == 'positive').sum()

    water = "water"
    parameters_df['water'] = (df_particular['complaint'] == water)
    count3 = (df_particular[df_particular['complaint'] == water]['level'] == 'negative').sum()
    count_3 = (df_particular[df_particular['complaint'] == water]['level'] == 'negative').sum()

    road = "road"
    parameters_df['road'] = (df_particular['complaint'] == road)
    count4 = (df_particular[df_particular['complaint'] == road]['level'] == 'negative').sum()
    count_4 = (df_particular[df_particular['complaint'] == road]['level'] == 'negative').sum()
    total = len(df_particular['complaint'])
    prob_neg_clean = count1 / total
    prob_neg_foot = count2 / total
    prob_neg_water = count3 / total
    prob_neg_road = count4 / total

    # creating the dataset
    data = {'Cleanliness': prob_neg_clean, 'Footpath': prob_neg_foot, 'Water': prob_neg_water,
            'Road': prob_neg_road}

    courses = list(data.keys())
    values = list(data.values())

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(courses, values, width=0.4)

    # Add a horizontal line at the benchmark value
    ax.axhline(cl_benchmark, color='red', linestyle=':', label='clean', xmin=0, xmax=1)
    plt.legend(loc='best')
    ax.axhline(fp_benchmark, color='orange', linestyle='--', label='footpath', xmin=0, xmax=2)
    plt.legend(loc='best')
    ax.axhline(rd_benchmark, color='green', linestyle='dashed', label='road', xmin=0, xmax=3)
    plt.legend(loc='best')
    ax.axhline(wt_benchmark, color='black', linestyle='dashdot', label='water', xmin=0, xmax=4)
    plt.legend(loc='best')

    # Add axis labels and title
    ax.set_xlabel('Complaints')
    ax.set_ylabel('Mean')
    st.pyplot(fig)

    labels = ['clean-', 'clean+', 'footpath-', 'footpath+', 'water-', 'water+', 'road-', 'road+']
    values = [count1, count_1, count2, count_2, count3, count_3, count4, count_4]
    colors = ['tab:blue', 'orange', 'green', 'red', 'purple', 'black', 'pink', 'gray']
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors)
    # Create a pie chart
    fig1, ax1 = plt.subplots()
    ax1.pie(values, labels=labels, radius=2, autopct='%1.1f%%', startangle=60)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Display the pie chart
    st.pyplot(fig1)
if choice == "Comparision_top3":
    data2 = {sorted_dicdata[0][0]: dict_cl.get(sorted_dicdata[0][0]),
             sorted_dicdata[1][0]: dict_cl.get(sorted_dicdata[1][0]),
             sorted_dicdata[2][0]: dict_cl.get(sorted_dicdata[2][0])}
    data3 = {sorted_dicdata2[0][0]: dict_fp.get(sorted_dicdata2[0][0]),
             sorted_dicdata2[1][0]: dict_fp.get(sorted_dicdata2[1][0]),
             sorted_dicdata2[2][0]: dict_fp.get(sorted_dicdata2[2][0])}
    data4 = {sorted_dicdata3[0][0]: dict_rd.get(sorted_dicdata3[0][0]),
             sorted_dicdata3[1][0]: dict_rd.get(sorted_dicdata3[1][0]),
             sorted_dicdata3[2][0]: dict_rd.get(sorted_dicdata3[2][0])}
    data5 = {sorted_dicdata4[0][0]: dict_wt.get(sorted_dicdata4[0][0]),
             sorted_dicdata4[1][0]: dict_wt.get(sorted_dicdata4[1][0]),
             sorted_dicdata4[2][0]: dict_wt.get(sorted_dicdata4[2][0])}

    courses2 = list(data2.keys())
    values2 = list(data2.values())

    courses3 = list(data3.keys())
    values3 = list(data3.values())

    courses4 = list(data4.keys())
    values4 = list(data4.values())

    courses5 = list(data5.keys())
    values5 = list(data5.values())



    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(courses3, values3, width=0.4)
    plt.title('Footpath', fontweight='bold', fontsize=20)
    ax.axhline(fp_benchmark, color='orange', linestyle='--', label='footpath_benchmark', xmin=0, xmax=2)
    plt.legend(loc='best')
    ax.set_xlabel('Complaints')
    ax.set_ylabel('Mean')
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(courses4, values4, width=0.4)
    plt.title('Road', fontweight='bold', fontsize=20)
    ax.axhline(rd_benchmark, color='green', linestyle='dashed', label='road_benchmark', xmin=0, xmax=3)
    plt.legend(loc='best')
    ax.set_xlabel('Complaints')
    ax.set_ylabel('Mean')
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(courses5, values5, width=0.4)
    plt.title('Water', fontweight='bold', fontsize=20)
    ax.axhline(wt_benchmark, color='black', linestyle='dashdot', label='water_benchmark', xmin=0, xmax=4)
    plt.legend(loc='best')
    # Add axis labels and title
    ax.set_xlabel('Complaints')
    ax.set_ylabel('Mean')
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(courses2, values2, width=0.4)
    plt.title('Cleanliness', fontweight='bold', fontsize=20)
    ax.axhline(cl_benchmark, color='red', linestyle=':', label='clean_benchmark', xmin=0, xmax=1)
    plt.legend(loc='best')
    ax.set_xlabel('Complaints')
    ax.set_ylabel('Mean')
    st.pyplot(fig)

    #
    # x = np.random.rand(50)
    # y = np.random.rand(50)
    # z = np.random.rand(50) * 100
    #
    # # Create a scatter plot with marker size corresponding to the third variable
    # fig, ax = plt.subplots()
    # ax.scatter(x, y, s=z)
    #
    # # Set axis labels and title
    # ax.set_xlabel('X')
    # ax.set_ylabel('Y')
    # ax.set_title('Bubble Chart')
    #
    # # Display the plot in the Streamlit app
    # st.pyplot(fig)

if choice == "Comparision_All_Cleanliness":

    labels = ["KarveNagar", "Ghole Road", "Kasaba", "Wanowrie Ramtekdi", "Dhankawadi", "Sinhgad Road", "Hadapsar",
              "Bhavani Peth", "Kondhwa", "Yerawada"]
    # values = [count1, count_1, count2, count_2, count3, count_3, count4, count_4]
    cl = [dict_cl['KarveNagar'], dict_cl['Ghole Road'], dict_cl['Kasaba'], dict_cl['Wanowrie Ramtekdi'],
          dict_cl['Dhankawadi'], dict_cl['Sinhgad Road'], dict_cl['Hadapsar'], dict_cl['Bhavani Peth'],
          dict_cl['Kondhwa'], dict_cl['Yerawada']]
    colors2 = ['tab:blue', 'orange', 'green', 'red', 'purple', 'black', 'pink', 'gray', 'yellow', 'violet']
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors2)
    # plt.title('Cleanliness', fontweight='bold', fontsize=20)
    # Create a pie chart
    fig3, ax3 = plt.subplots()
    ax3.pie(cl, labels=labels, radius=2, autopct='%1.1f%%', startangle=60)
    ax3.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Display the pie chart
    st.pyplot(fig3)

if choice == "Comparision_All_Footpath":
    labels = ["KarveNagar", "Ghole Road", "Kasaba", "Wanowrie Ramtekdi", "Dhankawadi", "Sinhgad Road",
                      "Hadapsar",
                      "Bhavani Peth", "Kondhwa", "Yerawada"]
    fp = [dict_fp['KarveNagar'], dict_fp['Ghole Road'], dict_fp['Kasaba'], dict_fp['Wanowrie Ramtekdi'],
          dict_fp['Dhankawadi'], dict_fp['Sinhgad Road'], dict_fp['Hadapsar'], dict_fp['Bhavani Peth'],
          dict_fp['Kondhwa'], dict_fp['Yerawada']]
    colors2 = ['tab:blue', 'orange', 'green', 'red', 'purple', 'black', 'pink', 'gray', 'yellow', 'violet']
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors2)
    # plt.title('Cleanliness')
    # Create a pie chart
    fig3, ax3 = plt.subplots()
    ax3.pie(fp, labels=labels, radius=2, autopct='%1.1f%%', startangle=60)
    ax3.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Display the pie chart
    st.pyplot(fig3)
if choice == "Comparision_All_Water":
    labels = ["KarveNagar", "Ghole Road", "Kasaba", "Wanowrie Ramtekdi", "Dhankawadi", "Sinhgad Road",
                      "Hadapsar",
                      "Bhavani Peth", "Kondhwa", "Yerawada"]
    fp = [dict_wt['KarveNagar'], dict_wt['Ghole Road'], dict_wt['Kasaba'], dict_wt['Wanowrie Ramtekdi'],
          dict_wt['Dhankawadi'], dict_wt['Sinhgad Road'], dict_wt['Hadapsar'], dict_wt['Bhavani Peth'],
          dict_wt['Kondhwa'], dict_wt['Yerawada']]
    colors2 = ['tab:blue', 'orange', 'green', 'red', 'purple', 'black', 'pink', 'gray', 'yellow', 'violet']
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors2)
   # Create a pie chart
    fig3, ax3 = plt.subplots()
    ax3.pie(fp, labels=labels, radius=2, autopct='%1.1f%%', startangle=60)
    ax3.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Display the pie chart
    st.pyplot(fig3)

if choice == "Comparision_All_Road":
    labels = ["KarveNagar", "Ghole Road", "Kasaba", "Wanowrie Ramtekdi", "Dhankawadi", "Sinhgad Road","Hadapsar","Bhavani Peth", "Kondhwa", "Yerawada"]
    fp = [dict_rd['KarveNagar'], dict_rd['Ghole Road'], dict_rd['Kasaba'], dict_rd['Wanowrie Ramtekdi'],
          dict_rd['Dhankawadi'], dict_rd['Sinhgad Road'], dict_rd['Hadapsar'], dict_rd['Bhavani Peth'],
          dict_rd['Kondhwa'], dict_rd['Yerawada']]
    colors2 = ['tab:blue', 'orange', 'green', 'red', 'purple', 'black', 'pink', 'gray', 'yellow', 'violet']
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors2)
    # plt.title('Cleanliness')
    # Create a pie chart
    fig4, ax4 = plt.subplots()
    ax4.pie(fp, labels=labels, radius=2, autopct='%1.1f%%', startangle=60)
    ax4.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Display the pie chart
    st.pyplot(fig4)
