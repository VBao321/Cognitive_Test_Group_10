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

def SRQuestion_bank(seed):
    np.random.seed(seed)
    question_list = []
    question_info["idx"]=0
    
    while question_info["idx"]<5:
        cube_arr = cc.CubeArrangement(create_random_cubes((3,3,3),['r','g','b']), grid=True, ticks=True)
        if cube_arr.check_cubes_arrange():
            question_info["idx"] += 1
            question_idx = question_info["idx"]
            cube_arr.fig.savefig(f"./Figures/SRQ_{question_idx}.png")
            question_list.append([f"./Figures/SRQ_{question_idx}.png",{}])
            view_list = ['xy','-xy','xz','-xz','yz','-yz']
            flip_list = ["x", "y", "z"]
            option_list = ["a", "b", "c", "d"]
            for idx in range(3):
                view = np.random.choice(view_list)
                view_list.remove(view)
                option = np.random.choice(option_list)
                option_list.remove(option)
                cube_arr.set_view(view=view)
                cube_arr.fig.savefig(f"./Figures/SRQ_{question_idx}_{option}.png")
                question_list[question_idx-1][1][f"./Figures/SRQ_{question_idx}_{option}.png"]=option
            view = np.random.choice(view_list)
            flip = np.random.choice(flip_list)
            cube_arr.set_view(view=view, flip=flip)
            answer = option = option_list[0]
            question_list[question_idx-1].append(answer)
            cube_arr.fig.savefig(f"./Figures/SRQ_{question_idx}_{option}.png")
            question_list[question_idx-1][1][f"./Figures/SRQ_{question_idx}_{option}.png"]=option
            
            
    while question_info["idx"]<9:
        cube_arr = cc.CubeArrangement(create_random_cubes((4,4,4),['r','g','b']), grid=True)
        if cube_arr.check_cubes_arrange():
            question_info["idx"] += 1
            question_idx = question_info["idx"]
            cube_arr.fig.savefig(f"./Figures/SRQ_{question_idx}.png")
            question_list.append([f"./Figures/SRQ_{question_idx}.png",{}])
            view_list = ['xy','-xy','xz','-xz','yz','-yz']
            flip_list = ["x", "y", "z"]
            option_list = ["a", "b", "c", "d"]
            for idx in range(3):
                view = np.random.choice(view_list)
                view_list.remove(view)
                option = np.random.choice(option_list)
                option_list.remove(option)
                cube_arr.set_view(view=view)
                cube_arr.fig.savefig(f"./Figures/SRQ_{question_idx}_{option}.png")
                question_list[question_idx-1][1][f"./Figures/SRQ_{question_idx}_{option}.png"]=option
            view = np.random.choice(view_list)
            flip = np.random.choice(flip_list)
            cube_arr.set_view(view=view, flip=flip)
            answer = option = option_list[0]
            question_list[question_idx-1].append(answer)
            cube_arr.fig.savefig(f"./Figures/SRQ_{question_idx}_{option}.png")
            question_list[question_idx-1][1][f"./Figures/SRQ_{question_idx}_{option}.png"]=option
        
    while question_info["idx"]<12:
        cube_arr = cc.CubeArrangement(create_random_cubes((5,5,5),['r','g','b','y']), grid=True)
        if cube_arr.check_cubes_arrange():
            question_info["idx"] += 1
            question_idx = question_info["idx"]
            cube_arr.fig.savefig(f"./Figures/SRQ_{question_idx}.png")
            question_list.append([f"./Figures/SRQ_{question_idx}.png",{}])
            view_list = ['xy','-xy','xz','-xz','yz','-yz']
            flip_list = ["x", "y", "z"]
            option_list = ["a", "b", "c", "d"]
            for idx in range(3):
                view = np.random.choice(view_list)
                view_list.remove(view)
                option = np.random.choice(option_list)
                option_list.remove(option)
                cube_arr.set_view(view=view)
                cube_arr.fig.savefig(f"./Figures/SRQ_{question_idx}_{option}.png")
                question_list[question_idx-1][1][f"./Figures/SRQ_{question_idx}_{option}.png"]=option
            view = np.random.choice(view_list)
            flip = np.random.choice(flip_list)
            cube_arr.set_view(view=view, flip=flip)
            answer = option = option_list[0]
            question_list[question_idx-1].append(answer)
            cube_arr.fig.savefig(f"./Figures/SRQ_{question_idx}_{option}.png")
            question_list[question_idx-1][1][f"./Figures/SRQ_{question_idx}_{option}.png"]=option
            
    return question_list
    
    