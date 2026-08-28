import time
from collections import defaultdict
from fastapi import Request, HTTPException, status

class SimpleRateLimiter:
    def __init__(self, max_requests: int = 15, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)

    def check(self, request: Request):
        client_ip = request.client.host if request.client else 'unknown'
        now = time.time()
        # Clean older entries
        self.requests[client_ip] = [t for t in self.requests[client_ip] if now - t < self.window_seconds]
        if len(self.requests[client_ip]) >= self.max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail='Слишком много запросов. Пожалуйста, подождите немного.'
            )
        self.requests[client_ip].append(now)

auth_rate_limiter = SimpleRateLimiter(max_requests=20, window_seconds=60)
order_rate_limiter = SimpleRateLimiter(max_requests=10, window_seconds=60)
