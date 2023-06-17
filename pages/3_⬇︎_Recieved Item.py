import pandas as pd
import streamlit as st
import datetime
from deta import Deta

st.set_page_config(page_title="Received Items", page_icon="👑")

deta = Deta(st.secrets["key_number"])
db = deta.Base("Receieve")
db1 = deta.Base("Stone")
all_items = db.fetch().items
n1 = db1.fetch().items

jn = st.number_input('Enter job number', value=1, step=1)
genre = st.radio("What kind of Receieve",('Partial', 'Full'))

today = datetime.date.today()
day=int(today.strftime("%d"))
m=int(today.strftime("%m"))
y=int(today.strftime("%Y"))

df = pd.DataFrame(n1)
stones = df['Stone name'].values.tolist()

if genre == 'Full':      
      flag = 0
      for j in all_items:
            if j['Job No'] == jn:
                flag = 1
                if str(j['Status']) == 'P':
                      st.write('')  
                      st.header('Details')
                      st.write('')
                      st.write('Recieved Status : Partially Recieved')
                      st.write('Recieved On  : ',str(j['Receieve Date']))
                      st.write('')
                      st.header('Update details')
                      st.write('')

                      with st.form("Full1"):  
                            d1 = st.date_input('Receive Date', datetime.date(y, m, day))
                            cmts1 = st.text_input('Comments', '')
                            d11 = d1.strftime("%m/%d/%Y")
                            submit_button = st.form_submit_button(label='Submit')

                      if submit_button:
                            keydata = str(j['key'])
                            db.update({"Receieve Date": d11, "Comments_Full" : cmts1, "Status":'F'},keydata,)
                            st.write("Data updated !")


                elif str(j['Status']) == 'F':
                      st.write('Item was already confirmed to be received, veiw full details on homepage')

                elif str(j['Status']) == 'N':
                      st.write('') 
                      st.header('Enter details')
                      st.write('')
                      with st.form("Full2"):               
                            d1 = st.date_input('Receieve Date', datetime.date(y, m, day))
                            cmts1 = st.text_input('Comments', '')
                            d11 = d1.strftime("%m/%d/%Y")
                            submit_button = st.form_submit_button(label='Submit')
                      if submit_button:         
                            keydata = str(j['key'])
                            db.update({"Receieve Date": d11, "Comments_Full" : cmts1, "Status":'F'},keydata,)
                            st.write("Data submitted !")

      if flag == 0 :
            st.write('Data not found !')
                        
if genre == 'Partial' :
      flag = 0
      for j in all_items:
            if j['Job No'] == jn:
                flag = 1                                       
                if str(j['Status']) == 'N':  
                      num_rows = st.slider('Number of different stones', min_value=0,max_value=10,value=1) 
                      with st.form("Part1"):
                            c1, c2 = st.columns(2)
                            with c1:
                                  d1 = st.date_input('Receive Date', datetime.date(y, m, day))                            
                            with c2:
                                  amt1 = st.number_input('Amount', value=0, step=1)                         
                            stone = [None] * num_rows
                            pc = [None] * num_rows

                            def add_row(row):
                                  with c1:
                                      stone[row] = st.selectbox('Stones', stones, key=f'stone{row}')
                                  with c2:
                                      pc[row] = st.number_input('PCs', step=1, key=f'pcs{row}')

                            for r in range(num_rows):
                                  add_row(r)
                            cmts1 = st.text_input('Comments', '')
                            submit_button = st.form_submit_button(label='Submit')
                                     
                      if submit_button: 
                             d11 = d1.strftime("%m/%d/%Y")
                             keydata = str(j['key'])
                             db.update({"Status":'P',"Receieve Date": d11, "Comments" : cmts1, "Receieve Amount" : amt1, "Stones": stone, "PCs":pc},keydata,)
                             st.write("Data submitted !")
               
                if str(j['Status']) == 'F':
                        st.write("This items is already fully receieved !")
                        
                if str(j['Status']) == 'P':
                        st.write("This items is already partially receieved !")
                        
      if flag == 0 :
            st.write('Data not found !')
