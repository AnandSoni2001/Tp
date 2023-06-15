import pandas as pd
import streamlit as st
import datetime
from deta import Deta

st.set_page_config(page_title="Enter Data", page_icon="📈")

deta = Deta(st.secrets["key_number"])
db = deta.Base("Jewel")
db1 = deta.Base("Stone")

n = db.fetch().items
n1 = db1.fetch().items

stones = []

for i in n1:
      item = i['Stone name']
      st.write(item)
      stones.append(item)
      
print(stones)
st.write(type(stones))

max = 0
for x in n:
      if x["Job Number"]>max :
            max = x["Job Number"]

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
        stone = st.text_input('Stone', stones)

    with col2:
        d1 = st.date_input("Receive Date", datetime.date(y, m, day))
        jadiyaname = st.text_input('Jadiya Name', '')
        jobn = st.number_input('Job number',value=max+1, step=1)
        gross = st.number_input('Gross Weight')
        chijat = st.number_input('Chijat')
        stonepcs = st.number_input('Stone PCs', value=1, step=1)

    total = kundan+chijat
    date_time = d.strftime("%m/%d/%Y")
    date_time_1 = d1.strftime("%m/%d/%Y")
    submit_button = st.form_submit_button(label='Submit')
    
if submit_button:
    db.put({"Issue Date" : date_time,
                "Receive Date" : date_time_1,
                "Item" : item,
                "Jadiya Name" : jadiyaname,
                "Ghat PCs" : ghatpcs,
                "Job Number" : jobn,
                "Pahad Weight" : pahad,
                "Gross Weight" : gross,
                "Kundan Weight" : kundan,
                "Chijat Weight" : chijat,
                "Total Weight" : total})
    st.write('Data has been submitted') 
    st.metric(label="Total Weight", value=total)
