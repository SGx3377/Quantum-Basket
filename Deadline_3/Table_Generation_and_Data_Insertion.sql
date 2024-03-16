-- SQL Script Quantum Basket
Create Database if not exists DBMS_Project1;
Use DBMS_Project1;

-- Table Creation of Head Office
Create table if not exists Head_Office(Head_Office_Name varchar(10) Primary Key,Address varchar(30) not null,Phone_Number bigint not null);
Alter table Head_Office add constraint check_Phone_Number_range check(Phone_Number between 1000000000 and 9999999999);
Alter table Head_Office modify column Head_Office_Name varchar(30);
-- Data insertion in Head_Office
Insert into Head_Office(Head_Office_Name,Address,Phone_Number) values
('Quantum Basket','Cyberhub, Gurugram, Haryana', 7695699110);

-- Table Creation of Customer
Create table if not exists Customer(Customer_ID integer Primary Key,First_Name varchar(40) not null,Last_Name varchar(20),Mail_ID varchar(30) unique,Phone_1 integer not null,Phone_2 integer,Phone_3 integer,Address_1 varchar(30) not null,Address_2 varchar(30),Address_3 varchar(30),Pincode_1 integer not null,Pincode_2 integer,Pincode_3 integer, Head_Office_Name varchar(30) references Head_Office(Head_Office_Name));
-- Constraints added to Customer Table 
ALTER TABLE Customer
ADD CONSTRAINT check_mail_id_length CHECK (LENGTH(Mail_ID) <= 30),
ADD CONSTRAINT check_phone_range CHECK (Phone_1 BETWEEN 1000000000 AND 9999999999),
ADD CONSTRAINT check_phone_range_2 CHECK (Phone_2 IS NULL OR (Phone_2 BETWEEN 1000000000 AND 9999999999)),
ADD CONSTRAINT check_phone_range_3 CHECK (Phone_3 IS NULL OR (Phone_3 BETWEEN 1000000000 AND 9999999999));
ALTER TABLE Customer
MODIFY COLUMN Phone_1 BIGINT NOT NULL,
MODIFY COLUMN Phone_2 BIGINT,
MODIFY COLUMN Phone_3 BIGINT;
CREATE INDEX idx_Customer_ID ON Customer(Customer_ID);
-- Data Insertion in Customer Table
INSERT INTO Customer (Customer_ID, First_Name, Last_Name, Mail_ID, Phone_1, Phone_2, Phone_3, Address_1, Address_2, Address_3, Pincode_1, Pincode_2, Pincode_3, Head_Office_Name)
VALUES
(1, 'Rahul', 'Kumar', 'rahul.kumar@email.com', 9876543210, 8765432109, NULL, '123 Ganga Nagar', 'Sector 5', 'Apartment 302', 411027, 411028, 411047, 'Quantum Basket'),
(2, 'Priya', 'Sharma', 'priya.sharma@email.com', 8765432101, NULL, NULL, '456 Yamuna Street', NULL, NULL, 380015, NULL, NULL, 'Quantum Basket'),
(3, 'Amit', 'Verma', 'amit.verma@email.com', 9988776655, NULL, NULL, '789 Krishna Vihar', NULL,'Flat 45', 500081, NULL, 420041, 'Quantum Basket'),
(4, 'Ananya', 'Bose', 'ananya.bose@email.com', 7766554433, NULL, NULL, '567 Jamuna Enclave', 'Block C', 'Flat 203', 700064, 700067, 110078, 'Quantum Basket'),
(5, 'Vikram', 'Singh', 'vikram.singh@email.com', 9876543221, 9876543223, NULL, '890 Saraswati Nagar', 'Apt 201', NULL, 110075, 110076, NULL, 'Quantum Basket'),
(6, 'Kavita', 'Mishra', 'kavita.mishra@email.com', 9988776655, NULL, NULL, '901 Ganges Heights', 'Block C',NULL, 201301, 301301, NULL, 'Quantum Basket'),
(7, 'Ravi', 'Jha', 'ravi.jha@email.com', 8899001122, NULL, NULL, '234 Indira Bhavan', 'Apt 202', NULL, 500032, 702774, NULL, 'Quantum Basket'),
(8, 'Sneha', 'Gupta', 'sneha.gupta@email.com', 7778889999, 8887776666, 6665554444, '789 Yamuna Residency', 'Block D', 'Flat 405', 380016, 382011, 382012, 'Quantum Basket'),
(9, 'Rajesh', 'Yadav', 'rajesh.yadav@email.com', 9988776655, NULL, NULL, '543 Ganga Vihar', NULL, NULL, 700028, NULL, NULL, 'Quantum Basket'),
(10, 'Neha', 'Chopra', 'neha.chopra@email.com', 8899001122, NULL, NULL, '678 Saraswati Bhavan', 'Apt 105', NULL, 110011, 110012, NULL, 'Quantum Basket'),
(11, 'Suresh', 'Kumar', 'suresh.kumar@email.com', 1111222233, 2222333344, 3333444455, '901 Narmada Apartments', 'Building B', 'Flat 89', 110085, 110086, 110087, 'Quantum Basket'),
(12, 'Anita', 'Roy', 'anita.roy@email.com', 5555666677, NULL, NULL, '345 Saraswati Vihar', NULL, 'Flat 56', 201302, NULL, 201305, 'Quantum Basket'),
(13, 'Manish', 'Gupta', 'manish.gupta@email.com', 8888777766, NULL, NULL, '567 Ganges Enclave', NULL, NULL, 700045, NULL, NULL, 'Quantum Basket'),
(14, 'Pooja', 'Mehta', 'pooja.mehta@email.com', 7777888899, NULL, NULL, '890 Jamuna Towers', 'Apt 301', NULL, 380018,401401, NULL, 'Quantum Basket'),
(15, 'Alok', 'Shukla', 'alok.shukla@email.com', 3333444455, 4444555566, NULL, '123 Yamuna Residency', 'Building C', 'Flat 201', 110091, 110092, 10078, 'Quantum Basket'),
(16, 'Arjun', 'Gupta', 'arjun.gupta@email.com', 9876543213, NULL, NULL, '234 Yamuna Apartments', 'Block B', 'Flat 56', 110020, 110001, 122002, 'Quantum Basket'),
(17, 'Shreya', 'Rao', 'shreya.rao@email.com', 8765432107, 7654321096, NULL, '567 Ganga Residency', 'Block D', NULL, 500030, 500031, NULL, 'Quantum Basket'),
(18, 'Rohit', 'Singh', 'rohit.singh@email.com', 9988776658, NULL, NULL, '789 Narmada Society', NULL, NULL, 380014, NULL, NULL, 'Quantum Basket'),
(19, 'Neha', 'Jaiswal', 'neha.jaiswal@email.com', 7766554437, NULL, NULL, '567 Saraswati Bhavan', 'Apt 303', NULL, 201303, 203506, NULL, 'Quantum Basket'),
(20, 'Amitabh', 'Mukherjee', 'amitabh.mukherjee@email.com', 9876543221, 9876543223, NULL, '890 Jamuna Towers', 'Apt 401', NULL, 110010, 110013, NULL, 'Quantum Basket'),
(21, 'Kirti', 'Rathore', 'kirti.rathore@email.com', 9988776651, NULL, NULL, '901 Krishna Vihar', 'Tower A', 'Flat 89', 201304, 465606, 230323, 'Quantum Basket'),
(22, 'Sanjay', 'Shukla', 'sanjay.shukla@email.com', 8899001133, NULL, NULL, '234 Indira Bhavan', 'Apt 105', NULL, 500034, 500798, NULL, 'Quantum Basket'),
(23, 'Shikha', 'Choudhary', 'shikha.choudhary@email.com', 7778889994, 8887776663, 6665554441, '789 Saraswati Nagar', 'Block B', 'Flat 301', 380019, 382014, 102230, 'Quantum Basket'),
(24, 'Vishal', 'Kumar', 'vishal.kumar@email.com', 9988776652, NULL, NULL, '543 Krishna Vihar', NULL, 'Flat 45', 700020, NULL, 700021, 'Quantum Basket'),
(25, 'Anjali', 'Sharma', 'anjali.sharma@email.com', 8899001144, NULL, NULL, '678 Yamuna Residency', NULL, 'Apt 201', 110014, NULL, 100020, 'Quantum Basket');

