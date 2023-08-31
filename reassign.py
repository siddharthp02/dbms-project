import pandas as pd 
import streamlit as st
from database import view_all_data, get_customer,view_only_customer_names, delete_data,view_only_orders,view_customer_orders,reassign_driver,sum_drivers
import plotly.express as px
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
  'longitude'],
  'reassigned_order': ['order_id', 'cluster_no', 'driver_id']}


def reassign_order():
    result = view_all_data("customer")
    df = pd.DataFrame(result, columns=attributes["customer"])
    with st.expander("Current customers"):
        st.dataframe(df)
    
    result = view_all_data("orders")
    df = pd.DataFrame(result, columns=attributes["orders"])
    with st.expander("Order per driver"):
        task_df = df['driver_id'].value_counts().to_frame()
        task_df = task_df.reset_index()
        st.dataframe(task_df)
        p1 = px.pie(task_df, names='index', values='driver_id')
        st.plotly_chart(p1)
    # with st.expander("Amount per driver"):
    #     task_df = df['driver_'].value_counts().to_frame()
    #     task_df = task_df.reset_index()
    #     st.dataframe(task_df)
    #     p1 = px.pie(task_df, names='index', values='driver_id')
    #     st.plotly_chart(p1)
    
    result = sum_drivers()
    # st.write(result)
    df = pd.DataFrame(result, columns=["driver_id","driver_sum"]) 
    with st.expander(f"Sum chart"):
        st.dataframe(df)
        # data_canada = px.df.gapminder()
        fig = px.bar(df, x='driver_sum', y='driver_id')
        st.plotly_chart(fig)

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
        selected_order = st.selectbox("Order to reassign", list_of_orders) 
        if st.button("Reassign driver"):
            reassign_driver(selected_order)
            st.success("Driver has been reassigned..")  
        new_result = view_customer_orders(customer_id)
        df3 = pd.DataFrame(new_result, columns=attributes["orders"]) 
        with st.expander("Updated data"):
            st.dataframe(df3)

        
