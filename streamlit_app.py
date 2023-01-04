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
cur.execute('select OPPID,CDUID,MODEL_PREDICTED_PROBABILITY  from "CD_ANALYTICS_TESTDB"."ANALYTICSTESTDB_SCHEMA"."SPRING_CLTV_PREDICTIONS" limit 100')
df = cur.fetch_pandas_all()

st.title("Spring Financial CLTV Scores")

AgGrid(df)