-- Create Customer_Wallet table as a weak entity
CREATE TABLE if not exists Customer_Wallet(Customer_ID int references Customer(Customer_ID),UPI_ID varchar(50),Balance decimal(10, 2),PRIMARY KEY (Customer_ID, UPI_ID));
CREATE INDEX idx_Customer_Wallet_Customer_ID ON Customer_Wallet(Customer_ID);
-- Data Insertion in Customer Wallet
INSERT INTO Customer_Wallet (Customer_ID, UPI_ID, Balance)
VALUES
    (1, 'rahul.kumar@upi', 1000.00),
    (2, 'priya.sharma@upi', 800.00),
    (3, 'amit.verma@upi', 1200.00),
    (4, 'ananya.bose@upi', 1500.00),
    (5, 'vikram.singh@upi', 900.00),
    (6, 'kavita.mishra@upi', 1100.00),
    (7, 'ravi.jha@upi', 1300.00),
    (8, 'sneha.gupta@upi', 950.00),
    (9, 'rajesh.yadav@upi', 850.00),
    (10, 'neha.chopra@upi', 1000.00),
    (11, 'suresh.kumar@upi', 1200.00),
    (12, 'anita.roy@upi', 1100.00),
    (13, 'manish.gupta@upi', 1300.00),
    (14, 'pooja.mehta@upi', 950.00),
    (15, 'alok.shukla@upi', 850.00),
    (16, 'arjun.gupta@upi', 1000.00),
    (17, 'shreya.rao@upi', 1200.00),
    (18, 'rohit.singh@upi', 1100.00),
    (19, 'neha.jaiswal@upi', 1300.00),
    (20, 'amitabh.mukherjee@upi', 950.00),
    (21, 'kirti.rathore@upi', 850.00),
    (22, 'sanjay.shukla@upi', 1000.00),
    (23, 'shikha.choudhary@upi', 1200.00),
    (24, 'vishal.kumar@upi', 1100.00),
    (25, 'anjali.sharma@upi', 1300.00);

