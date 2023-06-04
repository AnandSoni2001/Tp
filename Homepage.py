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
    authenticator.logout('Logout', 'main', key='unique_key')
    st.write(f'Welcome *{name}*')
    st.title("# Welcome to your website 👋")
elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')


deta = Deta(st.secrets["key_number"])
db = deta.Base("Jewel")

st.set_page_config(page_title="See Data", page_icon="⬇︎")      
        
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
