import random
import numpy as np
import tkinter as tk


def load_pref_file(filename):
    # Open tge
    with open(filename, 'r') as file:
        lines = file.readlines()
    # Convert lines to a NumPy array
    preferences = np.array([[int(x) for x in line.split()] for line in lines])
    # Check that the number of lines is even
    num_lines = len(lines)
    if num_lines % 2 != 0:
        raise ValueError("The number of lines in the file must be even.")

    # Calculate the midpoint
    midpoint = num_lines // 2
    # Return the two halves of the preferences array
    return preferences[:midpoint], preferences[midpoint:]


def create_random_solution(num_of_entries):
    # Generate a list of random numbers from 1 to 30 without repetition
    random_solution = random.sample(range(1, num_of_entries + 1), num_of_entries)
    return random_solution


def create_solutions(group_size, num_of_solutions):
    # Check validity of the params.
    if num_of_solutions <= 0 or group_size <= 0:
        return None

    # Set an empty array solution.
    solutions_generated = []

    # Create solutions.
    for i in range(num_of_solutions):
        solutions_generated.append(create_random_solution(group_size))

    # Return the solutions.
    return np.array(solutions_generated)


def evaluate_single_solution(solution, men_pref, women_pref, solution_size):
    # Set the rank.
    rank = 0

    # Calculate the rank.
    for i in range(solution_size):
        # The woman to check the match with.
        woman = solution[i]

        # The array of the man to check (man i+1 but in indexed in the men prefs so i).
        man_arr = men_pref[i]
        women_arr = women_pref[woman - 1]

        # Extract the location of the woman in the man array.
        indices = np.where(man_arr == woman)[0]
        woman_index = indices[0] + 1

        # Extract the location of the man in the woman array.
        indices = np.where(women_arr == i + 1)[0]
        man_index = indices[0] + 1

        # Add to the rank.
        rank += (woman_index + man_index)

    # Return the rank.
    return rank


def softmax(x, temperature=0.8):
    x = np.array(x)
    e_x = np.exp((x - np.max(x)) / temperature)
    return e_x / e_x.sum()


def evaluate_solutions(solutions, men_preferences, women_preferences, rank_num):
    # Set the ranks.
    ranks = []

    # Set the rank sum.
    rank_sum = 0

    # Calculate the rank for each solution.
    for solution, rank, prob in solutions:
        # Calculate the rank.
        single_rank = evaluate_single_solution(solution, men_preferences, women_preferences, rank_num)
        # Add to the rank sum.
        rank_sum += single_rank
        # Append the rank.
        ranks.append((solution, single_rank, prob))

    # Sort the ranks.
    ranks.sort(key=lambda x: x[1])

    # Normalize the ranks.
    normalized_ranks = []

    # Calculate the max rank.
    min_rank = rank_num * 2
    max_rank = min_rank * rank_num * 2

    # Calculate initial probabilities.
    initial_probs = []
    for solution, rank, probs in ranks:
        normalized_rank = 100 - ((rank - min_rank) / (max_rank - min_rank)) * 100
        initial_prob = (rank_sum - rank) / rank_sum
        normalized_ranks.append((solution, normalized_rank, initial_prob))
        initial_probs.append(initial_prob)

    # Apply softmax to the initial probabilities.
    softmax_probs = softmax(np.array(initial_probs))

    # Update normalized_ranks with softmax probabilities.
    normalized_ranks = [(sol, norm_rank, softmax_prob) for (sol, norm_rank, _), softmax_prob in
                        zip(normalized_ranks, softmax_probs)]
    return normalized_ranks


def crossover_mutations(mutations, arr_size, swaps):
    array_amount = len(mutations)

    for i in range(array_amount):
        for _ in range(swaps):
            # Get distinct random indices
            randx, randy = random.sample(range(arr_size), 2)

            # Swap values
            mutations[i][0][randx], mutations[i][0][randy] = mutations[i][0][randy], mutations[i][0][randx]

    return mutations


def weighted_random_choice(items, weights, k, temperature=0.02):
    # Normalize the weights.
    weights = softmax(weights, temperature)

    # Validate the weights.
    weights_sum = np.sum(weights)

    # Adjust the weights if the sum is not 1. Add the difference to the last weight.
    if weights_sum > 1:
        weights[-1] += 1 - weights_sum
    # Adjust the weights if the sum is less than 1. Add the difference to the first weight.
    elif weights_sum < 1:
        weights[0] += 1 - weights_sum

    # Choose k items.
    chosen_indices = np.random.choice(len(items), size=k, replace=False, p=weights)

    # Return the chosen items and their indices.
    return [items[i] for i in chosen_indices], chosen_indices


