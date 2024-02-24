import matplotlib.pyplot as plt
import numpy as np

class CubeArrangement:
    """
    A class handles the arrangement of cubes in a 3D space.

    It allows for the visualization and manipulation of cubes with different colors and positions.

    Attributes:
        cubes (np.ndarray): A 3D numpy array representing the initial state of the cubes, where each element is a string indicating the cube's color.
        ticks (bool): Flag to indicate whether to display axis ticks.
        grid (bool): Flag to indicate whether to display the grid.
        view (str): A string indicating the initial viewing angle of the plot.
        flip (str): A string indicating if the plot should be flipped along a certain axis.
        rot (int): An integer representing the rotation angle of the plot.
    """

    def __init__(self, cubes=None , ticks=False, grid=False, view='', flip='', rot=0):
        """
        Initialize the cube arrangement with optional customization.

        Parameters:
            cubes (np.ndarray, optional): A 3D numpy array representing the initial state of the cubes, where each element is a string indicating the cube's color. Default is an empty array.
            ticks (bool, optional): Flag to indicate whether to display axis ticks. Default is False.
            grid (bool, optional): Flag to indicate whether to display the grid. Default is False.
            view (str, optional): A string indicating the initial viewing angle of the plot. Default is an empty string.
            flip (str, optional): A string indicating if the plot should be flipped along a certain axis. Default is an empty string.
            rot (int, optional): An integer representing the rotation angle of the plot. Default is 0.
        
        Returns:
            None
        """

        # Ensure 'cubes' is a numpy.array, initializing it to an empty array if not provided.
        # Prevent ambiguous boolean array evaluations by explicitly checking type, rather than solely relying on a None check.
        if type(cubes) != np.ndarray:
            if cubes == None:
                cubes = np.full((5,5,5),'')

        # Assign attributes.
        self.cubes = cubes
        self.nx, self.ny, self.nz = self.cubes.shape
        self.ticks = ticks
        self.grid = grid
        self.view = view
        self.flip = flip
        self.rot = rot

        # Plot cubes with initial settings.
        self.plot_voxels()

        return
        
    def plot_voxels(self):
        """
        Plots the 3D voxels based on the cube locations and colors. This method visualizes the current state of the cubes.
        """

        # Track cubes' positions and assign colors.
        self.cubes_loc = np.zeros(self.cubes.shape)
        self.cubes_loc[self.cubes!=''] = 1
        self.facecolors = self.cubes

        # Create 3D plot with configured voxels.
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d', proj_type='ortho', box_aspect=(4,4,4))
        self.voxels = self.ax.voxels(self.cubes_loc, facecolors=self.facecolors, edgecolors='k', shade=False)

        # Adjust viewpoint and customize background.
        self.set_view()
        self.set_background()

        # delete figure
        plt.close(self.fig)

        return
    
    def set_view(self, view=None, flip=None, rot=None):
        """
        Sets the view of the 3D plot with specific angles and rotation. This method allows for adjusting the perspective from which the plot is viewed.

        Parameters:
            view (str, optional): A string indicating the desired viewing angle of the plot. Overrides the class attribute if provided.
            flip (str, optional): A string indicating if the plot should be flipped along a certain axis. Overrides the class attribute if provided.
            rot (int, optional): An integer representing the rotation angle of the plot. Default is 0. Overrides the class attribute if provided.
        
        Returns:
            None
        """

        # Update 'view', 'flip', and 'rot' if provided.
        if view != None:
            self.view = view
        if flip != None:
            self.flip = flip
        if rot != None:
            self.rot = rot

        # Define plot boundaries based on cube dimensions.
        self.ax.axes.set_xlim3d(0, self.nx)
        self.ax.axes.set_ylim3d(0, self.ny)
        self.ax.axes.set_zlim3d(0, self.nz)

        # Configure orientation and rotation based on 'view' and 'rot'.
        if self.view == 'xy':
            self.ax.view_init(90, -90, 0+self.rot)
        elif self.view == '-xy':
            self.ax.view_init(-90, 90, 0-self.rot)
        elif self.view == 'xz':
            self.ax.view_init(0, -90, 0+self.rot)
        elif self.view == '-xz':
            self.ax.view_init(0, 90, 0-self.rot)
        elif self.view == 'yz':
            self.ax.view_init(0, 0, 0+self.rot)
        elif self.view == '-yz':
            self.ax.view_init(0, 180, 0-self.rot)
        else:
            self.ax.view_init(azim=self.ax.azim+self.rot)
        
        # Apply axis flipping as specified by 'flip'.
        if self.flip == "x":
            self.ax.axes.set_xlim3d(self.nx, 0)
        if self.flip == "y":
            self.ax.axes.set_ylim3d(self.ny, 0)
        if self.flip == "z":
            self.ax.axes.set_zlim3d(self.nz, 0)

        return
    
    def set_background(self, ticks=None, grid=None):
        """
        Customizes the background, including grid and tick visibility. This method allows for toggling the visibility of grid lines and axis ticks on the plot.

        Parameters:
            ticks (bool, optional): Flag to indicate whether to display axis ticks. Overrides the class attribute if provided.
            grid (bool, optional): Flag to indicate whether to display the grid. Overrides the class attribute if provided.
        
        Returns:
            None
        """

        # Update 'ticks' and 'grid' if provided.
        if ticks != None:
            self.ticks = ticks
        if grid != None:
            self.grid = grid

        # Remove tick labels and lines if ticks are disabled.
        if self.ticks==False:
            for axis in [self.ax.xaxis, self.ax.yaxis, self.ax.zaxis]:
                axis.set_ticklabels([])
                axis.line.set_linestyle('')
                axis._axinfo['tick']['inward_factor'] = 0.0
                axis._axinfo['tick']['outward_factor'] = 0.0
        
        # Remove tick labels.
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_zticks([])
        
        # Toggle grid visibility based on 'grid' setting.
        self.ax.grid(self.grid)

        # Hide or show the entire axis based on 'ticks' and 'grid' settings.
        if self.ticks==False and self.grid==False:
            self.ax.set_axis_off()
        else:
            self.ax.set_axis_on()

        return

    
    def update_all_cubes(self, cubes=None):
        """
        Updates the entire cube arrangement to a new state. This method can reset or change the arrangement based on the provided array.

        Parameters:
            cubes (np.ndarray, optional): A 3D numpy array representing the new state of the cubes, where each element is a string indicating the cube's color. Default is an empty array to reset.
        
        Returns:
            None
        """
        
        # Ensure 'cubes' is a numpy.array, initializing it to an empty array if not provided.
        # Prevent ambiguous boolean array evaluations by explicitly checking type, rather than solely relying on a None check.
        if type(cubes) != np.ndarray:
            if cubes == None:
                cubes = np.full((5,5,5),'')
        self.cubes = cubes

        # Plot cubes with new settings.
        self.plot_voxels()

        return
    
    def update_cubes(self, loc=[[0],[0],[0]], color="r"):
        """
        Updates specific cubes within the arrangement with a new color. This method allows for changing the color of selected cubes.

        Parameters:
            loc (list of lists): A list containing three lists, each representing the start and end indices along one axis.
            color (str): A string representing the new color of the selected cubes.
        
        Returns:
            None
        """
        
        self.loc = loc
        
        # Update colors if new cube location is within bounds, else print error.
        if (loc[0][-1] < self.cubes.shape[0] and loc[1][-1] < self.cubes.shape[1]) and loc[2][-1] < self.cubes.shape[2]:
            self.cubes[loc[0][0]:loc[0][-1]+1,loc[1][0]:loc[1][-1]+1,loc[2][0]:loc[2][-1]+1] = color            
        else:
            print("Specified location is outside the array boundaries.")
            
        # Plot cubes with new settings.
        self.plot_voxels()
            
        return
    
    def check_cubes_arrange(self):
        depth, rows, cols = self.cubes.shape
        z_1 = np.full((rows,cols),"")
        z_2 = np.full((rows,cols),"")
        x_1 = np.full((depth,cols),"")
        x_2 = np.full((depth,cols),"")
        y_1 = np.full((depth,cols),"")
        y_2 = np.full((depth,cols),"")
        for idx in range(depth):
            z_1_not_non = self.cubes[idx,:,:] != ''
            z_1[z_1_not_non] = self.cubes[idx,:,:][z_1_not_non]
            z_2_not_non = self.cubes[depth-idx-1,:,:] != ''
            z_2[z_2_not_non] = self.cubes[depth-idx-1,:,:][z_2_not_non]
        for idx in range(rows):
            x_1_not_non = self.cubes[:,idx,:] != ''
            x_1[x_1_not_non] = self.cubes[:,idx,:][x_1_not_non]
            x_2_not_non = self.cubes[:,rows-idx-1,:] != ''
            x_2[x_2_not_non] = self.cubes[:,rows-idx-1,:][x_2_not_non]
        for idx in range(cols):
            y_1_not_non = self.cubes[:,:,idx] != ''
            y_1[y_1_not_non] = self.cubes[:,:,idx][y_1_not_non]
            y_2_not_non = self.cubes[:,:,cols-idx-1] != ''
            y_2[y_2_not_non] = self.cubes[:,:,cols-idx-1][y_2_not_non]

        faces = [[z_1],[z_2],[x_1],[x_2],[y_1],[y_2]]
        for face in faces:
            for idx in range(3):
                face.append(np.rot90(face[idx]))

        faces_flip = []
        for face in faces:
            face_flip = []
            for direction in face:
                direction_flip = [np.fliplr(direction),np.flipud(direction)]
                face_flip.append(direction_flip)
            faces_flip.append(face_flip)

        for face_flip in faces_flip:
            for direction_flip in face_flip:
                for flip in direction_flip:
                    for face in faces:
                        for direction in face:
                            if np.array_equal(flip, direction):
                                return False
        
        return True

