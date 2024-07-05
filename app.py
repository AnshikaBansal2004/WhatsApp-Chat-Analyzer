import streamlit as st
import preprocessor,helper,sentiment
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import requests
import time

st.set_page_config(layout='wide',page_title='Whatsapp Chat Analyzer')
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
    
    #st.dataframe(df)
    #fetch unique users:-
    user_list=df['Contact'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user=st.sidebar.selectbox("Analysis With Respect to",user_list)
    

    #Analysis of every kind:-
    
    if st.sidebar.button("Show Analysis"):
        num_messages,num_words,num_media,num_urls=helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1, col2, col3, col4= st.columns(4)
        
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(num_words)
        with col3:
            st.header("Media Shared")
            st.title(num_media)
        with col4:
            st.header("Links Shared")
            st.title(num_urls)
        

        #timeline

        st.title("Monthly TimeLine")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['Message'],color='red')
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        st.title("Daily TimeLine")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['Message'], color='#795548')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        st.title("Activity Map")
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            custom_colors = ['#F2C53D', '#6BBE45', '#2AABE2', '#F95D6A', '#A64AC9','#E57373','#47D1B5']
            ax.bar(busy_day.index,busy_day.values,color=custom_colors)
            plt.xticks(rotation=45)
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color=['#F2C53D', '#6BBE45', '#2AABE2', '#F95D6A', 
                                                              '#A64AC9', '#E57373', '#42A5F5', '#FF9800', 
                                                              '#4CAF50', '#FF5722', '#9C27B0', '#795548'])
            plt.xticks(rotation=45)
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap,cmap='viridis')
        st.pyplot(fig)


        #Group-level Analysis(Most Busy Users):-

        if selected_user=="Overall":

            st.title('Most Busy Users 🗽')
            x,df_most_busy=helper.fetch_most_busy_users(df)
            fig, ax= plt.subplots()
            col1,col2=st.columns(2)
            with col1:
                custom_colors = ['#F2C53D', '#6BBE45', '#2AABE2', '#F95D6A', '#A64AC9']
                ax.bar(x.index,x.values,color=custom_colors)
                plt.xticks(rotation=45)
                st.pyplot(fig)

                
            with col2:
                st.dataframe(df_most_busy)
        
        #WordCloud:-
        st.title("Word Cloud ☁")
        Word_Cloud=helper.create_word_cloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(Word_Cloud)
        st.pyplot(fig)

        #Most_Common_Words:-
        st.title("Most Common Words")
        most_common_df=helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        custom_colors = ['#F2C53D', '#6BBE45', '#2AABE2', '#F95D6A', '#A64AC9']
        ax.barh(most_common_df[0],most_common_df[1],color=custom_colors)
        plt.xticks(rotation=45)
        st.pyplot(fig)


        # Sentiment Analysis Results
        df_sentiment = sentiment.analyze_sentiment(df)
        st.title("Sentiment Analysis")
        sentiment_counts = df_sentiment['Sentiment_Class'].value_counts()
        fig, ax = plt.subplots()
        ax.bar(sentiment_counts.index, sentiment_counts.values, color=['#4CAF50', '#FF5722', '#2196F3'])
        plt.xticks(rotation=0)
        st.pyplot(fig)

#about me section
if st.sidebar.button("About Me"):
          st.title('Creator: Anshika Bansal')
          st.markdown('<p style="font-family: Roboto; color: #ca124d; font-size: 40px; font-weight: bold"><p> I am a final-year Computer Science graduate at Vellore Institute of Technology, passionate about leveraging technology to solve real-world problems. My academic journey has been fueled by a strong enthusiasm for problem-solving, and an avid interest in the transformative power of Machine Learning. <br> I hope you find my project insightful!</p>', unsafe_allow_html=True)
        #   st.markdown('<p style="font-family: Roboto; color: black; font-size: 25px; font-weight: bold">From: Vellore Institute of Technology</p>', unsafe_allow_html=True)
          st.markdown('<p style="font-family: Roboto; color: #0077b5; font-size: 20px;"><a href="https://github.com/AnshikaBansal2004">GitHub</a></p>', unsafe_allow_html=True)
          st.markdown('<p style="font-family: Roboto; color: #0077b5; font-size: 20px;"><a href="https://www.linkedin.com/in/anshika-bansal-95b32021b/">LinkedIn</a></p>', unsafe_allow_html=True)
          
    


        
        
