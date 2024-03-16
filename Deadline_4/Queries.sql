-- SQL Queries
Use dbms_project1;

-- 1. Query to retrieve the customer name, their total order price and the discount applied and make a new column showing the discounted price
Select customer.first_name,total_price,discount_name,percentage,(total_price-(total_price/100)*percentage) as discounted_price
from orders 
join customer on orders.customer_id = customer.customer_id
join order_discount on orders.order_id=order_discount.order_id
join discount on discount.discount_id=order_discount.discount_id;

-- 2. Selecting customers and their orders and updating some customers mail id
Select customer.first_name,orders.*
from orders 
join customer on orders.customer_id = customer.customer_id
where customer.first_name='Ananya';

UPDATE Customer 
SET Mail_ID = "ravi.27@yahoo.com"
WHERE Customer_ID = 7;

-- 3. Get the items name and the warehouse from where they got delivered and then group by and order by according to customers
Select customer.first_name,orders.cart_id,item_name,warehouse.warehouse_id,warehouse.pincode from orders
join customer on customer.customer_id = orders.customer_id
join cart on orders.cart_id=cart.cart_id
join cart_items on cart.cart_id=cart_items.cart_id
join items on items.item_id=cart_items.item_id
join warehouse_items on items.item_id=warehouse_items.item_id
join warehouse on warehouse.warehouse_id=warehouse_items.warehouse_id
where warehouse.pincode=110075;

Select customer.first_name,orders.cart_id,warehouse.pincode, count(item_name) as total_no_of_items from orders
join customer on customer.customer_id = orders.customer_id
join cart on orders.cart_id=cart.cart_id
join cart_items on cart.cart_id=cart_items.cart_id
join items on items.item_id=cart_items.item_id
join warehouse_items on items.item_id=warehouse_items.item_id
join warehouse on warehouse.warehouse_id=warehouse_items.warehouse_id
where warehouse.pincode=110075
group by customer.first_name,orders.cart_id,warehouse.pincode
order by customer.first_name;

-- 4. Queries on Customer Wallet and Addresses
SELECT UPI_ID, Balance
FROM Customer_Wallet
right join Customer on Customer_Wallet.Customer_ID = Customer.Customer_ID
WHERE Customer_Wallet.Balance >= 1200;

SELECT Customer_ID, Address_1, Address_2, Address_3, Pincode_1, Pincode_2, Pincode_3
FROM Customer
WHERE Customer_ID = 7;

-- 5. See all items in a cart for a specific customer
SELECT C.First_Name, C.Last_Name, I.Item_Name
FROM Customer AS C
JOIN (
    SELECT CI.Customer_ID, CII.Item_ID
    FROM Cart AS CI
    JOIN Cart_Items AS CII ON CI.Cart_ID = CII.Cart_ID
    WHERE CI.Cart_Status = 'Open' AND CI.Customer_ID = 8
) AS InnerCartItems ON C.Customer_ID = InnerCartItems.Customer_ID
JOIN Items AS I ON InnerCartItems.Item_ID = I.Item_ID;


-- 6. Update the discount percentage for certain items during a specific period
UPDATE Discount
SET Percentage = 25
WHERE Discount_Name = 'ThirdDiscount'
AND Start_Date BETWEEN '2024-02-20' AND '2024-03-10';


-- 7. Update the items price according to their category
UPDATE Items
SET Price = CASE 
                WHEN Category = 'Fruits' THEN Price * 1.1
                WHEN Category = 'Vegetables' THEN Price * 1.05
                WHEN Category = 'Dairy' THEN Price * 1.08
                ELSE Price
            END;


-- 8. Update the status of carts with more than 5 items to 'Pending'
UPDATE Cart
SET Cart_Status = 'Pending'
WHERE Cart_ID IN (
                    SELECT Cart_ID
                    FROM Cart_Items
                    GROUP BY Cart_ID
                    HAVING COUNT(Item_ID) > 5
                );


-- 9. To rank managers based on customer satisfaction and finding delivery partners from a particular warehouse
SELECT avg(Rating), Manager_ID
FROM order_feedback
GROUP BY Manager_ID
ORDER BY avg(Rating) desc;

SELECT DeliveryPartner_ID, Name, Phone_Number
FROM delivery_partner
WHERE Manager_ID = 6 AND Availability_Status = 'Available';


-- 10. To find all delivery partners who do not have any complaints against them
SELECT DF1.DeliveryPartner_ID
FROM delivery_partner as DF1
WHERE NOT EXISTS (
	SELECT DeliveryPartner
    FROM delivery_feedback as DF2
    WHERE DF1.DeliveryPartner_ID = DF2.DeliveryPartner AND
		DF2.Complaint IS NOT NULL
);

-- Extra Drop and Delete Query
Alter table Head_Office
drop column Address;

Delete from Customer
where Customer_ID in (14,16,6);

-- Constraint Violation (Will throw an error as primary key is being changed, there is a duplicate formation)
UPDATE Customer 
SET Customer_ID = 2
WHERE First_Name = 'Rahul';

