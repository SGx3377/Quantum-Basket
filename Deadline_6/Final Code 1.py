# pip install mysql-connector-python
import mysql.connector
from datetime import date
import time 
import mysql.connector
from mysql.connector import errorcode

def customer_signup(cursor, mydb):
    # Create the trigger before signing up a new customer
    create_trigger_sql = """
    CREATE TRIGGER insert_customer_wallet
    AFTER INSERT ON Customer
    FOR EACH ROW
    BEGIN
        DECLARE new_upi_id VARCHAR(50);
        DECLARE upi_exists INT;

        -- Generate a random UPI ID and check if it already exists
        REPEAT
            SET new_upi_id = CONCAT('UPI', FLOOR(1000 + RAND() * 9000)); -- Example UPI ID format
            SELECT COUNT(*) INTO upi_exists FROM Customer_Wallet WHERE UPI_ID = new_upi_id;
        UNTIL upi_exists = 0 END REPEAT;

        -- Insert into Customer_Wallet table
        INSERT INTO Customer_Wallet (Customer_ID, UPI_ID, Balance) VALUES (NEW.Customer_ID, new_upi_id, 0);
    END
    """
    try:
        cursor.execute(create_trigger_sql)
        print("Trigger 'insert_customer_wallet' created successfully.")
    except mysql.connector.Error as err:
        print("Error creating trigger:", err)
        
    print("Please Enter your details to continue using our application")

    first_name = input("Please enter your first_name: ")
    last_name = input("Please enter your last_name: ")
    phone_1 = int(input("Enter a 10-digit phone number: "))

    cursor.execute("SELECT mail_id FROM customer")
    result = cursor.fetchall()
    mail_ids = [row[0] for row in result if row[0] is not None]
    num_records = len(mail_ids)

    while True:
        mail_id = input("Please enter your mail_id: ")
        if mail_id in mail_ids:
            print("Mail_ID is already present, try again")
            continue
        else:
            break

    cursor.execute("SELECT password FROM customer")
    result = cursor.fetchall()
    passwords = [row[0] for row in result if row[0] is not None]

    while True:
        password = input("Please enter your password: ")
        if password in passwords:
            print("Password already in use, Try again")
            continue
        else:
            check_passwd = input("Please re-enter your password: ")
            if password == check_passwd:
                break
            else:
                print("Password doesn't match, try again")
                continue

    address_1 = input("Please enter your address: ")
    pincode_1 = int(input("Please enter a 6-digit pincode: "))

    sql_query = "INSERT INTO customer(Customer_ID, First_Name, Last_Name, Mail_ID, Phone_1, Address_1, Pincode_1, Head_Office_Name, Password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    new_customer = (num_records + 1, first_name, last_name, mail_id, phone_1, address_1, pincode_1, 'Quantum Basket', password)
    cursor.execute(sql_query, new_customer)

    # Commit the transaction
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
                print(f"Welcome {customer[0][1]} {customer[0][2]}")
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
    print(f"7. Address 1: {result[7]} and Pincode 1: {result[10]}")
    print(f"8. Address 2: {result[8]} and Pincode 2: {result[11]}")
    print(f"9. Address 3: {result[9]} and Pincode 3: {result[12]}")
    print(f"10. Password")
    # Get user input for which property to update
    choice = int(input("Enter the number of the property you want to update (or 0 to exit): "))
    if choice == 0:
        print("No changes made.")
        return

    if choice == 1:
        new_value = input("Enter the new first name: ")
        cursor.execute(f"UPDATE Customer SET First_Name = '{new_value}' WHERE Customer_ID = {customer_id}")
    elif choice == 2:
        new_value = input("Enter the new last name: ")
        cursor.execute(f"UPDATE Customer SET Last_Name = '{new_value}' WHERE Customer_ID = {customer_id}")
    elif choice == 3:
        new_value = input("Enter the new mail_id: ")
        cursor.execute(f"UPDATE Customer SET Mail_ID = '{new_value}' WHERE Customer_ID = {customer_id}")
    elif choice == 4:
        new_value = input("Enter the new Phone 1: ")
        cursor.execute(f"UPDATE Customer SET Phone_1 = {int(new_value)} WHERE Customer_ID = {customer_id}")
    elif choice == 5:
        new_value = input("Enter the new Phone 2: ")
        cursor.execute(f"UPDATE Customer SET Phone_2 = {int(new_value)} WHERE Customer_ID = {customer_id}")
    elif choice == 6:
        new_value = input("Enter the new Phone 3: ")
        cursor.execute(f"UPDATE Customer SET Phone_3 = {int(new_value)} WHERE Customer_ID = {customer_id}")
    elif choice == 7:
        new_value_1 =  input("Enter the new Address 1: ")
        new_value_2 = input("Enter the new Pincode 1: ")
        cursor.execute(f"UPDATE Customer SET Address_1 = '{new_value_1}' WHERE Customer_ID = {customer_id}")
        cursor.execute(f"UPDATE Customer SET Pincode_1 = {int(new_value_2)} WHERE Customer_ID = {customer_id}")
    elif choice == 8:
        new_value_1 =  input("Enter the new Address 2: ")
        new_value_2 = input("Enter the new Pincode 2: ")
        cursor.execute(f"UPDATE Customer SET Address_2 = '{new_value_1}' WHERE Customer_ID = {customer_id}")
        cursor.execute(f"UPDATE Customer SET Pincode_2 = {int(new_value_2)} WHERE Customer_ID = {customer_id}")
    elif choice == 9:
        new_value_1 =  input("Enter the new Address 3: ")
        new_value_2 = input("Enter the new Pincode 3: ")
        cursor.execute(f"UPDATE Customer SET Address_3 = '{new_value_1}' WHERE Customer_ID = {customer_id}")  
        cursor.execute(f"UPDATE Customer SET Pincode_3 = {int(new_value_2)} WHERE Customer_ID = {customer_id}")
    elif choice == 10:
        val = password_change(cursor,customer_id)
        if(val==0):
            return  
    print("Update successful!")
    cursor.execute(f"SELECT * FROM Customer WHERE Customer_ID = {customer_id}")
    result = cursor.fetchone()
    print("New Details:")
    print(f"1. First Name: {result[1]}")
    print(f"2. Last Name: {result[2]}")
    print(f"3. Mail ID: {result[3]}")
    print(f"4. Phone 1: {result[4]}")
    print(f"5. Phone 2: {result[5]}")
    print(f"6. Phone 3: {result[6]}")
    print(f"7. Address 1: {result[7]} and Pincode 1: {result[10]}")
    print(f"8. Address 2: {result[8]} and Pincode 2: {result[11]}")
    print(f"9. Address 3: {result[9]} and Pincode 3: {result[12]}")
    print(f"10. Password")
    cursor.execute("COMMIT")

def password_change(cursor,customer_id):
    current_password = input("Enter your current password: ")
    cursor.execute(f"SELECT Password FROM Customer WHERE Customer_ID = {customer_id}")
    db_password = cursor.fetchone()[0]
    if current_password == db_password:
        new_password = input("Enter your new password: ")
        cursor.execute(f"UPDATE Customer SET Password = '{new_password}' WHERE Customer_ID = {customer_id}")
        print("Password updated successfully!")
        cursor.execute("COMMIT")
        return 1
    else:
        print("Incorrect current password. Password not updated.")
        return 0