-- Table creation of Warehouse
Create table if not exists Warehouse(Warehouse_ID integer Primary Key,Address varchar(30),Pincode integer not null, Head_Office_Name varchar(30) references Head_Office(Head_Office_Name));
-- Data Insertion in Warehouse Table
INSERT INTO Warehouse (Warehouse_ID, Address, Pincode, Head_Office_Name)
VALUES
(1, '123 Main Street, Pune', 411027, 'Quantum Basket'),
(2, '456 Oak Avenue, Ahmedabad', 380015, 'Quantum Basket'),
(3, '789 Elm Road, Hyderabad', 500081, 'Quantum Basket'),
(4, '567 Pine Lane, Kolkata', 700064, 'Quantum Basket'),
(5, '890 Cedar Street, New Delhi', 110075, 'Quantum Basket'),
(6, '901 Birch Lane, Noida', 201301, 'Quantum Basket'),
(7, '234 Maple Road, Secunderabad', 500032, 'Quantum Basket'),
(8, '789 Oak Avenue, Ahmedabad', 380016, 'Quantum Basket'),
(9, '543 Cedar Lane, Kolkata', 700028, 'Quantum Basket'),
(10, '678 Elm Road, New Delhi', 110011, 'Quantum Basket');

-- Table Creation of Manager
Create table if not exists Manager(Manager_ID integer Primary Key,First_Name varchar(30) not null,Last_Name varchar(20),Phone_Number bigint not null,Email_ID varchar(30) unique,Salary integer,Joining_Date date,Warehouse_ID integer references Warehouse(Warehouse_ID),Head_Office_Name varchar(30) references Head_Office(Head_Office_Name));
-- Data Insertion in Manger table
INSERT INTO Manager (Manager_ID, First_Name, Last_Name, Phone_Number, Email_ID, Salary, Joining_Date, Warehouse_ID, Head_Office_Name)
VALUES
(1, 'Rahul', 'Sharma', 9876543210, 'rahul.sharma@email.com', 60000, '2022-01-10', 1, 'Quantum Basket'),
(2, 'Sonia', 'Singh', 8765432109, 'sonia.singh@email.com', 55000, '2022-02-15', 2, 'Quantum Basket'),
(3, 'Amit', 'Verma', 9988776655, 'amit.verma@email.com', 70000, '2021-12-05', 3, 'Quantum Basket'),
(4, 'Pooja', 'Gupta', 7766554433, 'pooja.gupta@email.com', 75000, '2021-11-20', 4, 'Quantum Basket'),
(5, 'Vikram', 'Yadav', 9876543211, 'vikram.yadav@email.com', 65000, '2022-03-01', 5, 'Quantum Basket'),
(6, 'Neha', 'Shukla', 9988776655, 'neha.shukla@email.com', 80000, '2021-10-15', 6, 'Quantum Basket'),
(7, 'Rajesh', 'Chopra', 8899001122, 'rajesh.chopra@email.com', 72000, '2022-01-25', 7, 'Quantum Basket'),
(8, 'Sneha', 'Kumar', 7778889999, 'sneha.kumar@email.com', 68000, '2022-02-10', 8, 'Quantum Basket'),
(9, 'Alok', 'Rathore', 4445556666, 'alok.rathore@email.com', 60000, '2021-11-10', 9, 'Quantum Basket'),
(10, 'Anjali', 'Sharma', 3333444455, 'anjali.sharma@email.com', 67000, '2022-03-15', 10, 'Quantum Basket');


