<h1 align="center">
  
![download](https://github.com/user-attachments/assets/e9d5fe35-4a52-4746-923d-cc1eccbe2cbd)
![download](https://github.com/user-attachments/assets/27ab19f8-bbf5-45db-8b53-9586feef66c7)

Genetic Algorithm - Matching 

  <br>
</h1>

<h4 align="center"> A Genetic Algorithm project focuses on "Matching" for Computational Biology course, Bar-Ilan University.


<p align="center">
  <a href="#description">Description</a> •
  <a href="#solution-representation">Solution Representation</a> •
  <a href="#algorithm">Algorithm</a> •
  <a href="#running-samples">Running Samples</a> •
  <a href="#installing-and-executing">Installing And Executing</a> •
  <a href="#author">Author</a> 
</p>

## Description

This project implements a genetic algorithm to solve the Stable Marriage Problem, also known as the Marriage Matching Problem. The goal is to find an optimal matching between 30 men and 30 women, based on their individual preferences.

### Key Features

1. **Data Processing**: The program reads preference data from a file named 'GA_input.txt', where each individual ranks all members of the opposite sex.

2. **Genetic Algorithm Implementation**:
    * Solution Representation: Each chromosome represents a complete matching of all pairs.
    * Fitness Function: Evaluates the quality of each matching based on overall satisfaction and stability.
    * Crossover: Implements a method to combine two parent solutions to create offspring.
    * Mutation: Introduces random changes to maintain genetic diversity.
    * Selection: Chooses the fittest individuals for the next generation.

3. **Optimization**: The algorithm runs for multiple generations, evolving better solutions over time.
   
4. **Convergence Handling**: Implements strategies to avoid premature convergence to local optima.
   
5. **Result Visualization**: Generates graphs showing the best, worst, and average fitness scores across generations
   
6. **Parameter Tuning**: Explores different combinations of population size and number of generations (with their product being 18,000) to find the most efficient configuration.

This project demonstrates key concepts in computational biology and optimization, including genetic algorithms, combinatorial optimization, and the application of evolutionary principles to solve complex matching problems. It provides insights into how biological-inspired algorithms can be used to tackle problems in social sciences and economics.

## Solution Representation

Our presentation of solution is an array  𝐴. The  index 𝑖 represent the man 𝑖  + 1, and 𝐴[𝐼] represent the woman i + 1.
For example:

A = [5, 4, 6, 1, 3, 2]

In the array above, man 1 (index 0) is matched with woman 5, and man 3 (index 2) is matched with woman 6. Of course, solution is valid if and only if the values in the array are all different and ranged between 1 to size_of_array (included). 


### Evaluation Function

First, we assume we get the preferences matrix for each sex, so the row represent a specific man/woman and the column represents what position the man/woman gave to a specific person. For example: If 𝑚𝑒𝑛_𝑝𝑟𝑒𝑓[2][5] = 4 so man 3 (𝑖+1) ranked woman 6 (𝑖+1) as his 4th preference.
If wo𝑚𝑒𝑛_𝑝𝑟𝑒𝑓[5][4] = 5 so woman 6 (𝑖+1) ranked man 5 (𝑖+1) as her 5th preference.

We calculate the rank of a solution by looking at each index 𝑖 in the solution. for index 𝑖 (man 𝑖+1), We check what position the value 𝐴[𝑖 −1] (the woman he matched with) is in the man preferences array (𝑚𝑒𝑛_𝑝𝑟𝑒𝑓[𝑖][𝐴[𝑖]] == 𝐴[𝑖]), and we add A[i] to the rank. After that, we check where 𝑖 (man 𝑖+1) is located in the woman preferences array (𝑤𝑜𝑚𝑒𝑛_𝑝𝑟𝑒𝑓[𝐴[𝑖]] == 𝐼 + 1), and than adding it to the rank.

For example:

A = [5, 4, 6, 1, 3, 2]

For this array, we look at man 1 in index 0. We can see he was matched with woman 5. Therefore, we look at the 𝑚𝑒𝑛_𝑝𝑟𝑒𝑓[0], and check what position is number 5. For this example, lets say 𝑚𝑒𝑛_𝑝𝑟𝑒𝑓[0][3] == 5. Than, we add 4 to the rank, because man 1 positioned woman 5 in the 4th position.
After that, we see that for 𝑤𝑜𝑚𝑒𝑛_𝑝𝑟𝑒𝑓[4][7] == 1, it means woman 5 positioned man 1 in the 8th place, so we add 8 to the rank.

As we can see, the minimal rank that can be achieved in a set of 60 people is 60 (all people receive their requests), and the maximal rank is 1800 (each person received his/her last preference, so 60 ∗ 30 = 1800). 

As we can see, lower rank is better. Therefore, after we calculate the rank, we normalize it by this formula:

![11](https://github.com/user-attachments/assets/1f8828ef-edef-4945-bb51-e4d0393d8935)

This normalized rank is ranged between 0 to 100. because we subtract the result from 100, we receive that a higher rank is better, of course while maintaining the rank original solution. Of course, we do not know the best or worst possible ranks regard to the preference matrix (if we did, we didn’t have to rank them…), so the values represent the rank compared to a best possible solution.

In addition, we calculate the probability of all solutions to be selected. We do it while using softmax algorithm with a temperature parameter β.

<img src="https://github.com/user-attachments/assets/04c2aa6b-31bf-4b2a-9ed8-c017133a565a" alt="init" width="500"/>
<img src="https://github.com/user-attachments/assets/f11c0a46-dbc7-4010-8c17-8cef12a32f69" alt="init" width="300"/>

The softmax algorithm receive a vector of our ranks, and return a probability distribution of the vector it received. We use the temperature parameter β to efficiently distribute the probabilities, and to enhance the values of the larger elements (that we want to be selected).


## Algorithm

### Elitism

Between each iteration, we set an elitism rate of 3 precent (%, rounded). This means that the best ranked 3% from all solutions will automatically move to the next phase.

### Mutations

We set the mutations rate to 20 precent. The mutation creation operation is that given a solution array, we randomly swap T times two values in the solution array (T is dynamically determined, will  be explained later in this report).


### Crossovers

We perform the crossovers on the remaining 77% of the solutions (the code is highly flexible for changes in any value, including the number of people, elitism or mutation rate).

we randomly choose 2 solutions from the remaining solution array, based on each solution probability that we calculated during the rank calculation (using softmax). 
 
Than, we divided both solutions into two halves. The first half of the solution is derived from the first parent, and the second half of the solution is derived from the second parent. After that, we validate our solution. If the validation found an error (duplicate), we search for a valid member (one we didn’t encounter yet) from the second parent.

We do It from the second parent to keep the new solution based on the first two parents.


### Early convergence

To deal with the early convergence, we decided to use an algorithm from the networks world. The algorithm is RTT Round-Trip delay. 

<img src="https://github.com/user-attachments/assets/ccc3a984-80e8-4eb2-8be2-e335fff704c7" alt="init" width="500"/>

The algorithm suppose to delay (increase!) the time a computer is waiting for an acknowledgement for a message (ping, packet, etc.) he sent. It’s important that  0< 𝛼<  1, we set it to 0.9. In our case, we use this formula to determine T – The amount of swaps we perform in each mutation for a given iteration.

Our samples are the average ranks evaluated in the iteration. We call this parameter “mutation-rate”. So, when the RTT difference was small, we increased the mutation-rate, and when it was high, we lowered the mutation rate! Since we start with a low value of mutation-rate, we climb up pretty low due to the minor changes in the average parameter. We also kept it below 16 not to perform a new random solution. The increase and decrease where by factor of 1.1 and 0.9 accordingly. 


## Running Samples

In this example, we made 3 runs. Each run has 100 iterations and 180 solutions. 
We can see that the worst solution in all 3 runs is extremely unstable, this is due to the mutation percentage. The average solution is relatively stable, but shows a linear incline. The best solution is the gradually changing in all iterations, reaching around 83% success.

<img src="https://github.com/user-attachments/assets/341a99c7-2110-4b1a-8bb5-18d823aef4a2" alt="init" width="500"/>

This is single run, reaching around 84% success.  We can see the best run has some convergence between iteration 22 to iteration 85. We can assume that due to the mutation rate increasing, the best solution increasing in addition.

<img src="https://github.com/user-attachments/assets/6d3bc758-45b6-47c2-9ad5-df3621a416e2" alt="init" width="500"/>

Here, we can see different combinations of solution number and iteration. The first run is 100 iterations and 180 solutions, the second is 150 iterations and 120 solutions, and the last run is 200 iterations with 90 solutions.
We notice that in the first run, the best solution is achieved after the full 100 iterations, what made it call to the evaluation function around 18,000 times.

<img src="https://github.com/user-attachments/assets/9a02200f-ab8a-4fa5-ada7-1059acb4b860" alt="init" width="500"/>

In the second run, the best solution was achieved after 45 iterations, what makes it 45*120 = 5,400 calls to the evaluation function. The third run, converged to the best solution after around 30 iteration, what makes it 30 * 90 2,700 calls to the evaluation function.
In conclusion, we can say that in our case, the best combination was run 3 with 90 solutions and 200 iterations.


## Installing And Executing
  
You can use [Git](https://git-scm.com). From your command line:

```bash
# Clone this repository.
$ git clone https://github.com/TalMizrahii/Genetic-Algorithm-Matching

# Go into the repository.
$ cd Genetic-Algorithm-Matching

# Run the program
$ GeneticAlgorithmMatching.exe

```
## Author

* [@Tal Mizrahi](https://github.com/TalMizrahii)
* Taltalon1927@gmail.com
