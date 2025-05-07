import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="COVID-19 Dashboard", layout="wide")
st.title("🦠 COVID-19 Data Dashboard")

# Sidebar for country selection
st.sidebar.title("🌍 Country Selector")
country = st.sidebar.selectbox("Choose a country", ["USA", "Philippines", "India", "Brazil", "Germany"])

# Fetch historical data
url = f"https://disease.sh/v3/covid-19/historical/{country}?lastdays=30"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    if "timeline" in data:
        timeline = data["timeline"]
        df = pd.DataFrame({
            "Date": pd.to_datetime(list(timeline["cases"].keys())),
            "Cases": list(timeline["cases"].values()),
            "Deaths": list(timeline["deaths"].values()),
            "Recovered": list(timeline["recovered"].values()),
        })

        # Compute daily differences
        df["New Cases"] = df["Cases"].diff().fillna(0)
        df["New Deaths"] = df["Deaths"].diff().fillna(0)
        df["New Recovered"] = df["Recovered"].diff().fillna(0)

        # Header for the daily statistics
        st.subheader(f"📊 Daily Statistics for {country}")

        col1, col2, col3 = st.columns(3)
        col1.metric("New Cases (Latest)", int(df['New Cases'].iloc[-1]))
        col2.metric("New Deaths (Latest)", int(df['New Deaths'].iloc[-1]))
        col3.metric("New Recovered (Latest)", int(df['New Recovered'].iloc[-1]))

        # Line chart for new cases, deaths, and recoveries
        st.subheader("📈 Daily Trends")
        st.line_chart(df.set_index("Date")[["New Cases", "New Deaths", "New Recovered"]])

        # Proportion of total cases, deaths, and recoveries
        st.subheader("📌 Proportion of Total")
        totals = {
            "Cases": df["Cases"].iloc[-1],
            "Deaths": df["Deaths"].iloc[-1],
            "Recovered": df["Recovered"].iloc[-1],
        }
        fig1, ax1 = plt.subplots()
        ax1.pie(totals.values(), labels=totals.keys(), autopct="%1.1f%%", startangle=90)
        ax1.axis("equal")
        st.pyplot(fig1)

        # New Cases, Deaths, and Recovered bar chart
        st.subheader("📊 New Cases, Deaths, and Recovered (Last 30 Days)")
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ax2.bar(df['Date'], df['New Cases'], label="New Cases", alpha=0.7, color='blue')
        ax2.bar(df['Date'], df['New Deaths'], label="New Deaths", alpha=0.7, color='red')
        ax2.bar(df['Date'], df['New Recovered'], label="New Recovered", alpha=0.7, color='green')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Count')
        ax2.set_title('New Cases, Deaths, and Recovered')
        ax2.legend()
        st.pyplot(fig2)

        # Moving Average chart for smooth trends
        st.subheader("📉 Moving Averages (7-Day)")
        df['7-Day Moving Avg Cases'] = df['New Cases'].rolling(window=7).mean()
        df['7-Day Moving Avg Deaths'] = df['New Deaths'].rolling(window=7).mean()
        df['7-Day Moving Avg Recovered'] = df['New Recovered'].rolling(window=7).mean()

        fig3, ax3 = plt.subplots(figsize=(10, 6))
        ax3.plot(df['Date'], df['7-Day Moving Avg Cases'], label="7-Day Moving Avg Cases", color='blue')
        ax3.plot(df['Date'], df['7-Day Moving Avg Deaths'], label="7-Day Moving Avg Deaths", color='red')
        ax3.plot(df['Date'], df['7-Day Moving Avg Recovered'], label="7-Day Moving Avg Recovered", color='green')
        ax3.set_xlabel('Date')
        ax3.set_ylabel('Count')
        ax3.set_title('7-Day Moving Average of New Cases, Deaths, and Recovered')
        ax3.legend()
        st.pyplot(fig3)

        # Cumulative chart for cases, deaths, and recoveries
        st.subheader("📊 Cumulative Total (Cases, Deaths, Recovered)")
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        ax4.plot(df['Date'], df['Cases'], label="Cumulative Cases", color='blue', linewidth=2)
        ax4.plot(df['Date'], df['Deaths'], label="Cumulative Deaths", color='red', linewidth=2)
        ax4.plot(df['Date'], df['Recovered'], label="Cumulative Recovered", color='green', linewidth=2)
        ax4.set_xlabel('Date')
        ax4.set_ylabel('Cumulative Count')
        ax4.set_title('Cumulative Cases, Deaths, and Recovered')
        ax4.legend()
        st.pyplot(fig4)

        # Toggle for raw data
        if st.sidebar.checkbox("Show Raw Data"):
            st.subheader("🗃 Raw Data Table")
            st.dataframe(df)
    else:
        st.error("⚠️ Timeline data not found for this country.")
else:
    st.error(f"❌ API error: {response.status_code}")