-- Table Creation of Items and added check to see Stock_avalability
Create table if not exists Items(Item_ID integer Primary Key,Item_Name varchar(20) not null,Price integer not null,Category varchar(15),Stock_Availability integer not null,Ratings varchar(5),FAQ varchar(20),check(Stock_Availability>0 and Price>=0));
CREATE INDEX idx_Item_ID ON Items(Item_ID);
INSERT INTO Items (Item_ID, Item_Name, Price, Category, Stock_Availability, Ratings, FAQ)
VALUES
(1, 'Bananas', 30, 'Fruits', 100, '4.8', 'FAQ-1'),
(2, 'Apples', 40, 'Fruits', 80, '4.6', 'FAQ-2'),
(3, 'Carrots', 20, 'Vegetables', 50, '4.5', 'FAQ-3'),
(4, 'Potatoes', 25, 'Vegetables', 60, '4.4', 'FAQ-4'),
(5, 'Milk', 50, 'Dairy', 120, '4.7', 'FAQ-5'),
(6, 'Bread', 30, 'Bakery', 80, '4.5', 'FAQ-6'),
(7, 'Eggs', 40, 'Dairy', 100, '4.6', 'FAQ-7'),
(8, 'Tomatoes', 35, 'Vegetables', 70, '4.3', 'FAQ-8'),
(9, 'Rice (5kg)', 300, 'Grains', 40, '4.4', 'FAQ-9'),
(10, 'Chicken Breast', 200, 'Meat', 30, '4.7', 'FAQ-10'),
(11, 'Oranges', 35, 'Fruits', 60, '4.5', 'FAQ-11'),
(12, 'Cucumbers', 15, 'Vegetables', 40, '4.2', 'FAQ-12'),
(13, 'Yogurt', 45, 'Dairy', 80, '4.6', 'FAQ-13'),
(14, 'Pasta (500g)', 40, 'Grains', 50, '4.3', 'FAQ-14'),
(15, 'Salmon Fillet', 250, 'Seafood', 20, '4.8', 'FAQ-15'),
(16, 'Strawberries', 60, 'Fruits', 30, '4.7', 'FAQ-16'),
(17, 'Spinach', 25, 'Vegetables', 45, '4.5', 'FAQ-17'),
(18, 'Cheese', 70, 'Dairy', 60, '4.6', 'FAQ-18'),
(19, 'Quinoa (1kg)', 120, 'Grains', 25, '4.4', 'FAQ-19'),
(20, 'Shrimp', 180, 'Seafood', 35, '4.5', 'FAQ-20'),
(21, 'Avocado', 50, 'Fruits', 40, '4.6', 'FAQ-21'),
(22, 'Bell Peppers', 30, 'Vegetables', 60, '4.3', 'FAQ-22'),
(23, 'Almond Milk', 60, 'Dairy', 50, '4.5', 'FAQ-23'),
(24, 'Cereal', 25, 'Grains', 70, '4.2', 'FAQ-24'),
(25, 'Tilapia Fillet', 120, 'Seafood', 25, '4.4', 'FAQ-25'),
(26, 'Grapes', 40, 'Fruits', 35, '4.7', 'FAQ-26'),
(27, 'Zucchini', 20, 'Vegetables', 45, '4.2', 'FAQ-27'),
(28, 'Soy Milk', 55, 'Dairy', 40, '4.4', 'FAQ-28'),
(29, 'Brown Rice (1kg)', 80, 'Grains', 30, '4.6', 'FAQ-29'),
(30, 'Tuna Can', 35, 'Seafood', 55, '4.5', 'FAQ-30'),
(31, 'Kiwi', 60, 'Fruits', 30, '4.5', 'FAQ-31'),
(32, 'Broccoli', 25, 'Vegetables', 40, '4.3', 'FAQ-32'),
(33, 'Coconut Milk', 45, 'Dairy', 35, '4.6', 'FAQ-33'),
(34, 'Quinoa (500g)', 70, 'Grains', 20, '4.4', 'FAQ-34'),
(35, 'Sardines Can', 30, 'Seafood', 50, '4.2', 'FAQ-35'),
(36, 'Pineapple', 45, 'Fruits', 25, '4.6', 'FAQ-36'),
(37, 'Cauliflower', 30, 'Vegetables', 35, '4.3', 'FAQ-37'),
(38, 'Cashew Milk', 65, 'Dairy', 30, '4.5', 'FAQ-38'),
(39, 'Barley (1kg)', 50, 'Grains', 15, '4.7', 'FAQ-39'),
(40, 'Mackerel Fillet', 100, 'Seafood', 20, '4.6', 'FAQ-40');

