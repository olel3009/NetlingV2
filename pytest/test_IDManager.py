def test_IDManager():
    from Settings.IDManager import IDManager
    IDManager.id = 0
    assert IDManager.generateID() == 1
    assert IDManager.generateID() == 2