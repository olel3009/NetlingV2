import pytest
def test_addObjects():
    from Object import Object
    from Enviroment import Enviroment
    env = Enviroment()
    obj = Object(10, 10, 0, 0, 0, env=env)
    env.addObjects(obj)
    assert obj in env.objects
    from  Quadtree import rect
    range1 = rect(0, 0, env.width, env.height)
    assert len(env.quadtree.query(range1, 0)) == 1

def test_removeObjects():
    from Object import Object
    from Enviroment import Enviroment
    env = Enviroment()
    obj = Object(0, 0, 0, 0, 0, env=env)
    env.addObjects(obj)
    env.removeObjects(obj)
    assert obj not in env.objects

def test_update():
    from Object import Object
    from Enviroment import Enviroment
    env = Enviroment()
    obj = Object(0, 0, 0, 0, 0, env)
    env.addObjects(obj)
    env.objects[0].x = 75
    env.objects[0].y = 75
    env.update()
    from  Quadtree import rect
    range1 = rect(50, 50, 50, 50)
    assert len(env.quadtree.query(range1, 0)) == 1

def test_collssion():
    from Object import Object
    from Enviroment import Enviroment
    env = Enviroment()
    obj = Object(0, 0, 0, 10, 10, env)
    obj2 = Object(0, 0, 0, 10, 10, env)
    env.addObjects(obj)
    env.addObjects(obj2)
    assert env._collissionByObjects(obj) == obj2
    assert env._collissionByObjects(obj2) == obj
    obj2.x = 100
    obj2.y = 100
    env.update()
    assert env._collissionByObjects(obj) == None
    assert env._collissionByObjects(obj2) == None

def test_CollissionEvent():
    from Object import Object
    from Enviroment import Enviroment
    env = Enviroment()
    obj = Object(0, 0, 0, 10, 10, env)
    obj2 = Object(0, 0, 0, 10, 10, env)
    env.addObjects(obj)
    env.addObjects(obj2)
    env._collissionEvent()
    assert env.eventManager[0].data == (obj, obj2)
    obj2.x = 100
    obj2.y = 100
    env.update()
    env._collissionEvent()
    assert len(env.eventManager) == 0

def test_Eat():
    from Agent import Agent
    from Enviroment import Enviroment
    from Food import Food
    env = Enviroment()
    agent = Agent(10, 10, 0, 10, 10, noBrain=True, env=env, fooodlevel=10)
    food = Food(10, 10, 0, 10, 10, 10, env=env)
    env.addObjects(agent)
    env.addObjects(food)
    env.update()
    assert len(env.objects) == 1
    assert agent.foodlevel == 20

def test_collectAll():
    from Object import Object
    from Enviroment import Enviroment
    env = Enviroment()
    obj = Object(0, 0, 0, 10, 10, env=env)
    env.addObjects(obj)
    assert env.collectAll() == [{"x": 0, "y": 0, "r": 0, "width": 10, "height": 10, "id": obj.id, "type": obj.type}]
    obj1 = Object(0, 0, 0, 10, 10, env=env)
    env.addObjects(obj1)
    assert env.collectAll() == [{"x": 0, "y": 0, "r": 0, "width": 10, "height": 10, "id": obj.id, "type": obj.type}, {"x": 0, "y": 0, "r": 0, "width": 10, "height": 10, "id": obj1.id, "type": obj1.type}]

def test_spawn():
    from Enviroment import Enviroment
    from Object import Object
    env = Enviroment()
    env.spawnObjects(Object, 10)
    assert len(env.objects) == 10
def test_collission():
    from Object import Object
    from Enviroment import Enviroment
    env = Enviroment()
    obj = Object(0, 0, 0, 10, 10, env)
    obj2 = Object(5, 5, 0, 10, 10, env)
    env.addObjects(obj)
    env.addObjects(obj2)
    assert env._collissionByObjects(obj) == obj2
    assert env._collissionByObjects(obj2) == obj
