import ipywidgets as widgets
from IPython.display import display, Image, clear_output, HTML, Javascript
from functools import partial
import time

class Question:
    """
    A class to represent a question with optional image, customizable display style, and timing functionality.
    
    Attributes:
        description (str): The question text.
        description_img (str, optional): URL or path to an optional image to display with the question.
        description_style (str): CSS style for the question text.
        answer: The correct answer to the question.
        submission: The answer submitted by the user.
        correctness (bool, optional): Whether the submitted answer is correct.
        shown (bool): Whether the question has been displayed.
        total_time (float, optional): The total time taken from displaying to answering the question.
    """
    
    def __init__(self, description, description_img=None, description_style="color:red; font-size: 30px"):
        """
        Initializes the Question object with description, optional image, and style.

        Parameters:
            description (str): The question text.
            description_img (str, optional): URL or path to an optional image to display with the question. Defaults to None.
            description_style (str): CSS style for the question text. Defaults to "color:red; font-size: 30px".
        
        Returns:
            None
        """
        
        # Assign attributes.
        self.description = description
        self.description_img = description_img
        self.description_style = description_style
        self.answer = None
        self.submission = None
        self.correctness = None
        self.shown = False
        self.total_time = None

        return

    def update_description(self, description):
        """
        Updates the question's description.

        Parameters:
            description (str): The new question text.
        
        Returns:
            None
        """
        
        self.description = description

        return

    def display_question(self):
        """
        Displays the question text with optional image and applies specified style. Marks the question as shown and starts timing from this point.
        
        Parameters:
            None
        
        Returns:
            None
        """
        
        # Create HTML output to display both the image and the question text if provided with image.
        if self.description_img != None:
            html_out = HTML(f"""
                            <img src='{self.description_img}' width='400' height='400'>
                            <span style='{self.description_style}'>{self.description}</span>
                            """)
        else:
            html_out = HTML(f"""
                            <span style='{self.description_style}'>{self.description}</span>
                            """)
        
        # Display the generated HTML output.
        display(html_out)

        # Mark the question as having been displayed.
        self.shown = True

        # Record the current time as the start time.
        self.start_time = time.time()

        return
    
    def check_answer(self):
        """
        Checks if the submitted answer is correct and updates the correctness attribute.
        
        Parameters:
            None

        Returns:
            None
        """
        
        # Check if a submission exists and update correctness accordingly.
        if self.submission != None:
            if self.answer == self.submission:
                self.correctness = True
            else:
                self.correctness = False
        
        return
    
    def get_time(self):
        """
        Calculates and returns the time related to the question's display and submission status.
        - If the question has not been shown, it returns a message indicating that timing has not started.
        - If the question has been shown but not answered, it returns the time elapsed since the question was displayed up to the current moment.
        - If the question has been answered, it returns the total time taken from displaying the question to when the answer was submitted.
        
        This method ensures that once the total time is calculated after an answer is submitted, subsequent calls will return the same total time.

        Returns:
            float or str: Depending on the question's state, it returns either the time elapsed in seconds or a message. For unshown questions, it returns a message indicating timing hasn't started. For shown but unanswered questions, it returns the time elapsed since the question was displayed. For answered questions, it returns the total time taken to answer the question.
        """
        
        # Return warning if question not displayed, else calculate/return time based on submission status.
        if self.shown == False:
            warning = "The question has not been displayed; consequently, the timer has not commenced."
            return warning
        
        elif self.submission == None:
            self.end_time = time.time()
            self.elapsed_time = self.end_time-self.start_time
            
            # Calculate elapsed time
            return self.elapsed_time
        
        elif self.total_time == None:
            self.end_time = time.time()
            self.total_time = self.end_time-self.start_time
            
            # Calculate total time
            return self.total_time
        
        else:
            # Return calculated total time
            return self.total_time