-- Warehouse_Items
Create table if not exists Warehouse_Items(Warehouse_ID integer references Warehouse(Warehouse_ID),Item_ID integer references Items(Item_ID),Primary key(Warehouse_ID,Item_ID));
INSERT INTO Warehouse_Items (Warehouse_ID, Item_ID)
VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
(2, 6), (2, 7), (2, 8), (2, 9), (2, 10),
(3, 11), (3, 12), (3, 13), (3, 14), (3, 15),
(4, 16), (4, 17), (4, 18), (4, 19), (4, 20),
(5, 21), (5, 22), (5, 23), (5, 24), (5, 25),
(6, 26), (6, 27), (6, 28), (6, 29), (6, 30),
(7, 31), (7, 32), (7, 33), (7, 34), (7, 35),
(8, 36), (8, 37), (8, 38), (8, 39), (8, 40),
(9, 1), (9, 2), (9, 3), (9, 4), (9, 5),
(10, 6), (10, 7), (10, 8), (10, 9), (10, 10),
(4, 11), (4, 12), (4, 13), (4, 14), (4, 15),
(5, 16), (5, 17), (5, 18), (5, 19), (5, 20),
(6, 21), (6, 22), (6, 23), (6, 24), (6, 25),
(7, 26), (7, 27), (7, 28), (7, 29), (7, 30),
(8, 31), (8, 32), (8, 33), (8, 34), (8, 35),
(1, 36), (1, 37), (1, 38), (1, 39), (1, 40),
(2, 1), (2, 2), (2, 3), (2, 4), (2, 5),
(3, 6), (3, 7), (3, 8), (3, 9), (3, 10),
(1, 11), (1, 12), (1, 13), (1, 14), (1, 15),
(9, 21), (9, 22), (9, 23), (9, 24), (9, 25),
(10, 26), (10, 27), (10, 28), (10, 29), (10, 30);

-- Cart
Create table if not exists Cart(Cart_ID integer Primary Key,Date_Created date,Cart_Status varchar(30),Customer_ID integer references Customer(Customer_ID));
-- Insert data into Cart table
INSERT INTO Cart (Cart_ID, Date_Created, Cart_Status, Customer_ID)
VALUES
(1, '2024-02-06', 'Open', 1),
(2, '2024-02-06', 'Checked Out', 2),
(3, '2024-02-06', 'Open', 3),
(4, '2024-02-06', 'Checked Out', 4),
(5, '2024-02-06', 'Open', 5),
(6, '2024-02-06', 'Open', 6),
(7, '2024-02-06', 'Checked Out', 7),
(8, '2024-02-06', 'Open', 8),
(9, '2024-02-06', 'Checked Out', 9),
(10, '2024-02-06', 'Checked Out', 10),
(11, '2024-02-07', 'Open', 11),
(12, '2024-02-07', 'Open', 12),
(13, '2024-02-07', 'Checked Out', 13),
(14, '2024-02-07', 'Checked Out', 14),
(15, '2024-02-07', 'Open', 15),
(16, '2024-02-07', 'Checked Out', 16),
(17, '2024-02-07', 'Checked Out', 17),
(18, '2024-02-07', 'Open', 18),
(19, '2024-02-07', 'Open', 19),
(20, '2024-02-07', 'Checked Out', 20);
-- Cart_Items
Create Table if not exists Cart_Items(Cart_ID integer references Cart(Cart_ID),Item_ID integer references Items(Item_ID),primary key(Cart_ID,Item_ID));
-- Insert data into Cart_Items table
INSERT INTO Cart_Items (Cart_ID, Item_ID)
VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
(2, 6), (2, 7), (2, 8), (2, 9), (2, 10),
(3, 11), (3, 12), (3, 13), (3, 14), (3, 15),
(4, 16), (4, 17), (4, 18), (4, 19), (4, 20),
(5, 21), (5, 22), (5, 23), (5, 24), (5, 25),
(6, 26), (6, 27), (6, 28), (6, 29), (6, 30),
(7, 31), (7, 32), (7, 33), (7, 34), (7, 35),
(8, 36), (8, 37), (8, 38), (8, 39), (8, 40),
(9, 1), (9, 2), (9, 3), (9, 4), (9, 5),
(10, 6), (10, 7), (10, 8), (10, 9), (10, 10),
(11, 16), (11, 17), (11, 18), (11, 19), (11, 20),
(12, 21), (12, 22), (12, 23), (12, 24), (12, 25),
(13, 26), (13, 27), (13, 28), (13, 29), (13, 30),
(14, 31), (14, 32), (14, 33), (14, 34), (14, 35),
(15, 36), (15, 37), (15, 38), (15, 39), (15, 40),
(16, 1), (16, 2), (16, 3), (16, 4), (16, 5),
(17, 6), (17, 7), (17, 8), (17, 9), (17, 10),
(18, 11), (18, 12), (18, 13), (18, 14), (18, 15),
(19, 16), (19, 17), (19, 18), (19, 19), (19, 20),
(20, 21), (20, 22), (20, 23), (20, 24), (20, 25);


