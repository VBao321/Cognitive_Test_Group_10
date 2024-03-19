import numpy as np
import random
import cube_constructor as cc

question_info = {"idx":0}

def create_random_cubes(shape, colors):
    """
    Fills a 3D numpy array with color streaks starting from random positions and extending for random lengths in random directions.
    
    Parameters:
        shape (list): Shape of the 3D array [depth, rows, cols].
        colors (str): List of colors to use.
    
    Returns:
        cubes (np.ndarray): A 3D numpy array with colored streaks.
    """
    
    # Initialize array with empty strings.
    cubes = np.full(shape, "")

    depth, rows, cols = shape
    for color in colors:
        
        # Choose a random starting point in 3D space.
        start_depth = np.random.randint(depth-1)
        start_row = np.random.randint(rows-1)
        start_col = np.random.randint(cols-1)
        
        # Randomly choose direction: 0 for along depth, 1 for row, 2 for column.
        direction = np.random.choice([0, 1, 2])
        
        # Determine the length and fill the array based on the chosen direction.
        if direction == 0:
            length = np.random.randint(2, depth - start_depth + 1)
            cubes[start_depth:start_depth+length, start_row, start_col] = color
        elif direction == 1:
            length = np.random.randint(2, rows - start_row + 1)
            cubes[start_depth, start_row:start_row+length, start_col] = color
        else:
            length = np.random.randint(2, cols - start_col + 1)
            cubes[start_depth, start_row, start_col:start_col+length] = color

    return cubes

def random_SRQuestion(shape, colors):
    """
    Generates a spatial reasoning question with a specific shape and set of colors.
    
    Parameters:
        shape (tuple): The dimensions of the cube arrangement (e.g., (3, 3, 3) for a 3x3x3 grid).
        colors (list): A list of colors used in the cube arrangement.

    Returns:
        tuple: A tuple containing four elements:
            1. image (str): Path to the question's descriptive image.
            2. options (list): Paths to the question's option images, provided as a list of strings.
            3. answer (str): The correct answer's option identifier.
            4. grid_size (int): The dimension of the 3D space used in the question, represented as an integer.
    """
    
    # Initialize options and solvability check.
    options = []
    solvable = False
    
    # Get size of the 3d space.
    grid_size = shape[0]
    
    # Generate new random cubes until the question is solvable.
    while solvable == False:
        cube_arr = cc.CubeArrangement(create_random_cubes(shape,colors), grid=True, ticks=True)
        solvable = cube_arr.check_solution()
    
    # Increment question index.
    question_info["idx"] += 1
    question_idx = question_info["idx"]
    
     # Save the question description image according to index.
    cube_arr.fig.savefig(f"./Spatial_Reasoning_Test/Figures/SRQ_{question_idx}.png", dpi=300, bbox_inches='tight', pad_inches=0)
    image = f"./Spatial_Reasoning_Test/Figures/SRQ_{question_idx}.png"
    
    # Prepare lists for view, rotation, and options generation.
    view_list = ['xy','-xy','xz','-xz','yz','-yz']
    flip_list = ["x", "y", "z"]
    option_list = ["a", "b", "c", "d"]
    rot_list = [0, 90, 180, 270]
    
    # Generate three incorrect options (viable views).
    for idx in range(3):
        view = np.random.choice(view_list)
        view_list.remove(view)
        option = np.random.choice(option_list)
        option_list.remove(option)
        rot = np.random.choice(rot_list)
        cube_arr.set_view(view=view, rot=rot)
        cube_arr.fig.savefig(f"./Spatial_Reasoning_Test/Figures/SRQ_{question_idx}_{option}.png", dpi=300,  bbox_inches='tight', pad_inches=0)
        options.append(f"./Spatial_Reasoning_Test/Figures/SRQ_{question_idx}_{option}.png")
    
    # Determine the impossible view after flip.
    view = cube_arr.check_solution()
    
    # Remove ineffective flip axis form the flip list.
    if view[-2:] == "xy":
        flip_list.remove("z")
    if view[-2:] == "xz":
        flip_list.remove("y")
    if view[-2:] == "yz":
        flip_list.remove("x")
    
    # Generate the correct option (unviable view).
    flip= np.random.choice(flip_list)
    rot = np.random.choice(rot_list)
    cube_arr.set_view(view=view, flip=flip, rot=rot)
    answer = option = option_list[0]
    cube_arr.fig.savefig(f"./Spatial_Reasoning_Test/Figures/SRQ_{question_idx}_{option}.png", dpi=300, bbox_inches='tight', pad_inches=0)
    options.append(f"./Spatial_Reasoning_Test/Figures/SRQ_{question_idx}_{option}.png")
    
    return image, options, answer, grid_size

def SRQuestion_bank(seed):
    """
    Generates a bank of spatial reasoning questions and their answers, based on specified seed.

    Parameters:
        seed (int): The seed value for the random number generator to ensure that the questions generated are reproducible.

    Returns:
        tuple: Contains four lists:
            1. image_list (list): A list of paths to the description images of each question.
            2. options_list (list): A list of lists containing paths to the option images for each question.
            3. answer_list (list): A list of string indicating the correct option for each question.
            4. grid_size_list (list): The dimensions of the 3D space used for each question.
    """
    
    # Set random seed.
    np.random.seed(seed)
    
    # Initial lists to store data.
    image_list = []
    options_list = []
    answer_list = []
    grid_size_list = []
    
    # Reset question index for each time run this function.
    question_info["idx"]=0
    
    # Define difficulty levels with grid sizes and color schemes.
    level_list = [[(3,3,3), ["r", "g", "b"]],
                  [(4,4,4), ["r", "g", "b"]],
                  [(5,5,5), ["r", "g", "b"]]]
    
    # Generate questions for each level.
    for level in level_list:
        for idx in range(3):
            question = random_SRQuestion(level[0], level[1])
            image_list.append(question[0])
            options_list.append(question[1])
            answer_list.append(question[2])
            grid_size_list.append(question[3])
        
    return image_list, options_list, answer_list, grid_size_list