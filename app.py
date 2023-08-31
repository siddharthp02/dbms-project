import streamlit as st
import pandas as pd
from create import create_order
from create import create_customer
from delete import delete_orders
from read import read
from update import update_customer
from queries import execute
from reassign import reassign_order
from database import reset_db,clustering_total,assign_driver,reassign_driver,view_all_data,view_only_orders

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

attributesfull = {'orders': ['order_id',
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
 'cluster': ['cluster_no', 'cluster_latitude', 'cluster_longitude'],
 'delivery_partner': ['driver_id', 'driver_name'],
 'driver_log': ['updated_id', 'Olddriver', 'Newdriver'],
 'reassigned_order': ['order_id', 'cluster_no', 'driver_id'],
 'delivery_partner_pincode': ['pincode', 'driver_id'],
 'order_backup':['order_id','track_id','customer_id','order_amount','driver_id']}

def main():
    st.title("Order management system")
    menu = ["Add", "View", "Edit", "Remove","Query","Reassign"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Add":
        tablename = st.selectbox("Table", list(attributes.keys()))
        st.subheader(f"Enter {tablename} details :")
        if(tablename == "orders"):
            create_order()
        elif(tablename == "customer"):
            create_customer()
    elif choice == "View":
        tablename = st.selectbox("Table", list(attributesfull.keys()))
        st.subheader(f"View table {tablename}")
        read(tablename)
    elif choice == "Edit":
        st.subheader("Update created tasks")
        tablename = st.selectbox("Table", ['customer'])
        if(tablename == "customer"):
            update_customer()
    elif choice == "Remove":
        tablename = st.selectbox("Table", ['orders'])
        st.subheader("Delete created tasks")
        delete_orders()
    elif choice == "Query":
        execute()
    elif choice == "Reassign":
        reassign_order()
    else:
        st.subheader("About tasks")
    
    if st.sidebar.button("Assign driver"):
        assign_driver()
        st.success("Driver has been assigned.")
    if st.sidebar.button("Perform clustering"):
        clustering_total()
        st.success("Clustering has been performed.")
    # if st.sidebar.button("Reassign driver"):
    #     reassign_driver()
    #     st.success("Driver has been reassigned..")    
    if st.sidebar.button("Reset db"):
        reset_db()
        st.success("SQL connection reset.")
    
if __name__ == '__main__':
    main()