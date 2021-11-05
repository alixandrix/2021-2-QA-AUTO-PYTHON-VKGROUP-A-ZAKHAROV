import os
import uuid
import numpy
import pytest
from PIL import Image


def create_image(my_dir):
    imarray = numpy.random.rand(401, 241, 3) * 255
    im = Image.fromarray(imarray.astype('uint8')).convert('RGBA')
    im.save(os.path.join(my_dir, 'result_image.png'))
    return os.path.abspath(os.path.join(my_dir, 'result_image.png'))

"""@pytest.fixture
def create_name():
    return str(uuid.uuid4())"""