def head_office(cursor,customer_id,address_no):
    # Finding the closest warehouse for the customer
    cursor.execute(f"Select pincode from warehouse") 
    warehouses = [list(x) for x in cursor]
    pincode = ''
    if(address_no=='Address_1'):
        pincode = 'Pincode_1'
    elif(address_no=='Address_2'):
        pincode = 'Pincode_2'
    else:
        pincode = 'Pincode_3'
    cursor.execute(f"Select {address_no},{pincode} from customer where customer_id={customer_id}")
    customer = [list(x) for x in cursor]
    if(customer[0][0]==None):
        print(f"There is no such address present please update the respective new address and pincode")
        update_credentials(cursor, customer_id)
        cursor.execute(f"Select {address_no},{pincode} from customer where customer_id={customer_id}")
        customer = [list(x) for x in cursor]
    old_diff = abs(warehouses[0][0]-customer[0][1])
    place = 0
    for i in range (0,len(warehouses)):
        new_diff = abs(warehouses[i][0]-customer[0][1])
        if(old_diff>new_diff):
            old_diff = new_diff
            place = i
    print(f"You order will be delivered from the closest pincode {warehouses[place][0]}")
    return warehouses[place][0]

def adding_to_cart(cursor,customer_id,pincode):
    cursor.execute(f"Select * from cart")
    result_carts = cursor.fetchall()
    carts = [list(x) for x in result_carts]
    cart_id = customer_id
    cart_present_flag = 0
    storage_cell = 0
    for i in range(0,len(carts)):
        if(cart_id==carts[i][-1]):
            cart_present_flag = 1
            storage_cell = i
            if(carts[i][-2]=='Checked Out'):
                carts[i][-2]='Open'
                cursor.execute(f"Update cart set cart_status='Open' where customer_id={customer_id}")
                cursor.execute(f"Delete from cart_items where cart_id={cart_id}")
                cursor.execute("COMMIT")
            break
    if(cart_present_flag==0):
        sql_query_1 = "Insert into cart values(%s,%s,%s,%s)"
        values = (customer_id,date.today(),'Open',customer_id)
        cursor.execute(sql_query_1,values)
        carts.append(list(values))
        cursor.execute("COMMIT")
    while True:
        cursor.execute(f"Select cart_items.item_id,item_name,num_items from cart_items join items on items.item_id=cart_items.item_id where cart_id={cart_id}")
        cart = [list(x) for x in cursor]
        cursor.execute(f"""SELECT warehouse_items.item_id, item_name, price, category, ratings, faq FROM warehouse_items JOIN warehouse ON warehouse_items.warehouse_id = warehouse.warehouse_id JOIN items ON items.item_id = warehouse_items.item_id WHERE warehouse.pincode = '{pincode}'""")
        items = cursor.fetchall()
        print("Warehouse Items:")
        print("{:<10} {:<30} {:<10} {:<15} {:<10} {:<20}".format("Item ID", "Item Name", "Price", "Category", "Ratings", "FAQ"))
        print("-" * 92)  # Separator line
        for item in items:
            print("{:<10} {:<30} {:<10} {:<15} {:<10} {:<20}".format(*item))

        print(f"Select 1 for Adding Items to Cart")
        print(f"Select 2 for Removing Items/Decreasing Quantity of items from Cart")
        print(f"Select 3 for Ordering the items")
        print(f"Select 4 for Leaving the Cart")
        checker = int(input("Enter your choice: "))
        if checker == 1:
            item_id = int(input("Enter the item_id to add in the cart: "))
            num_items = int(input("Enter the quantity you want to purchase: "))
            existing_items = [item for item in cart if item[0] == item_id]  # Check if item is already in cart
            if existing_items:
                new_quantity = existing_items[0][2] + num_items  # Update quantity if item already in cart
                cursor.execute(f"UPDATE cart_items SET num_items = {new_quantity} WHERE cart_id = {cart_id} AND item_id = {item_id}")
            else:
                sql_query_2 = "INSERT INTO cart_items VALUES (%s, %s, %s)"
                cart_values = (cart_id, item_id, num_items)
                cursor.execute(sql_query_2, cart_values)
            cursor.execute(f"Select cart_items.item_id,item_name,num_items from cart_items join items on items.item_id=cart_items.item_id where cart_id={cart_id}")
            cart1 = [list(x) for x in cursor]
            print("Cart Items:")
            print("{:<10} {:<30} {:<10}".format("Item ID", "Item Name", "Quantity"))
            print("-" * 56)  # Separator line
            for item in cart1:
                print("{:<10} {:<30} {:<10}".format(item[0], item[1], item[2]))
            cursor.execute("COMMIT")

        elif(checker==2):
            print("Cart Items:")
            print("{:<10} {:<30} {:<10}".format("Item ID", "Item Name", "Quantity"))
            print("-" * 56)  # Separator line
            for item in cart:
                print("{:<10} {:<30} {:<10}".format(item[0], item[1], item[2]))
            if(len(cart)!=0):
                item_id_1 = int(input("Enter the item_id to remove or decrease quantity from cart: "))
                checker_2 = int(input("Enter 1 to remove the item or 2 to decrease quantity: "))
                if(checker_2==1):
                    cursor.execute(f"Delete from cart_items where item_id={item_id_1}")
                    cursor.execute("COMMIT")
                else:
                    quantity_decrease = int(input("How much quantity to decrease: "))
                    cursor.execute(f"Update cart_items set num_items = num_items-{quantity_decrease} where item_id={item_id_1}")
                    cursor.execute("COMMIT")
            else:
                print("Your cart in empty")
        elif(checker==3):
            cursor.execute(f"Update cart set cart_status='Checked Out' where cart_id={cart_id}")
            cursor.execute("COMMIT")
            ordering_the_items(cursor,customer_id,cart_id,pincode)
            break
        else:
            print("Your cart has been saved")
            break
    cursor.execute("COMMIT")

