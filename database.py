import mysql.connector 
import pandas as pd
mydb = mysql.connector.connect(
host="localhost", user="root", password="", database="order_management_system_427"
)
c = mydb.cursor()

from sqlalchemy import create_engine
# def create_table(): 
#     c.execute('CREATE TABLE IF NOT EXISTS TRAIN_DUPLICATE_427(Train_no TEXT,name TEXT,Train_type TEXT,Source TEXT,Destination TEXT,Availability TEXT)')

#get attributes
attributes = {"orders":[],"customer":[]}
c.execute('show columns from orders')
for x in c:
    attributes["orders"].append(x[0])
c.execute('show columns from customer')
for x in c:
    attributes["customer"].append(x[0])

def reset_db():
    global mydb
    mydb = mysql.connector.connect(
    host="localhost", user="root", password="", database="order_management_system_427"
    )
    global c

    c = mydb.cursor()
    

def add_data(tablename,values):
    c.execute("SET FOREIGN_KEY_CHECKS=0 ")
    q = f"INSERT INTO {tablename}("
    for item in attributes[tablename][:-1]:
        q+=item+","
    q+=attributes[tablename][-1]+") VALUES ("
    for item in values[:-1]:
        q+="'"+str(item)+"',"
    q+="'"+str(values[-1])+"')"

    c.execute(q) 
    mydb.commit()

def execute_query(q):
    try:
        c.execute(q)
        data = c.fetchall()
        return data
    except Exception as e:
        return e
        

def view_all_data(tablename): 
    c.execute(f'SELECT * FROM {tablename}') 
    data = c.fetchall()
    return data

def view_only_customer_names(): 
    c.execute('SELECT customer_name from customer') 
    data = c.fetchall()
    return data

def view_customer_orders(customerid): 
    c.execute(f'SELECT * from orders WHERE customer_id = {customerid}') 
    data = c.fetchall()
    return data

def view_only_orders(customerid): 
    c.execute(f'SELECT order_id from orders WHERE customer_id = {customerid}') 
    data = c.fetchall()
    return data

def get_customer(name): 
    c.execute('SELECT * FROM customer WHERE customer_name="{}"'.format(name)) 
    data = c.fetchall()
    return data

def get_pincodes():
    c.execute("SELECT pincode from delivery_partner_pincode")
    data = c.fetchall()
    return data
    
def edit_data(tablename,new_values,old_values):
    c.execute("SET FOREIGN_KEY_CHECKS=0 ")

    q = f"UPDATE {tablename} SET "
    for index,item in enumerate(attributes[tablename][:-1]):
        q+=item+"='"+str(new_values[index])+"', "
    q+=attributes[tablename][-1]+"='"+str(new_values[-1]) +"'"
    q+=" WHERE "
    for index,item in enumerate(attributes[tablename][:-1]):
        q+=item+"='"+str(old_values[index])+"' AND "
    q+=attributes[tablename][-1]+"='"+str(old_values[-1])+"'"
    print(q)
    c.execute(q) 
    mydb.commit()
    data = c.fetchall()
    return data
def delete_data(tablename,name): 
    if(tablename == "orders"):
        c.execute(f'DELETE FROM {tablename} WHERE order_id={name}') 
    else:
        c.execute(f'DELETE FROM {tablename} WHERE customer_id={name}') 
    mydb.commit()

def assign_driver():
    c.execute("CALL ASSIGN_DRIVER()")
    mydb.commit()

def reassign_driver(oid):
    c.execute(f"CALL REASSIGN_DRIVER6({oid})")
    mydb.commit()

def sum_drivers():
    c.execute("select driver_id,SUM(order_amount) as driver_sum from orders group by driver_id;")
    data = c.fetchall()
    return data

from os.path import exists
import json
import os
import haversine as hs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import seaborn as sns; sns.set()



def get_pc_per_driver(driverspincodes,drivers):
    pc_per_driver = {}
    for index,rows in driverspincodes.iterrows():
        pc = rows.pincode
        driver = drivers.loc[drivers['driver_id'] == rows.driver_id]["driver_name"].values[0]
        if(driver not in pc_per_driver):
            pc_per_driver[driver] = []
        pc_per_driver[driver].append(pc)
    return pc_per_driver  

