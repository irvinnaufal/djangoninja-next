import logging
from django.db import DatabaseError
from ..utils.response import error_response

# ✅ Setup global logger
logger = logging.getLogger(__name__)

# ✅ Utility for logging & error handling
def handle_service_call(function, success_message="Operation successful"):
    """Wrapper to handle service calls with logging and error handling."""
    def wrapper(*args, **kwargs):
        try:
            # Execute the actual service function
            result = function(*args, **kwargs)
            # Log the success message and relevant information (avoiding sensitive data)
            logger.info(f"{success_message}: {function.__name__} executed successfully")
            # Return the result from the service function
            return result
        
        except DatabaseError as e:
            logger.error(f"Database error in {function.__name__}: {e}")
            return error_response("Database error", 500)
        
        except Exception as e:
            logger.error(f"Unexpected error in {function.__name__}: {e}")
            return error_response("Internal server error", 500)
    
    return wrapper
