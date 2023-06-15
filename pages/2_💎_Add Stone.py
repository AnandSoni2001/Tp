import pandas as pd
import streamlit as st
from deta import Deta

st.set_page_config(page_title="Stone Data 💎", page_icon="")

deta = Deta(st.secrets["key_number"])
db = deta.Base("Stone")

with st.form("My"):
  stone = st.text_input('Add new stone', 'Enter name')
  submit_button = st.form_submit_button(label='Submit')
    
if submit_button:
  db.put({"Stone name" : stone})
  st.write('Stone has been added to list') 
  
a = st.button('View Stone')  
if a:
  res = db.fetch()
  all_items = res.items
  try:
      df = pd.DataFrame(all_items)

      df_print = df.drop('key', axis=1)
      st.write(df_print)

      csv = convert_df(df_print)

      st.download_button(
          label="Download all data",
          data=csv,
          file_name='data.csv',
          mime='text/csv',
      )
      
   except:
      st.write('No data to display')