def get_active_drivers(pc_per_driver,customers,orders):
    active_drivers = {}
    for index,rows in customers.iterrows():
        if(rows.customer_id == 0):
            continue

        for order in orders.loc[orders['customer_id'] == rows.customer_id].values:
            trackid = order[1]
            locality = rows.locality
            community = rows.community
            houseno = rows.house_no
            pcode = rows.pincode
            lat = rows.latitude
            long = rows.longitude
            phoneno = rows.phone_no
            amount = order[3]
            cname = rows.customer_name
            oid = order[0]
            for key,vals in pc_per_driver.items():
                if pcode in vals:
                    if(key not in active_drivers):
                        active_drivers[key] = []
                    active_drivers[key].append([community,int(pcode),float(lat),float(long),float(amount),cname,int(oid),float(trackid),locality,float(phoneno),houseno])

    for driver in active_drivers:
        active_drivers[driver].sort(key = lambda x:x[4])
   
    return active_drivers

def driversum(driver):
    dsum = 0
    for order in driver:
        dsum += order[4]
    return dsum

def driver_name(active_drivers,dnum):
    return list(active_drivers.keys())[dnum]

def sort_drivers(active_drivers):
    rands = sorted(active_drivers.items(), key = lambda kv:driversum(kv[1]))
    active_drivers = dict((x,y) for x, y in rands)
    return active_drivers

def display_amounts(active_drivers,threshold):
    
#     active_drivers.sort(key = lambda x: driversum(active_drivers[driver_name(active_drivers.index(x))]))
    for driver in range(len(active_drivers)):
        tsum = driversum(active_drivers[driver_name(active_drivers,driver)])
        if(tsum > threshold):
            print(f"\nABOVE THRESHOLD(+{tsum-threshold}) : ",end = "")
        print(f"{driver_name(active_drivers,driver)} ==> {tsum}\n")
        
# def elbow_curve(orders):
#     K_clusters = range(1,50)
#     kmeans = [KMeans(n_clusters=i) for i in K_clusters]
#     Y_axis = orders[['Latitude']]
#     X_axis = orders[['Longitude']]
#     score = [kmeans[i].fit(Y_axis).score(Y_axis) for i in range(len(kmeans))]
#     # Visualize
#     plt.plot(K_clusters, score)
#     plt.xlabel('Number of Clusters')
#     plt.ylabel('Score')
#     plt.title('Elbow Curve')
#     plt.show()
    
def clustering(customers,cluster_num):
    X = customers[['community','latitude','longitude']]
    kmeans = KMeans(n_clusters = cluster_num, init ='k-means++')
    kmeans.fit(X[X.columns[1:3]]) # Compute k-means clustering.
    X['cluster_label'] = kmeans.fit_predict(X[X.columns[1:3]])
    centers = kmeans.cluster_centers_ # Coordinates of cluster centers.
    labels = kmeans.predict(X[X.columns[1:3]]) # Labels of each point
    #     X.drop_duplicates(inplace=True)
    #     X = X.T.drop_duplicates().T
    return X,centers,labels


def display_cluster(order_to_cluster,centers,labels):
    order_to_cluster.plot.scatter(x = 'latitude', y = 'longitude', c=labels, s=50, cmap='viridis')
    plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
    
def get_orders(drivernum,active_drivers): # can shorten this look into it
    dataf = pd.DataFrame(active_drivers[list(active_drivers.keys())[drivernum]] , columns = ["community","pcode","lat","long","amount","customer name","order id","track id","locality","phone no","house no"])
    return dataf

def get_communities_of_driver(name,active_drivers): # can shorten this look into it
    drivernum = list(active_drivers.keys()).index(name)
    dataf = get_orders(drivernum,active_drivers)
    
#     dataf = pd.DataFrame(active_drivers[list(active_drivers.keys())[drivernum]] , columns = ["community","pcode","lat","long","amount"])
    communities = list(dataf["community"])
    return communities

def get_row_of_driver(order_to_cluster,place):
#     return order_to_cluster.loc[orders['Community'] == dataf["community"][num]]
    return order_to_cluster.loc[order_to_cluster['community'] == place]