-- Table Creation of Discount
Create Table if not exists Discount(Discount_ID integer Primary Key,Discount_Name varchar(20) unique,Percentage integer not null,Price_Above integer,Start_Date date,End_Date date,Head_Office_Name varchar (30) references Head_Office(Head_Office_Name),check(Percentage>0 and Price_Above>=150));
-- Data Insertion in Discount Table
INSERT INTO Discount (Discount_ID, Discount_Name, Percentage, Price_Above, Start_Date, End_Date, Head_Office_Name)
VALUES
(1, 'FirstDiscount', 10, 150, '2024-02-01', '2024-02-15', 'Quantum Basket'),
(2, 'SecondDiscount', 15, 200, '2024-02-10', '2024-02-28', 'Quantum Basket'),
(3, 'ThirdDiscount', 20, 250, '2024-02-20', '2024-03-10', 'Quantum Basket');

-- Table Creation of Order
Create Table if not exists Orders(Order_ID int Primary Key,Total_Price int not null,Total_Number_of_Items int not null,OrderStatus varchar(20) not null,PaymentMode varchar(20) not null,OrderDate date not null,OrderPriority varchar(20) not null,Customer_ID int references Customer(Customer_ID),Cart_ID int references Cart(Cart_ID),Head_Office_Name varchar(30) references Head_Office(Head_Office_Name));
CREATE INDEX idx_Orders_ID ON Orders(Order_ID);
CREATE INDEX idx_Orders_Customer_ID ON Orders(Customer_ID);
CREATE INDEX idx_Orders_Cart_ID ON Orders(Cart_ID);
-- Insert data into Order table for checked-out carts
INSERT INTO Orders (Order_ID, Total_Price, Total_Number_of_Items, OrderStatus, PaymentMode, OrderDate, OrderPriority, Customer_ID, Cart_ID, Head_Office_Name)
VALUES
    (1, 200, 5, 'Shipped', 'Credit Card', '2024-02-07', 'Express', 2, 2, 'Quantum Basket'),
    (2, 150, 4, 'Processing', 'PayPal', '2024-02-08', 'Standard', 4, 4, 'Quantum Basket'),
    (3, 180, 3, 'Shipped', 'Credit Card', '2024-02-09', 'Express', 7, 7, 'Quantum Basket'),
    (4, 220, 6, 'Processing', 'PayPal', '2024-02-10', 'Standard', 9, 9, 'Quantum Basket'),
    (5, 250, 6, 'Shipped', 'PayPal', '2024-02-11', 'Express', 10, 10, 'Quantum Basket'),
    (6, 130, 3, 'Processing', 'Credit Card', '2024-02-12', 'Standard', 13, 13, 'Quantum Basket'),
    (7, 170, 4, 'Shipped', 'PayPal', '2024-02-13', 'Express', 14, 14, 'Quantum Basket'),
    (8, 190, 5, 'Processing', 'Credit Card', '2024-02-14', 'Standard', 16, 16, 'Quantum Basket'),
    (9, 210, 6, 'Shipped', 'PayPal', '2024-02-15', 'Express', 17, 17, 'Quantum Basket'),
    (10, 200, 4, 'Processing', 'Credit Card', '2024-02-16', 'Standard', 20, 20, 'Quantum Basket');

-- Table Cration of Order_Discount
CREATE TABLE if not exists Order_Discount(Order_ID int references Orders(Order_ID),Discount_ID int references Discount(Discount_ID),Primary Key(Order_ID,Discount_ID));
-- Insert data into the Order_Discount table
INSERT INTO Order_Discount (Order_ID, Discount_ID)
VALUES
    (1, 1), -- Order 1 with FirstDiscount
    (2, 2), -- Order 2 with SecondDiscount
    (3, 1), -- Order 3 with FirstDiscount
    (4, 3), -- Order 4 with ThirdDiscount
    (5, 2), -- Order 5 with SecondDiscount
    (6, 1), -- Order 6 with FirstDiscount
    (7, 3), -- Order 7 with ThirdDiscount
    (8, 2), -- Order 8 with SecondDiscount
    (9, 1), -- Order 9 with FirstDiscount
    (10, 3); -- Order 10 with ThirdDiscount

