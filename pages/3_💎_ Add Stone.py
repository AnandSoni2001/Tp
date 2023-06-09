import pandas as pd
import streamlit as st
from deta import Deta

st.set_page_config(page_title="Stone Data 💎", page_icon="")

deta = Deta(st.secrets["key_number"])
db = deta.Base("Stone")
res = db.fetch()
all_items = res.items

with st.form("New"):
  stone = st.text_input('Add new stone', '')
  submit_button = st.form_submit_button(label='Submit')
    
if submit_button:
  flag = 0  
  for i in all_items:
    if i['Stone name'].upper() == stone.upper():
        st.write('Stone already present')
        flag = 1        
  if flag == 0:
    db.put({"Stone name" : stone})
    st.write('Stone has been added to list') 
  
a = st.button('View Stone')  
if a:
  df = pd.DataFrame(all_items)
  df_print = df.drop('key', axis=1)
  st.write(df_print)
