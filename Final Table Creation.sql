-- Drop Tables
DROP TABLE RENT;
DROP TABLE RENTAL_INVENTORY;
DROP TABLE KIOSK;
DROP TABLE CAST;
DROP TABLE GAME_TYPE;
DROP TABLE MOVIE_GENRE;
DROP TABLE PAYMENT_METHOD;
DROP TABLE ORDERS;
DROP TABLE MOVIES;
DROP TABLE GAMES;
DROP TABLE CUSTOMER;
DROP TABLE CAST_MEMBERS;
DROP TABLE GENRE;
DROP TABLE TYPE;
DROP TABLE EMPLOYEES;
DROP TABLE VENDORS;
DROP TABLE INVENTORY;
DROP TABLE HOST;
DROP TABLE MEMBERSHIP;
DROP TABLE ZIP;

-- Create ZIP Table
CREATE TABLE ZIP (
    region varchar(15) NOT NULL,
    zip_code varchar(6) NOT NULL PRIMARY KEY,
    city varchar(20) NOT NULL,
    state varchar(3) NOT NULL
)

-- Create MEMBERSHIP table
CREATE TABLE MEMBERSHIP (
    membership_status_id int NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    membership_status_desc varchar(50) NOT NULL,
    discount float NOT NULL,
    late_fee float NOT NULL
)

-- Create HOST table
CREATE TABLE HOST (
    host_id int NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    host_name varchar(50) NOT NULL,
    host_st_address varchar(100) NOT NULL,
    host_email varchar(100) NOT NULL,
    host_phone varchar(30) NOT NULL,
    host_zip_code varchar(10) NOT NULL
)

-- Create INVENTORY table 
CREATE TABLE INVENTORY (
    inventory_id int NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    title varchar(50) NOT NULL,
    release_year varchar(20) NOT NULL,
    movie bit NOT NULL
)

-- Create VENDORS table 
CREATE TABLE VENDORS (
    vendor_id int NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    vendor_name varchar(50) NOT NULL,
    vendor_st_address varchar(50) NOT NULL,
    vendor_zip_code varchar(10) NOT NULL,
    vendor_phone varchar(30) NOT NULL,
    vendor_email varchar(100) NOT NULL
)

-- Create EMPLOYEES table
CREATE TABLE EMPLOYEES (
    employee_id int NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    employee_fname varchar(50) NOT NULL,
    employee_lname varchar(50) NOT NULL,
    employee_gender varchar(10) NOT NULL,
    employee_st_address varchar(100) NOT NULL,
    employee_zip_code char(5) NOT NULL,
    employee_mobile varchar(30) NULL,
    employee_email varchar(100) NOT NULL,
    employee_auth_code int NULL,
    employee_title varchar(25) NOT NULL
)

-- Create GENRE TABLE table
CREATE TABLE GENRE (
    genre_id int NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    genre_desc varchar(50) NOT NULL
)

-- Create CAST_MEMBERS table
CREATE TABLE CAST_MEMBERS (
    cast_id int NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    cast_fname varchar(50) NOT NULL,
    cast_lname varchar(50) NOT NULL
)

-- Create CUSTOMER table
CREATE TABLE CUSTOMER (
    customer_id int NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    customer_fname varchar(50) NOT NULL,
    customer_lname varchar(50) NOT NULL,
    customer_gender varchar(10) NOT NULL,
    customer_st_address varchar(100) NOT NULL,
    customer_zip_code varchar(10) NOT NULL,
    customer_mobile_phone varchar(30) NOT NULL,
    customer_email varchar(100) NOT NULL,
    membership_status_id int NOT NULL,
    customer_date_created datetime NOT NULL,
    customer_birthday datetime NOT NULL,
    customer_age_range varchar(20) NOT NULL,
    FOREIGN KEY (membership_status_id) REFERENCES MEMBERSHIP(membership_status_id)
)

-- Create GAMES table
CREATE TABLE GAMES (
    inventory_id int NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    game_publisher varchar(50) NOT NULL,
    game_platform varchar(50) NOT NULL,
    game_esrb_rating varchar(5) NOT NULL,
    FOREIGN KEY (inventory_id) REFERENCES INVENTORY(inventory_id)
)

-- Create TYPE table
CREATE TABLE TYPE (
    type_id int NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    type_desc varchar(50) NOT NULL
)

