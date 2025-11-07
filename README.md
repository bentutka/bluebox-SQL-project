# BlueBox Data Management System
University of Arkansas — ISYS / Data Management Final Project  
Team Members: Kaitlyn Le, Ruth Walters, Ben Tutka  

---

## Project Overview
BlueBox is a fictional nationwide DVD and video game rental company with over 100,000 customers.  
This project aimed to design, implement, and demonstrate a complete data management system for BlueBox, including a functioning backend database, SQL queries, data pipelines, and a Python-based reporting interface.

The system provides management with data-driven insights into:
- Customer demographics and behavior  
- Rental and inventory performance  
- Vendor utilization and product trends  

---

## Core Objectives
- Design a relational database supporting multiple operational areas  
- Create a data dictionary, conceptual model, and ERD to define schema relationships  
- Generate and import synthetic data using Python (Faker, NumPy)  
- Implement SQL queries for marketing, inventory, and vendor analysis  
- Build a reporting interface in Python to generate customizable management reports  
- Provide a user manual and presentation to illustrate system functionality  

---

## System Architecture

### Database Design
- Database Platform: Microsoft SQL Server  
- Tools Used: Microsoft Visual Studio Integration Services (SSIS), Python (pyodbc), Excel  
- Core Entities:  
  CUSTOMER, INVENTORY, MOVIES, GAMES, ORDERS, VENDORS, EMPLOYEES, PAYMENT_METHOD, RENT, RENTAL_INVENTORY, ZIP, GENRE, TYPE, and supporting bridge tables (MOVIE_GENRE, GAME_TYPE, CAST, etc.)

- Key Relationships:  
  - CUSTOMER ↔ RENT (via customer ID)  
  - INVENTORY ↔ MOVIES / GAMES  
  - RENTAL_INVENTORY links INVENTORY to KIOSK  
  - ORDERS link EMPLOYEES, VENDORS, and INVENTORY  

The database enforces referential integrity through primary and foreign key constraints and maintains data consistency with cleanup scripts such as `FixRentalInventory.sql`.

---

## Data Generation and Integration
Data was synthetically generated using:
- Python Faker library for random names, addresses, phone numbers, and dates  
- NumPy random generators for numeric and categorical distributions  
- CSV exports imported via Visual Studio Integration Services (SSIS) into SQL Server  

The project includes:
- `13_FakeDataGeneration.ipynb` — data generation script  
- `15_ZipCodes.csv` — real US ZIP data (cleaned of duplicates)  

---

## SQL Scripts
### Schema and Setup
- `Final Table Creation.sql` — creates all tables and constraints  
- `FixRentalInventory.sql` — repairs FK mismatches and ensures referential integrity  

### Analysis Queries
- `Marketing Queries.sql` — demographic breakdowns, genre and game popularity reports  
- `Inventory Queries.sql` — identifies top movies, games, studios, and cast members  
- `Vendors-Queries.sql` — top vendors and most rented items by supplier  

All queries are optimized for aggregation and comparative reporting across demographic and inventory dimensions.

---

## Application Interface
### Non-Functional Prototype v2
Implemented in Python (`management_reporting.py`, `NonfunctionalInterface_v2.py`) using pyodbc, pandas, and matplotlib.

Three core management views:
1. Marketing Management View — customer demographics and product preferences  
2. Inventory Management View — rental activity by product and studio  
3. Vendor Management View — vendor performance and category trends  

Reports are exported in Markdown format (.md) with visualizations such as pie charts and bar charts.

---

## User Manual
See `10_UserManual.pdf` or `Group7-User-Manual.docx` for detailed walkthroughs on:
- Navigating the CLI interface  
- Generating general or custom reports  
- Selecting parameters (product type, region, gender, age range)  
- Exiting or switching views  

Each report provides actionable insights and supporting visualizations to guide marketing and inventory decisions.

---

## Challenges and Lessons Learned
- Maintaining referential integrity across multiple bridge tables  
- Integrating Visual Studio SSIS with Python back-end queries  
- Late-stage pivot from GUI to CLI interface due to compatibility issues  

Outcome: a functioning prototype capable of generating dynamic SQL-based reports from a normalized database.

---

## Future Improvements
- Migrate from text-based CLI to a visual dashboard (web or Tkinter/Streamlit UI)  
- Expand to include employee and sales reporting  
- Add more user-customizable filters and data visualizations  
- Deploy to a cloud database environment for multi-user access  

---

## Technologies Used
| Category | Tools / Languages |
|-----------|------------------|
| Database | Microsoft SQL Server, T-SQL |
| ETL / Integration | Microsoft Visual Studio SSIS |
| Programming / Reporting | Python (pyodbc, pandas, matplotlib, tabulate) |
| Visualization | matplotlib, seaborn |
| Data Generation | Faker, NumPy |
| Documentation / Presentation | Microsoft Word, Excel, PowerPoint |

---

## Conclusion
The BlueBox Data Management System demonstrates a complete implementation of a modern database environment—from schema design and data generation to reporting and visualization.  
The project showcases skills in SQL design, ETL integration, Python programming, and data analysis, serving as a full academic capstone deliverable.