def crossover_creation(crossover_arr, rank_num, num_crossover):
    new_solutions = []

    # Perform crossover to create num_crossover new solutions.
    while len(new_solutions) < num_crossover:
        # Randomly select two solutions from crossover_arr based on their probabilities.
        solution1, solution2 = weighted_random_choice(crossover_arr, [item[2] for item in crossover_arr], 2)[0]

        # Perform crossover operation.
        new_solution = crossover_operation(solution1[0], solution2[0], rank_num)

        # Add the new solution to the list with default rank and probability.
        new_solutions.append((new_solution, 0, 0))

    return new_solutions


def crossover_operation(solution1, solution2, rank_num):
    # Half the size of the solution
    half_size = rank_num // 2

    # Perform crossover by combining half of solution1 and half of solution2
    new_solution = solution1[:half_size] + solution2[half_size:]

    # Ensure the new solution is valid (contains all unique elements)
    new_solution = validate_solution(new_solution, rank_num)

    return new_solution


def validate_solution(solution, rank_num):
    # Convert the solution to a set to remove duplicates
    solution_set = set(solution)

    # Ensure all elements are between 1 and rank_num and unique
    while len(solution_set) < rank_num:
        # Generate a new random solution if duplicates are found
        solution = random.sample(range(1, rank_num + 1), rank_num)

        solution_set = set(solution)

    return solution


