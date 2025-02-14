from functools import wraps
from flask import request
from datetime import datetime, timedelta
import threading
from collections import defaultdict

# Store request counts and timeout info
ip_requests = defaultdict(lambda: defaultdict(list))
ip_timeout = defaultdict(datetime)
lock = threading.Lock()

def rate_limit(max_requests=7, timeout_minutes=5):
    def decorator(f):
        @wraps(f)
        def wrapped_function(*args, **kwargs):
            ip = request.remote_addr
            route = request.path
            now = datetime.now()

            # Check if IP is in timeout
            if ip in ip_timeout and ip_timeout[ip] > now:
                remaining = (ip_timeout[ip] - now).seconds
                flash(f'Rate limit exceeded. Please try again in {remaining} seconds.', 'error')
                return redirect("/")

            with lock:
                # Remove requests older than 1 minute
                current_time = datetime.now()
                ip_requests[ip][route] = [
                    req_time for req_time in ip_requests[ip][route] 
                    if (current_time - req_time).seconds <= 60
                ]

                # Add current request
                ip_requests[ip][route].append(current_time)

                # Check if rate limit exceeded
                if len(ip_requests[ip][route]) > max_requests:
                    # Set timeout
                    ip_timeout[ip] = datetime.now() + timedelta(minutes=timeout_minutes)
                    # Clear requests for this route
                    ip_requests[ip][route] = []
                    flash(f'Rate limit exceeded. Please try again in {timeout_minutes} minutes.', 'error')
                    return redirect("/")

            return f(*args, **kwargs)
        return wrapped_function
    return decorator