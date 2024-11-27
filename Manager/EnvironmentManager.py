import logging
from Manager.QuadTreeManager import Quadtree, rect
from Manager.EventManager import Events, CollissionEvent
import random
from Objects.Agent import Agent
from Manager.CognitiveManager import Brain
from Objects.Food import Food
from Manager.IDManager import GenomeManagerInstance
import neat
config_path = "config-feedforward"
NEATConfig = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         "config-feedforward")

class Enviroment():
    next_node_id = 0

    def __init__(self, width = 100, height = 100, agentsCount= 0, foodCount = 0, minCountAgent=-1, minCountFood=-1):
        self.objects = []
        self.logger = logging.getLogger(__name__)

        self.width = width
        self.height = height

        self.quadtree = Quadtree(self.width, self.height, 0, 0, 4)
        self.logger.debug("Quadtree created")

        self.eventManager = []
        self.logger.debug("EventManager created")
        self.logger.debug("Enviroment created")

        self.minCountAgent = minCountAgent
        self.minCountFood = minCountFood

        self.spawnObjects(Agent, agentsCount, rad=rect(0, 0, self.width, self.height), fooodlevel=100, maxfoodlevel=100)
        self.spawnObjects(Food, foodCount, rad=rect(0, 0, self.width, self.height), foodlevel=10)

    def addObjects(self, obj):
        self.objects.append(obj)
        self.quadtree.insert(obj)
        self.logger.debug(f"Object added at ({obj.x}, {obj.y})")

    def spawnObjects(self, instance, count = 1, width=10, height=10, rad=None, **kwargs):
        for i in range(count):
            if rad is None:
                x = random.randint(0, self.width)
                y = random.randint(0, self.height)
            else:
                x = random.randint(rad.x, rad.width + rad.x)
                y = random.randint(rad.y, rad.height + rad.y)
            obj = instance(x, y, 0,width, height, env=self, **kwargs)
            if isinstance(obj, Agent):
                obj.brain.mutate_randomly(10)
            self.addObjects(obj)
            self.logger.debug(f"Object spawned at ({obj.x}, {obj.y})")

    def removeObjects(self, obj):
        self.objects.remove(obj)
        self.quadtree.remove(obj)
        self.logger.debug(f"Object removed at ({obj.x}, {obj.y})")

    def update(self):
        for obj in self.objects:
            obj.update()
        self._collissionEvent()
        self.executeEvents()
        self.quadtree.clear()
        for obj in self.objects:
            self.quadtree.insert(obj)
        self.logger.debug("Quadtree updated")


        #TODO: Replace this with a better solution
        if self.minCountAgent != -1 and len([obj for obj in self.objects if isinstance(obj, Agent)]) < self.minCountAgent:
            agent_params = (250, 250, 0, 10, 10, 50, 100)
            agents = [obj for obj in self.objects if isinstance(obj, Agent)]
            parent1 = max(agents, key=lambda agent: agent.foodlevel)
            parent2 = max([agent for agent in agents if agent != parent1], key=lambda agent: agent.foodlevel)
            self.addObjects(self.create_offspring_from_parents(parent1, parent2, NEATConfig, self, agent_params))
        if self.minCountFood != -1 and len([obj for obj in self.objects if isinstance(obj, Food)]) < self.minCountFood:
            self.spawnObjects(Food, 1, rad=rect(0, 0, self.width, self.height), foodlevel=10)

    def collectAll(self):
        return [obj.collect() for obj in self.objects]

    def executeEvents(self):
        for event in self.eventManager:
            if event.event_type == Events.COLLISION:
                event.data[0].onCollission(event.data[1], self.eventManager)
            if event.event_type == Events.DEATH:
                event.data[0].onDeath(event.data[1], self.eventManager)
                try:
                    self.removeObjects(event.data[0])
                except:
                    pass
        self.eventManager = []

    def _collissionEvent(self):
        for obj in self.objects:
            collision = self._collissionByObjects(obj)
            if collision is not None:
                self.logger.debug(f"Collision detected between {obj.type} and {collision.type}")
                self.eventManager.append(CollissionEvent(obj, collision))

    def _collissionByObjects(self, obj):
        for other in self.objects:
            if other is not obj:
                if (obj.x < other.x + other.width and
                        obj.x + obj.width > other.x and
                        obj.y < other.y + other.height and
                        obj.y + obj.height > other.y):
                    return other
        return None

    def create_offspring_from_parents(self, parent1, parent2, config, env, agent_params):
        """
        Erzeugt einen neuen Agent durch Crossover und Mutation von zwei Eltern.

        Args:
            parent1 (Agent): Der erste Eltern-Agent.
            parent2 (Agent): Der zweite Eltern-Agent.
            config (neat.Config): Die NEAT-Konfiguration.
            env (Enviroment): Die Umgebung, in der die Agents agieren.
            agent_params (tuple): Standardparameter für Agents (x, y, r, width, height, foodlevel, maxfoodlevel).

        Returns:
            Agent: Der neue Agent.
        """
        x, y, r, width, height, foodlevel, maxfoodlevel = agent_params
        x = random.randint(0, self.width)
        y = random.randint(0, self.height)

        # Debug-Ausgabe für die Eltern
        print(
            f"Erzeuge Nachkomme aus Eltern:\n- Parent1 Fitness: {parent1.foodlevel}\n- Parent2 Fitness: {parent2.foodlevel}")
        if parent1.foodlevel < 50 or parent2.foodlevel < 50:
            a = Agent(x, y, r, width, height, foodlevel, maxfoodlevel, env=env)
            a.brain.mutate_randomly(10)
            return a
        parent1.brain.genome.fitness = parent1.foodlevel
        parent2.brain.genome.fitness = parent2.foodlevel

        child_genome = GenomeManagerInstance.NEATConfig.genome_type(GenomeManagerInstance.generateID())
        child_genome.configure_crossover(parent1.brain.genome, parent2.brain.genome,
                            GenomeManagerInstance.NEATConfig.genome_config)
        child_genome.mutate(GenomeManagerInstance.NEATConfig.genome_config)


        # 5. Mutiere das neue Genom
        try:
            child_genome.mutate(GenomeManagerInstance.NEATConfig.genome_config)
        except AssertionError as e:
            print(f"Mutation fehlgeschlagen: {e}. Initialisiere Genom neu.")
            child_genome.configure_new(GenomeManagerInstance.NEATConfig.genome_config)
        brain = Brain()
        brain.genome = child_genome
        brain.net = neat.nn.FeedForwardNetwork.create(child_genome, GenomeManagerInstance.NEATConfig)
        new_agent = Agent(x, y, r, width, height, foodlevel, maxfoodlevel, noBrain=False, env=env)
        new_agent.brain = brain
        print(f"Neuer Agent erstellt mit ID: {child_genome.key} und Gehirn-Netzwerk.")
        return new_agent
