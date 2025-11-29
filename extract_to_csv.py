import os
import csv
import numpy as np

# Base directory containing generation folders
base_dir = 'test_ga'  # Update this path to match your experiment directory

# Output CSV file
output_csv = 'traverser_ga_solution.csv'

# Headers for the CSV file
headers = ['Run', 'Fitness', 'Solution']

# Function to convert a solution vector to binary
def solution_to_binary(solution_vector):
    """
    Convert a solution vector to a binary string.
    """
    binary_vector = []
    for value in solution_vector.flatten():  # Flatten the array to handle 2D arrays
        # Convert each value to binary (assuming it's a float or integer)
        binary_value = ''.join(f'{byte:08b}' for byte in np.array(value, dtype=np.float32).tobytes())
        binary_vector.append(binary_value)
    return ' '.join(binary_vector)

# Open the CSV file for writing
with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)  # Write headers

    # Iterate through each generation folder
    for generation in sorted(os.listdir(base_dir)):
        if generation.startswith('generation_'):
            generation_dir = os.path.join(base_dir, generation)
            output_file = os.path.join(generation_dir, 'output.txt')

            # Check if the output.txt file exists
            if os.path.exists(output_file):
                # Read the fitness values from output.txt
                with open(output_file, 'r') as f:
                    lines = f.readlines()

                # Extract the fitness values and robot IDs
                for line in lines:
                    robot_id, fitness = line.strip().split()
                    robot_id = int(robot_id)
                    fitness = float(fitness)

                    # Load the solution vector from the corresponding .npz file
                    structure_file = os.path.join(generation_dir, 'structure', f'{robot_id}.npz')
                    if os.path.exists(structure_file):
                        with np.load(structure_file) as data:
                            solution_vector = data['arr_0']  # Use 'arr_0' as the solution vector
                        solution_binary = solution_to_binary(solution_vector)
                    else:
                        solution_binary = 'N/A'  # Handle missing structure file

                    # Write the data to the CSV file
                    run_number = int(generation.split('_')[1])  # Generation number as Run
                    writer.writerow([
                        run_number+1,
                        fitness,
                        solution_binary
                    ])

print(f'All robots\' fitness and solution vectors have been saved to {output_csv}')