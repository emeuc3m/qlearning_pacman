# qlearning_pacman

## Pacman trained with aproximate q-learning algorithm, using UC Berkeley CS188 Intro to AI Pacman's implemetation.

States are represented as a tuple containing the direction of the closest ghost or food dot and four booleans set to True if there is a wall
between the pacman and the closest objective.

The reward-function is just the rewards given by the game.

To do:
- [ ] Negative reward for getting closer to the ghost, so that it goes around tricky walls.

## Execution instructions 
To run the code, please first pip install the following dependencies:

pip3 install future
pip3 install tkinter

Keep in mind you may need to install some other dependency.

Some errors may happen when running in linux, so windows is recommended.

Finally, acces the folder "pacman" and run the following command:

`python3 busters.py -k 3 -l labAA1 -p QLearningAgent`

You can change the layout to any of the ones found in the folder _layouts_ , the -k flag needs to be adjusted to the number of ghosts in that layout.

You can train the model furthermore by adding -n and the number of desired trainning episodes. You will need to change the values of alpha and epsilon 
in the file _qlearningAgents.py_ .


