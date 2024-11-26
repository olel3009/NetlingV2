def test_object():
    from Object import Object
    obj = Object(0, 0, 0, 0, 0)
    assert obj.x == 0
    assert obj.y == 0
    assert obj.width == 0
    assert obj.height == 0

def test_agent_move():
    from Agent import Agent
    agent = Agent(0, 0, 0, 0, 0)
    agent.moveRelative(1, 1)
    assert agent.x == 1
    assert agent.y == 1

def test_agent_teleport():
    from Agent import Agent
    agent = Agent(0, 0, 0, 0, 0)
    agent.teleport(1, 1)
    assert agent.x == 1
    assert agent.y == 1