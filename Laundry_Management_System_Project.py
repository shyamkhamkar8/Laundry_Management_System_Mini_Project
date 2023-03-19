1# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 22:29:08 2022
#172.25.12.74
@author: DBDA
"""
import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir=r"C:\oraclexe\app\oracle\instantclient_19_9")

class data:
    def __init__(self):
        self.con = cx_Oracle.connect('shyam/123@localhost:1521/xe')
        self.cursor = self.con.cursor()
        

    def Connection_close(self):
        self.cursor.close()
        self.con.close()

    def Customer_insert(self,nam,mob,flt,lnd,dt):
          con=self.con
          cursor=self.cursor

          cursor.callproc('l_insert_customer',[self.Customer_key(),nam,mob,flt,lnd,dt])
          cursor.execute('commit')

          self.Connection_close()
          print("Successfully Inserted!")
          return 1

    def Customer_key(self):
        con=self.con
        cursor=self.cursor
        x=cursor.execute('select max(cid) from l_customer')
        x=[i[0] for i in x]

        if x[0]==None :
            return 1
        else:
            return x[0]+1

        self.Connection_close()
        

    def check_customer(self,nam,mob,flt,lnd,dt):
         con=self.con
         cursor=self.cursor
         x=cursor.execute("select count(*) from l_customer where  name='{}' and mob_no='{}' and flat_no='{}' and landmark='{}' and c_date='{}'".format(nam,mob,flt,lnd,dt))
         x=[i[0] for i in x]
         return x[0]
         self.Connection_close()

    def Order_key(self):
        con=self.con
        cursor=self.cursor
        x=cursor.execute('select max(order_id) from l_order')
        x=[i[0] for i in x]

        if x[0]==None :
            return 1
        else:
            return x[0]+1

        self.Connection_close()

    def Ord_cust_key(self,name):
        con=self.con
        cursor=self.cursor

        x=cursor.execute("select cid from l_customer where name='{}'".format(name))
        x=[i[0] for i in x]

        return x[0]

        self.Connection_close()

    def Order_insert(self,name,wet,sh,pt,act,dt):
        con=self.con
        cursor=self.cursor
        
        cursor.callproc('l_insert_order',[self.Order_key(),self.Ord_cust_key(name),wet,sh,pt,act,dt])
        cursor.execute('commit')

        self.Connection_close()
        print("Successfully Inserted!")
        return 1

    def Bill_Amount(self,oid):
        con=self.con
        cursor=self.cursor

        x=cursor.execute("select weight,no_of_shirt,no_of_pants,action from l_order where order_id={}".format(oid))
        lst=list(x)
        wet=lst[0][0]
        no_sh=lst[0][1]
        no_pt=lst[0][2]
        act=lst[0][3]

        y1=cursor.execute("select price from l_action")
        y1=list(y1)
        press_price=float(([i[0]for i in y1][1]))
        wash_price=float(([i[0]for i in y1][0]))

        res=0
        res1=0
        if act==1:
            res=wash_price*wet
            res1=0
            return res,res1
        elif act==2:
            res=0
            res1=(no_sh+no_pt)*press_price
            return res,res1
        else:
            res=wash_price*wet
            res1=(no_sh+no_pt)*press_price
            return res,res1

        self.Connection_close()

    def Billing_insert(self,oid,dt):
        con=self.con
        cursor=self.cursor
        val=self.Bill_Amount(oid)
        cursor.callproc('l_insert_billing',[oid,dt,val[0],val[1]])
        cursor.execute('commit')
        self.Connection_close()

        return 1


    #------------------------------------------------1.add customer detail----------------------------------

    def customer_insert(self):
        self.nam=input("enter name :")
        self.mob=input("enter contact number :")
        self.flt=input("flat number :")
        self.lnd=input("landmark :")
        self.dt=input("enter date in '23-oct-1998' format :")
        if self.nam=='' or self.mob=='' or self.flt=='' or self.lnd=='':
            print("Value are blank!")
        else:
            if(self.check_customer(self.nam, self.mob, self.flt, self.lnd, self.dt)==0):
                self.Customer_insert(self.nam, self.mob, self.flt, self.lnd, self.dt)
            else:
                print("customer detail already present")
   #------------------------------------------------------------------------------------------------------------
   #------------------------------------------------2.add order detail-------------------------------------------
    def order_insert(self):
       c=True
       while(c==True):
         self.name=input("enter name :")
         if(str(self.name).isalpha()):
             self.name=self.name
             c=False
             print("done")
       print("ok")      
       a=True
       while(a==True):
        self.wet=input("enter weight :")
        if(str(self.wet).isnumeric):
            self.wet=float(self.wet)
            a=False
       while(a==False):
        self.sh=input("enter no of shirts :")
        if(str(self.sh).isnumeric):
            self.sh=int(self.sh)
            a=True
       while(a==True):
        self.pt=input("enter no of pants :")
        if(str(self.sh).isnumeric):
            self.pt=int(self.pt)
            a=False
       while(a==False):
        self.pt=input("enter no of pants :")
        if(str(self.sh).isnumeric):
            self.pt=int(self.pt)
            a=True
       while(a==True):
        self.act=input("enter action 1.washing 2.press 3.both :")
        if(str(self.sh).isnumeric):
            self.act=int(self.act)
            a=False
       self.dt=input("enter order confirm date date in format ex. 23-oct-1998 :")
       self.Order_insert(self.name, self.wet, self.sh, self.pt, self.act, self.dt)

   #----------------------------------------------------------------------------------------------------------------
   #----------------------------------------------create bill-------------------------------------------------------

    def billing_insert(self):
        self.oid=int(input("enter order no"))
        self.dt=input("enter billing date in format ex. 23-oct-1998")
        # self.Bill_Amount(self.oid)
        self.Billing_insert(self.oid, self.dt)

   #-----------------------------------------------------------------------------------------------------------------

    def display_orderdetail(self):
        con=self.con
        cursor=self.cursor
        import pandas as pd
        x=cursor.execute("select o.cid,a.name,o.order_id,o.weight,o.no_of_shirt,o.no_of_pants,o.action,o.ord_date from l_order o,l_customer a where a.cid=o.cid")
        x=list(x)
        dict1={'CID':[],'NAME':[],'ORDERID':[],'WEIGTH':[],'NO_OF_SHIRT':[],'NO_OF_PANTS':[],'ACTION':[],'DATE':[]}
        for i in x:
            dict1['CID'].append(i[0])
            dict1['NAME'].append(i[1])
            dict1['ORDERID'].append(i[2])
            dict1['WEIGTH'].append(i[3])
            dict1['NO_OF_SHIRT'].append(i[4])
            dict1['NO_OF_PANTS'].append(i[5])
            dict1['ACTION'].append(i[6])
            dict1['DATE'].append(i[7])
        df=pd.DataFrame(dict1)
        print(df)


    def display_custdetail(self):
          con=self.con
          cursor=self.cursor
          import pandas as pd
          x=cursor.execute("select * from l_customer")
          x=list(x)
          dict1={'CID':[],'NAME':[],'MOBILE_NO':[],'FLAT_NO':[],'LANDMARK':[],'DATE':[]}
          for i in x:
              dict1['CID'].append(i[0])
              dict1['NAME'].append(i[1])
              dict1['MOBILE_NO'].append(i[2])
              dict1['FLAT_NO'].append(i[3])
              dict1['LANDMARK'].append(i[4])
              dict1['DATE'].append(i[5])
          df=pd.DataFrame(dict1)
          print(df)


    def display_billingdetail(self):
          con=self.con
          cursor=self.cursor
          import pandas as pd
          x=cursor.execute("select bill_no,b_date,washing_amt,press_amt,(washing_amt+press_amt) as TOTAL from l_billing")
          x=list(x)
          dict1={'BILL_ID':[],'B_DATE':[],'WASHING_AMT':[],'PRESS_AMT':[],'TOTAL':[]}
          for i in x:
              dict1['BILL_ID'].append(i[0])
              dict1['B_DATE'].append(i[1])
              dict1['WASHING_AMT'].append(i[2])
              dict1['PRESS_AMT'].append(i[3])
              dict1['TOTAL'].append(i[4])

          df=pd.DataFrame(dict1)
          print(df)

    def display_actiondetail(self):
        con=self.con
        cursor=self.cursor
        import pandas as pd
        x=cursor.execute("select * from l_Action")
        x=list(x)
        dict1={'ACT_ID':[],'ACTION':[],'PRICE':[]}
        for i in x:
              dict1['ACT_ID'].append(i[0])
              dict1['ACTION'].append(i[1])
              dict1['PRICE'].append(i[2])
        df=pd.DataFrame(dict1)
        print(df)  
        
        

    def update_actprice(self):
        con=self.con
        cursor=self.cursor
        self.id=int(input("enter act id to change price\n1. washing\n2. press :"))
        self.pri=float(input("enter price to update :"))
        cursor.callproc('update_actprice',[self.pri,self.id])
        cursor.execute('commit')
        print("Successfully Updated")
        
    def update_custdetail(self):
        con=self.con
        cursor=self.cursor
        self.cid=int(input("enter cid of customer who's record to update :"))
        self.name=input("enter mobile number to update :")
        self.mob_no=input("enter mobile number to update :")
        self.flat_no=input("enter flat number to update :")
        self.landmark=input("enter landmark number to update :")
        self.date=input("enter date number to update in format ex.23-oct-1998 :")
        cursor.callproc('update_custdetail',[self.cid,self.name,self.mob_no,self.flat_no,self.landmark,self.date])
        cursor.execute('commit')
        print("Successfully Updated")


   #--------------------------------------------------------------------------------------------------------------
p=data()


flag=True
while(flag):
    print("----laundry shop app main menu-----")
    try:
      detail=int(input("1. to add details \n2. to display report \n3. to update action price\n4. to close program\nenter your choice :"))
    except:
      print("\nwrong input\n")
      detail=0 #for not get match by any if below

    if(detail==1):
      tlag=True
      while(tlag):
        try:
          detail1=int(input("1. to add customer details\n2. to add order details\n3. to create bill\n4. to go back to main menu\nenter your choice :"))
        except:
            detail1=4
            print("\nwrong input\n")
        if(detail1==1):
            p.customer_insert()
        elif(detail1==2):
            # try:
             p.order_insert()
            # except:
            #   print("new customer please enter customer detail first")   
        elif(detail1==3):
            p.billing_insert()
        elif(detail1==4):
            tlag=False
    
    elif(detail==2):
       slag=True
       while(slag):
         report1=int(input("\n1. to display customer detail\n2. to display order detail\n3. to display bill detail\n4. to go back to main menu\nenter your choice : "))
         if(report1==1):
             print()
             p.display_custdetail()
            
         elif(report1==2):
             print()
             p.display_orderdetail()
         elif(report1==3):
             print()
             p.display_billingdetail()
         elif(report1==4):
             slag=False
    elif(detail==3):
         update1=int(input("\n1. to update action(example.washing) price\n2. to update customer details\nenter number : "))
         if(update1==1):
          p.update_actprice()
          p.display_actiondetail()
         elif(update1==2):
          p.update_custdetail()
          p.display_custdetail()
    elif(detail==4):
         flag=False