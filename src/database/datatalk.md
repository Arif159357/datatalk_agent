# Northwind Database Schema Documentation

This document provides a comprehensive overview of all data tables in the application based on the Northwind relational model. Each table includes detailed descriptions of its purpose, fields, and relational mapping.

## Core Personnel & HR Management

### Employees
*Purpose*: Central staff management table storing employee profiles, contact information, and the organizational reporting hierarchy.

| Field | Type | Description |
|-------|------|-------------|
| employee_id | Int (Primary Key) | Unique identifier for the employee |
| last_name | String | Employee surname |
| first_name | String | Employee given name |
| title | String? | Professional job title |
| title_of_courtesy | String? | Prefix (e.g., Mr., Ms., Dr.) |
| birth_date | DateTime? | Employee date of birth |
| hire_date | DateTime? | Date the employee joined the company |
| address | String? | Physical home address |
| city / region | String? | City and state/province of residence |
| postal_code | String? | Zip or postal code |
| country | String? | Country of residence |
| home_phone | String? | Personal contact number |
| extension | String? | Internal phone extension |
| photo | Binary/Blob? | Employee profile image |
| notes | Text? | Internal HR notes or biography |
| reports_to | Int? | Foreign key (Self-referencing) to the employee's manager |
| photo_path | String? | File system path to the employee photo |

*Relationships*: 
- Self-referencing (Managers to Subordinates)
- Has many Orders
- Has many Employee_Territories

### Employee_Territories
*Purpose*: Junction table mapping employees to the specific geographic sales territories they are responsible for.

| Field | Type | Description |
|-------|------|-------------|
| employee_id | Int (Primary Key) | Foreign key reference to Employees |
| territory_id | String (Primary Key) | Foreign key reference to Territories |

*Relationships*: 
- Belongs to Employees
- Belongs to Territories

---

## Product & Supply Chain Management

### Products
*Purpose*: Core product catalog storing item specifications, current inventory levels, and procurement triggers.

| Field | Type | Description |
|-------|------|-------------|
| product_id | Int (Primary Key) | Unique identifier for the product |
| product_name | String | Commercial name of the item |
| supplier_id | Int? | Foreign key reference to Suppliers |
| category_id | Int? | Foreign key reference to Categories |
| quantity_per_unit | String? | Detailed packaging description (e.g., "24 - 12 oz bottles") |
| unit_price | Decimal | Current list price per unit |
| units_in_stock | Int | Physical quantity currently in the warehouse |
| units_on_order | Int | Quantity currently pending in purchase orders |
| reorder_level | Int | Stock threshold that triggers a new purchase request |
| discontinued | Boolean | Flag indicating if the product is no longer active |

*Relationships*: 
- Belongs to Suppliers
- Belongs to Categories
- Has many Order_Details

### Categories
*Purpose*: High-level classification of products for catalog organization and reporting.

| Field | Type | Description |
|-------|------|-------------|
| category_id | Int (Primary Key) | Unique identifier for the category |
| category_name | String | Name of the grouping (e.g., Beverages, Grains) |
| description | Text? | Summary of product types within this category |
| picture | Binary/Blob? | Graphical icon representing the category |

*Relationships*: 
- Has many Products

### Suppliers
*Purpose*: External vendor management storing contact information for product sourcing.

| Field | Type | Description |
|-------|------|-------------|
| supplier_id | Int (Primary Key) | Unique identifier for the vendor |
| company_name | String | Registered business name of the supplier |
| contact_name | String? | Primary account representative |
| contact_title | String? | Job title of the contact person |
| address / city | String? | Physical street and city location |
| region / postal_code | String? | State/Province and Zip code |
| country | String? | Country of operation |
| phone / fax | String? | Contact numbers |
| homepage | Text? | Link to supplier's official website |

*Relationships*: 
- Has many Products

---

## Sales & Customer Management

### Customers

#### *Purpose*
The *Customers* table stores profile, contact, and geographic information for all business entities that purchase goods. It serves as the primary entity for CRM and accounts receivable tracking.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| customer_id | String | *Primary Key* | Unique 5-character identifier |
| company_name | String | *Required* | Name of the customer organization |
| contact_name | String? | | Name of the primary contact person |
| contact_title | String? | | Job title of the contact person |
| address | String? | | Billing/Main office address |
| city | String? | | City location |
| region | String? | | State, province, or region |
| postal_code | String? | | Zip or postal code |
| country | String? | | Country location |
| phone | String? | | Primary contact phone number |
| fax | String? | | Fax number |

