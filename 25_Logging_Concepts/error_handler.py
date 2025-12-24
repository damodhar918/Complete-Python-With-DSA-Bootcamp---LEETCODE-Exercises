"""
Error Handler Utilities for Logging

This module provides comprehensive error handling utilities including:
- Custom exception classes
- Error context management
- Structured error logging
- Error aggregation and reporting
- Retry mechanisms with logging
- File-based error handlers
"""

import logging
import logging.handlers
import traceback
import json
import os
from typing import Dict, Any, Optional, Callable, Type, List
from functools import wraps
from dataclasses import dataclass, asdict
from datetime import datetime
from contextlib import contextmanager


# ============================================================================
# Custom Exception Classes
# ============================================================================

class ApplicationError(Exception):
    """Base application error with logging support"""
    
    def __init__(self, message: str, error_code: Optional[str] = None, **context):
        self.message = message
        self.error_code = error_code or "UNKNOWN"
        self.context = context
        super().__init__(self.message)
    
    def log_error(self, logger: logging.Logger, level=logging.ERROR):
        """Log the error with context"""
        log_message = f"[{self.error_code}] {self.message}"
        if self.context:
            log_message += f" | Context: {self.context}"
        logger.log(level, log_message, exc_info=True)


class DatabaseError(ApplicationError):
    """Database-specific error"""
    pass


class ValidationError(ApplicationError):
    """Validation error for data validation failures"""
    pass


class APIError(ApplicationError):
    """API error with HTTP status code"""
    
    def __init__(self, message: str, status_code: int, **context):
        self.status_code = status_code
        super().__init__(message, error_code=f"API_{status_code}", **context)


class ConfigurationError(ApplicationError):
    """Configuration-related error"""
    pass


class TimeoutError(ApplicationError):
    """Operation timeout error"""
    pass


# ============================================================================
# Error Context Management
# ============================================================================

@dataclass
class ErrorRecord:
    """Record of an error for tracking and reporting"""
    timestamp: datetime
    operation: str
    error_type: str
    message: str
    severity: str
    context: Dict[str, Any]
    traceback: str


