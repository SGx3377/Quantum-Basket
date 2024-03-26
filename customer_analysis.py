# pip install mysql-connector-python
import mysql.connector
from datetime import date

def customer_signup(cursor,mydb):
    print("Please Enter your details to continue using our aplication")
    first_name = input("Please enter your first_name: ")
    last_name = input("Please enter your last_name: ")
    phone_1 = int(input("Enter a 10-digit phone number: "))
    # Embedded SQL
    cursor.execute(f"Select mail_id from customer")
    result = cursor.fetchall()
    mail_ids = [row[0] for row in result if row[0] is not None]
    num_records = len(mail_ids)
    while True:
        mail_id = input("Please enter your mail_id: ")
        if(mail_id in mail_ids):
            print(f"Mail_ID is already present, try again")
            continue
        else:
            break
    # Embedded SQL
    cursor.execute(f"Select password from customer")
    result = cursor.fetchall()
    passwords = [row[0] for row in result if row[0] is not None]
    while True:
        password = input("Please enter your password: ")
        if(password in passwords):
            print(f"Password already in use, Try again")
            continue
        else:
            check_passwd = input("Please re-enter your password: ")
            if(password==check_passwd):
                break
            else:
                print("Password doesn't match, try again")
                continue
    address_1 = input("Please enter you address: ")
    pincode_1 = int(input("Please enter a 6-digit pincode: "))
    # Embedded SQL
    sql_query = "Insert into customer(Customer_ID,First_Name,Last_Name,Mail_ID,Phone_1,Address_1,Pincode_1,Head_Office_Name,Password) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    new_customer = (num_records+1,first_name,last_name,mail_id,phone_1,address_1,pincode_1,'Quantum Basket',password)
    cursor.execute(sql_query,new_customer)
    mydb.commit()
    print("You have successfully signed up")
def customer_login(cursor):
    password = ''
    mail_id = ''
    while True:
        mail_id = input("Enter your registered mail_id: ")
        # Embedded SQL
        cursor.execute(f"SELECT * FROM customer WHERE mail_id = '{mail_id}'")
        result = cursor.fetchall()
        customer = []
        for x in result:
            customer.append(x)
        if len(customer) == 0:
            print('Sorry, your mail_id does not exist. Please try again')
            continue
        i = 3
        while i >= 0:
            password = input("Please enter your password: ")
            if customer[0][-1] == password:
                print("You have successfully logged in")
                return customer[0][0],1
            else:
                print(f"You have entered the wrong password, {i} tries left")
                i -= 1
        if i == 0:
            print("Your account has been locked temporarily")
            return customer[0][0],0
        
