from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')


class Hash:
    @staticmethod
    def bcrypt(password: str) -> str:
        """
        Static method that hashes given password
        :returns hashed password :type str
        """
        return pwd_cxt.hash(password)
