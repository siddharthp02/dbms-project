import pandas as pd
import streamlit as st
from database import view_all_data,clustering_total,reset_db

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
 'cluster': ['cluster_no', 'cluster_latitude', 'cluster_longitude'],
 'delivery_partner': ['driver_id', 'driver_name'],
 'driver_log': ['updated_id', 'Olddriver', 'Newdriver'],
 'reassigned_order': ['order_id', 'cluster_no', 'driver_id'],
 'delivery_partner_pincode': ['pincode', 'driver_id'],
 'order_backup':['order_id','track_id','customer_id','order_amount','driver_id']}


def read(tablename):
  result = view_all_data(tablename)
  # st.write(result)
  df = pd.DataFrame(result, columns=attributes[tablename]) 
  with st.expander(f"View all {tablename}"):
    st.dataframe(df)
  # if st.button("Reset db"):
  #   reset_db()S
  #   newresult = view_all_data(tablename)
  #   df3 = pd.DataFrame(newresult, columns=attributes[tablename]) 
  #   with st.expander("Updated data"):
  #       st.dataframe(df3)
  
    

  
  