def cluster_distancematrix(centers):
    cluster_list = []
    labellist = ["community","latitude","longitude","cluster_label"]
    for lat,long in centers:
        cluster_list.append([lat,long])

    table_part = []
    min_part = []
    for lat1,long1 in cluster_list:
        part = []
        for lat2,long2 in cluster_list:

            if (lat1,long1) == (lat2,long2):
                part.append(0)
            else:
                print((lat1,long1),(lat2,long2))
                part.append(hs.haversine((lat1,long1),(lat2,long2)))
        table_part.append(part)   
        min_part.append(min(part))

    dframe = pd.DataFrame(table_part, columns=list(range(len(centers))), index=list(range(len(centers))))

    dframe.drop_duplicates(inplace=True)
    dframe = dframe.T.drop_duplicates().T
    return dframe

def all_drivers_in_cluster(order_to_cluster,active_drivers,cnum):
    communities = order_to_cluster.loc[order_to_cluster['cluster_label'] == cnum]
    communities["community"]
    drivers_in_cluster = []
    # print(communities["Community"])
    for dname,driver in active_drivers.items():
        for order in driver:
    #         print(order[0],dname)
            if(order[0] in list(communities["community"])):
                drivers_in_cluster.append(dname)
                break
    return drivers_in_cluster,communities

def orders_of_driver_in_cluster(name,cnum,active_drivers,order_to_cluster): # can shorten this look into it
    drivers_in_cluster,communities = all_drivers_in_cluster(order_to_cluster,active_drivers,cnum)
    communities_of_cluster = list(communities["community"])
    communities_of_driver = get_communities_of_driver(name,active_drivers)
    intersect = set(communities_of_cluster).intersection(communities_of_driver)
#     dataf = pd.DataFrame(active_drivers[list(active_drivers.keys())[drivernum]] , columns = ["community","pcode","lat","long","amount"])
    return list(intersect)

#get popped orders -> check cluster theyre in and find all clusters -> check nearest cluster to each cluster 
#show possibility of sending these orders from this cluster to the next -> check which driver driver is in that cluster 
# and check which driver is closest.


def shift(driver,threshold,active_drivers,drivers,order_to_cluster,cmatrix):
    reassigned_order = {"order_id":[],"cluster_no":[],"driver_id":[]}
    ro_driver_names = {"order_id":[],"driver_names":[]}
    drivername = driver_name(active_drivers,driver)
    shifted_driver = active_drivers.pop(driver_name(active_drivers,driver))
    orderlist = []
    for order in shifted_driver:
        row = get_row_of_driver(order_to_cluster,order[0])
        mix = []
        a = sorted(cmatrix.iloc[row.iat[0,3]])
        s = np.array(cmatrix.iloc[row.iat[0,3]])
        sort_index = np.argsort(s)
        for n in range(len(a)):
            mix.append((a[n],sort_index[n]))
        
        print(drivername)
        print(drivers[drivers['driver_name'] == drivername]["driver_id"].values[0])
        
        clust = mix[0][1]
        
        count = 0
        clusters = []
        for mixed in mix:
            if(count >= 1):
                break
            dist = mixed[0]
            clust = mixed[1]
            drivers_in_cluster,communities = all_drivers_in_cluster(order_to_cluster,active_drivers,clust)
            if(drivers_in_cluster):
                for name in drivers_in_cluster:
                    specialised_orders = orders_of_driver_in_cluster(name,clust,active_drivers,order_to_cluster)
#                     ro_driver_names["order_id"].append(int(order[6]))
                    reassigned_order["order_id"].append(int(order[6]))  
                    reassigned_order["driver_id"].append(drivers[drivers['driver_name'] == name]["driver_id"].values[0])
                    reassigned_order["cluster_no"].append(clust)
#                     ro_driver_names["driver_names"].append(name)
                    count += 1
    active_drivers[drivername] = shifted_driver
    return reassigned_order
        

