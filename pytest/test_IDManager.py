def test_IDManager():
    from Manager.IDManager import IDManager
    IDManager.id = 0
    assert IDManager.generateID() == 1
    assert IDManager.generateID() == 2