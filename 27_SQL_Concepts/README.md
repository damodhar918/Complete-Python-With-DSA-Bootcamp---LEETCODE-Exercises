# 27_SQL_Concepts Documentation

## Module Overview

This module provides comprehensive coverage of SQL (Structured Query Language), one of the most important skills for data professionals, database administrators, and backend developers.

### Key Concepts

**SQL (Structured Query Language)**
- Declarative language for database management
- Standardized across most databases (MySQL, PostgreSQL, SQL Server, Oracle)
- Used for querying, inserting, updating, and managing data

**Database Fundamentals**
- Relational databases with tables, rows, and columns
- Primary keys for unique identification
- Foreign keys for relationships between tables
- Constraints for data integrity

### Learning Path

1. **Fundamentals** (Notebook 250): DDL, DML, basic SELECT, WHERE, ORDER BY
2. **Joins** (Notebook 251): INNER, LEFT, RIGHT, FULL, CROSS, SELF joins
3. **Aggregations** (Notebook 252): GROUP BY, aggregate functions, HAVING
4. **Advanced Concepts** (Notebook 253): Subqueries, CTEs, Views, Transactions, Indexes
5. **Python Integration** (Notebook 254): SQLite, MySQL, PostgreSQL, Pandas
6. **Real-World Applications** (Notebook 255): E-commerce analytics, business queries

## Quick Reference

### DDL (Data Definition)
```sql
-- Create table
CREATE TABLE table_name (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL
);

-- Modify structure
ALTER TABLE table_name ADD COLUMN new_col TEXT;

-- Delete table
DROP TABLE table_name;
```

### DML (Data Manipulation)
```sql
-- Insert
INSERT INTO table_name (col1, col2) VALUES (val1, val2);

-- Update
UPDATE table_name SET col1 = val1 WHERE condition;

-- Delete
DELETE FROM table_name WHERE condition;
```

### DQL (Data Query)
```sql
-- Select with conditions
SELECT col1, col2 FROM table_name WHERE condition;

-- Join tables
SELECT * FROM table1 JOIN table2 ON table1.id = table2.table1_id;

-- Group and aggregate
SELECT col1, COUNT(*) FROM table_name GROUP BY col1;
```

## Common Patterns

### Customer Lifetime Value
```sql
SELECT 
    customer_id,
    COUNT(order_id) as order_count,
    SUM(order_amount) as total_spent
FROM orders
GROUP BY customer_id
ORDER BY total_spent DESC;
```

### Product Performance
```sql
SELECT 
    p.name,
    COUNT(oi.item_id) as times_ordered,
    SUM(oi.quantity) as units_sold,
    SUM(oi.quantity * oi.price) as revenue
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id
ORDER BY revenue DESC;
```

### RFM Segmentation
```sql
SELECT 
    customer_id,
    COUNT(order_id) as frequency,
    SUM(amount) as monetary,
    CASE 
        WHEN SUM(amount) > 500 THEN 'VIP'
        WHEN SUM(amount) > 300 THEN 'Loyal'
        ELSE 'Standard'
    END as segment
FROM orders
GROUP BY customer_id;
```

## Performance Tips

1. **Indexing Strategy**
   - Index foreign keys
   - Index frequently searched columns
   - Avoid indexes on low-cardinality columns
   - Monitor index usage

2. **Query Optimization**
   - Use EXPLAIN to analyze queries
   - Filter early (WHERE clause)
   - Aggregate at database, not application
   - Use JOINs instead of multiple queries

3. **Database Design**
   - Normalize to 3NF (Third Normal Form)
   - Use appropriate data types
   - Set constraints for data quality
   - Plan for growth

## File Structure

```
27_SQL_Concepts/
├── 250_SQL_Fundamentals.ipynb
├── 251_SQL_Joins.ipynb
├── 252_SQL_Aggregations_And_GroupBy.ipynb
├── 253_Advanced_SQL_Concepts.ipynb
├── 254_Python_SQL_Integration.ipynb
├── 255_Real_World_SQL_Applications.ipynb
├── README.md (this file)
├── INDEX.md
├── SUMMARY.md
├── QUICKSTART.md
└── sql_utils.py (optional utilities)
```

## Database Systems Comparison

| Database | Best For | Python Driver | Complexity |
|----------|----------|---------------|-----------|
| SQLite | Local, simple apps | sqlite3 (built-in) | Easy |
| MySQL | Web apps, shared hosting | mysql.connector | Medium |
| PostgreSQL | Enterprise, advanced features | psycopg2 | Medium |
| Oracle | Large enterprises | cx_Oracle | Hard |
| MongoDB | Document stores, NoSQL | pymongo | Medium |

## Related Modules

- **25_Logging_Concepts**: Log database operations
- **26_Process_And_Threads**: Concurrent database access
- Use together for production-grade applications

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Slow queries | Missing indexes | Create indexes on filter columns |
| N+1 queries | Multiple roundtrips | Use JOINs instead of loops |
| Deadlocks | Circular locks | Use transactions properly |
| Data inconsistency | No constraints | Add PRIMARY KEY, FOREIGN KEY |
| Out of memory | Large result sets | Use pagination or LIMIT |

## Integration with Python

```python
import sqlite3
import pandas as pd

# Connect
conn = sqlite3.connect('database.db')

# Query to DataFrame
df = pd.read_sql_query("SELECT * FROM table", conn)

# DataFrame to SQL
df.to_sql('new_table', conn)

# Close
conn.close()
```

## Best Practices

✓ **DO**
- Use parameterized queries to prevent SQL injection
- Set appropriate data types
- Create foreign key relationships
- Use transactions for data integrity
- Index properly for performance
- Document your schema

✗ **DON'T**
- Build SQL strings with concatenation
- Use SELECT * in production
- Skip constraints for "flexibility"
- Create too many indexes (write performance)
- Ignore NULL handling
- Store large binary data in databases

## Resources

- [SQL Tutorial](https://www.w3schools.com/sql/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

---

**Estimated Completion Time**: 60-75 minutes (all 6 notebooks)  
**Difficulty Level**: Beginner to Intermediate  
**Prerequisites**: Basic Python knowledge, understanding of data structures