*Relationships*: 
- Has many Orders
- Has many Customer_Customer_Demo

### Orders

#### *Purpose*
The *Orders* table tracks the header-level details of every transaction, including shipping logistics, responsible staff, and the chronological lifecycle of the order.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| order_id | Int | *Primary Key* | Unique sequential transaction ID |
| customer_id | String? | *Foreign Key* | Reference to the Customer placing the order |
| employee_id | Int? | *Foreign Key* | Reference to the Employee who sold the order |
| order_date | DateTime? | | Timestamp when the order was created |
| required_date | DateTime? | | Deadline requested by the customer |
| shipped_date | DateTime? | | Timestamp when the order left the warehouse |
| ship_via | Int? | *Foreign Key* | Reference to the Shipper/Carrier used |
| freight | Decimal | *Default: 0* | Shipping and handling fees charged |
| ship_name | String? | | Recipient name for delivery |
| ship_address | String? | | Destination street address |
| ship_city | String? | | Destination city |
| ship_region | String? | | Destination state/province |
| ship_postal_code | String? | | Destination Zip code |
| ship_country | String? | | Destination country |

*Relationships*: 
- Belongs to Customers
- Belongs to Employees
- Belongs to Shippers
- Has many Order_Details

### Order_Details
*Purpose*: Individual line items for every order, capturing the specific products, quantities, and pricing at the point of sale.

| Field | Type | Description |
|-------|------|-------------|
| order_id | Int (PK/FK) | Reference to the parent Order |
| product_id | Int (PK/FK) | Reference to the Product sold |
| unit_price | Decimal | Actual selling price (may differ from list price) |
| quantity | Int | Number of units purchased |
| discount | Float | Percentage discount applied to this line item |

*Relationships*: 
- Belongs to Orders
- Belongs to Products

---

## Logistics & Geography

### Shippers
*Purpose*: Management of third-party shipping carriers (e.g., Speedy Express).

| Field | Type | Description |
|-------|------|-------------|
| shipper_id | Int (Primary Key) | Unique carrier identifier |
| company_name | String | Name of the logistics provider |
| phone | String? | Carrier contact number |

*Relationships*: 
- Has many Orders

### Territories
*Purpose*: Specific geographic districts for sales tracking.

| Field | Type | Description |
|-------|------|-------------|
| territory_id | String (Primary Key) | Unique alphanumeric territory code |
| territory_description | String | Name of the territory |
| region_id | Int | Foreign key reference to Regions |

*Relationships*: 
- Belongs to Region
- Has many Employee_Territories

### Region
*Purpose*: Broad geographic classifications (e.g., North, South).

| Field | Type | Description |
|-------|------|-------------|
| region_id | Int (Primary Key) | Unique identifier for the region |
| region_description | String | Name of the region |

*Relationships*: 
- Has many Territories

---

## Marketing & Supplemental Data

### Customer_Demographics
*Purpose*: Definitions of customer segments for targeted marketing.

| Field | Type | Description |
|-------|------|-------------|
| customer_type_id | String (Primary Key) | Unique ID for the demographic segment |
| customer_desc | Text? | Detailed description of the segment |

*Relationships*: 
- Has many Customer_Customer_Demo

### Customer_Customer_Demo
*Purpose*: Junction table linking customers to multiple demographic classifications.

| Field | Type | Description |
|-------|------|-------------|
| customer_id | String (Primary Key) | Foreign key to Customers |
| customer_type_id | String (Primary Key) | Foreign key to Customer_Demographics |

*Relationships*: 
- Belongs to Customers
- Belongs to Customer_Demographics

### US_States
*Purpose*: Reference table for standardizing US state information and abbreviations.

| Field | Type | Description |
|-------|------|-------------|
| state_id | Int (Primary Key) | Unique numeric ID |
| state_name | String? | Full name of the state |
| state_abbr | String? | Two-letter state code |
| state_region | String? | Geographic US region (e.g., "Midwest") |