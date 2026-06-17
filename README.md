# Fast-Food Management System (Backend)
🖥️ **Looking for the Frontend?** Check out the Vanilla JS Single Page Application repository [here](https://github.com/YourUsername/fast-food-system-frontend).
---

Welcome to the backend repository of the **Fast-Food Management System** (`fast-food-system`). This project is a robust, enterprise-grade, and decoupled restaurant management and food delivery platform. It is built using **Django REST Framework (DRF)** and **MySQL**, adhering to advanced database normalization practices (following Elmasri and Navathe's relational database principles), secure custom authentication mechanisms, and strict business logic constraints.

---

## 📌 Project Overview

This backend serves as the core engine for the platform, handling complex workflows such as:
- **Hierarchical Employee Management:** Tracking restaurant admins, chefs, delivery staff, and waiters with appropriate system permissions.
- **Advanced Order Lifecycle:** Managing order transitions from `Pending` ➔ `Preparing` ➔ `Delivering` ➔ `Delivered` or `Cancelled`.
- **Verified Purchase Review System:** A bulletproof, database-enforced, and serializer-validated feedback loop ensuring only authentic customers can review completed orders exactly once.
- **Custom JWT Security:** Stateless session management bypassed from default Django user models to interact with a custom, high-performance `USERS` entity.

---

## 🛠️ Tech Stack & Infrastructure

- **Backend Framework:** Django 5.x & Django REST Framework (DRF)
- **Database Server:** MySQL 8.0+
- **Authentication Protocol:** Custom JSON Web Tokens (JWT)
- **Architecture Style:** RESTful API with Decoupled Frontend/Backend (SPA Compatible)
- **Environment:** Designed and optimized for Linux (Ubuntu) environments.

---

## 🗄️ Database Architecture & Schema Design

The relational database schema is highly normalized (up to 3NF) to minimize redundancy and guarantee transactional integrity. It implements sub-type clusters for employees (`STAFF` and `RESTAURANT_ADMIN` inherit from `EMPLOYEE` via strict primary key mapping/cascading).

### Entity Relationship Summary
1. **`USERS` ➔ `ADDRESS`:** One-to-Many. A user can store multiple addresses.
2. **`RESTAURANT` ➔ `MENU_ITEM`:** One-to-Many. Items are bound to specific restaurant catalogs.
3. **`EMPLOYEE` Sub-types:** - `STAFF` (Delivery, Chef, etc.) shares a 1:1 relationship with `EMPLOYEE` via `Staff_ID`.
   - `RESTAURANT_ADMIN` shares a 1:1 relationship with `EMPLOYEE` via `Admin_ID`.
4. **`ORDERS` ➔ `REVIEW`:** **Strict One-to-One (`OneToOneField`)**. Implements the *Verified Purchase* pattern where an order can map to exactly one review transcript (Exclusive Arcs alternative).

### Complete DDL Schema (`schema.sql`)
```sql
CREATE DATABASE IF NOT EXISTS fastfood_db;
USE fastfood_db;

CREATE TABLE USERS (
    User_ID           INT          AUTO_INCREMENT PRIMARY KEY,
    Name              VARCHAR(100) NOT NULL,
    Email             VARCHAR(100) UNIQUE,
    Phone             VARCHAR(20)  UNIQUE NOT NULL,
    Password          VARCHAR(255) NOT NULL,
    Registration_Date DATETIME     DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE RESTAURANT (
    Restaurant_ID INT           AUTO_INCREMENT PRIMARY KEY,
    Name          VARCHAR(100)  NOT NULL,
    Address       VARCHAR(255),
    Phone         VARCHAR(20),
    Rating_Avg    DECIMAL(2,1)  DEFAULT 0,
    Opening_Hour  TIME,
    Closing_Hour  TIME,
    Delivery_Fee  DECIMAL(10,2) DEFAULT 0,
    Is_Active     BOOLEAN       DEFAULT TRUE,
    Total_Orders  INT           DEFAULT 0,
    Total_Revenue DECIMAL(12,2) DEFAULT 0
);

CREATE TABLE CATEGORY (
    Category_ID INT          AUTO_INCREMENT PRIMARY KEY,
    Name        VARCHAR(100) NOT NULL
);

CREATE TABLE ADDRESS (
    Address_ID  INT          AUTO_INCREMENT PRIMARY KEY,
    User_ID     INT          NOT NULL,
    City        VARCHAR(100),
    Street      VARCHAR(255),
    Zipcode     VARCHAR(20),
    Is_Verified BOOLEAN      DEFAULT FALSE,
    FOREIGN KEY (User_ID) REFERENCES USERS(User_ID) ON DELETE CASCADE
);

CREATE TABLE MENU_ITEM (
    Item_ID       INT           AUTO_INCREMENT PRIMARY KEY,
    Restaurant_ID INT           NOT NULL,
    Category_ID   INT           NOT NULL,
    Name          VARCHAR(100)  NOT NULL,
    Description   TEXT,
    Price         DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (Restaurant_ID) REFERENCES RESTAURANT(Restaurant_ID),
    FOREIGN KEY (Category_ID)   REFERENCES CATEGORY(Category_ID)
);

CREATE TABLE EMPLOYEE (
    Employee_ID   INT           AUTO_INCREMENT PRIMARY KEY,
    SSN           VARCHAR(20)   UNIQUE NOT NULL,
    Name          VARCHAR(100)  NOT NULL,
    Sex           VARCHAR(10),
    Salary        DECIMAL(10,2),
    Employed_Date DATE,
    Restaurant_ID INT           NOT NULL,
    User_ID       INT           NULL,
    FOREIGN KEY (Restaurant_ID) REFERENCES RESTAURANT(Restaurant_ID),
    FOREIGN KEY (User_ID)       REFERENCES USERS(User_ID)
);

CREATE TABLE RESTAURANT_ADMIN (
    Admin_ID      INT          PRIMARY KEY,
    Permission    VARCHAR(255),
    Restaurant_ID INT,
    FOREIGN KEY (Admin_ID)      REFERENCES EMPLOYEE(Employee_ID) ON DELETE CASCADE,
    FOREIGN KEY (Restaurant_ID) REFERENCES RESTAURANT(Restaurant_ID)
);

CREATE TABLE STAFF (
    Staff_ID        INT PRIMARY KEY,
    Avg_Rating      DECIMAL(2,1) DEFAULT 0,
    Role            ENUM('DeliveryPerson','Chef','Waiter','Cashier') NOT NULL,
    Approval_Status ENUM('Pending','Approved','Rejected') DEFAULT 'Pending',
    FOREIGN KEY (Staff_ID) REFERENCES EMPLOYEE(Employee_ID) ON DELETE CASCADE
);

CREATE TABLE ORDERS (
    Order_ID           INT           AUTO_INCREMENT PRIMARY KEY,
    User_ID            INT           NOT NULL,
    Address_ID         INT,
    Delivery_Staff_ID  INT           NULL,
    Restaurant_ID      INT           NULL,
    Status             VARCHAR(50)   NOT NULL,
    Preparation_Status ENUM('Pending','Preparing','Ready') DEFAULT 'Pending',
    Total_Price        DECIMAL(10,2) NOT NULL,
    Estimated_Delivery DATETIME,
    Created_At         DATETIME      DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (User_ID)           REFERENCES USERS(User_ID),
    FOREIGN KEY (Address_ID)        REFERENCES ADDRESS(Address_ID),
    FOREIGN KEY (Delivery_Staff_ID) REFERENCES STAFF(Staff_ID),
    FOREIGN KEY (Restaurant_ID)     REFERENCES RESTAURANT(Restaurant_ID)
);

CREATE TABLE ORDER_ITEM (
    OrderItem_ID INT           AUTO_INCREMENT PRIMARY KEY,
    Order_ID     INT           NOT NULL,
    Item_ID      INT           NOT NULL,
    Quantity     INT           NOT NULL CHECK (Quantity > 0),
    Unit_Price   DECIMAL(10,2),
    FOREIGN KEY (Order_ID) REFERENCES ORDERS(Order_ID) ON DELETE CASCADE,
    FOREIGN KEY (Item_ID)  REFERENCES MENU_ITEM(Item_ID)
);

CREATE TABLE PAYMENT (
    Payment_ID     INT           AUTO_INCREMENT PRIMARY KEY,
    Order_ID       INT           NOT NULL UNIQUE,
    Method         VARCHAR(50)   NOT NULL,
    Transaction_ID VARCHAR(100),
    Paid_At        DATETIME,
    Amount         DECIMAL(10,2),
    Status         ENUM('Pending','Paid','Failed','Refunded') DEFAULT 'Pending',
    FOREIGN KEY (Order_ID) REFERENCES ORDERS(Order_ID)
);

CREATE TABLE REVIEW (
    Review_ID   INT AUTO_INCREMENT PRIMARY KEY,
    Order_ID    INT NOT NULL UNIQUE,
    Rating      TINYINT NOT NULL CHECK (Rating BETWEEN 1 AND 5),
    Comment     TEXT NULL,
    Created_At  DATETIME DEFAULT CURRENT_TIMESTAMP NULL,
    CONSTRAINT fk_review_order FOREIGN KEY (Order_ID) REFERENCES ORDERS(Order_ID)
);
```
## 🔐 Security & Authentication Engine

We eschew default Django Session-based and default Auth User frameworks to avoid unneeded relational overhead. Authentication utilizes a lightweight, highly secure stateless JWT engine.

- **`CustomJWTAuthentication`:** Intercepts incoming HTTP requests, decodes the HTTP `Authorization: Bearer <token>` header, validates token expiration signatures, and populates `request.user` with an active instance of our custom `USERS` model.
- **`Permission Classes`:** Core views are locked behind `IsValidUser`. This custom guard prevents anonymous manipulation, validating token integrity on every request.

---

## 📡 API Documentation & Endpoints

### 1. Order History
Retrieves the logged-in user's order records, appended with dynamic real-time review matrices allowing front-end SPAs to dynamically toggle feedback interfaces.

- **Endpoint:** `GET /api/orders/`
- **Headers:** `Authorization: Bearer <JWT_TOKEN>`
- **Response Example (JSON):**
```json
[
  {
    "id": 17,
    "total_price": "2040000.00",
    "status": "Delivered",
    "created_at": "2026-06-14T09:20:40Z",
    "has_review": true,
    "review_data": {
      "rating": 5,
      "comment": "Superb quality! Hot, crisp, and extremely fast shipping.",
      "created_at": "2026-06-14T10:30:00Z"
    },
    "items": [
      {
        "item_name": "Special Burger",
        "quantity": 2,
        "unit_price": "250000.00"
      }
    ],
    "user_name": "Arta Danesh",
    "address_str": "Azadi St"
  }
]
```

### 2. Submit Review
Enables customer feedback submission governed by strict algorithmic validity layers.

- **Endpoint:** `POST /api/reviews/`
- **Headers:** `Authorization: Bearer <JWT_TOKEN>`
- **Payload Example (JSON):**
```json
{
  "order": 17,
  "rating": 5,
  "comment": "Absolutely incredible service."
}
```

### 3. Restaurants & Menus
Endpoints for browsing the food catalog.
Restaurant details retrieval:
```json
{
    "restaurant": {
        "id": 3,
        "name": "Crispy Chicken",
        "rating": 4.1,
        "delivery_fee": 20000.0,
        "address": "Karaj",
        "phone": "02633333333",
        "opening_hour": "10:00:00",
        "closing_hour": "22:00:00",
        "total_orders": 85
    },
    "categories": [
        "Fried Chicken",
        "Burger",
        "Appetizer"
    ],
    "items": [
        {
            "id": 3,
            "name": "Fried Chicken",
            "description": "3 pieces of chicken",
            "price": "290000.00",
            "category": "Fried Chicken"
        },
        {
            "id": 11,
            "name": "steak",
            "description": "Beef steak",
            "price": "1010000.00",
            "category": "Burger"
        },
        {
            "id": 12,
            "name": "french fries",
            "description": "french fries with hot cheese",
            "price": "220000.00",
            "category": "Appetizer"
        }
    ]
}
```

### 4. Profile Detail
```json
{
    "id": 11,
    "name": "arta",
    "email": "artadnsh@gmail.com",
    "phone": "09136966335",
    "registration_date": null
}
```

## 🧠 Business Logic & Serializer Validation Layers

The `ReviewSerializer` acts as an automated firewall inside the system. Before a row is written into `REVIEW`, the `validate()` lifecycle enforces three ironclad rules:

1. **Ownership Constraint:** `order.user != request.user` triggers an immediate validation fault. Users are prevented from commenting on orders belonging to other accounts.
2. **Lifecycle Constraint:** `order.status != 'Delivered'` blocks submissions. Orders that are `Pending`, `Preparing`, or `Delivering` cannot receive peer reviews.
3. **Idempotency Constraint:** A One-to-One unique constraint query runs globally. If `Review.objects.filter(order=order).exists()` is evaluated to true, the request is terminated with a descriptive error message preventing multiple submissions.

---

## ⚙️ Installation & Local Setup Guide

Follow these steps to spin up the backend environment locally on an Ubuntu/Linux machine:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/ArtADnsh/fast-food-system-backend.git
   cd fast-food-system-backend
   ```
   
2. **Setup the Virtual Environment:**
 * **Linux / macOS:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
 * **Windows (Command Prompt / CMD):**
   ```bash
   python -m venv venv
   venv\Scripts\activate.bat
   ```
 * **Windows (PowerShell):**
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
   
3. **Install Core Dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   
4. **Initialize Database Configurations:**
   Ensure you have MySQL installed and running on your system.
   
   **A. Install MySQL (if not already installed):**
   * **Linux (Ubuntu):**
     ```bash
     sudo apt update && sudo apt install mysql-server
     ```
   * **macOS:**
     ```bash
     brew install mysql && brew services start mysql
     ```
   * **Windows:** Download and run the official [MySQL Installer MSI](https://dev.mysql.com/downloads/installer/).
     
   **B. Create Database and Import Schema:**
   Execute the database setup commands based on your OS/Shell:
   
   * **Linux / macOS / Windows (CMD):**
     ```Bash
     mysql -u your_user -p -e "CREATE DATABASE fastfood_db;"
     mysql -u your_user -p fastfood_db < schema.sql
     ```
   * **Windows (PowerShell):**
     ```Bash
     mysql -u your_user -p -e "CREATE DATABASE fastfood_db;"
     Get-Content schema.sql | mysql -u your_user -p fastfood_db
     ```
     
5. **Run the Development Server:**
   ```bash
   python manage.py runserver   
   ```

## 👨‍💻 Contributor & Author
Developed by **Arta Danesh**.

For architectural design patterns or database restructuring suggestions, please open a formal thread inside the Issues tab.
