# 26_Process_And_Threads Documentation

## Module Overview

This module provides comprehensive coverage of concurrent and parallel programming in Python, essential for building high-performance applications.

### Key Concepts

**Concurrency vs Parallelism**
- **Concurrency**: Multiple tasks interleaved on single core
- **Parallelism**: Multiple tasks executing on multiple cores simultaneously

**Threading**: Use for I/O-bound operations (network, file I/O)
- Single process, multiple threads
- Shared memory space
- Limited by Global Interpreter Lock (GIL)
- Lower overhead

**Multiprocessing**: Use for CPU-bound operations (calculations, data processing)
- Multiple processes with separate memory
- True parallelism
- No GIL limitation
- Higher overhead

### Learning Path

1. **Foundations** (Notebook 244): Core concepts, GIL, threading vs multiprocessing
2. **Threading** (Notebook 245): Practical thread implementation, synchronization
3. **Multiprocessing** (Notebook 246): Process creation, IPC, shared memory
4. **Advanced Executors** (Notebook 247): ThreadPoolExecutor, ProcessPoolExecutor
5. **Web Scraping** (Notebook 248): Real-world threading use case
6. **Factorial Processing** (Notebook 249): Real-world multiprocessing use case

## Quick Reference

### When to Use Threading
- Web scraping
- API calls
- File I/O operations
- Database queries
- Network requests

### When to Use Multiprocessing
- CPU-intensive calculations
- Data processing
- Image processing
- Machine learning tasks
- Simulations

## Common Patterns

### Thread-Safe Shared Data
```python
import threading
data = []
lock = threading.Lock()

with lock:
    data.append(item)  # Thread-safe operation
```

### Process Pool for CPU Tasks
```python
from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor(max_workers=4) as executor:
    results = executor.map(cpu_function, data)
```

### Thread Pool for I/O Tasks
```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(io_function, urls)
```

## Performance Tips

1. **Worker Count**
   - Threading: 5-10 workers for I/O
   - Multiprocessing: number of CPU cores

2. **GIL Impact**
   - Threading doesn't help CPU-bound tasks
   - Use multiprocessing for CPU parallelism
   - Use threading for I/O concurrency

3. **Overhead Considerations**
   - Process creation is expensive
   - Use pools to reuse processes
   - Threading has lower overhead

## Best Practices

✓ **Always Set Timeouts**
```python
result = future.result(timeout=10)
```

✓ **Handle Exceptions**
```python
try:
    result = future.result()
except Exception as e:
    print(f"Task failed: {e}")
```

✓ **Use Context Managers**
```python
with ThreadPoolExecutor() as executor:
    # Automatically cleanup
    pass
```

✗ **Avoid**
- Creating unbounded number of threads
- Ignoring timeouts (infinite hangs)
- Sharing mutable objects across processes without synchronization
- Not handling exceptions in threads

## File Structure

```
26_Process_And_Threads/
├── 244_What_is_Process_And_Threads.ipynb
├── 245_MultiThreading_Practical_Implementation.ipynb
├── 246_Multiprocessing_With_Python.ipynb
├── 247_Thread_Pool_Executor_And_Process_Pool.ipynb
├── 248_Webscraping_Usecases_With_Multithread.ipynb
├── 249_Factorial_Usecase_With_MultiProcessing.ipynb
├── README.md (this file)
├── INDEX.md
├── SUMMARY.md
├── QUICKSTART.md
└── process_utils.py (optional utilities)
```

## Related Resources

- [Python Threading Module](https://docs.python.org/3/library/threading.html)
- [Python Multiprocessing Module](https://docs.python.org/3/library/multiprocessing.html)
- [Concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html)
- [Global Interpreter Lock (GIL)](https://wiki.python.org/moin/GlobalInterpreterLock)

## Troubleshooting

**Deadlock Issues**
- Ensure locks are always released
- Use context managers for automatic cleanup
- Avoid holding multiple locks

**Race Conditions**
- Use locks for shared data access
- Use queues for thread-safe communication
- Synchronize access properly

**Performance Problems**
- Check worker count (too many = overhead)
- Profile to identify bottlenecks
- Consider async instead of threads for I/O

## Integration with Logging

Combine with 25_Logging_Concepts for comprehensive monitoring:
```python
import logging
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

with ThreadPoolExecutor() as executor:
    futures = [executor.submit(task, item) for item in items]
    for future in futures:
        try:
            result = future.result()
            logger.info(f"Task completed: {result}")
        except Exception as e:
            logger.error(f"Task failed: {e}")
```

---

**Estimated Completion Time**: 45-60 minutes (all 6 notebooks)  
**Difficulty Level**: Intermediate to Advanced  
**Prerequisites**: Basic Python, understanding of synchronization primitives