class ErrorContext:
    """Manage error context and details"""
    
    def __init__(self, operation: str, **context):
        self.operation = operation
        self.context = context
        self.error_details: Dict[str, Any] = {}
    
    def log_error(self, exception: Exception, logger: logging.Logger):
        """Log error with full context"""
        self.error_details = {
            'operation': self.operation,
            'exception_type': type(exception).__name__,
            'exception_message': str(exception),
            'traceback': traceback.format_exc(),
            'context': self.context
        }
        
        logger.error(
            f"Error in {self.operation}: {str(exception)}",
            extra=self.error_details,
            exc_info=True
        )
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of error for API response"""
        return {
            'error': True,
            'operation': self.operation,
            'message': self.error_details.get('exception_message', 'Unknown error'),
            'type': self.error_details.get('exception_type', 'Unknown')
        }


class ErrorAggregator:
    """Aggregate and track errors for reporting"""
    
    def __init__(self):
        self.errors: List[ErrorRecord] = []
        self.error_counts: Dict[str, int] = {}
    
    def record_error(
        self,
        operation: str,
        exception: Exception,
        severity: str = "ERROR",
        **context
    ):
        """Record an error"""
        error_record = ErrorRecord(
            timestamp=datetime.now(),
            operation=operation,
            error_type=type(exception).__name__,
            message=str(exception),
            severity=severity,
            context=context,
            traceback=traceback.format_exc()
        )
        
        self.errors.append(error_record)
        
        # Update counts
        error_key = f"{operation}:{error_record.error_type}"
        self.error_counts[error_key] = self.error_counts.get(error_key, 0) + 1
    
    def get_report(self) -> Dict[str, Any]:
        """Generate error report"""
        total_errors = len(self.errors)
        critical = len([e for e in self.errors if e.severity == "CRITICAL"])
        errors = len([e for e in self.errors if e.severity == "ERROR"])
        warnings = len([e for e in self.errors if e.severity == "WARNING"])
        
        return {
            'total_errors': total_errors,
            'critical': critical,
            'errors': errors,
            'warnings': warnings,
            'error_types': self.error_counts,
            'recent_errors': [
                {
                    'timestamp': str(e.timestamp),
                    'operation': e.operation,
                    'type': e.error_type,
                    'message': e.message
                }
                for e in self.errors[-5:]  # Last 5 errors
            ]
        }
    
    def clear(self):
        """Clear all recorded errors"""
        self.errors.clear()
        self.error_counts.clear()


# ============================================================================
# Decorators and Context Managers
# ============================================================================

def retry_with_logging(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,),
    logger: Optional[logging.Logger] = None
):
    """Decorator for retry logic with logging"""
    
    if logger is None:
        logger = logging.getLogger(__name__)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            
            for attempt in range(1, max_attempts + 1):
                try:
                    logger.debug(
                        f"Attempt {attempt}/{max_attempts} for {func.__name__}"
                    )
                    return func(*args, **kwargs)
                    
                except exceptions as e:
                    if attempt == max_attempts:
                        logger.error(
                            f"All {max_attempts} attempts failed for {func.__name__}: {e}",
                            exc_info=True
                        )
                        raise
                    
                    logger.warning(
                        f"Attempt {attempt} failed: {e}. "
                        f"Retrying in {current_delay}s..."
                    )
                    import time
                    time.sleep(current_delay)
                    current_delay *= backoff
        
        return wrapper
    
    return decorator


def log_performance(logger: Optional[logging.Logger] = None):
    """Decorator to log function execution time and errors"""
    
    if logger is None:
        logger = logging.getLogger(__name__)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            start_time = time.time()
            logger.debug(f"Starting execution of {func.__name__}")
            
            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start_time
                
                if elapsed > 1.0:  # Log slow operations
                    logger.warning(
                        f"{func.__name__} took {elapsed:.2f}s (slow operation)"
                    )
                else:
                    logger.debug(
                        f"{func.__name__} completed in {elapsed:.2f}s"
                    )
                return result
                
            except Exception as e:
                elapsed = time.time() - start_time
                logger.error(
                    f"{func.__name__} failed after {elapsed:.2f}s: {str(e)}",
                    exc_info=True
                )
                raise
        
        return wrapper
    
    return decorator


@contextmanager
def error_handler(operation: str, logger: Optional[logging.Logger] = None):
    """Context manager for error handling"""
    
    if logger is None:
        logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Starting operation: {operation}")
        yield
        logger.info(f"Completed operation: {operation}")
    except Exception as e:
        logger.error(f"Failed operation: {operation}", exc_info=True)
        raise
    finally:
        logger.debug(f"Cleanup for operation: {operation}")


# ============================================================================
# Custom Handlers
# ============================================================================

class ErrorFileHandler(logging.handlers.RotatingFileHandler):
    """Custom file handler for error logging with automatic rotation"""
    
    def __init__(
        self,
        filename: str,
        max_bytes: int = 10*1024*1024,  # 10MB
        backup_count: int = 5,
        error_level: int = logging.ERROR
    ):
        super().__init__(filename, maxBytes=max_bytes, backupCount=backup_count)
        self.error_level = error_level
        
        # Detailed formatter for errors
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s] '
            '[%(filename)s:%(funcName)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.setFormatter(formatter)
        self.setLevel(error_level)
    
    def emit(self, record: logging.LogRecord):
        """Override to add extra processing"""
        try:
            # Only emit errors and above
            if record.levelno >= self.error_level:
                super().emit(record)
        except Exception:
            self.handleError(record)


class StructuredErrorFormatter(logging.Formatter):
    """Format errors as structured JSON for log aggregation tools"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'function': record.funcName,
            'line': record.lineno,
        }
        
        if record.exc_info:
            log_data['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': self.formatException(record.exc_info)
            }
        
        # Include extra fields
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'created', 'filename',
                          'funcName', 'levelname', 'levelno', 'lineno',
                          'module', 'msecs', 'message', 'pathname', 'process',
                          'processName', 'relativeCreated', 'thread', 'threadName',
                          'exc_info', 'exc_text', 'stack_info']:
                log_data[key] = str(value)
        
        return json.dumps(log_data)


