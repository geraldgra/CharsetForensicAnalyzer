import time
from uuid import uuid4


class RequestContextMiddleware:

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):

        #
        # Sólo peticiones HTTP
        #
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        #
        # Contexto de la petición
        #
        scope["transaction_id"] = str(uuid4())
        scope["started_at"] = time.perf_counter()

        await self.app(scope, receive, send)