-- Create Delivery_Partner table
CREATE TABLE if not exists Delivery_Partner(DeliveryPartner_ID INT PRIMARY KEY,Name VARCHAR(50) NOT NULL,Phone_Number BIGINT NOT NULL,DeliveryPartner_Rating FLOAT,DeliveryPartner_Feedback VARCHAR(255),Availability_Status VARCHAR(20) NOT NULL,Manager_ID INT REFERENCES Manager(Manager_ID),check(DeliveryPartner_Rating>=1 and DeliveryPartner_Rating<=5));
-- Insert data into Delivery_Partner table
INSERT INTO Delivery_Partner (DeliveryPartner_ID, Name, Phone_Number, DeliveryPartner_Rating, DeliveryPartner_Feedback, Availability_Status, Manager_ID)
VALUES
    (1, 'John Doe', 9876543210, 4.5, 'Good service', 'Available', 1),
    (2, 'Alice Smith', 8765432109, 4.2, 'Timely delivery', 'Available', 2),
    (3, 'Bob Johnson', 9988776655, 4.8, 'Excellent communication', 'Not Available', 3),
    (4, 'Emma Brown', 7766554433, 4.0, 'Friendly delivery', 'Available', 4),
    (5, 'Ryan Patel', 9876543211, 4.6, 'Professional service', 'Available', 5),
    (6, 'Lily Kumar', 9988776655, 4.4, 'Quick delivery', 'Available', 6),
    (7, 'Raj Chopra', 8899001122, 4.7, 'Responsive to feedback', 'Not Available', 7),
    (8, 'Sneha Gupta', 7778889999, 4.1, 'Courteous behavior', 'Available', 8),
    (9, 'Alok Rathore', 4445556666, 4.3, 'Safe handling of items', 'Available', 9),
    (10, 'Anjali Sharma', 3333444455, 4.9, 'Very satisfied', 'Available', 10),
    (11, 'Michael Wilson', 9988776655, 4.2, 'Friendly service', 'Not Available', 1),
    (12, 'Sophia Lee', 8899001122, 4.5, 'Fast and reliable', 'Available', 2),
    (13, 'David Brown', 7778889999, 4.7, 'Courteous behavior', 'Available', 3),
    (14, 'Olivia Patel', 4445556666, 4.1, 'Professional delivery', 'Not Available', 4),
    (15, 'William Gupta', 9876543211, 4.4, 'Responsive to customer needs', 'Available', 5),
    (16, 'Emily Singh', 9988776655, 4.8, 'Excellent communication skills', 'Available', 6),
    (17, 'Daniel Kumar', 8899001122, 4.3, 'Timely delivery', 'Available', 7),
    (18, 'Ava Chopra', 7778889999, 4.6, 'Safe handling of items', 'Available', 8),
    (19, 'Alexander Rathore', 4445556666, 4.0, 'Customer-focused service', 'Not Available', 9),
    (20, 'Sophie Sharma', 3333444455, 4.9, 'Satisfactory experience', 'Available', 10);

