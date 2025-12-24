# 27_SQL_Concepts - Quick Start Guide

Master SQL Fundamentals in 10 Minutes!

---

## What is SQL?

SQL (Structured Query Language) is the standard language for:
- **Querying** data from databases
- **Inserting** new records
- **Updating** existing records
- **Deleting** records
- **Creating** and managing tables

---

## 5-Minute Quick Start

### Basic Query Structure

```sql
SELECT columns
FROM table_name
WHERE conditions
ORDER BY column
LIMIT number;
```

### Example

```sql
SELECT name, salary
FROM employees
WHERE salary > 75000
ORDER BY salary DESC
LIMIT 5;
```

---

## Most Important Concepts

### 1. SELECT (Querying)
```sql
-- Get all columns
SELECT * FROM employees;

-- Get specific columns
SELECT name, salary FROM employees;

-- Get unique values
SELECT DISTINCT department FROM employees;
```

### 2. WHERE (Filtering)
```sql
-- Simple condition
WHERE salary > 50000

-- Multiple conditions
WHERE salary > 50000 AND department = 'Sales'

-- List of values
WHERE department IN ('Sales', 'Engineering')

-- Range
WHERE salary BETWEEN 50000 AND 100000
```

### 3. JOIN (Combining Tables)
```sql
-- INNER JOIN (matching only)
SELECT e.name, d.name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.id;

-- LEFT JOIN (all from left)
SELECT e.name, d.name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.id;
```

### 4. GROUP BY (Aggregating)
```sql
SELECT 
    department,
    COUNT(*) as count,
    AVG(salary) as avg_salary
FROM employees
GROUP BY department;
```

### 5. ORDER BY (Sorting)
```sql
-- Ascending (default)
ORDER BY salary ASC;

-- Descending
ORDER BY salary DESC;

-- Multiple columns
ORDER BY department ASC, salary DESC;
```

---

## Quick Cheat Sheet

### Aggregate Functions
```sql
COUNT(*)        -- Count rows
SUM(column)     -- Sum values
AVG(column)     -- Average
MIN(column)     -- Minimum
MAX(column)     -- Maximum
```

### Common Filters
```sql
=       -- Equal
>       -- Greater than
<       -- Less than
>=      -- Greater or equal
<=      -- Less or equal
!=      -- Not equal
LIKE    -- Pattern matching
IN      -- In list
BETWEEN -- In range
```

### Join Types
```sql
INNER JOIN  -- Matching records only
LEFT JOIN   -- All from left table
RIGHT JOIN  -- All from right table
FULL JOIN   -- All from both
CROSS JOIN  -- All combinations
```

---

## Step-by-Step Learning Path

### Step 1: Basic Queries (5 min)
```sql
-- Create a table
CREATE TABLE products (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10, 2)
);

-- Insert data
INSERT INTO products VALUES (1, 'Laptop', 999.99);

-- Query data
SELECT * FROM products;
```

### Step 2: Filtering (3 min)
```sql
-- Find expensive products
SELECT name, price FROM products
WHERE price > 100;

-- Find in range
SELECT * FROM products
WHERE price BETWEEN 50 AND 500;
```

### Step 3: Joining Tables (4 min)
```sql
-- Connect two tables
SELECT c.name, o.order_date
FROM customers c
JOIN orders o ON c.id = o.customer_id;
```

### Step 4: Aggregating (3 min)
```sql
-- Group and summarize
SELECT 
    category,
    COUNT(*) as count,
    AVG(price) as avg_price
FROM products
GROUP BY category;
```

### Step 5: Complex Queries (5 min)
```sql
-- Combine multiple techniques
SELECT 
    c.name,
    COUNT(o.id) as orders,
    SUM(o.amount) as total_spent
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.amount > 100
GROUP BY c.id
ORDER BY total_spent DESC;
```

---

## Real-World Example: Customer Analysis

```sql
-- Find top 10 customers by spending
SELECT 
    c.name,
    COUNT(o.id) as order_count,
    SUM(o.amount) as total_spent,
    AVG(o.amount) as avg_order
FROM customers c
JOIN orders o ON c.id = o.customer_id
WHERE o.date > '2024-01-01'
GROUP BY c.id
HAVING SUM(o.amount) > 500
ORDER BY total_spent DESC
LIMIT 10;
```

