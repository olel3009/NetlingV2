import random
import neat

config_path = "/config-feedforward"
NEATConfig = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         "config-feedforward")

class Brain:
    def __init__(self):
        self.genome = NEATConfig.genome_type(random.randint(0, 100000000))
        self.genome.configure_new(NEATConfig.genome_config)
        self.net = neat.nn.FeedForwardNetwork.create(self.genome, NEATConfig)

    def think(self, inputs, lens=None):
        inputs1 = []
        if lens:
            for obj in lens:
                inputs1 += obj.objToVector(obj)
        inputs1 += [0] * (12 - len(inputs1))
        return self.net.activate(inputs + inputs1)

    def objToVector(self, obj):
        distance = obj[0]
        angle = obj[1]
        object = obj[2]
        type = object.identifier
        return [distance, angle, type]
