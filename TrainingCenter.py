from Manager.QuadTreeManager import Quadtree
from Manager.EnvironmentManager import Enviroment
from Objects.Agent import Agent
from Objects.Food import Food


class TrainingCenter:
    def __init__(self, countOfFood, countOfAgents, width, height):
        self.width = width
        self.height = height
        self.quadtree = Quadtree(width, height, 0, 0, (countOfAgents + countOfFood) * 2)
        self.food = []
        self.agents = []
        self.countOfFood = countOfFood
        self.countOfAgents = countOfAgents
        self.env = Enviroment(width, height, 0, 0, -1, -1)
        self.time = 0

    def execute_training(self):
        """Executes one step of training and updates the environment."""
        self.env.update()
        # Filter the agents from the environment objects
        agents = [obj for obj in self.env.objects if isinstance(obj, Agent)]
        if len(agents) == 0:  # If no agents remain, terminate training
            return False
        self.time += 1
        return True


def initialize_training_centers(count, countOfFood, countOfAgents, width, height):
    """Creates a list of training centers with initialized food and agents."""
    training_centers = []
    for _ in range(count):
        tc = TrainingCenter(countOfFood, countOfAgents, width, height)
        # Add food objects
        for _ in range(countOfFood):
            tc.env.addObjects(Food(0, 0, 0, 10, 10, env=tc.env, foodlevel=30))
        # Add agent objects
        for _ in range(countOfAgents):
            a = Agent(0, 0, 0, 10, 10, 50, 100, env=tc.env)
            a.brain.mutate_randomly(10)
            tc.env.addObjects(a)
        training_centers.append(tc)
    return training_centers


def main():
    count_of_trainings = 100 # Number of simultaneous training centers
    max_iterations = 2      # Maximum number of iterations
    training_centers = initialize_training_centers(count_of_trainings, 10, 1, 100, 100)
    iteration = 0

    while training_centers and iteration < max_iterations:
        # Iterate through all training centers
        while len(training_centers) > 2:  # Schleife läuft, bis nur 2 Trainingscenter übrig sind
            for tc in training_centers[:]:  # Kopie der Liste durchlaufen
                if not tc.execute_training() and len(training_centers) > 2:  # Training ausführen und prüfen, ob es beendet ist
                    training_centers.remove(tc)  # Beenden und entfernen, wenn keine Agenten mehr
                    print(f"Training finished in {tc.time} steps")

        agents1 = [obj for obj in training_centers[0].env.objects if isinstance(obj, Agent)]
        agents2 = [obj for obj in training_centers[1].env.objects if isinstance(obj, Agent)]
        try:
            agents1[0].foodlevel = 100
        except:
            agents1.append(Agent(0, 0, 0, 10, 10, 50, 100, env=training_centers[0].env))

        try:
            agents2[0].foodlevel = 100
        except:
            agents2.append(Agent(0, 0, 0, 10, 10, 50, 100, env=training_centers[1].env))

        print("Creating offspring from the last two training centers...")
        # Create 1000 new training centers
        new_training_centers = []
        for _ in range(count_of_trainings):
            offspring_tc = TrainingCenter(10, 1, 100, 100)
            offspring_tc.env.addObjects(
                offspring_tc.env.create_offspring_from_parents(
                    agents1[0], agents2[0], None, offspring_tc.env,
                    (50, 50, 0, 10, 10, 50, 100)
                )
            )
            new_training_centers.append(offspring_tc)
        training_centers = new_training_centers  # Replace old training centers
        iteration = 0  # Reset iteration count for new generation

    iteration += 1

    if iteration >= max_iterations:
        print(f"Training terminated after reaching maximum iterations: {max_iterations}")
    print("Simulation complete.")


if __name__ == "__main__":
    main()