def ordering_the_items(cursor, customer_id, cart_id, pincode):
    cursor.execute(f"SELECT warehouse_items.item_id, warehouse_items.item_quantity FROM warehouse_items JOIN warehouse ON warehouse_items.warehouse_id = warehouse.warehouse_id WHERE warehouse.pincode = {pincode}")
    items_in_warehouse = {item_id: item_quantity for item_id, item_quantity in cursor}

    cursor.execute(f"SELECT item_id, num_items FROM cart_items WHERE cart_id = {cart_id}")
    customer_cart = {item_id: num_items for item_id, num_items in cursor}

    for item_id, num_items in customer_cart.items():
        if item_id in items_in_warehouse:
            available_quantity = items_in_warehouse[item_id]
            if num_items > available_quantity and available_quantity > 0:
                cursor.execute(f"SELECT item_name FROM items WHERE item_id={item_id}")
                item_name = cursor.fetchone()[0]
                print(f"Error: Item ID {item_id} and item name {item_name} quantity exceeds available stock.")
                num_items = available_quantity
                print(f"Updating the quantity according to our stock to {num_items}")
                cursor.execute(f"UPDATE cart_items SET num_items = {num_items} WHERE cart_id = {cart_id} AND item_id = {item_id}")
            elif available_quantity == 0:
                cursor.execute(f"SELECT item_name FROM items WHERE item_id={item_id}")
                item_name = cursor.fetchone()[0]
                print(f"Item ID {item_id} and Item Name {item_name} is out of stock in the warehouse.")
                print(f"Removing the item from your cart")
                cursor.execute(f"DELETE FROM cart_items WHERE item_id = {item_id} AND cart_id = {cart_id}")
        else:
            cursor.execute(f"SELECT item_name FROM items WHERE item_id={item_id}")
            item_name = cursor.fetchone()[0]
            print(f"Item ID {item_id} and Item Name {item_name} is not available in the warehouse.")
            print(f"Removing the item from your cart")
            cursor.execute(f"DELETE FROM cart_items WHERE item_id = {item_id} AND cart_id = {cart_id}")

    cursor.execute(f"SELECT item_id, num_items FROM cart_items WHERE cart_id = {cart_id}")
    customer_cart_1 = {item_id: num_items for item_id, num_items in cursor}
    if customer_cart_1:
        total_price = sum(num_items * get_item_price(cursor, item_id) for item_id, num_items in customer_cart_1.items())
        total_items = sum(num_items for num_items in customer_cart_1.values())
        payment_mode = input("Enter Payment Mode (Wallet, Credit Card, Cash, etc.): ")
        order_priority = input("Enter Order Priority (High, Medium, Low, etc.): ")
        order_status = 'Processing'
        head_office_name = 'Quantum Basket'

        if payment_mode.lower() == 'wallet':
            cursor.execute("SELECT Balance FROM Customer_Wallet WHERE Customer_ID = %s", (customer_id,))
            current_balance = cursor.fetchone()[0]
            if total_price > current_balance:
                print("Error: Insufficient balance in your wallet.")
                top_up_choice = input("Would you like to top up your wallet balance? (yes/no): ")
                if top_up_choice.lower() == 'yes':
                    top_up_balance(cursor, customer_id)
                else:
                    print("Payment failed. Order not placed.")
                    return

        cursor.execute(f"INSERT INTO Orders (Total_Price, Discounted_Price, Total_Number_of_Items, OrderStatus, PaymentMode, OrderDate, OrderPriority, Customer_ID, Head_Office_Name) VALUES ({total_price}, {total_price}, {total_items}, '{order_status}', '{payment_mode}', CURRENT_DATE(), '{order_priority}', {customer_id}, '{head_office_name}')")
        cursor.execute("SELECT LAST_INSERT_ID()")
        order_id = cursor.fetchone()[0]
        cursor.execute("COMMIT")
        apply_discount(cursor, order_id, total_price)
        update_warehouse_items(cursor, cart_id, pincode)
        save_updated_cart(cursor, customer_id, cart_id, pincode, order_id)
        print("Your order has been placed successfully")
        print("It will be delivered soon to your place")
    else:
        print("Error: Cart is empty. Order not placed.")

def update_warehouse_items(cursor,cart_id,pincode):
    cursor.execute(f"SELECT item_id, num_items FROM cart_items WHERE cart_id = {cart_id}")
    updated_cart = cursor.fetchall()
    cursor.execute(f"SELECT warehouse_id FROM warehouse WHERE pincode = {pincode}")
    warehouse_id_tuple = cursor.fetchone()
    warehouse_id = int(warehouse_id_tuple[0])
    for item_id, num_items in updated_cart:
        cursor.execute(f"Update warehouse_items set Item_Quantity= Item_Quantity - {num_items} where item_id={item_id} and warehouse_id={warehouse_id}")

def save_updated_cart(cursor, customer_id, cart_id, pincode,order_id):
    cursor.execute(f"SELECT item_id, num_items FROM cart_items WHERE cart_id = {cart_id}")
    updated_cart = cursor.fetchall()

    for item_id, num_items in updated_cart:
        cursor.execute(f"INSERT INTO Order_Items (Order_ID, Item_ID, num_items, pincode) VALUES ({order_id}, {item_id}, {num_items}, {pincode})")
    
    cursor.execute("COMMIT") 

def apply_discount(cursor, order_id, total_price):
    current_date = date.today()

    cursor.execute(f"SELECT Discount_ID,Discount_Name, Percentage FROM Discount WHERE Price_Above <= {total_price} AND (Start_Date IS NULL OR Start_Date <= '{current_date}') AND (End_Date IS NULL OR End_Date >= '{current_date}') ORDER BY Percentage DESC LIMIT 1")
    discount_info = cursor.fetchone()

    if discount_info:
        discount_id,discount_name, percentage = discount_info
        discount_amount = (total_price * percentage) / 100
        discounted_price = total_price - discount_amount

        # Print discount information
        print(f"Discount Applied: {discount_name} - {percentage}%")
        print(f"Discounted Price: ${discounted_price:.2f}")

        # Update the order with the discounted price
        cursor.execute(f"UPDATE Orders SET Discounted_Price = {discounted_price} WHERE Order_ID = {order_id}")
        cursor.execute("COMMIT")
    else:
        print("No applicable discounts found.")
   
def get_item_price(cursor, item_id):
    cursor.execute(f"SELECT Price FROM Items WHERE Item_ID = {item_id}")
    item_price = cursor.fetchone()[0]
    return item_price

def view_customer_orders(cursor, customer_id):
    cursor.execute("""
        SELECT Orders.Order_ID, Orders.Total_Price, Orders.Discounted_Price, Orders.Total_Number_of_Items,
               Orders.OrderStatus, Orders.PaymentMode, Orders.OrderDate, Orders.OrderPriority,
               Orders.Head_Office_Name
        FROM Orders
        WHERE Orders.Customer_ID = %s
    """, (customer_id,))
    orders = cursor.fetchall()

    if orders:
        print("Your Orders")
        print("----------------------------------------------------------")
        print("Order ID | Total Price | Discounted Price | Total Items | Order Status | Payment Mode | Order Date | Order Priority | Head Office Name")
        print("----------------------------------------------------------")
        for order in orders:
            order_id, total_price, discounted_price, total_items, order_status, payment_mode, order_date, order_priority, head_office_name = order
            print(f"{order_id:^9} | {total_price:^11} | {discounted_price:^16} | {total_items:^11} | {order_status:^12} | {payment_mode:^12} | {order_date} | {order_priority:^15} | {head_office_name}")
        print("----------------------------------------------------------")
    else:
        print("No orders found for your account.")

def check_wallet_details(cursor, customer_id):
    try:
        cursor.execute("SELECT UPI_ID, Balance FROM Customer_Wallet WHERE Customer_ID = %s", (customer_id,))
        wallet_data = cursor.fetchone()

        if wallet_data:
            upi_id, balance = wallet_data
            print("Wallet Details:")
            print(f"UPI ID: {upi_id}")
            print(f"Current Balance: ${balance:.2f}")
        else:
            print("Wallet details not found.")

    except mysql.connector.Error as err:
        print("Error:", err)

def top_up_balance(cursor, customer_id):
    try:
        amount = int(input("Enter the amount to top up: $"))
        cursor.execute("SELECT Balance FROM Customer_Wallet WHERE Customer_ID = %s", (customer_id,))
        current_balance = cursor.fetchone()[0]

        new_balance = current_balance + amount
        cursor.execute("UPDATE Customer_Wallet SET Balance = %s WHERE Customer_ID = %s", (new_balance, customer_id))
        cursor.execute("COMMIT")

        print(f"Wallet balance topped up successfully. New balance: ${new_balance}")

    except mysql.connector.Error as err:
        print("Error:", err)

