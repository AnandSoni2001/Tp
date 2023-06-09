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
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        x = st.button('Search')
    
    with col2:
        y = st.button('Delete')
        
    with col3:
        z = st.button('Update')
    
    if x:
        flag = 0
        for i in all_items:
            if i['Job Number'] == number:
                flag = 1
                st.write(i)
                
        if flag == 0:
            st.write('Data not found')
    
    if y:
        flag = 0
        #st.write('This button is under work !')        
        conf = st.text_input('Are you sure ? Type "YES" to confirm !')
        
        if conf == 'YES' :
            st.write('Okay great', conf)
            #for i in all_items:
            #    if i['Job Number'] == number:
            #        st.write(i)

            #if flag == 0:
            #    st.write('Data not found')
        
        #db.delete(key)
    
    if z:
        st.write('This button is under work !')
        
    st.write('\n')
    y = st.button('\nView all data !')
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



