# 27_SQL_Concepts - Complete Index

## Table of Contents

### Notebooks
- [250. SQL Fundamentals](#notebook-250)
- [251. SQL Joins](#notebook-251)
- [252. SQL Aggregations and Group By](#notebook-252)
- [253. Advanced SQL Concepts](#notebook-253)
- [254. Python SQL Integration](#notebook-254)
- [255. Real-World SQL Applications](#notebook-255)

---

## Notebook 250: SQL Fundamentals

**Duration**: 12 minutes  
**Concepts**: DDL, DML, CREATE, INSERT, SELECT, WHERE, ORDER BY, LIMIT

### Key Sections
1. Introduction to SQL
2. SQLite Setup
3. Data Definition Language (DDL) - CREATE
4. Data Manipulation Language (DML) - INSERT
5. Data Query Language (DQL) - SELECT
6. Filtering and Conditions (WHERE)
7. Sorting and Limiting (ORDER BY, LIMIT)
8. Data Manipulation - UPDATE and DELETE
9. Summary

### Code Examples
```sql
-- Create table
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT,
    salary REAL
);

-- Insert data
INSERT INTO employees VALUES (1, 'Alice', 'Sales', 75000);

-- Query with conditions
SELECT name, salary FROM employees 
WHERE salary > 75000 
ORDER BY salary DESC;
```

### Key Takeaways
- DDL: CREATE, ALTER, DROP for structure
- DML: INSERT, UPDATE, DELETE for data
- DQL: SELECT for querying
- WHERE clauses filter data
- ORDER BY sorts, LIMIT restricts results

---

## Notebook 251: SQL Joins

**Duration**: 12 minutes  
**Concepts**: INNER, LEFT, RIGHT, FULL, CROSS, SELF joins

### Key Sections
1. Setup Database with Multiple Tables
2. INNER JOIN
3. LEFT JOIN (LEFT OUTER JOIN)
4. RIGHT JOIN (RIGHT OUTER JOIN)
5. FULL OUTER JOIN
6. CROSS JOIN (Cartesian Product)
7. Self-Join
8. Join Comparison Summary

### Code Examples
```sql
-- INNER JOIN (matching records only)
SELECT s.name, c.course_name
FROM students s
INNER JOIN courses c ON s.course_id = c.course_id;

-- LEFT JOIN (all from left + matching right)
SELECT s.name, c.course_name
FROM students s
LEFT JOIN courses c ON s.course_id = c.course_id;

-- Self-join (hierarchy)
SELECT e.name, m.name as manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.emp_id;
```

### Key Takeaways
- INNER JOIN: Only matching records
- LEFT JOIN: All left table records
- RIGHT JOIN: All right table records
- FULL JOIN: All from both tables
- CROSS JOIN: All combinations
- Self-join: Join table with itself

---

## Notebook 252: SQL Aggregations and Group By

**Duration**: 10 minutes  
**Concepts**: COUNT, SUM, AVG, MIN, MAX, GROUP BY, HAVING

### Key Sections
1. Setup Sample Data
2. Basic Aggregate Functions
3. GROUP BY Clause
4. HAVING Clause
5. Complex Aggregations
6. Aggregate Functions Reference

### Code Examples
```sql
-- Group by with aggregates
SELECT 
    category,
    COUNT(*) as products,
    SUM(price) as total_value,
    AVG(price) as avg_price
FROM products
GROUP BY category;

-- HAVING filters groups
SELECT 
    category,
    SUM(sales) as total
FROM products
GROUP BY category
HAVING SUM(sales) > 1000;

-- Multiple grouping columns
SELECT category, brand, COUNT(*), SUM(quantity)
FROM products
GROUP BY category, brand;
```

### Key Takeaways
- COUNT(*): Count rows
- SUM(): Sum values
- AVG(): Average values
- MIN/MAX(): Min/max values
- GROUP BY: Aggregate by column
- HAVING: Filter groups (not rows)

---

## Notebook 253: Advanced SQL Concepts

**Duration**: 12 minutes  
**Concepts**: Subqueries, CTEs, Transactions, Views, Indexes

### Key Sections
1. Subqueries
2. Common Table Expressions (CTE) - WITH clause
3. UNION Operations
4. Views
5. Transactions - ACID Properties
6. Indexes for Performance
7. Advanced Concepts Summary

### Code Examples
```sql
-- Subquery
SELECT name, salary FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- CTE (Common Table Expression)
WITH high_earners AS (
    SELECT name, salary FROM employees WHERE salary > 80000
)
SELECT department, COUNT(*) FROM high_earners
GROUP BY department;

-- View
CREATE VIEW sales_summary AS
SELECT product, SUM(amount) as total
FROM sales
GROUP BY product;

-- Transaction
BEGIN TRANSACTION;
UPDATE employees SET salary = salary * 1.05;
COMMIT;
```

### Key Takeaways
- Subqueries: Queries within queries
- CTEs: Named temporary result sets
- Views: Saved queries
- Transactions: ACID-compliant operations
- Indexes: Speed up queries
- EXPLAIN: Analyze query performance

---

## Notebook 254: Python SQL Integration

**Duration**: 10 minutes  
**Concepts**: SQLite, Pandas, Context Managers, Error Handling

### Key Sections
1. SQLite with Python
2. Using Pandas with SQL
3. Connection Management with Context Manager
4. Error Handling
5. Advanced Query Features
6. Database Drivers Summary

### Code Examples
```python
import sqlite3
import pandas as pd

# Create connection
conn = sqlite3.connect('database.db')

# Query to DataFrame
df = pd.read_sql_query("SELECT * FROM table", conn)

# DataFrame to SQL
df.to_sql('new_table', conn, if_exists='replace')

# Context manager
with sqlite3.connect('database.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM table")
    results = cursor.fetchall()

# Error handling
try:
    cursor.execute("INSERT INTO table VALUES (?)", (value,))
    conn.commit()
except sqlite3.IntegrityError as e:
    conn.rollback()
    print(f"Error: {e}")
```

### Key Takeaways
- sqlite3: Built-in, simple
- Pandas integration: Easy DataFrames
- Context managers: Automatic cleanup
- Error handling: Catch integrity/SQL errors
- Parameterized queries: Prevent SQL injection
- Connection pooling: For multiple connections

---

## Notebook 255: Real-World SQL Applications

**Duration**: 14 minutes  
**Concepts**: E-commerce database, Analytics, RFM, Business queries

### Key Sections
1. E-Commerce Database Setup
2. Customer Analytics (CLV)
3. Product Analytics
4. Order Analytics
5. Complex Business Queries
6. Database Optimization
7. Key Takeaways

### Code Examples
```sql
-- Customer Lifetime Value
SELECT customer_id, name,
       COUNT(order_id) as orders,
       SUM(amount) as total_spent
FROM orders
GROUP BY customer_id
ORDER BY total_spent DESC;

-- RFM Segmentation
SELECT customer_id,
       COUNT(*) as frequency,
       SUM(amount) as monetary,
       CASE WHEN SUM(amount) > 500 THEN 'VIP'
            WHEN SUM(amount) > 300 THEN 'Loyal'
            ELSE 'Standard' END as segment
FROM orders
GROUP BY customer_id;

-- Product Affinity
SELECT p1.name, p2.name, COUNT(*) as together
FROM order_items oi1
JOIN order_items oi2 ON oi1.order_id = oi2.order_id
JOIN products p1 ON oi1.product_id = p1.id
JOIN products p2 ON oi2.product_id = p2.id
WHERE oi1.product_id < oi2.product_id
GROUP BY oi1.product_id, oi2.product_id;
```

### Key Takeaways
- E-commerce schema design
- CLV and customer segmentation
- Product performance analysis
- Cross-sell opportunities
- Index strategy for performance
- EXPLAIN for query optimization

---

## Quick Decision Trees

### Which JOIN?
```
Do you need:
├─ Only matching records? → INNER JOIN
├─ All from left table? → LEFT JOIN
├─ All from right table? → RIGHT JOIN
├─ All from both tables? → FULL OUTER JOIN
├─ All combinations? → CROSS JOIN
└─ Same table relationships? → SELF JOIN
```

### Which Aggregate?
```
Do you want:
├─ Count of records? → COUNT(*)
├─ Sum of values? → SUM(column)
├─ Average value? → AVG(column)
├─ Min or max? → MIN/MAX(column)
└─ Multiple summaries? → GROUP BY
```

### Which Optimization?
```
Performance problem?
├─ Slow WHERE filters? → Add index
├─ Slow JOINs? → Index foreign keys
├─ Large result sets? → Use LIMIT, pagination
├─ Complex queries? → Create views, CTEs
└─ Repeated queries? → Materialized views, caching
```

---

## Common Patterns

| Pattern | Use Case | Example |
|---------|----------|---------|
| DISTINCT | Remove duplicates | SELECT DISTINCT country FROM customers |
| CASE WHEN | Conditional values | CASE WHEN age > 18 THEN 'Adult' ... |
| COALESCE | Handle NULLs | COALESCE(phone, 'N/A') |
| CAST | Type conversion | CAST(date_str AS DATE) |
| LIKE | Pattern matching | WHERE name LIKE 'A%' |
| IN | Multiple values | WHERE status IN ('active', 'pending') |
| BETWEEN | Range check | WHERE salary BETWEEN 50000 AND 100000 |
| EXISTS | Subquery check | WHERE EXISTS (SELECT 1 FROM orders...) |

---

## Performance Benchmarks

| Operation | Records | Time | Notes |
|-----------|---------|------|-------|
| SELECT all | 1M | 50ms | Without index |
| WHERE filter | 1M | 100ms | With index: 10ms |
| GROUP BY | 100K | 200ms | Requires sorting |
| JOIN | 1M + 100K | 300ms | Depends on index |
| INSERT batch | 10K | 50ms | With transaction |
| UPDATE batch | 100K | 200ms | Without index |

---

## Integration Examples

### With Logging (25_Logging_Concepts)
```python
import logging
import sqlite3

logger = logging.getLogger(__name__)

try:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO table VALUES (?)", (data,))
    conn.commit()
    logger.info("Data inserted successfully")
except Exception as e:
    logger.error(f"Database error: {e}")
    conn.rollback()
```

### With Threading (26_Process_And_Threads)
```python
from concurrent.futures import ThreadPoolExecutor
import sqlite3

def query_db(sql):
    conn = sqlite3.connect('database.db')
    return pd.read_sql_query(sql, conn)

with ThreadPoolExecutor(max_workers=5) as executor:
    queries = [query1, query2, query3]
    results = executor.map(query_db, queries)
```

---

## Progress Tracking

- [x] 250: Fundamentals
- [x] 251: Joins
- [x] 252: Aggregations
- [x] 253: Advanced
- [x] 254: Python Integration
- [x] 255: Real-World Applications

---

**Module Status**: Complete  
**Total Notebooks**: 6  
**Total Duration**: ~60-75 minutes  
**Last Updated**: 2024
