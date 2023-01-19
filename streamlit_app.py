import streamlit as st
import snowflake.connector
import pandas as pd
from snowflake import connector
import snowflake
import numpy as np
from st_aggrid import AgGrid
from collections import namedtuple
import altair as alt
from PIL import Image
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query('select * from "CD_ANALYTICS_TESTDB"."ANALYTICSTESTDB_SCHEMA"."SPRING_CLTV_PREDICTIONS_REPORT"')

df = pd.DataFrame(rows, columns=['OPPID','CDUID','Can_Pay_$160','PREDICTED_PROBABILITY'])


# ctx = snowflake.connector.connect(
#     user="SVC_SPRING_DATASCIENCE",
#     password="silla!_lepidoptera682",
#     account="KYA28640",
#     warehouse="ANALYSTS_WH",
#     database="CD_ANALYTICS_TESTDB",
#     schema="ANALYTICSTESTDB_SCHEMA"
# )
# cur = ctx.cursor()
# cur.execute('select OPPID,CDUID,MODEL_PREDICTED_PROBABILITY  from "CD_ANALYTICS_TESTDB"."ANALYTICSTESTDB_SCHEMA"."SPRING_CLTV_PREDICTIONS" limit 1000')
# df = cur.fetch_pandas_all()

image=Image.open("SpringFinancial.jpg")
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

    
    
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)



def filter_dataframe(df):
    user_text_input = st.text_input(
        f"Please enter CDUID here:",
        )
    if user_text_input:
        df = df[df['CDUID'].astype(str).str.contains(user_text_input)]

    return df    
    
    
    
if check_password():
    st.header('_CLTV Scores_ :zap:')
    st.caption('Please click the checkbox below to filter for the OPPID and CDUID you want!', unsafe_allow_html=False)
    st.dataframe(filter_dataframe(df))
