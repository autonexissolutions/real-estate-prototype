import streamlit as st
import pandas as pd
import openai
import os

# Load property listings
df = pd.read_csv("properties.csv")

# OpenAI key from Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🏡 Real Estate Assistant")

user_query = st.text_input("What kind of property are you looking for?")

if user_query:
    # Format listings
    listings = "\n".join(
        f"{row['Name']} - {row['Area']} - ₹{row['Price']} - {row['BHK']} BHK - {row['Description']}"
        for _, row in df.iterrows()
    )

    prompt = f"""
A customer is looking for a property: {user_query}.
Here are the available listings:
{listings}

Pick 2 matching listings, show them briefly, and ask for name and phone to proceed.
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )

    reply = response['choices'][0]['message']['content']
    st.markdown("### 🤖 Assistant")
    st.write(reply)

    st.markdown("### 📇 Interested? Leave your contact info:")

    with st.form("lead_form"):
        name = st.text_input("Your Name")
        phone = st.text_input("Your Phone Number")
        submit = st.form_submit_button("Submit")

        if submit and name and phone:
            with open("leads.csv", "a") as f:
                f.write(f"{name},{phone},{user_query}\n")
            st.success("✅ Thank you! Our agent will contact you soon.")