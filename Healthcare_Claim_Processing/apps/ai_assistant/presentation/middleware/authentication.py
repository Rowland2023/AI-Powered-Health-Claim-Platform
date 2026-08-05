from fastapi import HTTPException, Request


class AuthenticationMiddleware:

    async def __call__(
        self,
        request: Request,
        call_next,
    ):

        # TODO
        # Validate JWT
        # Attach authenticated user

        return await call_next(request)