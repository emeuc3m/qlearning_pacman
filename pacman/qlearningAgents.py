## qlearningAgents.py
# ------------------

from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)
    """
    def __init__(self, ghostAgents = None, **args):
        "Initialize Q-values"
        ReinforcementAgent.__init__(self, **args)

        self.actions = {"West":0, "East":1, "North":2, "South":3}

        #Load Qtable in memory
        self.readQtable()

        #QLearning parameters
        
        #Training values
        #self.epsilon  = 0.2
        #self.alpha    = 0.2

        #Deployment values
        self.epsilon  = 0.0
        self.alpha    = 0.0

        self.discount = 0.8


        #special variables for the states in Q table
        self.set_dict = {"West":0, "East":16, "North":32, "South":48, "North-West":64, "North-East":80, "South-West":96, "South-East":112}

        self.bool_dict = {

            "True, True, True, True": 0,
            "True, True, True, False": 1,
            "True, True, False, True": 2,
            "True, False, True, True": 3,
            "False, True, True, True": 4,
            "True, True, False, False": 5,
            "True, False, True, False": 6,
            "False, True, True, False": 7,
            "True, False, False, True": 8,
            "False, True, False, True": 9,
            "False, False, True, True": 10,
            "True, False, False, False": 11,
            "False, True, False, False": 12,
            "False, False, True, False": 13,
            "False, False, False, True": 14,
            "False, False, False, False": 15

        }


    @staticmethod
    def get_living_ghosts_positions(gameState):

        ghosts_positions = gameState.getGhostPositions()
        living_ghosts = gameState.getLivingGhosts() # Booleans
        living_ghosts_positions = [] #lista con las posiciones de los fantasmas vivos

        for ii, alive in enumerate(living_ghosts):
            if ii != 0: # Pacman es el agente en la posicion 0
                if alive:
                    living_ghosts_positions.append(ghosts_positions[ii-1])

        return living_ghosts_positions


    @staticmethod
    def get_food_positions(gameState):

        food_map = gameState.getFood()
        food_positions = []
        for ii, col in enumerate(food_map):
            for jj, row in enumerate(col):
                # If there is food on that position, append it
                if food_map[ii][jj]:
                    food_positions.append((ii, jj))

        return food_positions


    @staticmethod
    def get_wall_positions(gameState):

        wall_map = gameState.getWalls()
        walls_positions = []

        for ii, col in enumerate(wall_map):
            for jj, row in enumerate(col):
                # If there is food on that position, append it
                if wall_map[ii][jj]:
                    walls_positions.append((ii, jj))

        return walls_positions



    def format_state(self, gameState):
        """
        ESTA FUNCION COGE EL ESTADO DEL JUEGO DEL PACMAN Y LO TRANSFORMA EN EL ESTADO
        DEFINIDO PARA EL ALGORITMO Q-LEARNING. EN ESTE CASO, UN ESTADO SE IDENTIFICA POR LA TUPLA:
        (DIRECCION_OBJETIVO_MAS_CERCANO, PARED_OESTE, PARED_ESTE, PARED_NORTE, PARED_SUR)
        """

        self.original_gamestate = gameState

        pacman_position  = gameState.getPacmanPosition()


        #Para sacar en qué direccion se encuentra el fantasma más cercano:
        living_ghosts_positions = self.get_living_ghosts_positions(gameState)
        ghost_distances = [util.manhattanDistance(pacman_position, x) for x in living_ghosts_positions]


        #En el caso de que no queden fantasmas vivos
        if len(ghost_distances) == 0:
            return 'TERMINAL_STATE'


        # Para sacar las posiciones en las que se encuentran las bolas
        food_positions = self.get_food_positions(gameState)
        food_distances = [util.manhattanDistance(pacman_position, x) for x in food_positions]



        #Cuál es el objetivo que está mas cerca
        closest_ghost_distance = min(ghost_distances)


        # Si no hay comida
        if len (food_distances) == 0:

            closest_food_distance = 9999999999999
        else:

            closest_food_distance = min(food_distances)



        # Comparar distancia a comida y fantasma más cercanos
        if closest_ghost_distance > closest_food_distance:

            #Dónde está el punto de comida mas cercano
            closest_objective_pos = food_positions[food_distances.index(closest_food_distance)]

        else:

            #Dónde está el fantasma que está más cerca
            closest_objective_pos = living_ghosts_positions[ghost_distances.index(closest_ghost_distance)]
        


        #Evaluar posicion relativa del objetivo a pacman
        direcciones = []
        
        #el objetivo esta encima?
        if(pacman_position[1] < closest_objective_pos[1]): 
            direcciones.append("North")
        #el objetivo esta debajo?
        elif(pacman_position[1] > closest_objective_pos[1]):
            direcciones.append("South")

        #el objetivo esta a la izquierda?
        if(pacman_position[0] > closest_objective_pos[0]):
            direcciones.append("West")
        #el objetivo esta a la derecha?    
        elif(pacman_position[0] < closest_objective_pos[0]):
            direcciones.append("East")

        if len(direcciones)==2:
            orientacion = direcciones[0]+'-'+direcciones[1]
        else:
            orientacion = direcciones[0]



        #Mirar si hay una pared entre pacman y el objetivo mas cercano
        walls_positions = self.get_wall_positions(gameState)


        north_wall = False
        south_wall = False
        west_wall = False
        east_wall = False

        
        for wall_pos in walls_positions:

            
            if(pacman_position[1] < closest_objective_pos[1]):
                #evaluar hacia arriba
                if wall_pos[0] == pacman_position[0] and (wall_pos[1] in range(pacman_position[1], closest_objective_pos[1])):
                    #Si hay una pared entre medias
                    north_wall = True

            elif(pacman_position[1] > closest_objective_pos[1]):
                #evaluar hacia abajo
                if wall_pos[0] == pacman_position[0] and (wall_pos[1] in range(closest_objective_pos[1], pacman_position[1])):
                    #Si hay una pared entre medias
                    south_wall = True


            if(pacman_position[0] > closest_objective_pos[0]):
                #evaluar hacia la izquierda
                if wall_pos[1] == pacman_position[1] == closest_objective_pos[1] and (wall_pos[0] in range(closest_objective_pos[0], pacman_position[0])):
                    #Si hay una pared entre medias
                    west_wall = True

            elif(pacman_position[0] < closest_objective_pos[0]):
                #evaluar hacia la derecha
                if wall_pos[1] == pacman_position[1] == closest_objective_pos[1] and (wall_pos[0] in range(pacman_position[0], closest_objective_pos[0])):
                    #Si hay una pared entre medias
                    east_wall = True
        
        return (orientacion, west_wall, east_wall, north_wall, south_wall)
        

    def readQtable(self):
        "Read qtable from disc"

        self.table_file = open("qtable.txt", "r+") 

        table = self.table_file.readlines()
        q_table = []

        for i, line in enumerate(table):
            row = line.split()
            row = [float(x) for x in row]
            q_table.append(row)

        self.q_table = q_table


    def writeQtable(self):
        "Write qtable to disc"
        self.table_file.seek(0)
        self.table_file.truncate()
        for line in self.q_table:
            for item in line:
                self.table_file.write(str(item)+" ")
            self.table_file.write("\n")

        self.table_file.close()

            
    def printQtable(self):
        "Print qtable"
        for line in self.q_table:
            print(line)
        print("\n")    


    def computePosition(self, state):
        """
        Compute the row of the qtable for a given state.
        """

        #Calcular el set al que pertenece el estado (ver documentacion)
        state_set = self.set_dict[state[0]]
        
        #Calcular el offset dentro del set al que pertenece el estado
        booleans = str(state[1]) + ", " + str(state[2]) + ", " +  str(state[3]) + ", " + str(state[4])
        offset = self.bool_dict[booleans]

        return state_set + offset


    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        position = self.computePosition(state)
        action_column = self.actions[action]

        return self.q_table[position][action_column]


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        if state == 'TERMINAL_STATE':
          return 0

        return max(self.q_table[self.computePosition(state)])


    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        if state == 'TERMINAL_STATE':
          return None

        legalActions = [x for x in self.original_gamestate.getLegalActions() if x != 'Stop']

        best_actions = [legalActions[0]]


        best_value = self.getQValue(state, legalActions[0])
        for action in legalActions:
            value = self.getQValue(state, action)
            if value == best_value:
                best_actions.append(action)
            if value > best_value:
                best_actions = [action]
                best_value = value

        return random.choice(best_actions)


    def getAction(self, gameState):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.
        """

        #ESTA FUNCION ES LA PRINCIPAL LLAMADA POR EL BUCLE PRINCIPAL DEL JUEGO


        # Pick Action
        legalActions = [x for x in gameState.getLegalActions() if x != 'Stop']
        action = None

        if len(legalActions) == 0:
             return action

        flip = util.flipCoin(self.epsilon)

        if flip:
            return random.choice(legalActions)


        #Interpretar un estado como se ha difinido para el algoritmo Q-Learning
        state = self.format_state(gameState)


        return self.getPolicy(state)


    def update(self, state, action, nextState, reward):
        """
        The parent class calls this to observe a
        state = action => nextState and reward transition.
        You should do your Q-Value update here

        Q-Learning update:

        if terminal_state:
        Q(state,action) <- (1-self.alpha) Q(state,action) + self.alpha * (r + 0)
        else:
        Q(state,action) <- (1-self.alpha) Q(state,action) + self.alpha * (r + self.discount * max a' Q(nextState, a'))

        """

        print("Next state score: ", nextState.getScore())
        print("Current state score: ", state.getScore())

        #interpret states
        currentState = self.format_state(state)
        nextState = self.format_state(nextState)


        print("Started in state: "+str(currentState)+
                "\nTook action: "+str(action)+
                "\nEnded in state: "+str(nextState)+
                "\nGot reward: "+str(reward)+
                "\nDiscount rate: "+str(self.discount)+"\n")

       
        # TRACE for transition and position to update. Comment the following lines if you do not want to see that trace
        print("Update Q-table with transition: ", currentState, action, nextState, reward)
        
        position = self.computePosition(currentState)
        action_column = self.actions[action]
        
        print("Corresponding Q-table cell to update:", position, action_column)


        if currentState == 'TERMINAL_STATE':
            self.q_table[position][action_column] = (1-self.alpha)*self.q_table[position][action_column] + (self.alpha * (reward + 0))
        else:
            self.q_table[position][action_column] = (1-self.alpha)*self.q_table[position][action_column] + (self.alpha * (reward + (self.discount * self.computeValueFromQValues(nextState))))


    def getPolicy(self, state):
        "Return the best action in the qtable for a given state"
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        "Return the highest q value for a given state"
        return self.computeValueFromQValues(state)



class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"

        feats = self.featExtractor.getFeatures(state, action)
        for f in feats:
          self.weights[f] = self.weights[f] + self.alpha * feats[f]*((reward + self.discount * self.computeValueFromQValues(nextState)) - self.getQValue(state, action))

        # util.raiseNotDefined()

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