def update_credentials(cursor, customer_id):
    # Fetch the customer's current details from the database
    cursor.execute(f"SELECT * FROM Customer WHERE Customer_ID = {customer_id}")
    result = cursor.fetchone()
    
    # Display current details for reference and let the customer choose what to update
    print("Current Details:")
    print(f"1. First Name: {result[1]}")
    print(f"2. Last Name: {result[2]}")
    print(f"3. Mail ID: {result[3]}")
    print(f"4. Phone 1: {result[4]}")
    print(f"5. Phone 2: {result[5]}")
    print(f"6. Phone 3: {result[6]}")
    print(f"7. Address 1: {result[7]}")
    print(f"8. Address 2: {result[8]}")
    print(f"9. Address 3: {result[9]}")
    print(f"10. Pincode 1: {result[10]}")
    print(f"11. Pincode 2: {result[11]}")
    print(f"12. Pincode 3: {result[12]}")

    # Get user input for which property to update
    choice = int(input("Enter the number of the property you want to update (or 0 to exit): "))

    if choice == 0:
        print("No changes made.")
        return

    # Prompt for new value based on user's choice and update the database
    new_value = input("Enter the new value: ")

    if choice == 1:
        cursor.execute(f"UPDATE Customer SET First_Name = '{new_value}' WHERE Customer_ID = {customer_id}")
    elif choice == 2:
        cursor.execute(f"UPDATE Customer SET Last_Name = '{new_value}' WHERE Customer_ID = {customer_id}")
    elif choice == 3:
        cursor.execute(f"UPDATE Customer SET Mail_ID = '{new_value}' WHERE Customer_ID = {customer_id}")
    elif choice == 4:
        cursor.execute(f"UPDATE Customer SET Phone_1 = {int(new_value)} WHERE Customer_ID = {customer_id}")
    elif choice == 5:
        cursor.execute(f"UPDATE Customer SET Phone_2 = {int(new_value)} WHERE Customer_ID = {customer_id}")
    elif choice == 6:
        cursor.execute(f"UPDATE Customer SET Phone_3 = {int(new_value)} WHERE Customer_ID = {customer_id}")
    elif choice == 7:
        cursor.execute(f"UPDATE Customer SET Address_1 = '{new_value}' WHERE Customer_ID = {customer_id}")
    elif choice == 8:
        cursor.execute(f"UPDATE Customer SET Address_2 = '{new_value}' WHERE Customer_ID = {customer_id}")
    elif choice == 9:
        cursor.execute(f"UPDATE Customer SET Address_3 = '{new_value}' WHERE Customer_ID = {customer_id}")
    elif choice == 10:
        cursor.execute(f"UPDATE Customer SET Pincode_1 = {int(new_value)} WHERE Customer_ID = {customer_id}")
    elif choice == 11:
        cursor.execute(f"UPDATE Customer SET Pincode_2 = {int(new_value)} WHERE Customer_ID = {customer_id}")
    elif choice == 12:
        cursor.execute(f"UPDATE Customer SET Pincode_3 = {int(new_value)} WHERE Customer_ID = {customer_id}")
    elif choice == 13:
        current_password = input("Enter your current password: ")
        cursor.execute(f"SELECT Password FROM Customer WHERE Customer_ID = {customer_id}")
        db_password = cursor.fetchone()[0]
        if current_password == db_password:
            new_password = input("Enter your new password: ")
            cursor.execute(f"UPDATE Customer SET Password = '{new_password}' WHERE Customer_ID = {customer_id}")
            print("Password updated successfully!")
        else:
            print("Incorrect current password. Password not updated.")
    cursor.execute("COMMIT")
    print("Update successful!")

def ordering_the_items(cursor,customer_id):
    cursor.execute(f"Select * from cart")
    result_carts = cursor.fetchall()
    carts = [list(x) for x in result_carts]
    cart_present_flag = 0
    for i in range(0,len(carts)):
        if(customer_id==carts[i][-1]):
            cart_present_flag = 1
            break
    if(cart_present_flag==0):
        sql_query_1 = "Insert into cart values(%s,%s,%s,%s)"
        values = (customer_id,date.today(),'Open',customer_id)
        cursor.execute(sql_query_1,values)
        carts.append(list(values))
    cursor.execute("COMMIT")
# Example of using the function
def main():
    # Establish a connection to MySQL
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='Tintin0011*/',
        database='dbms_project1'
    )
    cursor = mydb.cursor()
    print("Welcome to Quantum Basket")
    print("Please sign in or sign up to continue using our application")
    func = input("Please enter Sign In or Sign Up: ")
    while True:
        if(func=='Sign In'):
            customer_id,value = customer_login(cursor)
            if(value==1):
                check = input("Do you want to update your credentials (Yes/No): ")
                if(check=='Yes'):
                    update_credentials(cursor,customer_id)
                else:
                    ordering_the_items(cursor,customer_id)
                    break
            else:
                check_1 = input("Do you want to Sign In again or Sign Up:")
                if(check_1=='Sign In'):
                    continue
                else:
                    func = 'Sign Up'
                    continue
        elif(func=='Sign Up'):
            customer_signup(cursor,mydb)
            break
    cursor.close()
    mydb.close()

if __name__ == "__main__":
    main()