def write_order_feedback(cursor, customer_id):
    # Trigger creation SQL statement
    create_trigger_sql = """
       CREATE TRIGGER set_null_trigger 
       BEFORE INSERT ON order_feedback
       FOR EACH ROW
          IF NEW.complaint = '' THEN
              SET NEW.complaint = NULL;
          END IF;

    """

    try:
        # Execute trigger creation SQL
        cursor.execute(create_trigger_sql)
        print("Trigger 'setnull_trigger' created successfully.")
    except mysql.connector.Error as err:
        print("Error creating trigger:", err)

    cursor.execute(f"""
        SELECT Orders.Order_ID
        FROM Orders
        LEFT JOIN Order_Feedback ON Orders.Order_ID = Order_Feedback.Order_ID
        WHERE Orders.OrderStatus = 'Delivered' 
        AND Order_Feedback.OrderFeedback_ID IS NULL 
        AND Orders.Customer_ID = %s
    """, (customer_id,))
    eligible_orders = cursor.fetchall()

    if eligible_orders:
        print("Orders eligible for feedback:")
        for order_id in eligible_orders:
            print(f"Order ID: {order_id[0]}")

        order_id_input = int(input("Enter the Order ID to write feedback: "))
        if (order_id_input,) in eligible_orders:
            cursor.execute("SELECT pincode FROM order_items WHERE order_id = %s limit 1", (order_id_input,) )
            warehouse_pincode = cursor.fetchone()  # Assuming only one pincode per order ID
            if warehouse_pincode:
                warehouse_pincode = warehouse_pincode[0]  # Extracting pincode from the result tuple
                cursor.execute("SELECT warehouse_id FROM warehouse WHERE pincode = %s", (warehouse_pincode,))
                warehouse_data = cursor.fetchone()
                if warehouse_data:
                    manager_id = int(warehouse_data[0])  # Extracting manager ID as an integer
                else:
                    print("Warehouse ID not found for the given pincode.")
            else:
                print("Pincode not found for the given order ID.")

            feedback = input("Enter your feedback (max 150 characters): ")
            complaint = input("Enter any complaint (max 150 characters): ")
            rating = int(input("Enter your rating (1-5): "))

            cursor.execute("""
                INSERT INTO Order_Feedback (Feedback, Complaint, Rating, Manager_ID, Customer_ID, Order_ID)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (feedback, complaint, rating, manager_id, customer_id, order_id_input))
            cursor.execute("COMMIT")
            print("Feedback submitted successfully.")
        else:
            print("Invalid Order ID or not eligible for feedback.")
    else:
        print("No eligible orders found for feedback.")

def write_delivery_feedback(cursor, customer_id):
    # Trigger creation SQL statement
    create_trigger_sql = """
        CREATE TRIGGER update_deliveryRating
        AFTER INSERT ON delivery_feedback
        FOR EACH ROW
            UPDATE delivery_partner
            SET deliveryPartner_rating = (deliveryPartner_rating * num_orders_delivered + NEW.rating) / (num_orders_delivered + 1),
                num_orders_delivered = num_orders_delivered + 1
            WHERE deliveryPartner_ID = NEW.deliveryPartner
    """

    try:
        # Execute trigger creation SQL
        cursor.execute(create_trigger_sql)
        print("Trigger 'update_deliveryRating' created successfully.")
    except mysql.connector.Error as err:
        print("Error creating trigger:", err)

    cursor.execute(f"""
        SELECT Order_ID, DeliveryPartner_ID
        FROM delivers
        WHERE Customer_ID = {customer_id} AND Delivery_Status = 'Delivered'
    """)
    delivered_orders = cursor.fetchall()

    if delivered_orders:
        print("Delivered Orders:")
        for order_id, delivery_partner_id in delivered_orders:
            print(f"Order ID: {order_id}, Delivery Partner ID: {delivery_partner_id}")

        order_id_input = int(input("Enter the Order ID to write delivery feedback: "))
        delivery_partner_input = int(input("Enter the Delivery Partner ID: "))

        if (order_id_input, delivery_partner_input) in delivered_orders:
            cursor.execute(f"SELECT * FROM Delivery_Feedback WHERE Order_ID = {order_id_input} AND DeliveryPartner = {delivery_partner_input}")
            existing_feedback = cursor.fetchone()

            if existing_feedback:
                print("Feedback already submitted for this order and delivery partner.")
            else:
                cursor.execute("SELECT pincode FROM order_items WHERE order_id = %s limit 1", (order_id_input,))
                warehouse_pincode = cursor.fetchone()  # Assuming only one pincode per order ID
                if warehouse_pincode:
                    warehouse_pincode = warehouse_pincode[0]  # Extracting pincode from the result tuple
                    cursor.execute("SELECT warehouse_id FROM warehouse WHERE pincode = %s", (warehouse_pincode,))
                    warehouse_data = cursor.fetchone()
                    if warehouse_data:
                        manager_id = int(warehouse_data[0])  # Extracting manager ID as an integer
                    else:
                        print("Warehouse ID not found for the given pincode.")
                else:
                    print("Pincode not found for the given order ID.")
                feedback = input("Enter your feedback (max 150 characters): ")
                complaint = input("Enter any complaint (max 150 characters): ")
                rating = int(input("Enter your rating (1-5): "))

                cursor.execute(f"""
                    INSERT INTO Delivery_Feedback (DeliveryPartner, Rating, Complaint, Feedback, Manager_ID, Customer_ID, Order_ID)
                    VALUES ({delivery_partner_input}, {rating}, '{complaint}', '{feedback}', {manager_id}, {customer_id}, {order_id_input})
                """)
                cursor.execute("COMMIT")
                print("Delivery feedback submitted successfully.")
        else:
            print("Invalid Order ID or Delivery Partner ID.")
    else:
        print("No delivered orders found.")


def customer_interface(cursor, mydb):
    print("Customer Interface")
    print("Please sign in or sign up to continue using our application")

    func = input("Please enter 'Sign In' or 'Sign Up': ")

    if func == 'Sign In':
        customer_id, value = customer_login(cursor)
        if value == 1:
            while True:
                print("Choose 1 for updating your credentials:")
                print("Choose 2 for ordering items")
                print("Choose 3 to check your orders")
                print("Choose 4 to check wallet details")
                print("Choose 5 to top up wallet balance")
                print("Choose 6 to write order feedback")
                print("Choose 7 to write delivery feedback")
                print("Choose 8 to sign out")
                check = int(input("Enter your choice: "))
                if check == 1:
                    update_credentials(cursor, customer_id)
                elif check == 2:
                    cursor.execute(f"SELECT Address_1, Address_2, Address_3 FROM Customer WHERE Customer_ID = {customer_id}")
                    address_row = cursor.fetchone()
                    address_1, address_2, address_3 = address_row
                    print("Address 1:", address_1)
                    print("Address 2:", address_2 if address_2 else "N/A")  
                    print("Address 3:", address_3 if address_3 else "N/A")  
                    address_no = input("For which address you want to order (Address_1, Address_2, Address_3): ")
                    warehouse_pincode = head_office(cursor, customer_id, address_no)
                    adding_to_cart(cursor, customer_id, warehouse_pincode)
                elif check == 3:
                    view_customer_orders(cursor, customer_id)
                elif check == 4:
                    check_wallet_details(cursor, customer_id)
                elif check == 5:
                    top_up_balance(cursor, customer_id)
                elif check == 6:
                    write_order_feedback(cursor, customer_id)
                elif check == 7:
                    write_delivery_feedback(cursor, customer_id)
                elif check == 8:
                    print("Signing out...")
                    break
                else:
                    print("Invalid choice.")
        else:
            check_1 = input("Do you want to Sign In again or Sign Up:")
            if check_1 == 'Sign In':
                customer_interface(cursor, mydb)
            else:
                func = 'Sign Up'
                customer_signup(cursor, mydb)
    elif func == 'Sign Up':
        customer_signup(cursor, mydb)
    else:
        print("Invalid input. Please enter 'Sign In' or 'Sign Up'.")
# Customer Interface Ends

# Manager Interface Starts
def manager_login(cursor):
    print("Manager Login")
    email = input("Enter your Email ID: ")
    manager_id = int(input("Enter your Manager ID: "))

    cursor.execute("SELECT Warehouse_ID FROM Manager WHERE Email_ID = %s AND Manager_ID = %s", (email, manager_id))
    warehouse_id = cursor.fetchone()

    if warehouse_id:
        return warehouse_id[0]
    else:
        print("Error: Invalid Email ID or Manager ID.")
        return None

def add_items_to_warehouse(cursor, warehouse_id):
    print("Add Items to Warehouse")
    while True:
        item_id = int(input("Enter Item ID to add to warehouse (0 to exit): "))
        if item_id == 0:
            break
        
        item_quantity = int(input("Enter Item Quantity: "))

        cursor.execute("SELECT * FROM Items WHERE Item_ID = %s", (item_id,))
        item_data = cursor.fetchone()

        if item_data:
            # Check if item is already in Warehouse_Items for this warehouse
            cursor.execute("SELECT * FROM Warehouse_Items WHERE Item_ID = %s AND Warehouse_ID = %s", (item_id, warehouse_id))
            existing_item = cursor.fetchone()

            if existing_item:
                # Item exists in Warehouse_Items, update quantity
                updated_quantity = existing_item[2] + item_quantity
                cursor.execute("UPDATE Warehouse_Items SET Item_Quantity = %s WHERE Warehouse_ID = %s AND Item_ID = %s",
                               (updated_quantity, warehouse_id, item_id))
                print("Item quantity updated in warehouse successfully.")
            else:
                # Item does not exist in Warehouse_Items, insert new item
                cursor.execute("INSERT INTO Warehouse_Items (Warehouse_ID, Item_ID, Item_Quantity) VALUES (%s, %s, %s)",
                               (warehouse_id, item_id, item_quantity))
                print("New item added to warehouse successfully.")
        else:
            print("Error: Item ID not found in Items table.")

        cursor.execute("COMMIT")
        
def view_and_dispatch_orders(cursor, warehouse_id):
    while True:
        print("1. View all orders from your warehouse")
        print("2. Dispatch orders with status 'Processing'")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            view_orders(cursor, warehouse_id)
        elif choice == '2':
            dispatch_orders(cursor,warehouse_id)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def view_orders(cursor, warehouse_id):
    # Fetch orders from the specified warehouse using pincode
    cursor.execute(f"SELECT pincode FROM warehouse WHERE warehouse_id = {warehouse_id}")
    warehouse_pincode_tuple = cursor.fetchone()
    warehouse_pincode = int(warehouse_pincode_tuple[0])
    
    cursor.execute("""
        SELECT DISTINCT Orders.Order_ID, Orders.Total_Price, Orders.Discounted_Price, Orders.Total_Number_of_Items,
               Orders.OrderStatus, Orders.PaymentMode, Orders.OrderDate, Orders.OrderPriority,
               Orders.Customer_ID, Orders.Head_Office_Name
        FROM Orders
        INNER JOIN Order_Items ON Orders.Order_ID = Order_Items.Order_ID
        WHERE Order_Items.pincode = %s
    """, (warehouse_pincode,))
    
    orders = cursor.fetchall()

    if orders:
        print("Orders Placed from your Warehouse")
        print("----------------------------------------------------------")
        print("Order ID | Total Price | Discounted Price | Total Items | Order Status | Payment Mode | Order Date | Order Priority | Customer ID | Head Office Name")
        print("----------------------------------------------------------")
        total_price_all_orders = 0  # Initialize total price variable
        discounted_price_all_orders = 0
        for order in orders:
            order_id, total_price, discounted_price, total_items, order_status, payment_mode, order_date, order_priority, customer_id, head_office_name = order
            print(f"{order_id:^9} | {total_price:^11} | {discounted_price:^16} | {total_items:^11} | {order_status:^12} | {payment_mode:^12} | {order_date} | {order_priority:^15} | {customer_id:^11} | {head_office_name}")
            total_price_all_orders += total_price  # Accumulate total price of each order
            discounted_price_all_orders += discounted_price

        print("----------------------------------------------------------")
        print("Total Price of All Orders:", total_price_all_orders)  # Print total price of all orders
        print("Discounted Price of All Orders:", discounted_price_all_orders)
        print("----------------------------------------------------------")
    else:
        print("No orders found from your warehouse")

def dispatch_orders(cursor, warehouse_id):
    try:
        # Start a transaction
        cursor.execute("START TRANSACTION")

        cursor.execute(f"SELECT pincode FROM warehouse WHERE warehouse_id = {warehouse_id} FOR UPDATE")
        warehouse_pincode_tuple = cursor.fetchone()
        warehouse_pincode = int(warehouse_pincode_tuple[0])
        
        cursor.execute("""
            SELECT DISTINCT Orders.Order_ID
            FROM Orders
            INNER JOIN Order_Items ON Orders.Order_ID = Order_Items.Order_ID
            WHERE Order_Items.pincode = %s and Orders.OrderStatus = 'Processing' FOR UPDATE
        """, (warehouse_pincode,))
        processing_orders = cursor.fetchall()

        if processing_orders:
            print("Orders Ready for Dispatch (Order Status: Processing)")
            print("----------------------------------------------------------")
            print("Order ID")
            print("----------------------------------------------------------")
            for order_id in processing_orders:
                print(f"{order_id[0]}")

            print("----------------------------------------------------------")
            dispatch_option = input("Enter the Order ID to dispatch or 'exit' to return to main menu: ")

            if dispatch_option.lower() != 'exit':
                try:
                    order_id_to_dispatch = int(dispatch_option)
                    if (order_id_to_dispatch,) in processing_orders:
                        # Perform dispatch action here, for example, update order status
                        cursor.execute("""
                            UPDATE Orders
                            SET OrderStatus = 'Dispatched'
                            WHERE Order_ID = %s
                        """, (order_id_to_dispatch,))
                        print(f"Order ID {order_id_to_dispatch} has been successfully dispatched.")
                    else:
                        print("Invalid Order ID. Please enter a valid Order ID.")
                except ValueError:
                    print("Invalid input. Please enter a valid Order ID.")
        else:
            print("No orders with status 'Processing' found.")

        # Commit the transaction if all statements executed successfully
        cursor.execute("COMMIT")
    except mysql.connector.errors.DatabaseError as e:
        # Rollback the transaction in case of deadlock or other database errors
        cursor.execute("ROLLBACK")
        print(f"Error during transaction: {e}")
        
        # Retry the transaction after a short delay in case of deadlock
        print("Retrying transaction...")
        time.sleep(1)  # Delay for 1 second
        dispatch_orders(cursor, warehouse_id)  # Retry the transaction

def assign_delivery_partner(cursor, manager_id):
    # Trigger creation SQL statement
    create_trigger_sql = """
        CREATE TRIGGER update_deliveryPartnerStatus
        AFTER INSERT ON delivers
        FOR EACH ROW
            UPDATE delivery_partner
            SET availability_status = 'Not Available'
            WHERE deliveryPartner_ID = NEW.deliveryPartner_ID
    """

    try:
        # Execute trigger creation SQL
        cursor.execute(create_trigger_sql)
        print("Trigger 'update_deliveryPartnerStatus' created successfully.")
    except mysql.connector.Error as err:
        print("Error creating trigger:", err)

    try:
        cursor.execute(f"SELECT pincode FROM warehouse WHERE warehouse_id = {manager_id} FOR UPDATE")
        warehouse_pincode_tuple = cursor.fetchone()
        warehouse_pincode = int(warehouse_pincode_tuple[0])

        cursor.execute("""
            SELECT DISTINCT Orders.Order_ID
            FROM Orders
            INNER JOIN Order_Items ON Orders.Order_ID = Order_Items.Order_ID
            WHERE Order_Items.pincode = %s and Orders.OrderStatus = 'Dispatched' FOR UPDATE
        """, (warehouse_pincode,))
        processing_orders = cursor.fetchall()

        if processing_orders:
            print("Processing Orders (Order Status: Dispatched):")
            for order_id in processing_orders:
                print(f"Order ID: {order_id[0]}")

            order_id = int(input("Enter the Order ID to assign a delivery partner: "))

            if (order_id,) in processing_orders:
                cursor.execute("""
                    SELECT DeliveryPartner_ID, Name, num_orders_delivered
                    FROM Delivery_Partner
                    WHERE Manager_ID = %s AND Availability_Status = 'Available'
                """, (manager_id,))
                available_partners = cursor.fetchall()

                if available_partners:
                    print("Available Delivery Partners:")
                    for partner in available_partners:
                        print(f"ID: {partner[0]}, Name: {partner[1]}, Orders Delivered: {partner[2]}")

                    delivery_partner_id = int(input("Enter the Delivery Partner ID: "))

                    if any(partner[0] == delivery_partner_id for partner in available_partners):
                        cursor.execute("""
                            INSERT INTO delivers (Customer_ID, Order_ID, DeliveryPartner_ID, Delivery_Status)
                            VALUES (
                                (SELECT Customer_ID FROM Orders WHERE Order_ID = %s),
                                %s,
                                %s,
                                'In Transit'
                            )
                        """, (order_id, order_id, delivery_partner_id))

                        cursor.execute("""
                            UPDATE Delivery_Partner
                            SET num_orders_delivered = num_orders_delivered + 1
                            WHERE DeliveryPartner_ID = %s
                        """, (delivery_partner_id,))

                        cursor.execute("""
                            UPDATE Orders
                            SET OrderStatus = 'Out for Delivery'
                            WHERE Order_ID = %s
                        """, (order_id,))
                        cursor.execute("COMMIT")

                        print("Delivery partner assigned successfully.")
                    else:
                        print("Error: Selected delivery partner is not available.")
                else:
                    print("No available delivery partners under your management.")
            else:
                print("Invalid Order ID or order not suitable for assignment.")

        else:
            print("No processing orders found (Order Status: Dispatched) under your warehouse.")

    except mysql.connector.Error as err:
        print("Error:", err)


def see_delivery_partners(cursor, manager_id):
    cursor.execute("SELECT * FROM Delivery_Partner WHERE Manager_ID = %s", (manager_id,))
    delivery_partners = cursor.fetchall()

    if delivery_partners:
        print("Delivery Partners:")
        for partner in delivery_partners:
            print(f"Partner ID: {partner[0]}")
            print(f"Name: {partner[1]}")
            print(f"Phone Number: {partner[2]}")
            print(f"Rating: {partner[3]}")
            print(f"Feedback: {partner[4]}")
            print(f"Availability Status: {partner[5]}")
            print("-----------------------------------")
    else:
        print("No delivery partners found under this manager.")

def add_remove_delivery_partner(cursor, manager_id):
    while True:
        print("\nDelivery Partners Management")
        print("1. Add New Delivery Partner")
        print("2. Remove Delivery Partner")
        print("3. Exit Delivery Partners Management")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_new_delivery_partner(cursor, manager_id)
        elif choice == '2':
            remove_delivery_partner(cursor, manager_id)
        elif choice == '3':
            print("Exiting Delivery Partners Management")
            break
        else:
            print("Invalid choice. Please try again.")

def add_new_delivery_partner(cursor, manager_id):
    name = input("Enter Name: ")
    phone_number = input("Enter Phone Number: ")
    availability_status = input("Enter Availability Status: ")
    rating = float(input("Enter Rating: "))
    feedback = input("Enter Feedback: ")

    cursor.execute("""
        INSERT INTO Delivery_Partner (Name, Phone_Number, DeliveryPartner_Rating, DeliveryPartner_Feedback, Availability_Status, Manager_ID)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, phone_number, rating, feedback, availability_status, manager_id))
    print("New delivery partner added successfully.")
    cursor.execute("COMMIT")

