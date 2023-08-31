import pandas as pd 
import streamlit as st
from database import view_all_data, get_customer,view_only_customer_names, delete_data,view_only_orders,view_customer_orders

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


def delete_orders():

    result = view_all_data("customer")
    df = pd.DataFrame(result, columns=attributes["customer"])
    with st.expander("Current customers"):
        st.dataframe(df)
    list_of_customers = [i[0] for i in view_only_customer_names()]
    selected_customer = st.selectbox("Customer", list_of_customers)
    selected_result = get_customer(selected_customer)
    if selected_result:
        customer_id = selected_result[0][0]
        customer_name = selected_result[0][1]
        result2 = view_customer_orders(customer_id)
        df2 = pd.DataFrame(result2,columns = attributes["orders"]) 
        with st.expander(f"Customer{customer_name} orders:"):
            st.dataframe(df2)
        list_of_orders = [i[0] for i in view_only_orders(customer_id)] 
        selected_order = st.selectbox("Order to Delete", list_of_orders) 
        st.warning("Do you want to delete : {}".format(selected_order)) 
        if st.button("Delete order"):
            delete_data("orders",selected_order)
            st.success("Order has been deleted successfully")
        new_result = view_customer_orders(customer_id)
        df3 = pd.DataFrame(new_result, columns=attributes["orders"]) 
        with st.expander("Updated data"):
            st.dataframe(df3)

        


def delete():
    result = view_all_data()
    df = pd.DataFrame(result, columns=['Train_no','name','Train_type'	,'Source'	,'Destination','Availability']) 
    with st.expander("Current data"):
        st.dataframe(df)
    list_of_trains = [i[0] for i in view_only_names()] 
    selected_train = st.selectbox("Task to Delete", list_of_trains) 
    st.warning("Do you want to delete ::{}".format(selected_train)) 
    if st.button("Delete train"):
        delete_data(selected_train)
        st.success("train has been deleted successfully")
    new_result = view_all_data()
    df2 = pd.DataFrame(new_result, columns=['Train_no','name','Train_type'	,'Source'	,'Destination','Availability']) 
    with st.expander("Updated data"):
        st.dataframe(df2)