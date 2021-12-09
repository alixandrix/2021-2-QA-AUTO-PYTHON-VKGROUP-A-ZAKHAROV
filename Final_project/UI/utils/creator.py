from dataclasses import dataclass
import faker

faker = faker.Faker()


class Builder:

    @staticmethod
    def registration_form(username=None, password=None, email=None):

        @dataclass
        class Registr:
            username: str = None
            password: str = None
            email: str = None

        if username is None:
            username = faker.lexify(text='???????')

        if password is None:
            password = faker.bothify(text='?????')

        if email is None:
            email = faker.email()

        return Registr(username=username, password=password, email=email)
