import pandas as pd
import streamlit as st
from deta import Deta

st.set_page_config(page_title="Stone Data 💎", page_icon="")

deta = Deta(st.secrets["key_number"])
db = deta.Base("Stone")
res = db.fetch()
all_items = res.items

with st.form("My"):
  stone = st.text_input('Add new stone', 'Enter name')
  submit_button = st.form_submit_button(label='Submit')
    
if submit_button:
  flag = 0
  
  for i in all_items:
    if upper(i['Stone name']) == upper(stone):
        st.write('Stone already present')
        flag = 1
        break
        
  if flag == 0:
    db.put({"Stone name" : stone})
    st.write('Stone has been added to list') 
  
a = st.button('View Stone')  
if a:
  try:
    for i in all_items:
      df = pd.DataFrame(i, index=[1])
      df_print = df.drop('key', axis=1)
      st.write(df_print)
      
  except:
    st.write('No data to display')
