import pandas as pd
import streamlit as st
import datetime
from deta import Deta

st.set_page_config(page_title="Received Items", page_icon="👑")

deta = Deta(st.secrets["key_number"])
db = deta.Base("Receive")
db1 = deta.Base("Stone")

n = db.fetch().items
n1 = db1.fetch().items

jn = st.number_input('Enter job number')

st.title('Please select one of the box !')
c1, c2 = st.columns(2)

with c1:
      part_butt = st.button('Partially received')

with c2:
      full_butt = st.button('Fully received')
  
today = datetime.date.today()
day=int(today.strftime("%d"))
m=int(today.strftime("%m"))
y=int(today.strftime("%Y"))

res = db.fetch()
all_items = res.items

df = pd.DataFrame(n1)
stones = df['Stone name'].values.tolist()

if full_butt :        
      flag = 0
      for j in all_items:
            if j['Job Number'] == jn:
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
                            base.update({"Receive Date": d11, "Comments" : cmts1},keydata,)
                            st.write("Data updated !")


                elif str(j['Status']) == 'F':
                      st.write('Item was already confirmed to be received, veiw full details on homepage')

                elif str(j['Status']) == 'N':
                      st.write('') 
                      st.header('Enter details')
                      st.write('')
                      with st.form("Full2"):               
                            d1 = st.date_input('Receive Date', datetime.date(y, m, day))
                            cmts1 = st.text_input('Comments', '')
                            submit_button = st.form_submit_button(label='Submit')
                      if submit_button:         
                            db.put({"Receive Date" : d11, "Comments" :cmts1})
                            st.write("Data submitted !")

      if flag == 0 :
            st.write('Data not found !')
                        
if part_butt :
      flag = 0
      for j in all_items:
            if j['Job Number'] == jn:
                flag = 1
                flag1 = 0
                flag2 = 0                     
                num_rows = st.slider('Number of different stones', min_value=1,max_value=10,value=1)                     
                if str(j['Status']) == 'N':
                      col1, col2 = st.columns(2)
                      with col1:
                            if st.session_state.get('button') != True:
                                  st.session_state['button'] = part_butt
                            if st.session_state['button'] == True:
                                  o1 = st.checkbox('Amount')
                      with col2:
                            if st.session_state.get('button') != True:
                                  st.session_state['button'] = part_butt
                            if st.session_state['button'] == True:
                                  o2 = st.checkbox('Stones')
                                     
                      with st.form("Part1"):
                            c1, c2 = st.columns(2)       
                            d1 = st.date_input('Receive Date', datetime.date(y, m, day))
                                     
                            if o1 and st.session_state['button'] == True:
                                  amt1 = st.number_input("Amount")
                                  flag1 = 1   
                            
                            if o2 and st.session_state['button'] == True:
                                  flag2 = 1   
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
                             db.put({"Receive Date" : d11, "Comments" :cmts1, "Receive Amount" : amt1, "Stones": stone, "PCs":pc}) 
                             st.write("Data submitted !")