def shift_all(active_drivers, reassigned_order,ro_driver_names,drivers,order_to_cluster,cmatrix): 
    r = 3
    for dnum in range(len(active_drivers)):
        reassigned_order_part = shift(dnum,0,active_drivers,drivers,order_to_cluster,cmatrix)
        reassigned_order["order_id"].extend(reassigned_order_part["order_id"])
        reassigned_order["cluster_no"].extend(reassigned_order_part["cluster_no"])
        reassigned_order["driver_id"].extend(reassigned_order_part["driver_id"])
#         ro_driver_names["order_id"].extend(ro_driver_names_part["order_id"])
#         ro_driver_names["driver_names"].extend(ro_driver_names_part["driver_names"])
        active_drivers = sort_drivers(active_drivers)
    return reassigned_order
        
def add_order_to_driver(oid,drivername):
    df2 = pd.read_excel("orders2.xlsx","Sheet1")
    df2.name = "orders"
    row = df2.loc[df2['Order Id'] == oid]
    
    
    community = row.iat[0,4]
    pcode = row.iat[0,5]
    lat = row.iat[0,6]
    long = row.iat[0,7]
    amount = row.iat[0,14]
    cname = row.iat[0,10]
    oid = row.iat[0,13]
#     active_drivers[key].append([community,pcode,lat,long,amount,cname,oid])
    print(community,pcode,lat,long,amount,cname,oid)
#     for order in 
    active_drivers[drivername].append([community,pcode,lat,long,amount,cname,oid])

def read_output(filename,sheetname):
    df = pd.read_excel(filename,sheetname)
    df = df.fillna(-1)
    orders = []
    row = 1
    while(row<df.index.stop):
        order = dict()
        order["Order id"] = df.iat[row,1]
        order["Customer name"] = df.iat[row,2]
        order["GPS"] = df.iat[row,4]
        order["Community"] = df.iat[row,7]
        order["Amount"] = df.iat[row,9]
        order["Assigned driver"] = df.iat[row,10]
        order["Cluster"] = []
        while(row<df.index.stop and df.iat[row,11]!=-1):
            eachcluster = dict()
            eachcluster[df.iat[row,11]] = []
            eachcluster[df.iat[row,11]].append(df.iat[row,12])
            if(df.iat[row,13]!=-1):
                eachcluster[df.iat[row,11]].append(df.iat[row,13])
            if(df.iat[row,14]!=-1):
                eachcluster[df.iat[row,11]].append(df.iat[row,14])
            order["Cluster"].append(eachcluster)
            row+=1
        orders.append(order)
        row+=1
    return orders

def shift_order(oid,fromdriver,todriver,active_drivers):#new code
    if(exists("active_drivers_saved.json") and os.stat("active_drivers_saved.json").st_size != 0):
        with open("active_drivers_saved.json", "r") as file:
            active_drivers = json.load(file)
       
    df2 = pd.read_excel("orders2.xlsx","Sheet1")
    df2.name = "orders"
    row = df2.loc[df2['Order Id'] == oid]
    community = row.iat[0,4]
    pcode = row.iat[0,5]
    lat = row.iat[0,6]
    long = row.iat[0,7]
    amount = row.iat[0,14]
    cname = row.iat[0,10]
    oid = row.iat[0,13]
    print(community,pcode,lat,long,amount,cname,oid)
    active_drivers[fromdriver].remove([community,pcode,lat,long,amount,cname,oid])
    active_drivers[todriver].append([community,pcode,lat,long,amount,cname,oid])
    for drivername in active_drivers.keys():
        driver = active_drivers[drivername] 
        for order in range(len(driver)):
            active_drivers[drivername][order] = [driver[order][0],int(driver[order][1]),float(driver[order][2]),float(driver[order][3]),float(driver[order][4]),driver[order][5],int(driver[order][6])]

    with open("active_drivers_saved.json", "w") as outfile:
        json.dump(active_drivers, outfile)

    
    return active_drivers

def rearrange(oid,fromdriver,todriver,active_drivers,orders):#new code
    active_drivers = shift_order(oid,fromdriver,todriver,active_drivers)
    active_drivers = sort_drivers(active_drivers)
    order_to_cluster,centers,labels = clustering(orders,20)
    dataf = get_orders(0,active_drivers)
    cmatrix = cluster_distancematrix(centers)
    drivers_in_cluster,communities = all_drivers_in_cluster(order_to_cluster,active_drivers,0)
    mainobject = shift_all(active_drivers)
    print(mainobject)
    return active_drivers
  
