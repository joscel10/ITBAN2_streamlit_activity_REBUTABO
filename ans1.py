import streamlit as st
import pandas as pd

# Title
st.title("📁 CSV File Uploader & Filter")

# File upload
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Preview of Uploaded Data")
    st.dataframe(df.head())

    # Show raw data toggle
    if st.sidebar.checkbox("Show full raw data"):
        st.write("🔍 Full Raw Data")
        st.dataframe(df)

    # Filter section
    st.sidebar.subheader("🔎 Filter Data")
    column_to_filter = st.sidebar.selectbox("Select a column", df.columns)

    unique_values = df[column_to_filter].dropna().unique()
    selected_values = st.sidebar.multiselect(f"Select value(s) for {column_to_filter}", unique_values)

    if selected_values:
        filtered_df = df[df[column_to_filter].isin(selected_values)]
        st.subheader(f"📂 Filtered Data based on {column_to_filter}")
        st.dataframe(filtered_df)

        # Download filtered data
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered CSV",
            data=csv,
            file_name='filtered_data.csv',
            mime='text/csv',
        )
    else:
        st.info("ℹ️ Please select at least one filter value from the sidebar.")
    
    # Additional Filters (Numeric & Date Filters)
    st.sidebar.subheader("🔧 Additional Filters")
    
    # Numeric filter (if numeric columns are present)
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    if numeric_columns:
        selected_numeric_column = st.sidebar.selectbox("Select numeric column to filter", numeric_columns)
        min_value = st.sidebar.number_input(f"Min value for {selected_numeric_column}", value=float(df[selected_numeric_column].min()))
        max_value = st.sidebar.number_input(f"Max value for {selected_numeric_column}", value=float(df[selected_numeric_column].max()))
        
        filtered_df = filtered_df[filtered_df[selected_numeric_column].between(min_value, max_value)]
        st.write(f"Filtered data for {selected_numeric_column} between {min_value} and {max_value}")
        st.dataframe(filtered_df)
    
    # Summary Statistics (for numeric columns)
    st.subheader("📊 Summary Statistics")
    if numeric_columns:
        st.write("📈 Summary statistics for numeric columns:")
        st.dataframe(df[numeric_columns].describe())

    # Handle missing data option
    st.sidebar.subheader("🧹 Handle Missing Data")
    handle_missing = st.sidebar.radio("How to handle missing data?", ["Do nothing", "Drop missing data", "Fill missing data"])
    if handle_missing == "Drop missing data":
        df = df.dropna()
        st.write("🚮 Dropped rows with missing data.")
    elif handle_missing == "Fill missing data":
        fill_value = st.sidebar.text_input("Enter value to fill missing data", "0")
        df = df.fillna(fill_value)
        st.write(f"✅ Filled missing data with {fill_value}")

else:
    st.warning("⚠️ Please upload a CSV file to begin.")
