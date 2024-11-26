def test_quadtree_subdivision():
    from Quadtree import Quadtree
    from Object import Object
    qt = Quadtree(100, 100, 0, 0, 3)

    obj2 = Object(25, 25, 0, 0, 0, env="test")
    qt.insert(obj2)

    obj3 = Object(25, 75, 0, 0, 0, env="test")
    qt.insert(obj3)

    obj4 = Object(75, 25, 0, 0, 0, env="test")

    qt.insert(obj4)

    obj5 = Object(75, 75, 0, 0,0, env="test")
    qt.insert(obj5)

    assert qt.isSubdivided() == True

def test_quadtree_insert_and_query():
    from Quadtree import Quadtree
    from Object import Object
    qt = Quadtree(100, 100, 0, 0, 4)
    obj = Object(0, 0, 0, 0, 0, env="test")
    qt.insert(obj)
    from Quadtree import rect
    range1 = rect(0, 0, 100, 100)

    results = qt.query(range1, 0)
    for level, element in results:
        assert element == obj
        assert level == 0

def test_quadtree_query_specific_range():
    from Quadtree import Quadtree, rect
    from Object import Object
    qt = Quadtree(100, 100, 0, 0, 4)
    
    obj2 = Object(25, 25, 0, 0, 0, env="test")
    qt.insert(obj2)
    obj3 = Object(25, 75, 0, 0, 0, env="test")
    qt.insert(obj3)
    obj4 = Object(75, 25, 0, 0, 0, env="test")
    qt.insert(obj4)
    obj5 = Object(75, 75, 0, 0, 0, env="test")
    qt.insert(obj5)
    obj6 = Object(50, 50, 0, 0, 0, env="test")
    qt.insert(obj6)

    assert qt.isSubdivided() == True
    range2 = rect(50, 50, 50, 50)
    assert len(qt.query(range2, 0)) == 1
    result = qt.query(range2, 0)
    assert result[0][0] == 1