def calculate_rank_stats(current_ranks):
    # Sort the ranks in descending order
    current_ranks_sorted = sorted(current_ranks, reverse=True, key=lambda x: x[1])

    # Get the best, median, and worst ranks
    best_rank = current_ranks_sorted[0][1]
    worst_rank = current_ranks_sorted[-1][1]
    median_rank = current_ranks_sorted[len(current_ranks_sorted) // 2][1]

    # Calculate the average rank
    total_rank = sum(rank[1] for rank in current_ranks)
    average_rank = total_rank / len(current_ranks)

    return best_rank, median_rank, worst_rank, average_rank


def crossover(iters, solutions, men_preferences, women_preferences, rank_num, solution_number, elitism_percent=10,
              mutation_percent=10):
    current_ranks = solutions
    mutation_rate = 0.1
    average_rank_history = []

    # Save the best solution, worst solution, and average solution.
    best_solutions = []
    worst_solutions = []
    average_solutions = []
    # Get the initial best solution.
    best_solution = solutions[0]

    for _ in range(iters):
        current_ranks = evaluate_solutions(current_ranks, men_preferences, women_preferences, rank_num)

        best_rank, median_rank, worst_rank, average_rank = calculate_rank_stats(current_ranks)
        average_rank_history.append(average_rank)

        best_solutions.append(best_rank)
        worst_solutions.append(worst_rank)
        average_solutions.append(average_rank)

        if len(average_rank_history) > 1:
            EstimatedRTT = (1 - mutation_rate) * average_rank_history[-2] + mutation_rate * average_rank
            if average_rank >= EstimatedRTT:
                mutation_rate *= 1.1
            else:
                mutation_rate *= 0.9

        num_elitism = solution_number * elitism_percent // 100
        num_mutations = solution_number * mutation_percent // 100
        num_crossover = solution_number - num_elitism - num_mutations

        probabilities = [item[2] for item in current_ranks]

        elitism_arr = current_ranks[:num_elitism]

        remaining_solutions = current_ranks[num_elitism:]
        remaining_probabilities = probabilities[num_elitism:]
        crossover_arr, chosen_indices = weighted_random_choice(remaining_solutions, remaining_probabilities,
                                                               num_crossover)

        remaining_indices = set(range(len(current_ranks))) - set(range(num_elitism)) - set(
            num_elitism + chosen_indices)
        remaining_indices = list(remaining_indices)[:num_mutations]

        mutations_arr = [current_ranks[idx] for idx in remaining_indices]
        mutation_rate = (round(mutation_rate) % 15) + 1

        mutations_arr = crossover_mutations(mutations_arr, rank_num, mutation_rate)
        crossover_arr = crossover_creation(crossover_arr, rank_num, num_crossover)

        num_solution_test = len(crossover_arr) + len(mutations_arr) + len(elitism_arr)
        gap_solutions = []
        if num_solution_test < solution_number:
            gap_solutions = create_solutions(rank_num, solution_number - num_solution_test)
            gap_solutions = [(np.array(solution), 0, 0) for solution in gap_solutions]

        current_ranks = elitism_arr + crossover_arr + mutations_arr + gap_solutions

        best_solution = evaluate_solutions(current_ranks, men_preferences, women_preferences, rank_num)[0]

    return best_solution[0], best_solutions, worst_solutions, average_solutions


def init_ranks(solutions, solution_size):
    # Set the initial normalized ranks.
    init_normalized = []

    # Calculate the max rank.
    max_rank = solution_size * solution_size * 2

    # Calculate the probability.
    probability = 1 / solution_size

    # Normalize the ranks.
    for solution in solutions:
        # Convert the solution to a NumPy array.
        solution_array = np.array(solution)
        # Append the solution, max rank, and probability to the normalized list.
        init_normalized.append((solution_array, max_rank, probability))

    # Return the initial normalized ranks.
    return init_normalized


def run_ga(iterations):
    solution_num = 18000 // iterations
    print(f"Running Genetic Algorithm with {iterations} iterations and {solution_num} solutions")
    men_prefs, women_prefs = load_pref_file('./GA_input.txt')
    rank_size = len(men_prefs)
    init_solutions = create_solutions(rank_size, solution_num)
    init_normalized_ranks = init_ranks(init_solutions, rank_size)
    return crossover(iterations,
                     init_normalized_ranks,
                     men_prefs,
                     women_prefs,
                     rank_size,
                     solution_num,
                     elitism_percent=1,
                     mutation_percent=20)


def plot_results(results, canvas):
    # Clear previous drawings on the canvas
    canvas.delete("all")

    # Define plot parameters
    width = 600
    height = 400
    padding = 50

    # Determine the number of iterations
    num_iterations = len(results[0][0])  # Assuming all results have the same length

    # Determine x-axis scaling
    x_scale = (width - 2 * padding) / num_iterations

    # Find maximum and minimum y-values across all runs
    all_y_values = [value for result in results for y_values in result for value in y_values]
    min_y = min(all_y_values)
    max_y = max(all_y_values)
    y_range = max_y - min_y

    # Function to map y-values to canvas coordinates
    def map_y(y):
        return height - padding - (y - min_y) * (height - 2 * padding) / y_range

    # Draw axes
    canvas.create_line(padding, padding, padding, height - padding, width=2)  # y-axis
    canvas.create_line(padding, height - padding, width - padding, height - padding, width=2)  # x-axis

    # Plot each result
    colors = ['blue', 'red', 'green']  # Colors for best, worst, average
    for i, result in enumerate(results):
        for j, y_values in enumerate(result):
            color = colors[j]
            for k in range(1, len(y_values)):
                x1 = padding + (k - 1) * x_scale
                y1 = map_y(y_values[k - 1])
                x2 = padding + k * x_scale
                y2 = map_y(y_values[k])
                canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

    # Add labels
    canvas.create_text(padding, padding // 2, text='Iterations', anchor='w', font=('Arial', 12))
    canvas.create_text(padding // 2, height // 2, text='Values', anchor='w', font=('Arial', 12), angle=90)

    # Add legend
    legend_y = padding
    for j, label in enumerate(['Best', 'Worst', 'Average']):
        legend_x = width - padding - 100
        canvas.create_rectangle(legend_x, legend_y + j * 20, legend_x + 20, legend_y + j * 20 + 20, fill=colors[j])
        canvas.create_text(legend_x + 30, legend_y + j * 20 + 10, text=label, anchor='w', font=('Arial', 12))

    # Update canvas
    canvas.update()


def run_gui():
    def start_algorithm():
        running_label.config(text="Running...", font=('Arial', 14))
        root.update_idletasks()

        iterations = 100
        results = []
        best_high = []

        # Run the genetic algorithm for the specified number of iterations
        for _ in range(1):  # Run 1 time
            best_sol, best_sols, worst_sols, average_sols = run_ga(iterations)
            results.append((best_sols, worst_sols, average_sols))
            best_high.append((best_sol, best_sols[-1]))

        # Display best solutions
        plot_results(results, canvas)

        best_solutions_text = "\n".join(f"Run {i + 1}: Best Solution: {best_sol}, Rank: {best_rank}"
                                        for i, (best_sol, best_rank) in enumerate(best_high))
        best_sol_label.config(text=f'Best Solutions:\n{best_solutions_text}', font=('Arial', 12, 'bold'),
                              justify=tk.LEFT, anchor='w', padx=10, pady=10, bg='lightgray')

        running_label.config(text="")

    root = tk.Tk()
    root.title('Genetic Algorithm Optimization')

    # Increase size of the GUI window
    root.geometry('1000x700')  # Width x Height

    # Add some padding and margins
    root.configure(padx=20, pady=20)

    start_button = tk.Button(root, text='Start Algorithm', font=('Arial', 14), command=start_algorithm)
    start_button.pack(pady=10)

    running_label = tk.Label(root, text='', font=('Arial', 14))
    running_label.pack()

    best_sol_label = tk.Label(root, text='Best Solutions: ', font=('Arial', 14))
    best_sol_label.pack(pady=10, fill='both')

    # Create a canvas for drawing the plot
    canvas = tk.Canvas(root, width=600, height=400, bg='white')
    canvas.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    run_gui()