---

## Common Mistakes to Avoid

### ❌ Wrong
```sql
-- Selecting ungrouped columns
SELECT name, COUNT(*) FROM orders GROUP BY dept;
-- name should be in GROUP BY!
```

### ✓ Correct
```sql
SELECT dept, COUNT(*) FROM orders GROUP BY dept;
```

### ❌ Wrong
```sql
-- NULL handling
SELECT * FROM users WHERE email = NULL;
-- Should use IS NULL!
```

### ✓ Correct
```sql
SELECT * FROM users WHERE email IS NULL;
```

---

## Practice Exercises

### Exercise 1: Basic Query
```sql
-- Find all employees in the 'Sales' department
-- Expected: List of sales employees
```

### Exercise 2: Filtering
```sql
-- Find products with price between $100-$500
-- Expected: Products in that price range
```

### Exercise 3: Aggregation
```sql
-- Count orders by customer
-- Expected: Customer names with order counts
```

### Exercise 4: Join
```sql
-- Show customer name and their order dates
-- Expected: Paired customer-order data
```

### Exercise 5: Complex
```sql
-- Find customers who spent more than average
-- Expected: Customers above average spending
```

---

## Tools to Practice

| Tool | Use | Pros |
|------|-----|------|
| SQLite | Local/Testing | Free, built-in, simple |
| MySQL | Web apps | Popular, fast |
| PostgreSQL | Enterprise | Powerful, reliable |
| Online Editors | Learning | No installation |

---

## 30-Second Summary

SQL lets you:
1. **GET** data: SELECT FROM WHERE
2. **CHANGE** data: INSERT UPDATE DELETE
3. **COMBINE** tables: JOIN
4. **SUMMARIZE** data: GROUP BY, COUNT, SUM
5. **SORT** results: ORDER BY, LIMIT

---

## Next Steps

1. **Start with Notebook 250** for fundamentals
2. **Practice basic SELECT queries** on your own data
3. **Move to Notebook 251** when comfortable with basics
4. **Build complexity gradually** through notebooks
5. **Apply to real data** in your projects

---

## Common Patterns

### Find Top N
```sql
SELECT * FROM sales
ORDER BY revenue DESC
LIMIT 10;
```

### Find Duplicates
```sql
SELECT email, COUNT(*)
FROM users
GROUP BY email
HAVING COUNT(*) > 1;
```

### Running Total
```sql
SELECT amount,
       SUM(amount) OVER (ORDER BY date) as running_total
FROM sales;
```

### Percentage of Total
```sql
SELECT category,
       revenue,
       100.0 * revenue / SUM(revenue) OVER () as pct
FROM sales;
```

### Most Recent Per Group
```sql
SELECT * FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY date DESC)
    FROM orders
) WHERE row_number = 1;
```

---

## Quick Wins

### Get Started in 10 Minutes
- Learn SELECT, WHERE, ORDER BY
- Write your first query
- Feel the power of SQL!

### Master in 1 Hour
- Learn all join types
- Practice with real data
- Write complex queries

### Become Proficient in 5 Hours
- Complete all 6 notebooks
- Practice on real datasets
- Understand optimization

---

## Resources

- [Notebook 250](./250_SQL_Fundamentals.ipynb) - Fundamentals
- [Notebook 251](./251_SQL_Joins.ipynb) - Joins
- [Notebook 252](./252_SQL_Aggregations_And_GroupBy.ipynb) - Aggregations
- [Notebook 253](./253_Advanced_SQL_Concepts.ipynb) - Advanced
- [Notebook 254](./254_Python_SQL_Integration.ipynb) - Python Integration
- [Notebook 255](./255_Real_World_SQL_Applications.ipynb) - Real-World Apps

---

## Key Takeaway

**SQL is the bridge between raw data and insights.**

Master these 6 notebooks and you'll be able to:
- Query any relational database
- Extract business insights
- Analyze data efficiently
- Optimize database performance

Ready? Start with [Notebook 250](./250_SQL_Fundamentals.ipynb)!

---

**Time to Proficiency**: 2-3 hours  
**Difficulty**: Beginner-friendly  
**No Prerequisites Needed**: Start now!
