from passlib.context import CryptContext
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from anyio import to_thread

ph = PasswordHasher()

async def hash(password: str) -> str:
    return await to_thread.run_sync(ph.hash, password)

async def verify(plain_password: str, hashed_password: str) -> bool:
    def _verify():
        try:
            return ph.verify(hashed_password, plain_password)
        except VerifyMismatchError:
            return False
    
    return await to_thread.run_sync(_verify)