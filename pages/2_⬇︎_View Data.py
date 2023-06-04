import pandas as pd
import streamlit as st
import datetime
from deta import Deta

deta = Deta(st.secrets["key_number"])
db = deta.Base("Jewel")

st.set_page_config(page_title="See Data", page_icon="4k-Spiderman-Wallpaper.jpg")      
        
y = st.button('Press this button')
if y:
    res = db.fetch()
    all_items = res.items

    # fetch until last is 'None'
    while res.last:
      res = db.fetch(last=res.last)
      all_items += res.items

    for x in all_items:
        st.write(x)
