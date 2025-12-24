# 25. Logging Concepts in Python

## Overview
This folder contains comprehensive coverage of Python logging concepts, from basic setup to production-ready implementations. Logging is essential for debugging, monitoring, and maintaining applications.

## Contents

### 1. [250_Logging_In_Python.ipynb](250_Logging_In_Python.ipynb) (15 minutes)
**Duration:** 15 minutes

Covers the fundamentals of logging in Python:
- **Introduction to Logging** - Why logging is important
- **Basic Logging Setup** - Simple logging configuration
- **Log Levels** - DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Handlers** - StreamHandler, FileHandler
- **Formatters** - Customizing log message format
- **Exception Logging** - Logging exceptions with traceback
- **Disabling/Enabling Loggers** - Controlling log output

**Key Takeaways:**
- Use logging instead of print() for production code
- Understand log levels and their use cases
- Configure handlers and formatters appropriately
- Include exception information when logging errors

### 2. [251_Logging_With_Multiple_Loggers.ipynb](251_Logging_With_Multiple_Loggers.ipynb) (5 minutes)
**Duration:** 5 minutes (Quick Reference)

Advanced logger configuration for complex applications:
- **Multiple Loggers Basics** - Creating separate loggers for different modules
- **Logger Hierarchy** - Understanding logger naming conventions
- **Different Log Levels for Different Modules** - Per-logger level configuration
- **Logger Propagation** - How child loggers propagate to parents
- **Module-Specific Loggers** - Best practice pattern
- **Efficient Logger Setup** - Utility classes for logger management

**Key Concepts:**
- Logger hierarchy with dot notation (e.g., `myapp.database.cache`)
- Each module should use `logging.getLogger(__name__)`
- Child loggers inherit from parent loggers
- Control propagation to avoid duplicate messages

### 3. [252_Logging_Real_World_Implementation.ipynb](252_Logging_Real_World_Implementation.ipynb)
**Duration:** Full practical guide

Real-world logging patterns for production applications:
- **Application Structure** - Centralized logging configuration
- **Module-Level Logging** - DatabaseManager example
- **API Service Logging** - Request/response tracking
- **Performance Monitoring** - Execution time logging decorator
- **Context Variables** - Adding request IDs to logs
- **Configuration File Based Logging** - Using dictConfig
- **Best Practices** - Production-ready patterns

**Real-World Examples Include:**
- RotatingFileHandler for log management
- Separate error log files
- Request ID tracking across logs
- Performance monitoring decorators
- Exception handling with full tracebacks

### 4. [253_Error_Handling_With_Logging.ipynb](253_Error_Handling_With_Logging.ipynb)
**Duration:** Complete error handling guide

Comprehensive error handling techniques with logging:
- **Basic Exception Logging** - exc_info and exception() methods
- **Custom Exception Classes** - Domain-specific exceptions
- **Error Context Management** - Preserving error information
- **Try-Except-Finally Patterns** - Resource cleanup with logging
- **Retry Logic** - Retry decorators with exponential backoff
- **Error Aggregation** - Tracking and reporting errors
- **Structured Error Logging** - JSON formatted logs
- **Error Recovery Patterns** - Fallback strategies
- **Error File Handlers** - Specialized file handlers for errors
- **Best Practices** - Do's and don'ts for error handling

**Key Features:**
- Custom exception hierarchies
- Error context preservation
- Automatic error aggregation
- Performance monitoring with error tracking
- Structured logging for log aggregation tools

## Additional Resources

### error_handler.py
Standalone Python module providing:
- Custom exception classes (DatabaseError, ValidationError, APIError)
- Error context management utilities
- Error aggregation and reporting
- Decorators for retry logic and performance monitoring
- Specialized file handlers for error logging
- Configuration utilities for error handler setup

**Usage:**
```python
from error_handler import ErrorHandlerConfig, retry_with_logging, log_performance

# Setup error handlers
ErrorHandlerConfig.setup_error_handlers('logs')

# Use decorators
@retry_with_logging(max_attempts=3)
def unstable_function():
    pass

@log_performance()
def monitored_function():
    pass
```

### Basic Logging (30 seconds)
```python
import logging

# Configure
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Use
logger = logging.getLogger(__name__)
logger.info("Application started")
```

### Multiple Modules (Best Practice)
```python
# In each module
import logging
logger = logging.getLogger(__name__)

# In main/config
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Production Setup
```python
import logging.handlers

