from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Security:
    """
    Classe responsável por prover métodos de segurança.
    A classe possui os seguintes métodos:
    - verify_password: Método para verificar a senha.
    - get_password_hash: Método para obter o hash da senha.
    """

    def verify_password(self, plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        return pwd_context.hash(password)


# Instanciando a classe Security
security = Security()
