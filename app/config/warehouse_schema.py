"""
Warehouse Schema Metadata

Provides schema information to the AI SQL Agent.
"""

WAREHOUSE_SCHEMA = """
DATABASE: InsightIQ Data Warehouse

=========================================
TABLE: dim_product
=========================================

ProductKey
ProductID
ProductName
Category
Subcategory
Color
StandardCost
ListPrice


=========================================
TABLE: dim_customer
=========================================

CustomerKey
CustomerID
CustomerName
CustomerType
City
State
Country


=========================================
TABLE: dim_date
=========================================

DateKey
FullDate
Day
Month
MonthName
Quarter
Year
Week
DayOfWeek
IsWeekend


=========================================
TABLE: dim_territory
=========================================

TerritoryKey
TerritoryID
Region
CountryRegionCode
Continent


=========================================
TABLE: fact_sales
=========================================

SalesKey
SalesOrderID
SalesOrderDetailID

ProductKey
CustomerKey
DateKey
TerritoryKey

OrderQty
UnitPrice
UnitPriceDiscount
LineTotal


=========================================
RELATIONSHIPS
=========================================

fact_sales.ProductKey
    ->
dim_product.ProductKey

fact_sales.CustomerKey
    ->
dim_customer.CustomerKey

fact_sales.DateKey
    ->
dim_date.DateKey

fact_sales.TerritoryKey
    ->
dim_territory.TerritoryKey
"""