import streamlit as st


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

    input7=col.text_input("Email", placeholder='someone@gmail.com')

    input7=col.text_input("Enter Mobile Number",placeholder="+91XXXXXXXXXX")

    a,b,c,= st.columns([6,3,6])

    submitclick=b.button("Submit")

    if submitclick:
        st.balloons()



  

            