def remove_delivery_partner(cursor, manager_id):
    partner_id = input("Enter Partner ID to remove: ")
    cursor.execute("DELETE FROM Delivery_Partner WHERE DeliveryPartner_ID = %s AND Manager_ID = %s", (partner_id, manager_id))
    if cursor.rowcount > 0:
        print("Delivery partner removed successfully.")
        cursor.execute("COMMIT")
    else:
        print("No such delivery partner found under this manager.")

def see_order_feedback(cursor, manager_id):
    cursor.execute(f"""
        SELECT OrderFeedback_ID, Feedback, Complaint, Rating, Customer_ID, Order_ID
        FROM Order_Feedback
        WHERE Manager_ID = {manager_id}
    """)
    feedback_data = cursor.fetchall()

    if feedback_data:
        print("Order Feedback:")
        print("{:<15} {:<15} {:<15} {:<8} {:<12} {:<8}".format(
            "Feedback ID", "Feedback", "Complaint", "Rating", "Customer ID", "Order ID"))
        print("-" * 75)  # Separator line

        for feedback in feedback_data:
            feedback_id, feedback_text, complaint, rating, customer_id, order_id = feedback
            # Replace None values with "NA"
            feedback_id = feedback_id if feedback_id is not None else "NA"
            feedback_text = feedback_text if feedback_text is not None else "NA"
            complaint = complaint if complaint is not None else "NA"
            rating = rating if rating is not None else "NA"
            customer_id = customer_id if customer_id is not None else "NA"
            order_id = order_id if order_id is not None else "NA"

            print("{:<15} {:<15} {:<15} {:<8} {:<12} {:<8}".format(
                feedback_id, feedback_text, complaint, rating, customer_id, order_id))
        print("-" * 75)  # Separator line
    else:
        print("No order feedback found for this manager.")
        
