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
    db1 = deta.Base("Receieve")
    
    res = db.fetch()
    all_items = res.items
    
    res1 = db1.fetch()
    all_items1 = res1.items
    
    st.write('\n')
    
    opt = st.radio("Select an operation",('All data','Search', 'Update', 'Delete'), horizontal = True)       
        
    def convert_df(df):
        return df.to_csv().encode('utf-8')
    
    if opt == 'Search':
        number = st.number_input('Enter Job Number', step=1, value=1)
        x = st.button('Submit')
        if x:
            flag = 0
            st.header('Details') 

            for i in all_items:
                if i['Job Number'] == number:
                    flag = 1

                    st.write('Job Number : ', str(i['Job Number']))
                    c1, c2 = st.columns(2)

                    with c1:
                        st.write('Jadiya Name : ', str(i['Jadiya Name']))
                        st.write('Ghat PCs : ', str(i['Ghat PCs']))
                        st.write('Issue Date : ', str(i['Issue Date']))
                        st.write('Amount : ', str(i['Amount']))
                        st.write('Gross Weight : ', str(i['Gross Weight']))


                    with c2:
                        st.write('Kundan/Gold : ', str(i['Kundan/Gold']))
                        st.write('Pahad Weight : ', str(i['Pahad Weight']))
                        st.write('Kundan Weight : ', str(i['Kundan Weight']))
                        st.write('Chijat Weight : ', str(i['Chijat Weight']))
                        st.write('Total Weight : ', str(i['Total Weight']))

                    st.write('Stones : ', str(i['Stones']))
                    st.write('PCs : ', str(i['PCs']))
                    st.write('Comments : ', str(i['Comments']))

                    st.write('')
                    st.header('Receieve Status')
                    st.write('')
                    flag1 = 0

                    c11, c22 = st.columns(2)
                    for j in all_items1 :
                        if j['Job No'] == number:
                            flag1 = 1
                            if str(j['Status']) == 'P':
                                st.write('Recieved Status : Partially Recieved')
                                with c11:
                                    st.write('Recieved On  : ',str(j['Receieve Date']))
                                st.write('Stones : ', str(j['Stones']))
                                st.write('PCs : ', str(j['PCs']))
                                st.write('Comments after partially receieved : ', str(j['Comments']))
                                with c22:
                                    st.write('Amount Recieved : ', str(j['Receieve Amount']))
                            elif str(j['Status']) == 'F':
                                st.write('Recieved Status : Item has been fully recieved !')
                                st.write('Comments after fully receieved : ', str(j['Comments_Full']))
                            elif str(j['Status']) == 'N':
                                st.write('Recieved Status : Item not recieved yet !')
                    if flag1 == 0:
                        st.write('Recieve Status : Item not found')

            if flag == 0:
                st.write('Data not found')

    if opt=='Delete':
        number = st.number_input('Enter Job Number', step=1, value=1)
        agree = st.checkbox('Are you sure, this action cannot be undone ?')
        x = st.button('Delete')
        if x and agree :
            flag = 0   
            for i in all_items:
                if i['Job Number'] == number:
                    flag = 1
                    keydata = str(i['key'])
                    db.delete(keydata)
                    st.write('Data deleted')

                    for j in all_items1:
                        if j['Job No'] == number:
                            keydata1 = str(j['key'])
                            db1.delete(keydata1)

            if flag == 0:
                st.write('Data not found') 
            
    if opt=='Update':
        st.write('Key under construction!')
    
    if opt =='All data':
        a = st.button('View !')
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



