from dataclasses import dataclass

import faker

fake = faker.Faker()

class Builder:

    @staticmethod
    def segment(name=None):

        @dataclass
        class Segment:
            name: str = None

        if name is None:
            name = fake.bothify(text='??????????')

        return Segment(name=name)
