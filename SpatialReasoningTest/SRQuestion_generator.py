import numpy as np
import random
import cube_constructor as cc

question_info = {"idx":0}

def create_random_cubes(shape, colors):
    """
    Fills a 3D numpy array with color streaks starting from random positions
    and extending for random lengths in random directions.
    
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
    options = {}
    solvable = False
    cube_arr = cc.CubeArrangement()
    grid_size = shape[0]
    while solvable == False:
        cube_arr = cc.CubeArrangement(create_random_cubes(shape,colors), grid=True, ticks=True)
        solvable = cube_arr.check_solution()
    question_info["idx"] += 1
    question_idx = question_info["idx"]
    cube_arr.fig.savefig(f"./Figures/SRQ_{question_idx}.png")
    image = f"./Figures/SRQ_{question_idx}.png"
    view_list = ['xy','-xy','xz','-xz','yz','-yz']
    flip_list = ["x", "y", "z"]
    option_list = ["a", "b", "c", "d"]
    rot_list = [0, 90, 180, 270]
    for idx in range(3):
        view = np.random.choice(view_list)
        view_list.remove(view)
        option = np.random.choice(option_list)
        option_list.remove(option)
        rot = np.random.choice(rot_list)
        cube_arr.set_view(view=view, rot=rot)
        cube_arr.fig.savefig(f"./Figures/SRQ_{question_idx}_{option}.png")
        options[f"./Figures/SRQ_{question_idx}_{option}.png"]=option
        
    view = cube_arr.check_solution()
    if view[-2:] == "xy":
        flip_list.remove("z")
    if view[-2:] == "xz":
        flip_list.remove("y")
    if view[-2:] == "yz":
        flip_list.remove("x")
    flip= np.random.choice(flip_list)
    rot = np.random.choice(rot_list)
    cube_arr.set_view(view=view, flip=flip, rot=rot)
    answer = option = option_list[0]
    cube_arr.fig.savefig(f"./Figures/SRQ_{question_idx}_{option}.png")
    
    options[f"./Figures/SRQ_{question_idx}_{option}.png"]=option
    
    return image, options, answer, grid_size

def SRQuestion_bank(seed):
    np.random.seed(seed)
    image_list = []
    options_list = []
    answer_list = []
    grid_size_list = []
    question_info["idx"]=0
    
    level_list = [[(3,3,3), ["r", "g", "b"]],
                  [(4,4,4), ["r", "g", "b"]],
                  [(5,5,5), ["r", "g", "b"]]]
    for level in level_list:
        for idx in range(3):
            question = random_SRQuestion(level[0], level[1])
            image_list.append(question[0])
            options_list.append(question[1])
            answer_list.append(question[2])
            grid_size_list.append(question[3])
        
    return image_list, options_list, answer_list, grid_size_list