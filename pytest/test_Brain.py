def test_brain():
    from Manager.EnvironmentManager import Enviroment
    from Objects.Agent import Agent
    env = Enviroment()
    agent = Agent(0, 0, 0, 10, 10, noBrain=False, env=env)
    env.addObjects(agent)

    agent1 = Agent(20, 0, 0, 10, 10, noBrain=False, env=env)
    env.addObjects(agent1)

    v = env.objects[0].getVission()
    assert len(v) == 1

    assert env.objects[0].brain.objToVector(v[0]) == [20.0, 0.0, 0.9]

def test_mutation():
    from Manager.EnvironmentManager import Enviroment
    from Objects.Agent import Agent

    env = Enviroment()
    agent = Agent(0, 0, 0, 10, 10, noBrain=False, env=env)
    env.addObjects(agent)

    a = agent.brain.think([0, 1], agent.getVission())
    agent.brain.mutate_randomly(count=10)
    b = agent.brain.think([0, 1], agent.getVission())

    assert a != b

def test_brain_to_json():
    from Manager.EnvironmentManager import Enviroment
    from Objects.Agent import Agent

    env = Enviroment()
    agent = Agent(0, 0, 0, 10, 10, noBrain=False, env=env)
    env.addObjects(agent)

    assert len(agent.brain.genome_to_json()) == 2