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

    def think(self, inputs):
        return self.net.activate(inputs)