logger = logging.getLogger('app')
handler = logging.handlers.RotatingFileHandler(
    'app.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
```

## Log Levels Reference

| Level | Value | Use Case |
|-------|-------|----------|
| DEBUG | 10 | Detailed diagnostic information |
| INFO | 20 | General informational messages |
| WARNING | 30 | Warning messages (default) |
| ERROR | 40 | Error conditions |
| CRITICAL | 50 | Critical errors, program may fail |

## Best Practices

1. ✅ **Use named loggers** - `logging.getLogger(__name__)`
2. ✅ **Centralize configuration** - One place for logging setup
3. ✅ **Include context** - Request IDs, user IDs, etc.
4. ✅ **Log at appropriate levels** - Don't overuse DEBUG or INFO
5. ✅ **Include exception info** - Use `exc_info=True`
6. ✅ **Rotate log files** - Prevent disk space issues
7. ✅ **Format for readability** - Include timestamps and function names
8. ✅ **Monitor performance** - Log slow operations
9. ✅ **Separate error logs** - Maintain separate error.log
10. ❌ **Never log sensitive data** - No passwords, tokens, or PII

## Common Patterns

### Pattern 1: Module Logger
```python
import logging
logger = logging.getLogger(__name__)

def my_function():
    logger.info("Function called")
```

### Pattern 2: Class Logger
```python
import logging

class MyClass:
    logger = logging.getLogger(__name__)
    
    def method(self):
        self.logger.info("Method called")
```

### Pattern 3: Performance Monitoring
```python
import logging
import time
from functools import wraps

def log_performance(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        logging.info(f"{func.__name__} took {elapsed:.2f}s")
        return result
    return wrapper
```

## File Handlers

### StreamHandler
```python
# Log to console
handler = logging.StreamHandler()
```

### FileHandler
```python
# Log to file (fixed)
handler = logging.FileHandler('app.log')
```

### RotatingFileHandler
```python
# Log to file with rotation (production)
handler = logging.handlers.RotatingFileHandler(
    'app.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
```

### TimedRotatingFileHandler
```python
# Log to file with time-based rotation
handler = logging.handlers.TimedRotatingFileHandler(
    'app.log',
    when='midnight',
    interval=1,
    backupCount=7  # Keep 7 days
)
```

## Formatter Options

- `%(name)s` - Logger name
- `%(levelname)s` - Log level
- `%(message)s` - Log message
- `%(asctime)s` - Timestamp
- `%(filename)s` - Source filename
- `%(funcName)s` - Function name
- `%(lineno)d` - Line number
- `%(process)d` - Process ID
- `%(thread)d` - Thread ID
- `%(pathname)s` - Full file path

## Troubleshooting

**Problem:** No log output
- Solution: Ensure handler is added to logger
- Solution: Check logger level is not higher than message level

**Problem:** Duplicate messages
- Solution: Check logger propagation
- Solution: Ensure handlers aren't added multiple times

**Problem:** Slow logging
- Solution: Avoid expensive operations in log messages
- Solution: Use lazy evaluation with `%s` formatting

**Problem:** Lost logs
- Solution: Flush handlers before exit
- Solution: Use RotatingFileHandler to manage file size

## Practice Exercises

1. Create a simple application with logging at all levels
2. Set up multiple loggers for different modules
3. Implement RotatingFileHandler with proper backup count
4. Create a decorator to log function execution time
5. Set up context-based logging with request IDs
6. Configure logging from a dictionary
7. Implement separate error and info log files

## Further Reading

- Python `logging` module: https://docs.python.org/3/library/logging.html
- Logging configuration: https://docs.python.org/3/library/logging.config.html
- Handlers: https://docs.python.org/3/library/logging.handlers.html

## Summary

Logging is fundamental to professional Python development. By understanding:
- Basic logging setup
- Multiple loggers and hierarchy
- Production-ready patterns
- Comprehensive error handling

You can build robust, maintainable applications with proper debugging, monitoring, and error recovery capabilities.

---

**Total Duration:** ~50-60 minutes (including all notebooks and exercises)
**Difficulty:** Beginner to Advanced
**Prerequisites:** Basic Python knowledge

**Contents:**
- 4 comprehensive Jupyter notebooks
- 1 production-ready Python utility module
- Complete best practices guide
- Real-world code examples
