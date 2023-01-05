import streamlit as st
import snowflake.connector
import pandas as pd
from snowflake import connector
import snowflake
import numpy as np
from st_aggrid import AgGrid

#streamlit run C:\Users\marseille.ma\Streamlit\streamlit_SF.py

ctx = snowflake.connector.connect(
    user="SVC_SPRING_DATASCIENCE",
    password="silla!_lepidoptera682",
    account="KYA28640",
    warehouse="ANALYSTS_WH",
    database="CD_ANALYTICS_TESTDB",
    schema="ANALYTICSTESTDB_SCHEMA"
)
cur = ctx.cursor()
cur.execute('select OPPID,CDUID,MODEL_PREDICTED_PROBABILITY  from "CD_ANALYTICS_TESTDB"."ANALYTICSTESTDB_SCHEMA"."SPRING_CLTV_PREDICTIONS" limit 1000')
df = cur.fetch_pandas_all()

image=Image.open("C:/Users/marseille.ma/Streamlit/SpringFinancial.jpg")
st.image(image,width=300)


def check_password():
    """Returns `True` if the user had the correct password."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == 'spring':
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    st.header('_CLTV Scores_ :zap:')
    st.caption('Please click the column to filter for the OPPID and CDUID you want!', unsafe_allow_html=False)
    AgGrid(df)
