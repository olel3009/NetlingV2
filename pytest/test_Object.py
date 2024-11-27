def test_object():
    from Objects.Object import Object
    obj = Object(0, 0, 0, 0, 0, env="test")
    assert obj.x == 0
    assert obj.y == 0
    assert obj.width == 0
    assert obj.height == 0