-- Create MOVIES table
CREATE TABLE MOVIES (
    inventory_id int NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    movie_runtime int NOT NULL,
    movie_mpaa_rating varchar(5) NOT NULL,
    movie_studio varchar(50) NOT NULL,
    movie_plot varchar(255) NOT NULL,
    bluray_available Bit NOT NULL,
    FOREIGN KEY (inventory_id) REFERENCES INVENTORY(inventory_id)
)

-- Create ORDERS table
CREATE TABLE ORDERS (
    order_id int NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    total_price float NOT NULL,
    vendor_id int NOT NULL,
    employee_id int NOT NULL,
    item_quantity int NOT NULL,
    item_price float NOT NULL,
    inventory_id int NOT NULL,
    FOREIGN KEY (vendor_id) REFERENCES VENDORS(vendor_id),
    FOREIGN KEY (employee_id) REFERENCES EMPLOYEES(employee_id),
    FOREIGN KEY (inventory_id) REFERENCES INVENTORY(inventory_id)
)

-- Create PAYMENT_METHOD table
CREATE TABLE PAYMENT_METHOD (
    payment_id int NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    customer_id int NOT NULL,
    card_provider varchar(6) NOT NULL,
    card_number char(16) NOT NULL,
    exp_date datetime NOT NULL,
    security_code char(3) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES CUSTOMER(customer_id)
)

-- Create MOVIE GENRE table [BRIDGE]
CREATE TABLE MOVIE_GENRE (
    inventory_id int NOT NULL,
    genre_id int NOT NULL,
    CONSTRAINT pk_movie_genre PRIMARY KEY (inventory_id, genre_id),
    FOREIGN KEY (inventory_id) REFERENCES INVENTORY(inventory_id),
	FOREIGN KEY (genre_id) REFERENCES GENRE(genre_id)
)

-- Create GAME TYPE table [BRIDGE]
    CREATE TABLE GAME_TYPE (
    inventory_id int NOT NULL,
    type_id int NOT NULL,
    CONSTRAINT pk_game_type PRIMARY KEY (inventory_id, type_id),
    FOREIGN KEY (inventory_id) REFERENCES INVENTORY(inventory_id),
	FOREIGN KEY (type_id) REFERENCES TYPE(type_id)
)

-- Create CAST table [BRIDGE]
CREATE TABLE CAST (
    cast_id int NOT NULL,
    inventory_id int NOT NULL,
    CONSTRAINT pk_cast PRIMARY KEY (cast_id, inventory_id),
	FOREIGN KEY (cast_id) REFERENCES CAST_MEMBERS(cast_id),
    FOREIGN KEY (inventory_id) REFERENCES INVENTORY(inventory_id)
)

-- Create KIOSK table [BRIDGE]
CREATE TABLE KIOSK (
    kiosk_id int NOT NULL IDENTITY(1, 1) PRIMARY KEY,
    kiosk_st_address varchar(100) NOT NULL,
    kiosk_zip_code varchar(10) NOT NULL,
    host_id int NOT NULL,
	FOREIGN KEY (host_id) REFERENCES HOST(host_id)
)

-- Create RENTAL INVENTORY table [BRIDGE]
CREATE TABLE RENTAL_INVENTORY (
    quantity int NOT NULL,
    rental_rate float NOT NULL,
    inventory_id int NOT NULL,
    kiosk_id int NOT NULL,
    CONSTRAINT pk_rental_inventory PRIMARY KEY (inventory_id, kiosk_id),
    FOREIGN KEY (inventory_id) REFERENCES INVENTORY(inventory_id),
	FOREIGN KEY (kiosk_id) REFERENCES KIOSK(kiosk_id)
)

-- Create RENT table [BRIDGE]
CREATE TABLE RENT (
    inventory_id int NOT NULL,
    customer_id int NOT NULL,
    payment_id int NOT NULL,
    rental_period int NOT NULL,
    rental_start_date datetime NOT NULL,
    rental_end_date datetime NOT NULL,
    price_charged float NOT NULL,
    overdue bit NULL,
    overdue_duration int NULL,
    late_fee_total float NULL,
    CONSTRAINT pk_rent PRIMARY KEY (inventory_id, customer_id, payment_id),
    FOREIGN KEY (inventory_id) REFERENCES INVENTORY(inventory_id),
	FOREIGN KEY (customer_id) REFERENCES CUSTOMER(customer_id),
	FOREIGN KEY (payment_id) REFERENCES PAYMENT_METHOD(payment_id)
)