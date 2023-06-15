import yaml
import streamlit as st
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
import pandas as pd
import datetime
from deta import Deta

st.set_page_config(
    page_title="Kundans Data 💍",
    page_icon="💍",
    initial_sidebar_state="expanded",
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
    number = st.number_input('Enter Job Number', step=1, value=1)
    
    st.write('Enter operation :')
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        x = st.button('Search')
    
    with col2:
        y = st.button('Delete')
        
    with col3:
        z = st.button('Update')
        
    with col4:
        a = st.button('View all data !')
        
    def convert_df(df):
        return df.to_csv().encode('utf-8')
    
    if x:
        flag = 0
        
        c1, c2, c3 = st.columns(3) 
        
        for i in all_items:
            if i['Job Number'] == number:
                flag = 1
                
                with c1:
                    st.write('Job Number : ', str(i['Job Number']))
                    st.write('Issue Date : ', str(i['Issue Date']))
                    st.write('Amount : ', str(i['Amount']))
                    
                
                with c2:
                    st.write('Kundan/Gold : ', str(i['Kundan/Gold']))
                    st.write('Jadiya Name : ', str(i['Jadiya Name']))
                    st.write('Ghat PCs : ', str(i['Ghat PCs']))
                    
                with c3:
                    st.write('Pahad Weight : ', str(i['Pahad Weight']))
                    st.write('Kundan Weight : ', str(i['Kundan Weight']))
                    st.write('Chijat Weight : ', str(i['Chijat Weight']))
                    st.write('Gross Weight : ', str(i['Gross Weight']))
                    
                st.write('Stones : ', str(i['Stones']))
                st.write('PCs : ', str(i['PCs']))
                st.write('Total Weight : ', str(i['Total Weight']))

        if flag == 0:
            st.write('Data not found')

    if y:
        flag = 0   
        for i in all_items:
            if i['Job Number'] == number:
                flag = 1
                keydata = str(i['key'])
                db.delete(keydata)
                st.write('Data deleted')

        if flag == 0:
            st.write('Data not found') 
            
    if z:
        st.write('Key under construction!')
    
    if a:
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
            
elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')



