<h1 align="center">
  

![download](https://github.com/user-attachments/assets/a76303db-d2e3-4714-889b-25fa8d9f2880)

Genetic Algorithm - Matching 

  <br>
</h1>

<h4 align="center"> A Genetic Algorithm project focuses on "Matching" for Computational Biology course, Bar-Ilan University.


<p align="center">
  <a href="#description">Description</a> •
  <a href="#solution-representation">Solution Representation</a> •
  <a href="#hyperparameters">Hyperparameters</a> •
  <a href="#grid-size-selection">Grid Size Selection</a> •
  <a href="#results">Results</a> •
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

### 


### 


### 




## Hyperparameters


### Decay Functions



## Grid Size Selection: 

The digits dataset typically consists of 28x28 pixel images, resulting in 784-dimensional input vectors (since each pixel is a feature). A 10x10 SOM means there are 100 neurons in total, each with a weight vector of dimension 784. This setup allows each neuron to potentially capture a distinct pattern or cluster within the digit dataset.

Therefore, the grid size should be large enough to capture the variability and complexity present in the dataset. For digits 0 to 9, which have distinct visual patterns but variations in writing style, a 10x10 grid can provide sufficient resolution to differentiate between different digits.

A 10x10 grid strikes a balance between computational feasibility and adequate representation of the dataset. To conclude, 10x10 grid size is generally a good fit because it allows for effective clustering and visualization of digit patterns. Each neuron in the SOM can represent a distinct digit or a group of similar digits.

## Results

For the output of the model, we used Both suggested representation, in addition to a heatmap. On the left grids, we can see the SOM’s grid.

The grid contains the vector resulted, represented as a photo. Above each photo, we added what is the true label of the photo (how close it to the closest vector from digits_keys.csv file), and the percentage of entries that were mapped to this neuron.

The heatmap represent the color-coded from white (0% accuracy) to red (100% accuracy). Each cell contains the classification accuracy for data points mapped to that neuron.
This heatmap reveals how well each neuron performs in correctly identifying digits. This combined visualization allows for a comprehensive understanding of the SOM's performance, showing both the learned representations and the accuracy of classification across the map. 


<img src="https://github.com/user-attachments/assets/3c2f5a00-9899-4c38-a155-7a132671b7b5" alt="init" width="500"/>

In this 300 iterations run, we can see a very dense high accuracy on the corners of the heatmap, which perfectly coordinates with the clear, not blurred neurons of 6, 1 and 2. 

<img src="https://github.com/user-attachments/assets/62b13838-f324-4912-9fac-f6798e38e195" alt="init" width="500"/>
<img src="https://github.com/user-attachments/assets/8eaff925-5b55-48c3-98cb-944c178826c9" alt="init" width="500"/>

As we can see, when we increase the number of iterations, more and more accurate cells are presented in the heatmap. Compared to the 300 and 600 iteration’s runs, the 1200 is starting to fill almost all grid with accurate cells. 
On the other hand, in the 1,200 iteration’s run there ‘not accurate’ cells are much blurred and unclear. This is due to the transaction between cells. As the SOM learns, it creates smoother transitions between neighboring neurons, which can lead to less distinct representations in boundary areas or regions of uncertainty.

<img src="https://github.com/user-attachments/assets/1d403bfe-d72b-4b2c-a159-798ea16798e9" alt="init" width="500"/>

In this example, we ran the program for 10,000 iterations. We can clearly see this is the best run so far, not surprising due to our explanation about the connection between number of iterations to the SOM’s clarity. Of course, a perfect SOM is one with full red heatmap, but it would probably take forever on our PC’s. We can still see very white cells, like cell [2,9]. This is (as explained above) a result of two neighbors pulling each side of this cell to change it, but the overall result is excellent! This is also why we chose this solution as our final result.

### Comparing to non-batching method

<img src="https://github.com/user-attachments/assets/68fb275c-4090-4d4b-8996-dd581695cf08" alt="init" width="500"/>

To compare batch and non-batched methods, we can see the difference between the two pairs of images from the previous section to this section. Both runs has approximately the same amount of calls to the update function (~100k).
The accuracy heatmap shows a wider range of accuracy values with several cells having lower accuracy (e.g., 0.23, 0.26, 0.27).
There are noticeable cells with accuracy below 50%, indicating areas where the model was less efficient then the batch model.

## Installing And Executing
  
You can use [Git](https://git-scm.com). From your command line:

```bash
# Clone this repository.
$ git clone https://github.com/TalMizrahii/Self-Organizing-Map

# Go into the repository.
$ cd Self-Organizing-Map

# Run the program from the release section
$ SelfOrganizingMap.exe

```
## Author

* [@Tal Mizrahi](https://github.com/TalMizrahii)
* Taltalon1927@gmail.com