def see_delivery_feedback(cursor, manager_id):
    cursor.execute(f"""
        SELECT DeliveryFeedback_ID, DeliveryPartner, Rating, Complaint, Feedback, Customer_ID, Order_ID
        FROM Delivery_Feedback
        WHERE Manager_ID = {manager_id}
    """)
    feedback_data = cursor.fetchall()

    if feedback_data:
        print("Delivery Feedback:")
        print("{:<18} {:<15} {:<8} {:<13} {:<15} {:<12} {:<8}".format(
            "Feedback ID", "Delivery Partner", "Rating", "Complaint", "Feedback", "Customer ID", "Order ID"))
        print("-" * 95)  # Separator line

        for feedback in feedback_data:
            feedback_id, delivery_partner, rating, complaint, feedback_text, customer_id, order_id = feedback
            # Replace None values with "NA"
            feedback_id = feedback_id if feedback_id is not None else "NA"
            delivery_partner = delivery_partner if delivery_partner is not None else "NA"
            rating = rating if rating is not None else "NA"
            complaint = complaint if complaint is not None else "NA"
            feedback_text = feedback_text if feedback_text is not None else "NA"
            customer_id = customer_id if customer_id is not None else "NA"
            order_id = order_id if order_id is not None else "NA"

            print("{:<18} {:<15} {:<8} {:<13} {:<15} {:<12} {:<8}".format(
                feedback_id, delivery_partner, rating, complaint, feedback_text, customer_id, order_id))
        print("-" * 95)  # Separator line
    else:
        print("No delivery feedback found for this manager.")

