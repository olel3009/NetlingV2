import math


def test_agent_moveRelative():
    from Objects.Agent import Agent
    from Manager.EnvironmentManager import Enviroment
    agent = Agent(50, 50, 0, 0, 0, noBrain=True, env=Enviroment())
    agent.moveRelative(1, 1)
    assert agent.x == 51
    assert agent.y == 51

def test_agent_teleport():
    from Objects.Agent import Agent
    from Manager.EnvironmentManager import Enviroment
    agent = Agent(0, 0, 0, 0, 0, noBrain=True, env=Enviroment())
    agent.teleport(1, 1)
    assert agent.x == 1
    assert agent.y == 1

def test_agent_moveRelativeByAngle():
    from Objects.Agent import Agent
    from Manager.EnvironmentManager import Enviroment
    env = Enviroment()
    agent = Agent(50, 50, 0, 0, 0, noBrain=True, env=env)
    env.addObjects(agent)
    agent.moveRelativeByAngle(math.pi/4, 1)
    assert agent.x == 50 + math.cos(math.pi/4)
    assert agent.y == 50 + math.sin(math.pi/4)


def test_agent_feed():
    from Objects.Agent import Agent
    from Objects.Food import Food
    from Manager.EnvironmentManager import Enviroment
    environment = Enviroment()
    agent = Agent(0, 0, 0, 0, 0, noBrain=True, env=environment, fooodlevel=0)
    food = Food(0, 0, 0, 0, 0, 10, env=environment)
    agent.feed(food.foodlevel)
    assert agent.foodlevel == 10
    agent.feed(110)
    assert agent.foodlevel == 100

def test_brain():
    from Objects.Agent import Agent
    from Manager.EnvironmentManager import Enviroment
    env = Enviroment()
    agent = Agent(0, 0, 0, 0, 0, noBrain=True, env=env)
    env.addObjects(agent)
    agent.update()
    assert env.objects[0].x == 0
    assert env.objects[0].y == 0

def test_validMove():
    from Objects.Agent import Agent
    from Manager.EnvironmentManager import Enviroment
    env = Enviroment()
    agent = Agent(0, 0, 0, 0, 0, noBrain=True, env=env)
    assert agent.validMove(0, 0)
    assert agent.validMove(50, 50)
    assert not agent.validMove(-1, 0)
    assert not agent.validMove(0, -1)
    assert not agent.validMove(101, 0)
    assert not agent.validMove(0, 101)

def test_decreaseFood():
    from Objects.Agent import Agent
    from Manager.EnvironmentManager import Enviroment
    env = Enviroment()
    agent = Agent(0, 0, 0, 0, 0, noBrain=True, env=env, fooodlevel=0)
    agent.decreaseFood()
    assert agent.foodlevel == -1
    assert len(env.eventManager) == 1

def test_vision_rect():
    from Objects.Agent import Agent
    from Manager.EnvironmentManager import Enviroment
    env = Enviroment()
    agent = Agent(50, 50, 0, 10, 10, noBrain=True, env=env)
    env.addObjects(agent)
    v = agent.getVission()
    assert v == []
    env.objects[0].r = 0

    agent1 = Agent(80, 55, 0, 0, 0, noBrain=True, env=env)
    env.addObjects(agent1)
    v = env.objects[0].getVisionRect()
    assert len(env.quadtree.query(v)) == 1


def test_filtered_vision():
    from Objects.Agent import Agent
    from Manager.EnvironmentManager import Enviroment

    # Initialisiere die Umgebung
    env = Enviroment()

    # Erstelle den Hauptagenten mit Sichtfeld
    agent = Agent(50, 50, 0, 10, 10, noBrain=True, env=env)
    env.addObjects(agent)

    # Überprüfen, ob die Sicht zu Beginn leer ist
    v = agent.getVission()
    assert v == []

    # Teste für 8 verschiedene Winkel
    angles = [0, 45, 90, 135, 180, 225, 270, 315]
    results = []

    for angle in angles:
        # Setze die Rotation des Hauptagenten
        env.objects[0].r = angle

        # Platziere den zweiten Agenten passend zur Rotation
        if angle == 0:
            agent1 = Agent(80, 55, 0, 0, 0, noBrain=True, env=env)  # Rechts
        elif angle == 45:
            agent1 = Agent(80, 80, 0, 0, 0, noBrain=True, env=env)  # Rechts oben
        elif angle == 90:
            agent1 = Agent(50, 80, 0, 0, 0, noBrain=True, env=env)  # Oben
        elif angle == 135:
            agent1 = Agent(20, 80, 0, 0, 0, noBrain=True, env=env)  # Links oben
        elif angle == 180:
            agent1 = Agent(20, 55, 0, 0, 0, noBrain=True, env=env)  # Links
        elif angle == 225:
            agent1 = Agent(20, 20, 0, 0, 0, noBrain=True, env=env)  # Links unten
        elif angle == 270:
            agent1 = Agent(50, 20, 0, 0, 0, noBrain=True, env=env)  # Unten
        elif angle == 315:
            agent1 = Agent(80, 20, 0, 0, 0, noBrain=True, env=env)  # Rechts unten

        # Füge den zweiten Agenten hinzu und prüfe die Sicht
        env.addObjects(agent1)
        v = env.objects[0].getVission()

        # Überprüfe, ob der Agent korrekt erkannt wurde
        results.append((angle, len(v) == 1))

        # Entferne den zweiten Agenten für den nächsten Test
        env.objects.pop()

def test_testvision():
    from Objects.Agent import Agent
    from Manager.EnvironmentManager import Enviroment
    env = Enviroment()
    agent = Agent(50, 50, 0, 10, 10, fooodlevel=50, noBrain=True, env=env)
    env.addObjects(agent)
    from Objects.Food import Food
    env.addObjects(Food(80, 50, 0, 10, 10, 10, env=env))
    v = agent.getVission()
    assert len(v) == 1

    agent.moveRelativeByAngle(0, 30)
    env.update()
    assert len(env.objects) == 1

    agent.teleport(50, 50, 180)

    assert agent.r == 180
    env.addObjects(Food(30, 50, 0, 10, 10, 10, env=env))
    v = agent.getVission()
    assert len(v) == 1
