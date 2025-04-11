from passlib.context import CryptContext

# Creating a password context for hashing and verifying password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# function to hash a password coming from the user
def hash_password(password: str) -> str:
    "Hashing a password using bcrypt algo."
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    "Verify if a plain password matches its hashed version."
    return pwd_context.verify(plain_password, hashed_password)