def manager_interface(cursor, mydb):
    print("Manager Interface")
    manager_id = manager_login(cursor)
    if manager_id:
        while True:
            print("\nManager Options:")
            print("1. Add/Remove Items to Warehouse")
            print("2. View/Dispatch Orders from Warehouse")
            print("3. See Delivery Partners")
            print("4. Manage Delivery Partners")
            print("5. Assign Delivery Partner")
            print("6. See Order Feedback")
            print("7. See Delivery Feedback")
            print("8. Exit Manager Interface")

            choice = input("Enter your choice: ")

            if choice == '1':
                add_items_to_warehouse(cursor, manager_id)
            elif choice == '2':
                view_and_dispatch_orders(cursor, manager_id)
            elif choice == '3':
                see_delivery_partners(cursor, manager_id)
            elif choice == '4':
                add_remove_delivery_partner(cursor, manager_id)
            elif choice == '5':
                assign_delivery_partner(cursor, manager_id)
            elif choice == '6':
                see_order_feedback(cursor, manager_id)
            elif choice == '7':
                see_delivery_feedback(cursor, manager_id)
            elif choice == '8':
                print("Exiting Manager Interface")
                break
            else:
                print("Invalid choice. Please try again.")
# Manager Interface Ends

# Head Office Interface Starts
def display_all_customers(cursor):
    print("List of Customers:")
    cursor.execute("SELECT * FROM Customer")
    customers = cursor.fetchall()

    if customers:
        for customer in customers:
            print(f"Customer ID: {customer[0]}")
            print(f"First Name: {customer[1]}")
            print(f"Last Name: {customer[2]}")
            print(f"Mail ID: {customer[3]}")
            print(f"Phone 1: {customer[4]}")
            print(f"Phone 2: {customer[5]}")
            print(f"Phone 3: {customer[6]}")
            print(f"Address 1: {customer[7]}")
            print(f"Address 2: {customer[8]}")
            print(f"Address 3: {customer[9]}")
            print(f"Pincode 1: {customer[10]}")
            print(f"Pincode 2: {customer[11]}")
            print(f"Pincode 3: {customer[12]}")
            print("--------------------------------------")
        
        total_customers = len(customers)
        print(f"Total number of customers: {total_customers}")
    else:
        print("No customers found.")
        
def display_all_managers(cursor):
    print("List of Managers:")
    cursor.execute("SELECT * FROM Manager")
    managers = cursor.fetchall()

    if managers:
        for manager in managers:
            print(f"Manager ID: {manager[0]}")
            print(f"First Name: {manager[1]}")
            print(f"Last Name: {manager[2]}")
            print(f"Phone Number: {manager[3]}")
            print(f"Email ID: {manager[4]}")
            print(f"Salary: {manager[5]}")
            print(f"Joining Date: {manager[6]}")
            print(f"Warehouse ID: {manager[7]}")
            print("--------------------------------------")
    else:
        print("No managers found.")

def modify_manager_salary(cursor,mydb):
    manager_id = int(input("Enter Manager ID to modify salary: "))
    new_salary = int(input("Enter new salary: "))

    cursor.execute("UPDATE Manager SET Salary = %s WHERE Manager_ID = %s", (new_salary, manager_id))
    mydb.commit()
    print("Manager salary updated successfully.")
    
def add_item_to_items(cursor, mydb):
    print("Add Item to Items Table")
    item_id = int(input("Enter Item ID: "))
    item_name = input("Enter Item Name: ")
    price = int(input("Enter Price: "))
    category = input("Enter Category: ")
    ratings = input("Enter Ratings: ")
    faq = input("Enter FAQ: ")

    cursor.execute("INSERT INTO Items (Item_ID, Item_Name, Price, Category, Ratings, FAQ) VALUES (%s, %s, %s, %s, %s, %s)",
                   (item_id, item_name, price, category, ratings, faq))
    mydb.commit()
    print("Item added to Items table successfully.")
    
def remove_item_from_items(cursor, mydb):
    print("Remove Item from Items Table")
    item_id = int(input("Enter Item ID to remove: "))

    cursor.execute("SELECT * FROM Items WHERE Item_ID = %s", (item_id,))
    item_data = cursor.fetchone()

    if item_data:
        cursor.execute("DELETE FROM Items WHERE Item_ID = %s", (item_id,))
        mydb.commit()
        print("Item removed from Items table successfully.")
    else:
        print("Error: Item ID not found in Items table.")

def add_discount(cursor, mydb):
    print("Add Discount")
    discount_name = input("Enter Discount Name: ")
    percentage = int(input("Enter Percentage: "))
    price_above = int(input("Enter Price Above: "))
    start_date = input("Enter Start Date (YYYY-MM-DD): ")
    end_date = input("Enter End Date (YYYY-MM-DD): ")

    cursor.execute("INSERT INTO Discount (Discount_Name, Percentage, Price_Above, Start_Date, End_Date, Head_Office_Name) VALUES (%s, %s, %s, %s, %s, 'Quantum Basket')",
                   (discount_name, percentage, price_above, start_date, end_date))
    mydb.commit()
    print("Discount added successfully.")

def remove_discount(cursor, mydb):
    cursor.execute("SELECT * FROM Discount")
    discounts = cursor.fetchall()
    print("Discount Details:")
    print("{:<10} {:<20} {:<10} {:<15} {:<15} {:<15} {:<30}".format(
    "Discount ID", "Discount Name", "Percentage", "Price Above", "Start Date", "End Date", "Head Office Name"))
    print("-" * 105)  # Separator line
    for discount in discounts:
        discount_id, discount_name, percentage, price_above, start_date, end_date, head_office_name = discount
        start_date_formatted = start_date.strftime("%Y-%m-%d") if start_date else "N/A"
        end_date_formatted = end_date.strftime("%Y-%m-%d") if end_date else "N/A"
        print("{:<10} {:<20} {:<10} {:<15} {:<15} {:<15} {:<30}".format(
            discount_id, discount_name, percentage, price_above if price_above else "N/A",
            start_date_formatted, end_date_formatted, head_office_name))


    print("Remove Discount")
    discount_id = int(input("Enter Discount ID to remove: "))

    cursor.execute("DELETE FROM Discount WHERE Discount_ID = %s", (discount_id,))
    mydb.commit()
    print("Discount removed successfully.")

def head_office_interface(cursor, mydb):
    print("Head Office Login")
    head_office_name = input("Enter Head Office Name: ")

    cursor.execute("SELECT * FROM Head_Office WHERE Head_Office_Name = %s", (head_office_name,))
    office_data = cursor.fetchone()

    if office_data:
        print("Head office login successful.")
        while True:  # Loop for options until the user chooses to exit
            print("Choose an option:")
            print("1. View All Managers")
            print("2. Modify Manager Salary")
            print("3. View All Customers")
            print("4. Add Item to Items Table")
            print("5. Add Discount")
            print("6. Remove Discount")
            print("0. Exit")  # New option to exit

            option = input("Enter your choice: ")

            if option == '1':
                display_all_managers(cursor)
            elif option == '2':
                modify_manager_salary(cursor, mydb)
            elif option == '3':
                display_all_customers(cursor)
            elif option == '4':
                add_item_to_items(cursor, mydb)
            elif option == '5':
                add_discount(cursor, mydb)
            elif option == '6':
                remove_discount(cursor, mydb)
            elif option == '0':  # Exit option
                print("Exiting Head Office Interface.")
                break
            else:
                print("Invalid option.")
    else:
        print("Error: Invalid Head Office Name.")
