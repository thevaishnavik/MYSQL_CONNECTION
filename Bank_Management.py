from idlelib import query

import mysql.connector
class Bank_management:
    def __init__(self):
        try:
            self.con=mysql.connector.connect(user='root',password='root',host='localhost',database='bank_management')
            print("CONNECTED SUCCESSFULLY")
        except:
            print("FAILED TO CONNECT TO MYSQL")

    def create_account(self, customer_name, account_type, phone, balance):
        try:
            c = self.con.cursor()

            if balance < 0:
                print("BALANCE CANNOT BE NEGATIVE")
                return

            query = 'insert into accounts(customer_name,account_type,phone,balance) values(%s,%s,%s,%s)'

            data = (customer_name, account_type, phone, balance)

            c.execute(query, data)
            self.con.commit()

            print('ACCOUNT CREATED SUCCESSFULLY')


        except Exception as e:
                print("ERROR:", e)


    def view_accounts(self,amount):
        try:
            c=self.con.cursor()
            if amount:
                query='select * from accounts order by balance desc'

                c.execute(query)
            else:
                query='select * from accounts where balance>=%s'
                data=(amount,)
                c.execute(query,data)
            records=c.fetchall()
            if records:
                for row in records:
                    print(row)
            else:
                print('NO RECORDS FOUND')
        except:
            print("FAILED TO READ")


    def search_account(self,account_id):
        try:
            c=self.con.cursor()
            query="select * from accounts where account_id=%s"
            data=(account_id,)
            c.execute(query,data)
            record=c.fetchone()
            if record:
                print(record)
            else:
                print('RECORD NOT FOUND')
        except:
            print("FAILED TO SEARCH")

    def deposit(self,account_id,amount):
        try:
            c=self.con.cursor()
            if amount<=0:
                print("ENTER A POSITIVE AMOUNT")
                return
            query="update accounts set balance=balance+%s where account_id=%s"
            data=(amount,account_id)
            c.execute(query,data)
            self.con.commit()
            if c.rowcount>0:
                print('RECORD UPDATED SUCCESSFULLY')
            else:
                print("ACCOUNT ID NOT FOUND")
        except Exception as e:
                print("ERROR:", e)

    def withdraw(self, account_id, amount):
        try:
            c = self.con.cursor()

            if amount <= 0:
                print("ENTER A POSITIVE AMOUNT")
                return

            query = 'update accounts set balance=balance-%s where account_id=%s and balance>=%s'

            data = (amount, account_id, amount)

            c.execute(query, data)
            self.con.commit()

            if c.rowcount > 0:
                print("AMOUNT WITHDRAWN SUCCESSFULLY")
            else:
                c.execute(
                    "select account_id from accounts where account_id=%s",
                    (account_id,)
                )

                if c.fetchone():
                    print("INSUFFICIENT BALANCE")
                else:
                    print("ACCOUNT ID NOT FOUND")

        except Exception as e:
            print("ERROR:", e)

    def delete(self, account_id):
        try:
            c = self.con.cursor()
            confirm = input(
                "Are you sure you want to delete? (yes/no): "
            )

            if confirm.lower() != "yes":
                print("DELETE CANCELLED")
                return


            query = "delete from accounts where account_id=%s"
            data = (account_id,)

            c.execute(query, data)
            self.con.commit()

            if c.rowcount > 0:
                print("ACCOUNT DELETED SUCCESSFULLY")
            else:
                print("ACCOUNT ID NOT FOUND")

        except:
            print('FAILED TO DELETE')

    def summary(self):
        try:
            c = self.con.cursor()

            query ='select COUNT(*), SUM(balance), AVG(balance)from accounts'

            c.execute(query)
            record = c.fetchone()

            print("TOTAL ACCOUNTS:", record[0])
            print("TOTAL BALANCE:", record[1] or 0)
            print("AVERAGE BALANCE:", record[2] or 0)

            query ='select account_type, COUNT(*)from accounts GROUP BY account_type'
            c.execute(query)
            records = c.fetchall()

            print("ACCOUNTS BY TYPE:")

            for row in records:
                print(row[0], ":", row[1])
        except:
            print("FAILED TO DISPLAY SUMMARY")
b=Bank_management()
while(1):

        print("\n1. Create Account")
        print("2. View All Accounts")
        print("3. Search Account")
        print("4. Deposit Amount")
        print("5. Withdraw Amount")
        print("6. Delete Account")
        print("7. Account Summary")
        print("8. Exit")
        ch=int(input('ENTER YOUR CHOICE:'))

        if ch == 1:
            n = input("Enter customer name: ")
            t = input("Enter account type: ")
            p = input("Enter phone number: ")
            amount = float(input("Enter opening balance: "))
            b.create_account(n, t, p, amount)

        elif ch == 2:
            choice = input(
                "Filter by minimum balance? (y/n): "
            ).lower()

            if choice == 'y':
                amount = float(input("Enter minimum balance: "))

                if amount < 0:
                    print("Amount cannot be negative")
                else:
                    b.view_accounts(amount)
            else:
                b.view_accounts()

        elif ch == 3:
            i=int(input("Enter account ID: "))
            b.search_account(i)



        elif ch == 4:
            i = int(input("Enter account ID: "))
            amount = float(input("Enter deposit amount: "))
            b.deposit(i, amount)

        elif ch == 5:
            i = int(input("Enter account ID: "))
            amount = float(input("Enter withdrawal amount: "))
            b.withdraw(i, amount)

        elif ch == 6:
            i = int(input("Enter account ID: "))
            b.delete(i)

        elif ch == 7:
            b.summary()

        elif ch == 8:
            exit()

        else:
            print("INVALID CHOICE")













