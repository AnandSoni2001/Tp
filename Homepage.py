import yaml
import streamlit as st
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
import pandas as pd
import datetime
from deta import Deta

st.set_page_config(
    page_title="Jewel",
    page_icon="👋",
)

with open('pass.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'sidebar', key='unique_key')
    st.write(f'Hello *{name}*')
    st.title("Welcome to your website 👋")
    
    deta = Deta(st.secrets["key_number"])
    db = deta.Base("Jewel")
    
    res = db.fetch()
    all_items = res.items
    
    st.write('\n')
    number = st.number_input('Search by Job Number', step=1)
    x = st.button('Search')
    
    if x:
        for i in all_items:
            if i['Job Number'] == number:
                st.write(i)
    
    st.write('\n')
    y = st.button('View all data !')
    if y:
        # fetch until last is 'None'
        while res.last:
          res = db.fetch(last=res.last)
          all_items += res.items

        for x in all_items:
            st.write(x)
            
elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')



