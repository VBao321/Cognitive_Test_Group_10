import matplotlib.pyplot as plt
import numpy as np
import random

def points_in_ellipse(num_points, center, width, height, ax):
    """
    Generate random points within the boundary of an ellipse.

    Parameters:
        num_points (int): The number of points to generate.
        center (tuple): The center coordinates (x, y) of the ellipse.
        width (float): The width of the ellipse.
        height (float): The height of the ellipse.
        ax (matplotlib.axes.Axes): The Axes object to plot the ellipse.

    Returns:
        points (list): A list of generated points within the ellipse boundary, each represented as a tuple (x, y).
    """
    
    points = []
    
    while len(points) < num_points:
        
        # Generate a random point.
        x, y = np.random.rand(2)
        
        # Scale and shift the point to the ellipse's range.
        x = x * width + center[0] - width / 2
        y = y * height + center[1] - height / 2
        
        # Check if the point is inside the ellipse.
        if ((x - center[0])**2 / (width / 2)**2) + ((y - center[1])**2 / (height / 2)**2) <= 1:
            points.append((x, y))

    return points

def generate_images(num_points_l, num_points_r):
    """
    Generate images with points distributed within two ellipses and plot them.

    Parameters:
        num_points_l (int): The number of points to generate within the left ellipse.
        num_points_r (int): The number of points to generate within the right ellipse.

    Returns:
        fig (matplotlib.figure.Figure): The generated figure object containing the plot of the ellipses and points.
    """
    
    # Set up the figure and axis.
    fig, ax = plt.subplots(figsize=(8, 8))

    # Ellipse parameters.
    ellipse_l_center = (0.25, 0.5)
    ellipse_r_center = (0.75, 0.5)
    ellipse_width = 0.475
    ellipse_height = 0.8
    
    # Draw two ellipses to the plot.
    ellipse_l = plt.matplotlib.patches.Ellipse(ellipse_l_center, ellipse_width, ellipse_height, color='black', fill=False)
    ellipse_r = plt.matplotlib.patches.Ellipse(ellipse_r_center, ellipse_width, ellipse_height, color='black', fill=False)

    # Add the ellipses to the axes.
    ax.add_patch(ellipse_l)
    ax.add_patch(ellipse_r)

    # Generate points within each ellipse.
    points_ellipse_l = points_in_ellipse(num_points_l, ellipse_l_center, ellipse_width, ellipse_height, ax)
    points_ellipse_r = points_in_ellipse(num_points_r, ellipse_r_center, ellipse_width, ellipse_height, ax)

    # Plot the points.
    x_points_l, y_points_l = zip(*points_ellipse_l)
    x_points_r, y_points_r = zip(*points_ellipse_r)
    ax.scatter(x_points_l, y_points_l, color='blue', s=300)
    ax.scatter(x_points_r, y_points_r, color='orange', s=300)

    # Set the aspect of the plot to be equal.
    ax.set_aspect('equal')

    # Remove the axes
    ax.axis('off')

    # Set the limits of the plot.
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    return fig

def ANSQuestion_bank(seed):
    """
    Generate a question bank of images with points distributed within two ellipses,
    along with corresponding information about the number of points and the correct answer.

    Parameters:
        seed (int): The random seed for reproducibility.

    Returns:
        tuple: A tuple containing three lists:
            1. image_list (list): A list of paths to the generated images.
            2. num_points_list (list): A list of tuples containing the number of points generated within the left and right ellipses for each image.
            3. answer_list (list): A list of strings indicating the correct answer for each image, where 'left' corresponds to the left ellipse having more points, and 'right' corresponds to the right ellipse having more points.
    """
    
    # Set random seed.
    np.random.seed(seed)
    
    # Set ratios of numbers
    ratios = [(12,9), (16,12), (20,15), (14,12), (21,18), (18,6), (10,9), (20,18)]
    
    # Initial lists to store data.
    image_list = []
    num_points_list = []
    answer_list = []
    
    # Generate 64 images and add their information to the according list.
    for idx in range(64):
        
        # Randomly choose ellipse ratio index.
        random_index = np.random.choice(len(ratios))
        random_ratio = ratios[random_index]
        
        # Random answer and add it to list.
        answer = "Left" if np.random.randint(2)==0 else "Right"
        answer_list.append(answer)
        
        # Determine number of points in ellipses based on answer, and add them to list.
        num_points_l = random_ratio[0] if answer=="Left" else random_ratio[1]
        num_points_r = random_ratio[1] if answer=="Left" else random_ratio[0]
        num_points_list.append((num_points_l, num_points_r))
        
        # Generate and save image.
        fig = generate_images(num_points_l, num_points_r)
        fig.savefig(f'./ANS_Test/Figures/ANSQ_{idx}.png')

        # Add name of image to list.
        image_list.append(f'./ANS_Test/Figures/ANSQ_{idx}.png')

        # close image.
        plt.close(fig)
        
    return image_list, num_points_list, answer_list