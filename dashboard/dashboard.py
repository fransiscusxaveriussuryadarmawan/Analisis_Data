import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_summary(df):
    daily_summary = df.groupby('dteday').agg({
        "total_rentals_bikes": "sum",
        "casual": "sum",
        "registered_users": "sum"
    }).reset_index()
    return daily_summary

def plot_season_bar(df):
    urutan_musim = ['Springer', 'Summer', 'Fall', 'Winter']
    df['season'] = pd.Categorical(df['season'], categories=urutan_musim, ordered=True)
    grouped_season = df.groupby('season')['total_rentals_bikes'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x='season', y='total_rentals_bikes', data=grouped_season, ax=ax)
    ax.set_title('Pengaruh musim terhadap penyewaan sepeda')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Average penyewaan sepeda')
    ax.set_xticklabels(['Springer', 'Summer', 'Fall', 'Winter'])
    st.pyplot(fig)

def plot_season_pie(df):
    urutan_musim = ['Springer', 'Summer', 'Fall', 'Winter']
    df['season'] = pd.Categorical(df['season'], categories=urutan_musim, ordered=True)
    grouped_season_pie = df.groupby('season')['total_rentals_bikes'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(grouped_season_pie['total_rentals_bikes'],
           labels=['Springer', 'Summer', 'Fall', 'Winter'],
           autopct='%1.1f%%',
           startangle=90,
           colors=sns.color_palette('Set3'))
    ax.set_title('Pengaruh musim terhadap penyewaan sepeda')
    st.pyplot(fig)

def plot_workingday_bar(df):

    grouped_workingday = df.groupby('workingday')['total_rentals_bikes'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x='workingday', y='total_rentals_bikes', data=grouped_workingday, ax=ax)
    ax.set_title('Perbandingan penyewaan sepeda pada hari kerja vs akhir pekan')
    ax.set_xlabel('0 = Akhir Pekan, 1 = Hari Kerja')
    ax.set_ylabel('Average penyewaan sepeda')
    st.pyplot(fig)

def plot_workingday_pie(df):
    grouped_workingday_pie = df.groupby('workingday')['total_rentals_bikes'].sum()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(grouped_workingday_pie, 
           labels=['Akhir Pekan', 'Hari Kerja'], 
           autopct='%1.1f%%', 
           startangle=90, 
           colors=sns.color_palette('Set3'))
    ax.set_title('Perbandingan penyewaan sepeda pada hari kerja vs akhir pekan')
    st.pyplot(fig)

def plot_year_bar(df):
    grouped_year = df.groupby('year')['total_rentals_bikes'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x='year', y='total_rentals_bikes', data=grouped_year, ax=ax)
    ax.set_title('Perbandingan penyewaan sepeda pada tahun 2011 vs 2012')
    ax.set_xlabel('Tahun')
    ax.set_ylabel('Average penyewaan sepeda')
    st.pyplot(fig)

def plot_month_line(df):
    grouped_month_year = df.groupby(['year', 'month'])['total_rentals_bikes'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.lineplot(x='month', y='total_rentals_bikes', hue='year', data=grouped_month_year, palette='coolwarm', ax=ax)
    ax.set_title('Perbandingan penyewaan sepeda setiap bulan pada 2011 vs 2012')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Avewrage penyewaan sepeda')
    plt.xticks(rotation=45)
    st.pyplot(fig)



day_df = pd.read_csv("dashboard/day_new.csv")
hour_df = pd.read_csv("dashboard/hour_new.csv")

day_df['dteday'] = pd.to_datetime(day_df['dteday'])

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                 (day_df["dteday"] <= str(end_date))]

daily_summary = create_daily_summary(main_df)

st.header('Bike Sharing Dashboard :sparkles:')



col1, col2 = st.columns(2)

with col1:
    total_rentals = daily_summary['total_rentals_bikes'].sum()
    st.metric("Total Rentals", value=total_rentals)
 
with col2:
    total_casual = daily_summary['casual'].sum()
    st.metric("Total Casual Rentals", value=total_casual)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(daily_summary["dteday"], daily_summary["total_rentals_bikes"], marker='o', color="#90CAF9")
ax.set_title("Total Rentals Over Time", fontsize=20)
ax.set_xlabel("Date", fontsize=15)
ax.set_ylabel("Rentals", fontsize=15)
st.pyplot(fig)



st.subheader('Pengaruh musim terhadap penyewaan sepeda (Barplot)')
plot_season_bar(main_df)

st.subheader('Pengaruh musim terhadap penyewaan sepeda (Pie Chart)')
plot_season_pie(main_df)

st.subheader('Perbandingan penyewaan sepeda pada hari kerja vs akhir pekan (Barplot)')
plot_workingday_bar(main_df)

st.subheader('Perbandingan penyewaan sepeda pada hari kerja vs akhir pekan (Pie Chart)')
plot_workingday_pie(main_df)

st.subheader('Perbandingan penyewaan sepeda pada tahun 2011 vs 2012 (Barplot)')
plot_year_bar(main_df)

st.subheader('Perbandingan penyewaan sepeda pada tahun 2011 vs 2012 setiap bulan (Line Chart)')
plot_month_line(main_df)

st.caption('Copyright (c) Dicoding 2024')