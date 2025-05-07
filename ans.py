import streamlit as st
import re

# App title and header
st.title("📱 Welcome to the Streamlit App")
st.header("🔐 User Information Form")

# Function to validate email format
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

# Function to validate PIN (must be exactly 4 digits)
def is_valid_pin(pin):
    return pin.isdigit() and len(pin) == 4

# Input fields
with st.form("user_form"):
    email = st.text_input("📧 Enter your email address")
    pin = st.text_input("🔢 Enter your 4-digit PIN", type="password")
    submitted = st.form_submit_button("Submit")

# Display results after form submission
if submitted:
    if not is_valid_email(email):
        st.error("❌ Invalid email address. Please enter a valid email.")
    elif not is_valid_pin(pin):
        st.error("❌ Invalid PIN. Please enter a 4-digit PIN.")
    else:
        st.success("✅ Submission received!")
        st.write("You entered:")
        st.write(f"📧 Email: {email}")
        st.write(f"🔒 PIN: {'*' * len(pin)} (hidden for privacy)")
