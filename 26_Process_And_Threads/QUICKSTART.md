# 26_Process_And_Threads - Quick Start Guide

Get up and running with concurrent programming in Python in 5 minutes!

## What You'll Learn

- **Threading**: For I/O operations (web scraping, API calls)
- **Multiprocessing**: For CPU operations (calculations, data processing)
- **Practical Patterns**: Real-world web scraping and computing examples

## 5-Minute Quick Start

### Threading Example (I/O-Bound)

```python
from concurrent.futures import ThreadPoolExecutor
import time

def fetch_data(url):
    """Simulates fetching from URL"""
    time.sleep(1)
    return f"Data from {url}"

# Use threading for I/O-bound tasks
urls = ['url1', 'url2', 'url3', 'url4', 'url5']

# Sequential (5 seconds)
start = time.time()
results = [fetch_data(url) for url in urls]
print(f"Sequential: {time.time() - start:.1f}s")

# Threading (1.5 seconds) - 3x faster!
start = time.time()
with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(fetch_data, urls))
print(f"Threading: {time.time() - start:.1f}s")
```

### Multiprocessing Example (CPU-Bound)

```python
from concurrent.futures import ProcessPoolExecutor
import time

def compute(n):
    """CPU-intensive calculation"""
    count = 0
    for i in range(n):
        count += i ** 2
    return count

numbers = [1000000, 1000000, 1000000, 1000000]

# Multiprocessing for CPU-bound tasks
with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(compute, numbers))
    print(f"Results: {len(results)} computations completed")
```

## Key Concepts in 1 Minute

| Concept | Use For | Speed | Overhead |
|---------|---------|-------|----------|
| **Sequential** | Small tasks | Slow | None |
| **Threading** | I/O operations | 5-10x faster | Low |
| **Multiprocessing** | CPU operations | 3-4x per core | High |

## Decision Tree

```
Task Type?
├─ I/O-bound (network, files)?
│  └─> Use THREADING ✓
│      (WebScraping, API calls, file I/O)
│
└─ CPU-bound (calculation, processing)?
   └─> Use MULTIPROCESSING ✓
       (Data crunching, ML, simulations)
```

## 10-Minute Learning Plan

1. **Understand the Problem** (1 min)
   - Is your task I/O-bound or CPU-bound?
   - How many cores/workers do you need?

2. **Choose Your Tool** (1 min)
   - I/O → Threading
   - CPU → Multiprocessing

3. **Implement Basic Version** (5 min)
   - Copy template below
   - Adjust worker count
   - Test with real data

4. **Add Error Handling** (2 min)
   - Try/except around results
   - Set timeouts
   - Log errors

5. **Measure Performance** (1 min)
   - Time sequential vs concurrent
   - Calculate speedup

## Templates

### Threading Template
```python
from concurrent.futures import ThreadPoolExecutor

def worker_function(item):
    """Your I/O operation here"""
    # Example: requests.get(item)
    return result

items = [...]  # Your data

with ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(worker_function, items)
    
    # Or with error handling:
    futures = [executor.submit(worker_function, item) for item in items]
    for future in futures:
        try:
            result = future.result(timeout=10)
            print(result)
        except Exception as e:
            print(f"Error: {e}")
```

### Multiprocessing Template
```python
from concurrent.futures import ProcessPoolExecutor

def worker_function(item):
    """Your CPU operation here"""
    # Example: expensive_calculation(item)
    return result

if __name__ == '__main__':  # Important!
    items = [...]  # Your data
    
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = executor.map(worker_function, items)
        for result in results:
            print(result)
```

## Common Mistakes to Avoid

### ❌ Threading for CPU-bound
```python
# WRONG - GIL prevents speedup
with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(heavy_computation, data)
```
✓ Use multiprocessing instead

### ❌ Missing timeout
```python
# WRONG - Can hang indefinitely
result = future.result()  # No timeout!
```
✓ Always set timeout
```python
result = future.result(timeout=10)
```

### ❌ Multiprocessing without if __name__ == '__main__'
```python
# WRONG - Causes infinite recursion on Windows
with ProcessPoolExecutor() as executor:
    results = executor.map(func, data)
```
✓ Wrap in main
```python
if __name__ == '__main__':
    with ProcessPoolExecutor() as executor:
        results = executor.map(func, data)
```

### ❌ Too many workers
```python
# WRONG - Too much overhead
with ThreadPoolExecutor(max_workers=1000) as executor:
    ...
```
✓ Reasonable number
- Threading: 5-10
- Multiprocessing: Number of CPU cores

## Real-World Scenario

**Problem**: Scrape 100 websites, takes ~2 seconds per site

### Sequential: 200 seconds ⏱️
```python
results = [requests.get(url) for url in urls]
```

### Threading: 20 seconds ⏱️ (10x faster!)
```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(requests.get, urls))
```

## Performance Tips

1. **Find the right worker count**
   - Threading: Start with 5, measure, adjust
   - Multiprocessing: Use `os.cpu_count()`

2. **Profile before optimizing**
   ```python
   import time
   start = time.time()
   # Your code here
   print(f"Time: {time.time() - start:.2f}s")
   ```

3. **Handle failures**
   - Set timeouts
   - Use try/except
   - Log errors
   - Implement retry logic

4. **Monitor resources**
   - Check memory usage
   - Watch CPU utilization
   - Count active workers

## Next Steps

1. **Run the notebooks** in this folder (244-249)
2. **Try the templates** with your own data
3. **Measure the improvements** in your application
4. **Combine with logging** (see 25_Logging_Concepts)
5. **Scale to production** with proper error handling

## Useful Links

- [Threading Module](https://docs.python.org/3/library/threading.html)
- [Multiprocessing Module](https://docs.python.org/3/library/multiprocessing.html)
- [Concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html)

## Quick Reference Card

### Threading
```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(function, items)
```
✓ I/O operations  
✓ Low overhead  
✗ CPU-bound (GIL)

### Multiprocessing
```python
from concurrent.futures import ProcessPoolExecutor

if __name__ == '__main__':
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = executor.map(function, items)
```
✓ CPU operations  
✓ True parallelism  
✗ Higher overhead

### With Error Handling
```python
from concurrent.futures import as_completed

with executor:
    futures = [executor.submit(func, item) for item in items]
    for future in as_completed(futures):
        try:
            result = future.result(timeout=10)
        except Exception as e:
            print(f"Error: {e}")
```

---

**Estimated Time to Proficiency**: 30-45 minutes  
**Complexity Level**: Beginner-friendly with advanced options  
**No Prerequisites**: Works with basic Python knowledge

Ready to learn? Start with [244_What_is_Process_And_Threads.ipynb](./244_What_is_Process_And_Threads.ipynb)
