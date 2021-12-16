
import faker
import random

faker = faker.Faker()


class Builder:

    @staticmethod
    def username(username_length=random.randint(6, 16)):
        return faker.lexify(f"{''.join(['?' for _ in list(range(username_length))])}")

    @staticmethod
    def password(password_length=random.randint(1, 50)):
        return faker.lexify(f"{''.join(['?' for _ in list(range(password_length))])}")

    @staticmethod
    def email(email_length=random.randint(6, 64)):
        return faker.lexify(f"{''.join(['?' for _ in list(range(email_length-5))])}@?.??")


