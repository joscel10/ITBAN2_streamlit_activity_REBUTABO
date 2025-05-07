import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# --------------------------
# Database Configuration
# --------------------------
DB_USER = 'root'
DB_PASSWORD = None  # or your actual password as a string
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'store'

@st.cache_resource
def get_connection():
    if DB_PASSWORD is None:
        connection_url = f"mysql+pymysql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        connection_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(connection_url)

engine = get_connection()

# --------------------------
# Authentication
# --------------------------
st.sidebar.header("🔐 Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

def authenticate(user, pwd):
    return user == "admin" and pwd == "store123"

if authenticate(username, password):
    st.success(f"Welcome, {username} 👋")
    st.title("🛒 Customer & Product Management Dashboard")

    # --------------------------
    # Table Selector
    # --------------------------
    table = st.selectbox("Select Table", ["customers", "products"])

    # --------------------------
    # Table Viewer with Filter
    # --------------------------
    st.subheader("📄 Table Viewer")
    filter_query = st.text_input("Optional SQL Filter (e.g., city = 'New York')")

    view_query = f"SELECT * FROM {table}"
    if filter_query.strip():
        view_query += f" WHERE {filter_query}"

    with engine.connect() as conn:
        df = pd.read_sql(text(view_query), conn)
    st.dataframe(df)

    # --------------------------
    # Insert New Record
    # --------------------------
    st.subheader(f"➕ Add New Record to `{table}`")
    with st.form(key="insert_form"):
        with engine.connect() as conn:

            if table == "customers":
                full_name = st.text_input("Full Name")
                email = st.text_input("Email")
                phone = st.text_input("Phone")
                city = st.text_input("City")
                submit = st.form_submit_button("Insert Customer")
                if submit:
                    conn.execute(text("""
                        INSERT INTO customers (full_name, email, phone, city)
                        VALUES (:name, :email, :phone, :city)
                    """), {"name": full_name, "email": email, "phone": phone, "city": city})
                    conn.commit()
                    st.success("✅ Customer record inserted!")

            elif table == "products":
                product_name = st.text_input("Product Name")
                price = st.number_input("Price", min_value=0.0, step=0.01)
                stock = st.number_input("Stock Quantity", min_value=0)
                submit = st.form_submit_button("Insert Product")
                if submit:
                    conn.execute(text("""
                        INSERT INTO products (product_name, price, stock_quantity)
                        VALUES (:name, :price, :stock)
                    """), {"name": product_name, "price": price, "stock": stock})
                    conn.commit()
                    st.success("✅ Product added!")

else:
    st.warning("🔐 Please log in with valid credentials.")
