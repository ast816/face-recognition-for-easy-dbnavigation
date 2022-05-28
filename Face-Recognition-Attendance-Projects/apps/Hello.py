import streamlit as st
import pyodbc


server = 'asthasql.database.windows.net'
database = 'sql_facerecog'
username = 'azureadmin'
password = 'asthaface10_'   
driver= '{ODBC Driver 17 for SQL Server}'

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

def add_data(input1,input2,input3,input4,input5,input6,input7,input8,input9,input10):
    cursor.execute('INSERT INTO DETAILS VALUES(?,?,?,?,?,?,?,?,?,?)',(input1,input2,input3,input4,input5,input6,input7,input8,input9,input10))
    cnxn.commit()

def app():
    st.title('Hello New User')
    st.header('Add your Details')
    
    
   
    buff, col,= st.columns([6,6])

    input1=buff.text_input('Enter your name',placeholder='Name goes here')

    input2=buff.text_input('Enter Adhaar Card Number',placeholder='XXXX XXXX XXXX XXXX')

    input3=buff.text_input('Enter Driving License Number','')

    input4=buff.date_input("Enter DOB")

    input5=buff.text_input('Enter PAN',placeholder='XXXXXXXXXX')

    input6=col.date_input("Last Covid Test Date")

    input7=col.selectbox("Test Result",('Positive','Negative'),)

    input8=col.selectbox("Gender",('Male','Female','Other'),)

    input9=col.text_input("Email", placeholder='someone@gmail.com')

    input10=col.text_input("Enter Mobile Number",placeholder="+91XXXXXXXXXX")

    a,b,c,= st.columns([6,3,6])

    submitclick=b.button("Submit")

    if submitclick:
        add_data(input1,input2,input3,input4,input5,input6,input7,input8,input10,input9)
        st.balloons()



  

            