# ============================================================================
# Configuration
# ============================================================================

class ErrorHandlerConfig:
    """Configure error handlers for application"""
    
    @staticmethod
    def setup_error_handlers(log_dir: str = 'logs') -> logging.Logger:
        """Setup comprehensive error handling"""
        os.makedirs(log_dir, exist_ok=True)
        
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        
        # Clear existing handlers
        root_logger.handlers.clear()
        
        # Error handler - captures ERROR and CRITICAL
        error_handler = ErrorFileHandler(
            os.path.join(log_dir, 'errors.log'),
            error_level=logging.ERROR
        )
        root_logger.addHandler(error_handler)
        
        # Warning handler - captures WARNING and above
        warning_handler = logging.handlers.RotatingFileHandler(
            os.path.join(log_dir, 'warnings.log'),
            maxBytes=5*1024*1024,
            backupCount=3
        )
        warning_formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(message)s'
        )
        warning_handler.setFormatter(warning_formatter)
        warning_handler.setLevel(logging.WARNING)
        root_logger.addHandler(warning_handler)
        
        # Critical handler - captures only CRITICAL
        critical_handler = logging.FileHandler(
            os.path.join(log_dir, 'critical.log')
        )
        critical_formatter = logging.Formatter(
            '[%(asctime)s] CRITICAL: %(message)s | '
            '%(filename)s:%(funcName)s:%(lineno)d'
        )
        critical_handler.setFormatter(critical_formatter)
        critical_handler.setLevel(logging.CRITICAL)
        root_logger.addHandler(critical_handler)
        
        # Console handler for development
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            '[%(levelname)s] %(name)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.INFO)
        root_logger.addHandler(console_handler)
        
        logger = logging.getLogger('app')
        logger.info(f"Error handlers configured. Log directory: {log_dir}")
        
        return root_logger
    
    @staticmethod
    def setup_structured_logging(log_dir: str = 'logs') -> logging.Logger:
        """Setup structured JSON logging"""
        os.makedirs(log_dir, exist_ok=True)
        
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        root_logger.handlers.clear()
        
        # Structured error handler
        error_handler = ErrorFileHandler(
            os.path.join(log_dir, 'errors_structured.log')
        )
        error_handler.setFormatter(StructuredErrorFormatter())
        root_logger.addHandler(error_handler)
        
        logger = logging.getLogger('app')
        logger.info("Structured logging configured")
        
        return root_logger


# ============================================================================
# Utility Functions
# ============================================================================

def get_error_chain(exception: Exception) -> List[str]:
    """Get the full error chain"""
    chain = []
    current = exception
    
    while current is not None:
        chain.append(f"{type(current).__name__}: {str(current)}")
        current = current.__cause__ or current.__context__
    
    return chain


def safe_log(func: Callable, logger: Optional[logging.Logger] = None):
    """Decorator to safely log function calls without failing on errors"""
    
    if logger is None:
        logger = logging.getLogger(__name__)
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
            raise
    
    return wrapper


if __name__ == "__main__":
    # Setup logging
    ErrorHandlerConfig.setup_error_handlers()
    logger = logging.getLogger('app')
    
    # Example: Custom exception
    try:
        raise ValidationError(
            "Invalid email format",
            error_code="INVALID_EMAIL",
            email="user@example"
        )
    except ValidationError as e:
        e.log_error(logger)
    
    # Example: Error context
    ctx = ErrorContext('database_query', user_id=123)
    try:
        raise DatabaseError("Connection timeout", error_code="DB_TIMEOUT")
    except DatabaseError as e:
        ctx.log_error(e, logger)