-- Table Creation of delivers relation
CREATE TABLE if not exists delivers(Customer_ID int references Customer(Customer_ID),Order_ID int references Orders(Order_ID),DeliveryPartner_ID int references Delivery_Partner(DeliveryPartner_ID),Delivery_Status varchar(30) DEFAULT NULL,Delivery_Address varchar(90) DEFAULT NULL,DeliveryDate date DEFAULT NULL,Primary Key(Customer_ID,Order_ID,DeliveryPartner_ID));
-- Insert data into delivers table, choosing only available delivery partners and correct delivery addresses
INSERT INTO delivers (Customer_ID, Order_ID, DeliveryPartner_ID, Delivery_Status, Delivery_Address, DeliveryDate)
VALUES
    (2, 1, 1, 'Delivered', '456 Yamuna Street, 380015', '2024-02-09'), -- Customer 2, Order 1, Available Delivery Partner 1
    (4, 2, 2, 'Delivered', '567 Jamuna Enclave, Block C, Flat 203, 700064', NULL), -- Customer 4, Order 2, Available Delivery Partner 2
    (7, 3, 3, 'Pending', '234 Indira Bhavan, Apt 202, 500032', NULL), -- Customer 7, Order 3, Available Delivery Partner 3
    (9, 4, 4, 'Delivered', '543 Ganga Vihar, 700028', '2024-02-12'), -- Customer 9, Order 4, Available Delivery Partner 4
    (10, 5, 5, 'Delivered', '678 Saraswati Bhavan, Apt 105, 110011', NULL), -- Customer 10, Order 5, Available Delivery Partner 5
    (13, 6, 6, 'Pending', '567 Ganges Enclave, 700045', NULL), -- Customer 13, Order 6, Available Delivery Partner 6
    (14, 7, 7, 'Delivered', '890 Jamuna Towers, Apt 301, 380018', '2024-02-15'), -- Customer 14, Order 7, Available Delivery Partner 7
    (16, 8, 8, 'In Transit', '234 Yamuna Apartments, Block B, Flat 56, 110020', NULL), -- Customer 16, Order 8, Available Delivery Partner 8
    (17, 9, 9, 'Pending', '567 Ganga Residency, Block D, 500030', NULL), -- Customer 17, Order 9, Available Delivery Partner 9
    (20, 10, 10, 'Delivered', '678 Yamuna Residency, Apt 201, 110014', '2024-02-18'); -- Customer 20, Order 10, Available Delivery Partner 10

CREATE TABLE if not exists Delivery_Feedback(DeliveryFeedback_ID int PRIMARY KEY, DeliveryPartner INT references delivery_partner(DeliveryPratner_ID), Rating int NOT NULL, CHECK (Rating>=1 and Rating<=5),Complaint varchar(150) DEFAULT NULL,Feedback varchar(150) DEFAULT NULL,Manager_ID int references Manager(Manager_ID));
INSERT INTO Delivery_Feedback (DeliveryFeedback_ID, DeliveryPartner, Rating, Complaint, Feedback, Manager_ID)
VALUES
(1, 3, 5, NULL, 'Great service!', 1),
(2, 2, 3, 'Late delivery', 'Delivery took longer than expected', 2),
(3, 5, 4, NULL, 'Satisfied with the delivery', 4),
(4, 3, 2,'Damaged package', 'Received damaged items', 5),
(5, 8, 4, NULL, 'Good service overall', 7),
(6, 10, 5, NULL, 'Very satisfied with the delivery', 10);

Create table if not exists Writes_Delivery_Feedback(DeliveryFeedback_ID int references Delivery_Feedback(DeliveryFeedback_ID),Customer_ID int references Customer(Customer_ID),Order_ID int references Orders(Order_ID),Primary Key(DeliveryFeedback_ID,Customer_ID,Order_ID));
-- Insert data into Writes_Delivery_Feedback table 
INSERT INTO Writes_Delivery_Feedback (DeliveryFeedback_ID, Customer_ID, Order_ID)
VALUES
(1, 2, 1),
(2, 4, 2),
(3, 9, 4),
(4, 10, 5),
(5, 14, 7),
(6, 20, 10);

-- Create Order_Feedback table
CREATE TABLE if not exists Order_Feedback (OrderFeedback_ID int PRIMARY KEY,Feedback VARCHAR(150) DEFAULT NULL,Complaint VARCHAR(150) DEFAULT NULL,Rating int NOT NULL CHECK (Rating >= 1 AND Rating <= 5),Manager_ID int REFERENCES Manager(Manager_ID));

-- Insert data into Order_Feedback table
INSERT INTO Order_Feedback (OrderFeedback_ID, Feedback, Complaint, Rating, Manager_ID)
VALUES
    (1, 'Products were not fresh', NULL, 3, 1),
    (2, 'Satisfactory Products', 'One item was not delivered', 4, 2),
    (3, 'Excellent packaging and delivery', NULL, 5, 4),
    (4, 'Not Satisfied', 'Wrong item delivered', 2, 5),
    (5, 'Products are bad', 'Received Damaged Item',2, 7),
    (6, 'Product quality is good.', NULL, 5, 10);

CREATE TABLE if not exists Writes_Order_Feedback(OrderFeedback_ID int references Order_Feedback(OrderFeedback_ID),Customer_ID int references Customer(Customer_ID),Order_ID int references Orders(Order_ID),Primary Key(OrderFeedback_ID,Customer_ID,Order_ID));
INSERT INTO Writes_Order_Feedback (OrderFeedback_ID, Customer_ID, Order_ID)
VALUES
(1, 2, 1),
(2, 4, 2),
(3, 9, 4),
(4, 10, 5),
(5, 14, 7),
(6, 20, 10);