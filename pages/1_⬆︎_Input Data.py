import pandas as pd
import streamlit as st
import datetime
from deta import Deta

deta = Deta(st.secrets["key_number"])
db = deta.Base("Jewel")
db1 = deta.Base("Counter")

st.write(db1.fetch().items)
n=1
st.set_page_config(page_title="Enter Data", page_icon="📈")

today = datetime.date.today()
day=int(today.strftime("%d"))
m=int(today.strftime("%m"))
y=int(today.strftime("%Y"))
      
with st.form("My"):
    col1, col2 = st.columns(2)
    with col1:
        d = st.date_input("Issue Date", datetime.date(y, m, day))
        item = st.text_input('Item', '')
        ghatpcs = st.number_input('Ghat PCs', step=1)
        pahad = st.number_input('Pahad Weight')
        kundan = st.number_input('Kundan Weight')

    with col2:
        d1 = st.date_input("Receive Date", datetime.date(y, m, day))
        jadiyaname = st.text_input('Jadiya Name', '')
        jobn = st.number_input('Job number',value=n, step=1)
        gross = st.number_input('Gross Weight')
        chijat = st.number_input('Chijat')

    total = kundan+chijat
    date_time = d.strftime("%m/%d/%Y, %H:%M:%S")
    date_time_1 = d1.strftime("%m/%d/%Y, %H:%M:%S")
    submit_button = st.form_submit_button(label='Submit')
    
if submit_button:
    st.metric(label="Total", value=(kundan+chijat))
    db.put({"Issue Date" : date_time,
                "Receive Date" : date_time_1,
                "Item" : item,
                "Jadiya Name" : jadiyaname,
                "Ghat PCs" : ghatpcs,
                "Job Number" : jobn,
                "Pahad Weight" : pahad,
                "Gross Weight" : gross,
                "Kundan Weight" : kundan,
                "Chijat Weight" : chijat})
    st.write('Data has been submitted') 
