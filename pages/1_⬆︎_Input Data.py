import pandas as pd
import streamlit as st
import datetime
from deta import Deta

st.set_page_config(page_title="Enter Data", page_icon="📈")

deta = Deta(st.secrets["key_number"])
db = deta.Base("Jewel")
db1 = deta.Base("Stone")
db2 = deta.Base("Receieve")

n = db.fetch().items
n1 = db1.fetch().items
n2 = db2.fetch().items

df = pd.DataFrame(n1)
stones = df['Stone name'].values.tolist()

max = 0
for x in n:
      if x["Job Number"]>max :
            max = x["Job Number"]

today = datetime.date.today()
day=int(today.strftime("%d"))
m=int(today.strftime("%m"))
y=int(today.strftime("%Y"))

# a selection for the user to specify the number of rows
      
with st.form("My"):
    col1, col2 = st.columns(2)
    with col1:
        d = st.date_input("Issue Date", datetime.date(y, m, day))
        item = st.text_input('Kundan/Gold', '')
        ghatpcs = st.number_input('Ghat PCs', step=1)
        pahad = st.number_input('Pahad Weight')
        kundan = st.number_input('Kundan Weight')

    with col2:
        amt = st.number_input("Amount")
        jadiyaname = st.text_input('Jadiya Name', '')
        jobn = st.number_input('Job number',value=max+1, step=1)
        gross = st.number_input('Gross Weight')
        chijat = st.number_input('Chijat')
    
    stone = [None] * num_rows
    pc = [None] * num_rows
    
    num_rows = st.slider('Number of different stones', min_value=0,max_value=10,value=1)    

    def add_row(row):
          with col1:
              stone[row] = st.selectbox('Stones', stones, key=f'stone{row}')
          with col2:
              pc[row] = st.number_input('PCs', step=1, key=f'pcs{row}')
            
    for r in range(num_rows):
      add_row(r)
      
    comm = st.text_input('Comments', '')

    total = kundan+chijat
    date_time = d.strftime("%m/%d/%Y")
    submit_button = st.form_submit_button(label='Submit')
    
if submit_button:
    db.put({"Issue Date" : date_time,
                "Amount" : amt,
                "Kundan/Gold" : item,
                "Jadiya Name" : jadiyaname,
                "Ghat PCs" : ghatpcs,
                "Job Number" : jobn,
                "Pahad Weight" : pahad,
                "Gross Weight" : gross,
                "Kundan Weight" : kundan,
                "Chijat Weight" : chijat,
                "Total Weight" : total,
            "Stones": stone, "PCs":pc, "Comments" : comm
           })
      
    db2.put({"Job No" : jobn, "Status" : 'N'})
    st.write('Data has been submitted') 
    st.metric(label="Total Weight", value=total)
