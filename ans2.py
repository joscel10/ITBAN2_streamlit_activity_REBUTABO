import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Set page title
st.set_page_config(page_title="Data Warehousing & EDM", layout="wide")

# Sidebar setup
st.sidebar.title("📚 Data Warehousing Topics")
topic = st.sidebar.radio("Choose a topic:", [
    "Overview",
    "ETL Process",
    "Data Integration",
    "Data Governance",
    "Performance Optimization"
])

st.sidebar.markdown("🧠 **Tip:** Explore each section to build a solid understanding of data management in enterprises.")

# Expander for introduction
with st.expander("📖 Introduction: What is Data Warehousing and Enterprise Data Management?"):
    st.write("""
        **Data Warehousing** involves collecting, storing, and managing data from various sources to support business intelligence and decision-making.
        
        **Enterprise Data Management (EDM)** ensures that organizational data is secure, accurate, and available to the right users at the right time.
    """)

# Content rendering based on topic
if topic == "Overview":
    st.header("📦 Overview of Data Warehousing")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("What is a Data Warehouse?")
        st.write(""" A Data Warehouse is a central repository for integrated data from multiple sources, optimized for reporting and analysis. """)
    with col2:
        st.subheader("Key Components")
        st.markdown(""" 
        - 🧩 **Data Sources** – Internal/external systems (e.g., CRM, ERP)  
        - 🔄 **ETL Tools** – Extract, Transform, Load pipelines  
        - 🏪 **Data Marts** – Department-specific subsets  
        """)

    # Adding a visualization for understanding data flow
    st.subheader("📊 Data Flow in Data Warehousing")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_title("ETL Process Flow")
    ax.text(0.2, 0.8, 'Data Sources', horizontalalignment='center', verticalalignment='center', fontsize=12, color='blue')
    ax.text(0.5, 0.8, 'ETL Process', horizontalalignment='center', verticalalignment='center', fontsize=12, color='green')
    ax.text(0.8, 0.8, 'Data Warehouse', horizontalalignment='center', verticalalignment='center', fontsize=12, color='red')
    ax.plot([0.2, 0.5], [0.8, 0.8], color='black', linewidth=2)
    ax.plot([0.5, 0.8], [0.8, 0.8], color='black', linewidth=2)
    ax.axis('off')
    st.pyplot(fig)

elif topic == "ETL Process":
    st.header("🔄 ETL Process")
    st.write("""
        The **ETL Process** (Extract, Transform, Load) is foundational for populating a data warehouse:
        
        - **Extract**: Gather raw data from multiple sources  
        - **Transform**: Clean, normalize, and enrich the data  
        - **Load**: Store the transformed data into the data warehouse  
    """)

    # Show an interactive flowchart for the ETL process
    st.subheader("🔄 ETL Process Flow")
    st.image("https://www.tutorialspoint.com/data_warehousing/images/etl_process.png")

elif topic == "Data Integration":
    st.header("🔗 Data Integration")
    st.write("""
        Integration combines data from different sources into a unified view:
        
        - **Replication**: Copying data regularly  
        - **Federation**: Querying across sources without physical movement  
        - **Virtualization**: Real-time access to distributed systems  
    """)

elif topic == "Data Governance":
    st.header("🛡️ Data Governance")
    st.write("""
        Data Governance ensures responsible management of data:
        
        - **Data Quality**: Accuracy and completeness  
        - **Data Security**: Protecting sensitive info  
        - **Data Compliance**: GDPR, HIPAA, etc.  
    """)

elif topic == "Performance Optimization":
    st.header("⚡ Performance Optimization")
    st.write("""
        Improve warehouse performance using:
        
        - **Indexing**: Faster query access  
        - **Partitioning**: Manage massive tables  
        - **Query Optimization**: Efficient SQL + caching  
    """)

# Tabs for extended content
tab1, tab2, tab3 = st.tabs(["📈 Real-Time Analytics", "☁️ Cloud Warehousing", "🗄️ Data Archiving"])

with tab1:
    st.subheader("Real-Time Analytics")
    st.write("Enable instant insights using tools like Apache Kafka, Spark Streaming, and change data capture (CDC) mechanisms.")
    st.write("""
        Example: 
        - Streaming analytics platforms can allow instant access to real-time data for decision-making.
    """)

with tab2:
    st.subheader("Cloud Data Warehousing")
    st.write("Modern cloud platforms like Snowflake, BigQuery, and Redshift offer scalability, flexibility, and cost-efficiency.")
    st.write("""
        Cloud platforms allow automatic scaling and better management of computational resources.
    """)

with tab3:
    st.subheader("Data Archiving")
    st.write("Archiving strategies include cold storage, lifecycle policies, and compliance-driven retention techniques.")
    st.write("""
        Example: Using Amazon S3 Glacier for cold storage to save on long-term data retention costs.
    """)
