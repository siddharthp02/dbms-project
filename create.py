import streamlit as st
import pandas as pd
from database import add_data,view_all_data,view_only_customer_names,get_customer,get_pincodes
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

def create_order():
    result = view_all_data("customer")
    df = pd.DataFrame(result, columns=attributes["customer"])
    with st.expander("Current customers"):
        st.dataframe(df)
    list_of_customers = [i[0] for i in view_only_customer_names()]
    selected_customer = st.selectbox("Customer to Edit", list_of_customers)
    selected_result = get_customer(selected_customer)
    if selected_result:
        customer_id = selected_result[0][0]
        customer_name = selected_result[0][1]  
        col1,col2 = st.columns(2)
        with col1:
            order_id = st.text_input("Order id:")
            driver_id = 0
        with col2:
            track_id = st.text_input("Track id:")
            order_amount = st.text_input("Order amount:")
          
        if st.button("Add order"):
            add_data("orders",[order_id,track_id,customer_id,order_amount,driver_id])
            st.success(f"Successfully added order {order_id} to customer {customer_name}")

def create_customer():
    col1, col2 = st.columns(2)
    with col1:
        customer_id = st.text_input("customer id:")
        customer_name = st.text_input("Name:")
        email = st.text_input("Email:")
        phone_no = st.text_input("Phone No.:")
    with col2:
        house_no = st.text_input("House No.:")
        community = st.text_input("Community:")
        locality = st.text_input("Locality:")
        list_of_pincodes = [i[0] for i in get_pincodes()]
        pincode = st.selectbox("Pincode", list_of_pincodes)
        latitude = st.text_input("Latitude:")
        longitude = st.text_input("Longitude:")
    if st.button("Add customer"):
        add_data("customer",[customer_id,
        customer_name,
        email,
        phone_no,
        house_no,
        community,
        locality,
        pincode,
        latitude,
        longitude])
        st.success("Successfully added customer: {}".format(customer_name))