def bulkrearrange(oids,fromdriver,todriver,active_drivers,orders):
    for order in oids:
        active_drivers = shift_order(order,fromdriver,todriver,active_drivers)
    active_drivers = sort_drivers(active_drivers)
    order_to_cluster,centers,labels = clustering(orders,20)
    dataf = get_orders(0,active_drivers)
    cmatrix = cluster_distancematrix(centers)
    drivers_in_cluster,communities = all_drivers_in_cluster(order_to_cluster,active_drivers,0)
    mainobject = shift_all(active_drivers)
    print(mainobject)
    return active_drivers

def getstopno(filename,sheetname):
    df = pd.read_excel(filename,sheetname)
    df = df.fillna(-1)
    orders = []
    row = 1
    while(row<df.index.stop):
        order = dict()
        order["Order id"] = df.iat[row,0]
        order["Customer name"] = df.iat[row,1]
        order["GPS"] = df.iat[row,2]
        order["Community"] = df.iat[row,3]
        order["Amount"] = df.iat[row,4]
        order["Assigned driver"] = df.iat[row,5]
        order["Cluster"] = []
        while(row<df.index.stop and df.iat[row,6]!=-1):
            eachcluster = dict()
            eachcluster[df.iat[row,6]] = []
            eachcluster[df.iat[row,6]].append(df.iat[row,7])
            if(df.iat[row,8]!=-1):
                eachcluster[df.iat[row,6]].append(df.iat[row,8])
            if(df.iat[row,9]!=-1):
                eachcluster[df.iat[row,6]].append(df.iat[row,9])
            order["Cluster"].append(eachcluster)
            row+=1
        orders.append(order)
        row+=1
    return orders
    
    

def clustering_total():
    orders = pd.read_sql('SELECT * FROM orders', con=mydb)
    drivers = pd.read_sql('SELECT * FROM delivery_partner', con=mydb)
    driverspincodes = pd.read_sql('SELECT * FROM delivery_partner_pincode', con=mydb)
    customers = pd.read_sql('SELECT * FROM customer', con=mydb)
    pc_per_driver = get_pc_per_driver(driverspincodes,drivers)
    active_drivers = get_active_drivers(pc_per_driver,customers,orders)
    active_drivers = sort_drivers(active_drivers)
    order_to_cluster,centers,labels = clustering(customers,20)
    dataf = get_orders(0,active_drivers)
    cmatrix = cluster_distancematrix(centers)
    drivers_in_cluster,communities = all_drivers_in_cluster(order_to_cluster,active_drivers,0)
    clustertable = order_to_cluster[["cluster_label","latitude","longitude"]]
    clustercenters = {"cluster_no":[],"cluster_latitude":[],"cluster_longitude":[]}
    for index,item in enumerate(centers):
        clustercenters['cluster_no'].append(index)
        clustercenters['cluster_latitude'].append(item[0])
        clustercenters['cluster_longitude'].append(item[1])
    clustertable = pd.DataFrame(clustercenters)
    my_conn = create_engine("mysql+mysqldb://root:@localhost/order_management_system_427")
    clustertable.rename(columns = {'cluster_label':'cluster_no','latitude':'cluster_latitude','longitude':'cluster_longitude'}, inplace = True)
    c.execute("show tables")
    l = []
    for x in c:
        l.append(x)
    if(('cluster',) in l):
        c.execute("drop table cluster")
    if(('reassigned_order',) in l):
        c.execute("drop table reassigned_order")
    clustertable.to_sql(con=my_conn,name='cluster',if_exists='replace',index=False)
    reassigned_order = {"order_id":[],"cluster_no":[],"driver_id":[]}
    ro_driver_names = {"order_id":[],"driver_names":[]}
    reassigned_order = shift_all(active_drivers,reassigned_order,ro_driver_names,drivers,order_to_cluster,cmatrix)
    reassigned_order = pd.DataFrame(reassigned_order)
    reassigned_order = reassigned_order.drop_duplicates(subset=["order_id"])
    reassigned_order.to_sql(con=my_conn,name='reassigned_order',if_exists='replace',index=False)