"""
Warehouse Schema Metadata
"""

WAREHOUSE_SCHEMA = """
DATABASE: InsightIQ Data Warehouse

TABLE: dim_product
- product_key
- product_id
- product_name
- category
- subcategory
- color
- standard_cost
- list_price

TABLE: dim_customer
- customer_key
- customer_id
- customer_name
- customer_type
- city
- state
- country

TABLE: dim_date
- date_key
- full_date
- day
- month
- month_name
- quarter
- year
- week
- day_of_week
- is_weekend

TABLE: dim_territory
- territory_key
- territory_id
- region
- country_region_code
- continent

TABLE: fact_sales
- sales_key
- sales_order_id
- sales_order_detail_id
- product_key
- customer_key
- date_key
- territory_key
- order_qty
- unit_price
- unit_price_discount
- line_total

RELATIONSHIPS

fact_sales.product_key -> dim_product.product_key
fact_sales.customer_key -> dim_customer.customer_key
fact_sales.date_key -> dim_date.date_key
fact_sales.territory_key -> dim_territory.territory_key
"""