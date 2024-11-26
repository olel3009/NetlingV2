import math

from NetworkManager import environment


def test_agent_moveRelative():
    from Agent import Agent
    from Enviroment import Enviroment
    agent = Agent(50, 50, 0, 0, 0, noBrain=True, env=Enviroment())
    agent.moveRelative(1, 1)
    assert agent.x == 51
    assert agent.y == 51

def test_agent_teleport():
    from Agent import Agent
    from Enviroment import Enviroment
    agent = Agent(0, 0, 0, 0, 0, noBrain=True, env=Enviroment())
    agent.teleport(1, 1)
    assert agent.x == 1
    assert agent.y == 1

def test_agent_moveRelativeByAngle():
    from Agent import Agent
    from Enviroment import Enviroment
    env = Enviroment()
    agent = Agent(50, 50, 0, 0, 0, noBrain=True, env=env)
    env.addObjects(agent)
    agent.moveRelativeByAngle(math.pi/4, 1)
    assert agent.x == 50 + math.cos(math.pi/4)
    assert agent.y == 50 + math.sin(math.pi/4)


def test_agent_feed():
    from Agent import Agent
    from Food import Food
    from Enviroment import Enviroment
    environment = Enviroment()
    agent = Agent(0, 0, 0, 0, 0, noBrain=True, env=environment, fooodlevel=0)
    food = Food(0, 0, 0, 0, 0, 10, env=environment)
    agent.feed(food.foodlevel)
    assert agent.foodlevel == 10
    agent.feed(110)
    assert agent.foodlevel == 100

def test_brain():
    from Agent import Agent
    from Enviroment import Enviroment
    env = Enviroment()
    agent = Agent(0, 0, 0, 0, 0, noBrain=True, env=env)
    env.addObjects(agent)
    agent.update()
    assert env.objects[0].x == 0
    assert env.objects[0].y == 0

def test_validMove():
    from Agent import Agent
    from Enviroment import Enviroment
    env = Enviroment()
    agent = Agent(0, 0, 0, 0, 0, noBrain=True, env=env)
    assert agent.validMove(0, 0)
    assert agent.validMove(50, 50)
    assert not agent.validMove(-1, 0)
    assert not agent.validMove(0, -1)
    assert not agent.validMove(101, 0)
    assert not agent.validMove(0, 101)

def test_decreaseFood():
    from Agent import Agent
    from Enviroment import Enviroment
    env = Enviroment()
    agent = Agent(0, 0, 0, 0, 0, noBrain=True, env=env, fooodlevel=0)
    agent.decreaseFood()
    assert agent.foodlevel == -1
    assert len(env.eventManager) == 1