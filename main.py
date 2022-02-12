# streamlit_app.py

import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
#@st.cache(ttl=600)

def run_query(query):
    rows = conn.execute(query, headers=1)
    return rows

sheet_url = st.secrets["private_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}" LIMIT 1')


tickers = run_query(f'SELECT * FROM "{sheet_url}"')

st.title("Your Investment Portfolio")

st.header('Your Investment Overview')
# Print results.
for row in rows:
    initial_investment = "$"+str(round(row.Total_Invested,2))
    current_investment_worth = "$"+str(round(row.Current_Value,2))
    investment_growth = "$"+str(round((row.Current_Value)-(row.Total_Invested),2))

    investment_growth_perc = str(round(row.total_return_perc,2))+"%"

    st.metric(label="You invested", value=initial_investment)
    st.metric(label="You investment is currently worth", value=current_investment_worth, delta=investment_growth_perc)

    #st.write("You invested: $",float(f"{row.Total_Invested}"))
    #st.write("You investment is currently worth: $",round(row.Current_Value,2), "(",round(row.total_return_perc,2),"%)")
   # st.write(f"{row.name} has a :{row.pet}:")

st.header("Your Portfolio Breakdown")
for ticker in tickers:
    st.write("You invested $", round(ticker.Total_Spent,2), "in ",f"{ticker.Stock_Name}", " and it is currently worth $", round(ticker.Current_Net_Worth,2))

