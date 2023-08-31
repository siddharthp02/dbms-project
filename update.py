import pandas as pd
import streamlit as st
from database import get_pincodes,view_all_data, view_only_customer_names, get_customer, edit_data

attributes = {'orders': ['order_id',
  'track_id',
  'customer_id',
  'order_amount',
  'driver_id'],
 'customer': ['customer_id',
  'customer_name',
  'email',
  'phone_no',
  'house_no',
  'community',
  'locality',
  'pincode',
  'latitude',
  'longitude']}

def update_customer():
    tablename = "customer"
    result = view_all_data(tablename)
    df = pd.DataFrame(result, columns=attributes[tablename])
    with st.expander("Current data"):
        st.dataframe(df)
    list_of_customers = [i[0] for i in view_only_customer_names()]
    selected_customer = st.selectbox("Customer to Edit", list_of_customers)
    selected_result = get_customer(selected_customer)
    if selected_result:
        customer_id = selected_result[0][0]
        customer_name = selected_result[0][1]
        email = selected_result[0][2]
        phone_no = selected_result[0][3]
        house_no = selected_result[0][4]
        community= selected_result[0][5] 
        locality= selected_result[0][6]
        pincode= selected_result[0][7]
        latitude= selected_result[0][8]
        longitude= selected_result[0][9]
        col1, col2 = st.columns(2)
        with col1:
            new_customer_id = st.text_input("customer_id:",customer_id)
            new_customer_name = st.text_input("customer_name:",customer_name)
            new_email = st.text_input("email:",email)
            new_phone_no = st.text_input("phone_no:",phone_no)
            
        with col2:
            new_house_no = st.text_input("house_no:",house_no)
            new_community = st.text_input("community:",community)
            new_locality = st.text_input("locality:",locality)
            list_of_pincodes = [i[0] for i in get_pincodes()]
            new_pincode = st.selectbox("Pincode", list_of_pincodes)
            new_latitude = st.text_input("latitude:",latitude)
            new_longitude = st.text_input("longitude:",longitude)
        if st.button("Update customer"):
            edit_data("customer",[new_customer_id,new_customer_name,new_email,new_phone_no,new_house_no,new_community,new_locality,new_pincode,new_latitude,new_longitude],[customer_id,customer_name,email,phone_no,house_no,community,locality,pincode,latitude,longitude])
            st.success("Successfully updated:: {} to ::{}".format(customer_name, new_customer_name))
        result2 = view_all_data("customer")
    df2 = pd.DataFrame(result2, columns=attributes[tablename])
    with st.expander("Updated data"):
        st.dataframe(df2)