# Head Office Interface Ends

# Delivery Partner Interface Starts
def display_partner_stats(cursor, partner_id):
    cursor.execute("SELECT * FROM Delivery_Partner WHERE DeliveryPartner_ID = %s", (partner_id,))
    partner_data = cursor.fetchone()

    if partner_data:
        print("Partner ID:", partner_data[0])
        print("Name:", partner_data[1])
        print("Phone Number:", partner_data[2])
        print("Delivery Partner Rating:", partner_data[3])
        print("Delivery Partner Feedback:", partner_data[4])
        print("Availability Status:", partner_data[5])
    else:
        print("Delivery partner not found.")

def set_availability_status(cursor, partner_id):
    new_availability = input("Enter your new availability status: ")
    cursor.execute("UPDATE Delivery_Partner SET Availability_Status = %s WHERE DeliveryPartner_ID = %s",
                   (new_availability, partner_id))
    cursor.execute("COMMIT")  # Commit the changes to the database
    print("Availability status updated successfully.")

def deliver_order(cursor, partner_id):
    try:
        # Fetch orders assigned to the delivery partner
        cursor.execute("""
            SELECT Order_ID
            FROM delivers
            WHERE DeliveryPartner_ID = %s AND Delivery_Status = 'In Transit'
        """, (partner_id,))
        assigned_orders = cursor.fetchall()

        if assigned_orders:
            print("Orders to be Delivered:")
            for order in assigned_orders:
                print(f"Order ID: {order[0]}")

            order_id = int(input("Enter the Order ID to mark as delivered: "))

            # Check if the selected order is assigned to the delivery partner
            if (order_id,) in assigned_orders:
                cursor.execute("""
                    UPDATE delivers
                    SET Delivery_Status = 'Delivered'
                    WHERE Order_ID = %s AND DeliveryPartner_ID = %s
                """, (order_id, partner_id))
                cursor.execute("""
                    UPDATE Orders
                    SET OrderStatus = 'Delivered'
                    WHERE Order_ID = %s
                """, (order_id,))
                cursor.execute("""
                    UPDATE Delivery_Partner
                    SET Availability_Status = 'Available'
                    WHERE DeliveryPartner_ID = %s
                """, (partner_id,))
                cursor.execute("COMMIT")  # Commit the changes to the database
                
                # Fetch customer details and print delivery confirmation message
                cursor.execute("SELECT Customer_ID FROM Orders WHERE Order_ID = %s", (order_id,))
                customer_id_row = cursor.fetchone()
                customer_id = int(customer_id_row[0]) if customer_id_row else None
                cursor.execute("SELECT First_Name, Last_Name FROM Customer WHERE Customer_ID = %s", (customer_id,))
                customer_data = cursor.fetchone()

                # Print delivery confirmation message
                if customer_data:
                    print(f"Order with ID {order_id} was delivered successfully to {customer_data[0]} {customer_data[1]}.")

                    # Fetch order details including item names
                    cursor.execute("""
                        SELECT Items.Item_Name, Order_Items.num_items, Items.Price
                        FROM Order_Items
                        INNER JOIN Items ON Order_Items.Item_ID = Items.Item_ID
                        WHERE Order_Items.Order_ID = %s
                    """, (order_id,))
                    order_details = cursor.fetchall()

                    if order_details:
                        print("\nOrder Details:")
                        print("----------------------------------------------------------")
                        print("Item Name | Quantity | Price per Item")
                        print("----------------------------------------------------------")
                        total_price = 0
                        for item in order_details:
                            item_name, quantity, price = item
                            total_item_price = price * quantity
                            total_price += total_item_price
                            print(f"{item_name:<9} | {quantity:^9} | {price:^14}")
                        print("----------------------------------------------------------")

                        # Fetch total price and discounted price from Orders table
                        cursor.execute("SELECT Total_Price, Discounted_Price FROM Orders WHERE Order_ID = %s", (order_id,))
                        order_prices = cursor.fetchone()
                        if order_prices:
                            total_price = order_prices[0]
                            discounted_price = order_prices[1]
                            print(f"Total Price: {total_price} | Discounted Price: {discounted_price}")
                        else:
                            print("Total Price and Discounted Price not found in Orders table.")
                    else:
                        print("No order details found.")

                else:
                    print("Customer data not found.")

            else:
                print("Invalid Order ID or order not assigned to you.")

        else:
            print("No orders assigned to you for delivery.")

    except mysql.connector.Error as err:
        print("Error:", err)

def delivery_partner_interface(cursor, mydb):
    print("Delivery Partner Interface")
    partner_id = int(input("Enter your ID: "))  # Assuming delivery partner ID is numeric

    while True:
        try:
            cursor.execute("SELECT * FROM Delivery_Partner WHERE DeliveryPartner_ID = %s", (partner_id,))
            partner_data = cursor.fetchone()

            if partner_data:
                print("\nLogin successful!")
                print("Welcome,", partner_data[1])  # Display partner's name

                print("\nChoose an option:")
                print("1. View Stats")
                print("2. Set Availability")
                print("3. Deliver Order")
                print("4. Exit Delivery Interface")
                option = int(input("Enter your choice (1, 2, 3, or 4): "))

                if option == 1:
                    display_partner_stats(cursor, partner_id)
                elif option == 2:
                    set_availability_status(cursor, partner_id)
                elif option == 3:
                    deliver_order(cursor, partner_id)
                elif option == 4:
                    print("Exiting Delivery Partner Interface.")
                    break  # Exit the while loop and function
                else:
                    print("Invalid option. Please choose 1, 2, 3, or 4.")

            else:
                print("Delivery partner not found. Please check your ID.")

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Error: Access denied. Check your username and password.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Error: Database does not exist.")
            else:
                print("Error:", err)
# Delivery Partner Interface Ends

# Main Function Starts
def main():
    try:
        # Establish a connection to MySQL
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='Tintin0011*/',
            database='dbms_project1'
        )
        cursor = mydb.cursor()

        while True:
            print("Welcome to Quantum Basket")
            print("Are you a Manager, a Customer, a Head Office, or a Delivery Partner?")
            user_type = input("Enter 'Manager', 'Customer', 'Head Office', or 'Delivery Partner': ").lower()

            if user_type == 'manager':
                manager_interface(cursor, mydb)
            elif user_type == 'customer':
                customer_interface(cursor, mydb)
            elif user_type == 'head office':
                head_office_interface(cursor, mydb)
            elif user_type == 'delivery partner':
                delivery_partner_interface(cursor, mydb)
            elif user_type == 'exit':
                print("Exiting Quantum Basket.")
                break
            else:
                print("Invalid input. Please enter 'Manager', 'Customer', 'Head Office', 'Delivery Partner', or 'Exit'.")

        cursor.close()
        mydb.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Access denied. Check your username and password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: Database does not exist.")
        else:
            print("Error:", err)


if __name__ == "__main__":
    main()
