################# MAPAS PRUEBAS #################


#python3 busters.py -k 1 -l labAA1 -p QLearningAgent -n 50

#cp qtable.txt ../q_tables_learning/qtable_labAA1.txt

#python3 busters.py -k 2 -l labAA2 -p QLearningAgent -n 50

#cp qtable.txt ../q_tables_learning/qtable_labAA1_AA2.txt

#python3 busters.py -k 3 -l labAA3 -p QLearningAgent -n 100

#cp qtable.txt ../q_tables_learning/qtable_labAA1_AA2_AA3.txt

#rm -r ../q_tables_learning/qtable_labAA1_AA2_AA3_AA4.txt
#rm -r ../q_tables_learning/qtable_labAA1_AA2_AA3_AA4_AA5.txt

#cp ../q_tables_learning/qtable_labAA1_AA2_AA3_AA4.txt qtable.txt

#python3 busters.py -k 3 -l labAA4 -p QLearningAgent -n 50

#cp qtable.txt ../q_tables_learning/qtable_labAA1_AA2_AA3_AA4.txt

#python3 busters.py -k 3 -l labAA5 -p QLearningAgent -n 50

#cp qtable.txt ../q_tables_learning/qtable_labAA1_AA2_AA3_AA4_AA5.txt


################# MAPAS REALES #################

cp ../q_tables_learning/qtable_labAA1_AA2_AA3_AA4_AA5.txt qtable.txt 

python3 busters.py -k 3 -l capsuleClassic -p QLearningAgent -n 10

python3 busters.py -k 3 -l contestClassic -p QLearningAgent -n 10

python3 busters.py -k 2 -l mediumClassic -p QLearningAgent -n 10

python3 busters.py -k 1 -l mediumGrid -p QLearningAgent -n 10

python3 busters.py -k 3 -l minimaxClassic -p QLearningAgent -n 10

python3 busters.py -k 4 -l oneHunt -p QLearningAgent -n 10

python3 busters.py -k 1 -l openClassic -p QLearningAgent -n 10

python3 busters.py -k 4 -l originalClassic -p QLearningAgent -n 10

python3 busters.py -k 2 -l smallClassic -p QLearningAgent -n 10

python3 busters.py -k 1 -l smallGrid -p QLearningAgent -n 10

python3 busters.py -k 1 -l testClassic -p QLearningAgent -n 10

python3 busters.py -k 2 -l trappedClassic -p QLearningAgent -n 10


cp qtable.txt ../q_tables_learning/qtable_final.txt