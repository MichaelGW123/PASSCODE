# Michael Williamson
# Masters Research
# Calculating percent of file found in other file

# Importing Libraries

from matplotlib import pyplot as plt
import numpy as np
from pathlib import Path
import time

beginning = time.time()

# Flags for testing or modification purposes
# Set true when testing functionality (better with small test sets)
tester_flag = False
# True to show graph (see changing to graph format), false to save
show_flag = False

# Specific Input of Target and Generated Files
target_file_name = 'words90to100'  # specific file name
generated_lower_file_name = 'words80to90'  # lower entropy set file
# True if generated was trained off the same entropy as target, False if lower
same_file_flag = False
model_run = 2
"""For the Input runs, there will be 4 for each entropy set (only 2 for the lowest and highest).
The first will be different Entropy - Markov, then different Entropy - RNN.
3rd and 4th will be same Entropy - Markov and same Entropy - RNN respectively.
The model_run flag changes each run, 1 for Markov, 2 for RNN. The same_file_flag
changes once for each new target_file_name after 2 runs (one with Markov, one with RNN) 
starting with false for 2 runs, before switching to true for 2 runs.
This ordering helps keep the output document organized which allows for speedier access to
specific results."""

if model_run == 1:  # Name of model for saving/labeling purposes
    generating_model = 'Markov'
elif model_run == 2:
    generating_model = 'RNN'
if same_file_flag:  # Dictates which generated file is needed
    generated_file_name = f'PRED{target_file_name}-1000({generating_model})'
else:
    generated_file_name = f'PRED{generated_lower_file_name}-1000({generating_model})'

# Reading in Target File
start = time.time()
target_file_path = Path(__file__).with_name(target_file_name+'.txt')
target_file = open(target_file_path, 'r')
# Create unique set of each password, since duplicates don't matter in the target
unique_target_words = set(line.strip() for line in target_file)
target_length = len(unique_target_words)
target_file.close()
end = time.time()
print(f'Time to read and create set of Target dataset: {end-start}')
print(
    f'Target File - {target_file_name}\nTarget File Unique Occurences Length: {target_length}')

# Reading in Generated File
generated_file_path = Path(__file__).with_name(generated_file_name+'.txt')
start = time.time()
array_percentages = [0]
found = 0
percent = found/target_length
generated_length = 0
with open(generated_file_path, 'r') as generated_file:  # Loops through generated file
    for line in generated_file:
        current_line = line.strip()
        generated_length += 1
        if generated_length % 50000000 == 0:
            # To indicate progress and show program is properly running on larger datasets
            print(f'{generated_length} completed')
        # When the current generated passwords matches a password in the target file
        if current_line in unique_target_words:
            found += 1
            # Remove passwords found in target set since we don't want to increase 'found' if we guess the same thing again
            unique_target_words.remove(current_line)
            percent = (found/target_length)*100
        # Add whatever percentage currently matched to the array
        array_percentages.append(percent)
end = time.time()
print(f'Time to read and process data: {end-start}')
print(
    f'Generated File - {generated_file_name}\nGenerated File Length: {generated_length}')
# Once we've gone through the entire generated file, convert array to np array for space efficiency
# will be the y axis in the graph
array_percentages = np.array(array_percentages)
generated_list_length_array = np.arange(
    generated_length+1)  # create the x axis in the graph

# If testing, shows what the arrays are before graphing (hence why it is best with smaller data)
if tester_flag:
    print(f'Array of Percentages: {array_percentages}')
    print(f'Array of Guesses: {generated_list_length_array}')

# Store runtime data in file
runtime_info = Path(__file__).with_name('File percentages.txt')
file_percentages = open(runtime_info, 'a')
file_percentages.write(
    f'Target File: {target_file_name} - \nGenerating Model: {generating_model}\nTarget File Unique Occurences Length: {target_length}\nGenerated File Length: {generated_length}\n')
if same_file_flag:
    file_percentages.write(
        f'Generated File: {target_file_name} \nSame entropy set between Target and Generated\n')
else:
    file_percentages.write(
        f'Generated File: {generated_lower_file_name} \nTarget entropy is higher than Generated\n')
file_percentages.write(
    f'Percentages:\nQuarter - {array_percentages[generated_length//4]}\nHalfway - {array_percentages[generated_length//2]}\nComplete - {array_percentages[generated_length]}\n\n')
file_percentages.close()

# Generate Graph
start = time.time()
x = generated_list_length_array
y = array_percentages
plt.xlabel("Number of Generated Guesses")
plt.ylabel("Percent (%) Matching Target File")
if same_file_flag:  # Dictates title of the graph
    plt.title(
        f'Generated Matching Effectiveness - {generating_model}\nTarget: {target_file_name} (Same Set Used to Train)')
else:
    plt.title(
        f'Generated Matching Effectiveness - {generating_model}\nTarget: {target_file_name}')

# Modifications for graph appearence
# Limit the x and y axis so we don't have empty space outside of the number we could possibly have
plt.xlim([0, generated_list_length_array[generated_length-1]])
plt.ylim([0, 100])
# Custom decisions on the ticks to show progress
plt.yticks(np.arange(0, 100.1, 5))
plt.xticks(np.arange(0, generated_length+1, generated_length//10))

plt.plot(x, y)

"""The graph is interactive which consumes a significant amount of ram especially with the larger
datasets. The show flag was primarily only used when creating the modifications for graph 
appearance, to see what ticks and limits looked best before changing the values."""
if show_flag:  # Once again, primarily for testing purposes
    plt.show()
else:
    if same_file_flag:
        file_name = f'{target_file_name}-Same-{generating_model}'
    else:
        file_name = f'{target_file_name}-Lower-{generating_model}'
    plt.savefig(f'{file_name}.png')

end = time.time()
print(f'Time to generate and save graph: {end-start}')
print(f'Time to run program: {end-start}')
