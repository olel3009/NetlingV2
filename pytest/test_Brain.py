def test_brain():
    from Enviroment import Enviroment
    from Agent import Agent
    env = Enviroment()
    agent = Agent(0, 0, 0, 10, 10, noBrain=False, env=env)
    env.addObjects(agent)

    agent1 = Agent(20, 0, 0, 10, 10, noBrain=False, env=env)
    env.addObjects(agent1)

    v = env.objects[0].getVission()
    assert len(v) == 1

    assert env.objects[0].brain.objToVector(v[0]) == [20.0, 0.0, 0.9]

def test_mutation():
    from Brain import Brain
    from Enviroment import Enviroment
    from Agent import Agent

    env = Enviroment()
    agent = Agent(0, 0, 0, 10, 10, noBrain=False, env=env)
    env.addObjects(agent)

    a = agent.brain.think([0, 1], agent.getVission())
    agent.brain.mutate_randomly()
    b = agent.brain.think([0, 1], agent.getVission())

    assert a != b