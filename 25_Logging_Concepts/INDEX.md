# Logging Concepts - Index & Quick Navigation

## 📚 Learning Path

### Beginner Level (15 minutes)
Start with **Notebook 250** to understand logging fundamentals:
- [ ] Basic logging setup
- [ ] Log levels explanation
- [ ] Handlers and formatters
- [ ] Exception logging

### Intermediate Level (5 minutes)
Continue with **Notebook 251** for advanced configurations:
- [ ] Multiple loggers
- [ ] Logger hierarchy
- [ ] Different log levels per module
- [ ] Best practices

### Advanced Level (30+ minutes)
Master **Notebook 252** for production implementations:
- [ ] Real-world application structure
- [ ] Module-specific logging patterns
- [ ] Performance monitoring
- [ ] Configuration management

### Expert Level (20+ minutes)
Master **Notebook 253** for error handling:
- [ ] Custom exception classes
- [ ] Error context management
- [ ] Retry logic with backoff
- [ ] Error aggregation and reporting
- [ ] Structured error logging
- [ ] Error recovery patterns

---

## 🎯 Quick Reference

### When to Use Each Log Level

```
DEBUG (10)   → Development only, detailed diagnostic info
INFO (20)    → Major events: startup, shutdown, important state changes
WARNING (30) → Something unexpected, default level
ERROR (40)   → Error that needs attention but app continues
CRITICAL (50)→ Serious error, app may not continue
```

### Common Logging Patterns

#### Pattern 1: Module Entry Point
```python
import logging
logger = logging.getLogger(__name__)
logger.info(f"Module {__name__} loaded")
```

#### Pattern 2: Function Execution
```python
def process_data(items):
    logger.debug(f"Processing {len(items)} items")
    try:
        # Do work
        logger.info(f"Successfully processed {len(items)} items")
    except Exception as e:
        logger.error(f"Failed to process items: {e}", exc_info=True)
```

#### Pattern 3: Class Operations
```python
class DataProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("DataProcessor initialized")
    
    def process(self, data):
        self.logger.debug(f"Processing data: {type(data)}")
```

---

## 📋 Checklist: Setting Up Logging in Your Project

- [ ] **Create a config module**
  ```python
  # config.py
  import logging
  
  def setup_logging():
      logging.basicConfig(level=logging.INFO)
  ```

- [ ] **Initialize in main entry point**
  ```python
  # main.py
  from config import setup_logging
  setup_logging()
  ```

- [ ] **Use named loggers in all modules**
  ```python
  import logging
  logger = logging.getLogger(__name__)
  ```

- [ ] **Log important events**
  - Application startup/shutdown
  - Error conditions
  - State changes
  - Performance issues

- [ ] **Configure handlers for production**
  - File output (with rotation)
  - Separate error log
  - Appropriate format with timestamps

- [ ] **Never log sensitive information**
  - Passwords ❌
  - API tokens ❌
  - User PII ❌
  - Credit cards ❌

---

## 🔧 Configuration Examples

### Minimal Setup (Development)
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Standard Setup (Development + Testing)
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Production Setup (File + Console)
```python
import logging.handlers
import os

# Create logs directory
os.makedirs('logs', exist_ok=True)

# Configure root logger
root = logging.getLogger()
root.setLevel(logging.DEBUG)

# Console handler
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
root.addHandler(console)

# File handler with rotation
file = logging.handlers.RotatingFileHandler(
    'logs/app.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
file.setLevel(logging.DEBUG)
file.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))
root.addHandler(file)

# Error file handler
error_file = logging.FileHandler('logs/error.log')
error_file.setLevel(logging.ERROR)
error_file.setFormatter(file.formatter)
root.addHandler(error_file)
```

---

## 🐛 Debugging Tips

### Check Logger Status
```python
import logging

logger = logging.getLogger('myapp')
print(f"Logger level: {logger.level}")
print(f"Handlers: {logger.handlers}")
print(f"Propagate: {logger.propagate}")
```

### Verify Message Won't Be Logged
```python
if not logger.isEnabledFor(logging.DEBUG):
    print("DEBUG messages are disabled")
```

### Log with Extra Context
```python
logger.info("User action", extra={'user_id': 123, 'action': 'login'})
```

---

## 📊 Logger Hierarchy Visualization

```
root
 ├── myapp (level: DEBUG)
 │   ├── myapp.database (level: DEBUG)
 │   ├── myapp.api (level: INFO)
 │   └── myapp.auth (level: WARNING)
 └── external_lib (level: WARNING)
```

Each logger inherits from its parent until configured otherwise.

---

## ✅ Best Practices Checklist

- [ ] Use `__name__` for all module loggers
- [ ] Set logger level at module or root, handler level separately
- [ ] Use INFO for user-facing events, DEBUG for developers
- [ ] Include context in error messages (user ID, request ID, etc.)
- [ ] Use `exc_info=True` for all exception logging
- [ ] Rotate log files in production
- [ ] Use structured logging for important metrics
- [ ] Document your logging strategy in README
- [ ] Test logging configuration in CI/CD
- [ ] Monitor log file sizes and disk usage

---

## 📌 Related Notebooks & Modules

- **250_Logging_In_Python.ipynb** - Fundamentals
- **251_Logging_With_Multiple_Loggers.ipynb** - Advanced configuration
- **252_Logging_Real_World_Implementation.ipynb** - Production patterns
- **253_Error_Handling_With_Logging.ipynb** - Error handling and recovery
- **error_handler.py** - Reusable error handling utilities

---

## 🔧 Error Handling Utilities

### Using error_handler.py

```python
from error_handler import (
    ValidationError,
    ErrorHandlerConfig,
    retry_with_logging,
    error_handler,
    ErrorAggregator
)

# Setup error handlers
ErrorHandlerConfig.setup_error_handlers('logs')

# Custom exception
try:
    raise ValidationError(
        "Invalid input",
        error_code="INVALID_INPUT",
        field="email"
    )
except ValidationError as e:
    e.log_error(logger)

# Retry logic
@retry_with_logging(max_attempts=3, delay=1)
def unreliable_operation():
    pass

# Error context
with error_handler("database_operation"):
    # Do something
    pass

# Error aggregation
aggregator = ErrorAggregator()
try:
    raise ValueError("Test")
except ValueError as e:
    aggregator.record_error("operation", e)
print(aggregator.get_report())
```

---

## 🚀 Next Steps

1. **Run the notebooks** - Execute each code cell in order
2. **Modify examples** - Experiment with log levels, formats, handlers
3. **Use error_handler.py** - Import utilities into your projects
4. **Create a test project** - Build a small app with proper logging and error handling
5. **Review logs** - Examine actual log files in the `logs/` directory
6. **Implement in your code** - Add comprehensive logging to all your projects
7. **Monitor and adjust** - Track error rates and refine your strategy

## 📂 File Structure

```
25_Logging_Concepts/
├── 250_Logging_In_Python.ipynb
├── 251_Logging_With_Multiple_Loggers.ipynb
├── 252_Logging_Real_World_Implementation.ipynb
├── 253_Error_Handling_With_Logging.ipynb
├── error_handler.py              # Utility module
├── README.md                      # Complete guide
├── INDEX.md                       # This file
└── logs/                          # Created when handlers are initialized
    ├── app.log
    ├── errors.log
    ├── warnings.log
    └── critical.log
```

---

**Happy Logging! 📝**
