import pandas as pd
import streamlit as st
from database import execute_query

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
 'delivery_partner_pincode': ['pincode', 'driver_id']}


def execute():
    query = st.text_input("Type query :")
    result = execute_query(query)
    # st.write(result)
    s = query.lower().split()
    
    if(result):
        try:
            if( s[0]== "select" or s[0] == "select*"):
                tablename = s[-1]
                df = pd.DataFrame(result, columns=attributes[tablename]) 
                with st.expander(f"View all {tablename}"):
                    st.dataframe(df) 
            else:
                df = pd.DataFrame(result) 
                with st.expander(f"View all {tablename}"):
                    st.dataframe(df)
        except Exception as e:
            st.error(e)