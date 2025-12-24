# 26_Process_And_Threads - Complete Index

## Table of Contents

### Core Concepts
- [What is Process And Threads](#notebook-244)
- [MultiThreading Practical Implementation](#notebook-245)
- [Multiprocessing With Python](#notebook-246)
- [Thread Pool Executor And Process Pool](#notebook-247)
- [Webscraping Usecases With Multithread](#notebook-248)
- [Factorial Usecase With Multi Processing](#notebook-249)

---

## Notebook 244: What is Process And Threads

**Duration**: 14 minutes  
**Concepts**: Fundamentals, GIL, Threading vs Multiprocessing, Race Conditions

### Key Sections
1. Introduction to Processes and Threads
2. Sequential vs Concurrent Execution
3. Process Class in Python
4. Thread Class in Python
5. Understanding the Global Interpreter Lock (GIL)
6. CPU-Bound vs I/O-Bound Tasks
7. Race Conditions and Thread Safety
8. Synchronization Primitives Overview
9. Summary and Comparison

### Code Examples
```python
# Basic thread creation
import threading

def task():
    print("Running in thread")

t = threading.Thread(target=task)
t.start()
t.join()

# Basic process creation
import multiprocessing

def task():
    print("Running in process")

p = multiprocessing.Process(target=task)
p.start()
p.join()
```

### Key Takeaways
- Threads share memory; processes have isolated memory
- GIL prevents true parallel execution of Python code in threads
- Threading excels at I/O-bound tasks
- Multiprocessing excels at CPU-bound tasks
- Synchronization primitives prevent race conditions

---

## Notebook 245: MultiThreading Practical Implementation

**Duration**: 12 minutes  
**Concepts**: Thread Classes, Locks, Producer-Consumer, Events, Daemon Threads

### Key Sections
1. Custom Thread Class
2. Thread-Safe Shared Data
3. Producer-Consumer Pattern
4. Event-Based Synchronization
5. Thread-Local Storage
6. Daemon Threads
7. Condition Variables
8. Performance Comparison
9. Practical Patterns

### Code Examples
```python
# Thread-safe counter with Lock
import threading

class ThreadSafeCounter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()
    
    def increment(self):
        with self.lock:
            self.value += 1

# Producer-Consumer pattern
from queue import Queue

q = Queue()
# Producer thread puts items
# Consumer thread gets items
```

### Key Takeaways
- Use locks for protecting shared mutable state
- Queues provide thread-safe communication
- Daemon threads don't prevent program exit
- Condition variables enable complex synchronization
- Thread-local storage isolates data per thread

---

## Notebook 246: Multiprocessing With Python

**Duration**: 7 minutes  
**Concepts**: Process Creation, IPC, Shared Memory, Process Pool

### Key Sections
1. Process Basics
2. Inter-Process Communication (IPC)
3. Shared Memory and Values
4. CPU-Bound Task Performance
5. Process Pool and map()
6. Custom Initializer Pattern
7. Multiprocessing vs Threading Comparison

### Code Examples
```python
from multiprocessing import Process, Queue, Pool

# Communication via Queue
def producer(q):
    q.put("data")

def consumer(q):
    data = q.get()

# Process pool for CPU tasks
with Pool(processes=4) as pool:
    results = pool.map(cpu_function, data)
```

### Key Takeaways
- Multiprocessing enables true parallelism
- Use Queue for process communication
- Process creation has overhead; use pools
- Process pool is optimal for batch CPU tasks
- Memory is not shared between processes

---

## Notebook 247: Thread Pool Executor And Process Pool

**Duration**: 8 minutes  
**Concepts**: ThreadPoolExecutor, ProcessPoolExecutor, Futures, Advanced Patterns

### Key Sections
1. ThreadPoolExecutor Basics
2. ThreadPoolExecutor with submit()
3. ProcessPoolExecutor
4. Error Handling with Executors
5. Timeout Handling
6. Executor Comparison
7. Real-World Batch Processing

### Code Examples
```python
from concurrent.futures import ThreadPoolExecutor, as_completed

with ThreadPoolExecutor(max_workers=5) as executor:
    # Method 1: map
    results = executor.map(function, items)
    
    # Method 2: submit with futures
    futures = [executor.submit(function, item) for item in items]
    for future in as_completed(futures):
        try:
            result = future.result(timeout=10)
        except Exception as e:
            print(f"Error: {e}")
```

### Key Takeaways
- Executors simplify thread/process pool management
- `map()` returns results in order
- `submit()` returns futures immediately
- `as_completed()` processes results as they finish
- Always set timeouts to prevent hangs

---

## Notebook 248: Webscraping Usecases With Multithread

**Duration**: 10 minutes  
**Concepts**: Real-World Web Scraping, Rate Limiting, Retry Logic, Error Handling

### Key Sections
1. Simple Multi-Threaded Scraper
2. Scraper with Queue
3. Scraper with Rate Limiting
4. Scraper with Retry Logic
5. Best Practices for Web Scraping

### Code Examples
```python
from concurrent.futures import ThreadPoolExecutor
import requests

def fetch_page(url):
    response = requests.get(url, timeout=5)
    return response.text

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(fetch_page, url) for url in urls]
    results = [f.result() for f in futures]

# With rate limiting
class RateLimitedScraper:
    def __init__(self, requests_per_second=2):
        self.min_interval = 1.0 / requests_per_second
        self.last_request_time = 0
        self.lock = threading.Lock()
    
    def _wait_for_rate_limit(self):
        with self.lock:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.min_interval:
                time.sleep(self.min_interval - elapsed)
            self.last_request_time = time.time()
```

### Key Takeaways
- Threading excellent for I/O-bound web scraping
- Implement rate limiting to respect servers
- Use timeouts on all requests
- Implement exponential backoff for retries
- Respect robots.txt and ToS

---

## Notebook 249: Factorial Usecase With MultiProcessing

**Duration**: Flexible  
**Concepts**: CPU-Bound Computation, Multiprocessing Performance, Batch Processing

### Key Sections
1. Factorial Calculation Basics
2. Sequential Processing
3. Multiprocessing with Process Pool
4. Multiprocessing with Futures
5. Batch Processing Factorials
6. Error Handling in Multiprocessing
7. Performance Analysis

### Code Examples
```python
import multiprocessing
import math

def calculate_factorial(n):
    return {'number': n, 'factorial': math.factorial(n)}

if __name__ == '__main__':
    numbers = list(range(1, 21))
    
    with multiprocessing.Pool(processes=4) as pool:
        results = pool.map(calculate_factorial, numbers)
    
    for result in results:
        print(f"{result['number']}! = {result['factorial']}")
```

### Key Takeaways
- Multiprocessing provides significant speedup for CPU tasks
- Overhead breakeven at ~100K+ operations
- Use Process pools for batch operations
- Error handling crucial for reliability
- Consider memory when processing large numbers

---

## Quick Decision Matrix

| Task Type | I/O | CPU |
|-----------|-----|-----|
| **Threading** | ✓ Excellent | ✗ Poor |
| **Multiprocessing** | ✗ Overhead | ✓ Excellent |
| **AsyncIO** | ✓ Excellent | ✗ Not Suitable |

## Common Performance Expectations

- **Threading**: 2-3x speedup for I/O-bound (5-10 workers)
- **Multiprocessing**: 3-4x speedup per core for CPU-bound
- **Web Scraping**: 5-10x speedup typical with threading
- **Factorial Computation**: Linear speedup with cores

## Integration Examples

### With Logging (from 25_Logging_Concepts)
```python
import logging
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

with ThreadPoolExecutor() as executor:
    futures = [executor.submit(task, item) for item in items]
    for future in futures:
        try:
            result = future.result()
            logger.info(f"Completed: {result}")
        except Exception as e:
            logger.error(f"Failed: {e}")
```

## Progress Tracking

- [x] 244: Foundations
- [x] 245: Threading
- [x] 246: Multiprocessing  
- [x] 247: Executors
- [x] 248: Web Scraping
- [x] 249: Factorial Processing

---

**Module Status**: Complete  
**Last Updated**: 2024  
**Total Duration**: ~45-60 minutes
