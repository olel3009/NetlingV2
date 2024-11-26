import pytest

def test_addObjects():
    from Object import Object
    from Enviroment import Enviroment
    env = Enviroment()
    obj = Object(0, 0, 0, 0, 0)
    env.addObjects(obj)
    assert obj in env.objects