class ANSQuestion(Question):
    """
    A class to represent an Approximate Number System (ANS) question, extending the base Question class.
    
    ANS questions typically involve tasks that require estimation or comparison of quantities, suitable for assessing numerical cognition without relying on exact numerical operations.
    
    Attributes:
        answer (int): The correct answer to the ANS question, indicating the participant's choice. It should be 0 for selecting the option on the left or 1 for selecting the option on the right.
        Inherits all attributes from the 'Question' class, including 'description', 'description_img', 'description_style', and timing-related attributes.
    """
    
    def __init__(self, description, answer, description_img=None, description_style="color:red; font-size: 30px"):
        """
        Initializes an ANSQuestion object with a description, the correct binary answer, and optional customization. 
        Prepares the question for display and interaction by assembling option widgets and setting up observers for user responses.
        
        Parameters:
            description (str): The question text.
            answer (str): The correct answer to the ANS question, indicates the left option or right option.
            description_img (str, optional): URL or path to an optional image to display with the question. Defaults to None.
            description_style (str): CSS style for the question text. Defaults to "color:red; font-size: 30px".

        Returns:
            None
        """
        
        # Initialize base class.
        super().__init__(description, description_img, description_style)
        
        # Assign attributes.
        self.answer = answer

        # Create option widgets, and setup response observers.
        self.assemble_option_widgets()
        self.setup_observers()
        
        return

    def assemble_option_widgets(self):
        """
        Prepares interactive widgets for question options. Options are displayed as buttons

        Parameters:
            None

        Returns:
            None
        """
        
        # Create and configure two option buttons, then arrange them in a horizontal box.
        self.buttons = []
        
        for option in ["Left", "Right"]:
            button = widgets.Button(description=option)
            button.style.button_color = 'lightgray'

            button.layout.width = '150px'

            self.buttons.append(button)
        
        self.options_box = widgets.HBox(self.buttons)
        
        return

    def setup_observers(self):
        """
        Initializes observers for user interactions with option widgets.

        Parameters:
            None

        Returns:
            None
        """
        
        # Assign click event handler to capture submission and response time for each button.
        def on_button_click(b):
            self.submission = b.description
            self.get_time()
                
        for button in self.buttons:
            button.on_click(on_button_click)
            
        return

    def display_question(self):
        """
        Displays the question after showing the description and optional image for a brief period.
        Inherits the initial display behavior from the base class, then briefly pauses before showing a fixation cross and the question text with options.

        Parameters:
            None

        Returns:
            None
        """
        
        # Display initial question.
        super().display_question()
        
        # Pause
        time.sleep(0.75)
        
        # Clear Previous content.
        clear_output()
        
        # Define and display fixation cross with options.
        fixation_cross = "./Figures/Fixation_cross.png"
        html_out = HTML(f"""
                        <img src='{fixation_cross}' width='400' height='400'>
                        <span style='{self.description_style}'>{self.description}</span>
                        """)
        display(html_out, self.options_box)

        return

class SpatialReasoningQuestion(Question):  
    """
    A class to represent a Spatial Reasoning question, extending the base Question class.

    Spatial Reasoning questions are designed to assess a participant's ability to understand and remember the spatial relations among objects. These questions often involve identifying patterns, solving puzzles, or navigating through space, making them ideal for evaluating spatial awareness and logical thinking skills.

    Attributes:
        options (dict): A mapping of option descriptions to their image paths, used to present multiple choice options to the user.
        answer (int): The correct answer to the Spatial Reasoning question, typically represented as the index or key corresponding to the correct option in the `options` dictionary.
        Inherits all attributes from the 'Question' class, including 'description', 'description_img', 'description_style', and timing-related attributes.
    """
    
    def __init__(self, description, options, answer, description_img=None, description_style="color:red; font-size: 30px"):
        """
        Initializes a SpatialReasoningQuestion object with a description, the options, the correct answer, and optional customization.
        Prepares the question for display and interaction by assembling option widgets and setting up observers for user responses.

        Parameters:
            description (str): The text describing the spatial reasoning task.
            options (dict): A mapping of option labels to their associated image paths, used to present choices to the user.
            answer (int): The index or key of the correct option in the `options` dictionary.
            description_img (str, optional): An optional URL or path to a background or contextual image for the question. Defaults to None.
            description_style (str): CSS styling for the question text, allowing customization of its appearance. Defaults to "color:red; font-size: 30px".

        Returns:
            None
        """
        
        # Initialize base class.
        super().__init__(description, description_img, description_style)
        
        # Assign attributes.
        self.options = options
        self.answer = answer

        # Create option widgets, and setup response observers.
        self.assemble_option_widgets()
        self.setup_observers()
 
        return

    def assemble_option_widgets(self):
        """
        Prepares interactive widgets for question options. Options are displayed with associated images.

        Parameters:
            None

        Returns:
            None
        """
        # Initialize lists for option widgets and checkboxes.
        self.option_list = []
        self.checkboxs = []
        
        
        for option in self.options:
            
            # Create image widget and checkbox for each option.
            img_path = self.options[option]
            image = widgets.Image(
                value=open(img_path, 'rb').read(),
                format='png',
                width=400,
                height=400,
            )
            checkbox = widgets.Checkbox(description=option)
            
            # Add to checkbox list.
            self.checkboxs.append(checkbox)
            
            # Combine image and checkbox into a vertical box and add to option list.
            option_box = widgets.VBox([image, checkbox])
            
            self.option_list.append(option_box)
    
        # Group all option boxes horizontally.
        self.options_box = widgets.HBox(self.option_list)
        
        return

    def setup_observers(self):
        """
        Initializes observers for user interactions with option widgets.

        Parameters:
            None

        Returns:
            None
        """
        
        # Attach event handler to checkboxes for submission recording and time calculation.
        def on_checkbox_click(description, change):
            if change['new']==True:
                self.submission = description
                self.get_time()
                
        for checkbox in self.checkboxs:
            callback = partial(on_checkbox_click, checkbox.description)
            checkbox.observe(callback, names="value")
            
        return

    def display_question(self):
        """
        Inherits the initial display behavior from the base class, then show options.

        Parameters:
            None

        Returns:
            None
        """
        
        # Display initial question.
        super().display_question()
        
        # Display options.
        display(self.options_box)

        return
    