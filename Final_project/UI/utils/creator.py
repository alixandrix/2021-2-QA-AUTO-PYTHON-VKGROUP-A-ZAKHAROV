from dataclasses import dataclass
import faker

faker = faker.Faker()


class Builder:

    @staticmethod
    def username(username_length=None):
        return faker.lexify(f"{''.join(['?' for _ in list(range(username_length))])}@?.??")

    @staticmethod
    def password(password_length=None):
        return faker.lexify(f"{''.join(['?' for _ in list(range(password_length))])}@?.??")

    @staticmethod
    def email(email_length=None):
        return faker.lexify(f"{''.join(['?' for _ in list(range(email_length))])}@?.??")


    """@staticmethod
    def registration_form(username=None, password=None, email=None, username_length=None, password_length=None, email_length=None):

        @dataclass
        class Auth:
            username: str
            password: str
            email: str

        if username is None:
            username = faker.lexify(f"{''.join(['?' for _ in list(range(username_length))])}@?.??")

        if password is None:
            password = faker.lexify(f"{''.join(['?' for _ in list(range(password_length))])}@?.??")

        if email is None:
            email = faker.lexify(f"{''.join(['?' for _ in list(range(email_length - 5))])}@?.??")

        return Auth(username=username, password=password, email=email)
"""