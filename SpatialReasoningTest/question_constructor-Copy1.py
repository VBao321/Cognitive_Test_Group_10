import ipywidgets as widgets
from IPython.display import display, display_html, Image, HTML, Javascript
from IPython.display import clear_output as ipy_clear_output
from functools import partial
import time
from jupyter_ui_poll import ui_events

def clear_output(wait=False):
    """
    Clears the output and displays current question progress.
    
    Utilizes the IPython.display.clear_output function, enhancing it to show the progress based on the global 'question_idx' dictionary.
    
    Parameters:
        wait (bool, optional): Delays clearing the output until after pending messages are processed. Defaults to False.
    
    Returns:
        None
    """
    
    # Use clear_output function from IPython.display.
    ipy_clear_output(wait=wait)
    
    # Display progress bar.
    display(progress_bar)
    
    return
    
def set_progress_bar(max):
    """
    Initializes a progress bar

    Parameters:
        max (int): Final progress index.

    Returns:
        None
    """
    # Display progress indicator.
    
    idx = 0
    progress_bar = widgets.IntProgress(
        min=0,
        max=max,
        description=f"Q {idx}/{max}",
        orientation='horizontal'
    )
    
    return progress_bar

def update_progress_bar(progress_bar, idx):
    progress_bar.value = idx
    progress_bar.description = f"Q {idx}/{progress_bar.max}"
    
    return

class Question:
    """
    A class to represent a question with optional image, customizable display style, and timing functionality.
    
    Attributes:
        description (str): The question text.
        description_img (str, optional): URL or path to an optional image to display with the question.
        description_style (str): CSS style for the question text.
        timeout (int, optional): The maximum time for answering the question. Defaults to -1, infinite time.
        time_up (bool): Whether time is up
        answer: The correct answer to the question.
        submission: The answer submitted by the user.
        correctness (bool): Whether the submitted answer is correct.
        shown (bool): Whether the question has been displayed.
        total_time (float): The total time taken from displaying to answering the question.
    """
    
    def __init__(self, description, description_img=None, description_style="color:red; font-size: 30px", timeout=-1):
        """
        Initializes the Question object with description, optional image, and style.

        Parameters:
            description (str): The question text.
            description_img (str, optional): URL or path to an optional image to display with the question. Defaults to None.
            description_style (str): CSS style for the question text. Defaults to "color:red; font-size: 30px".
            timeout (int, optional): The maximum time for answering the question. Defaults to -1, infinite time.
        
        Returns:
            None
        """
        
        # Assign attributes.
        self.description = description
        self.description_img = description_img
        self.description_style = description_style
        self.timeout=-1
        self.time_up = False
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
                            <div style='display:grid; place-items: center;'>
                            <img src='{self.description_img}' style='width:310px; height:300px;'>
                            <p style='{self.description_style}'>{self.description}</p>
                            </div>
                            """)
        else:
            html_out = HTML(f"""
                            <span style='{self.description_style}'>{self.description}</span>
                            """)
        
        # Display the generated HTML output.
        display_html(html_out)

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
        - If the question has been shown but not answered within time limit, it returns the time elapsed since the question was displayed up to the current moment.
        - If the question has been answered or exceeds time limit, it returns the total time taken from displaying the question to when the answer was submitted.
        
        This method ensures that once the total time is calculated after an answer is submitted, subsequent calls will return the same total time.

        Parameters:
            None

        Returns:
            float or str: Depending on the question's state, it returns either the time elapsed in seconds or a message. For unshown questions, it returns a message indicating timing hasn't started. For shown but unanswered questions, it returns the time elapsed since the question was displayed. For answered questions, it returns the total time taken to answer the question.
        """
        
        # Return warning if question not displayed, else calculate/return time based on submission status.
        if self.shown == False:
            warning = "The question has not been displayed; consequently, the timer has not commenced."
            return warning
        
        elif self.submission == None and self.time_up == False:
            
            # Calculate elapsed time.
            self.end_time = time.time()
            self.elapsed_time = self.end_time-self.start_time
            
            return self.elapsed_time
        
        elif self.total_time == None:
            
            # Calculate total time.
            self.end_time = time.time()
            self.total_time = self.end_time-self.start_time
            
            return self.total_time
        
        else:
            # Return calculated total time
            return self.total_time
        
    def wait_for_submission(self, timeout=-1, interval=0.001, max_rate=20, allow_interupt=True):
        """
        Waits for user submission, processing UI events during the wait.

        Parameters:
            timeout (int, optional): How long to wait (seconds). -1 for no limit.
            interval (float, optional): Time between checks (seconds).
            max_rate (int, optional): Max checks per second for UI events.
            allow_interupt (bool, optional): Whether the loop allows interuption.
            
        Returns:
            None
        """

        n_proc = int(max_rate*interval)+1

        with ui_events() as ui_poll:
            keep_looping = True
            while keep_looping == True:
                
                # process UI events
                ui_poll(n_proc)

                # end loop if we have waited more than the timeout period
                if (timeout != -1) and (self.get_time() > timeout):
                    keep_looping = False
                    self.time_up = True

                # end loop if submission appears
                if allow_interupt==True and self.submission!=None:
                    keep_looping = False

                # add pause before looping to check submission again
                time.sleep(interval)

        return

class ANSQuestion(Question):
    """
    A class to represent an Approximate Number System (ANS) question, extending the base Question class.
    
    ANS questions typically involve tasks that require estimation or comparison of quantities, suitable for assessing numerical cognition without relying on exact numerical operations.
    
    Attributes:
        answer (int): The correct answer to the ANS question, indicating the participant's choice. It should be 0 for selecting the option on the left or 1 for selecting the option on the right.
        Inherits all attributes from the 'Question' class, including 'description', 'description_img', 'description_style', and timing-related attributes.
    """
    
    def __init__(self, description, answer, description_img=None, description_style="color:red; font-size: 30px", timeout=-1):
        """
        Initializes an ANSQuestion object with a description, the correct binary answer, and optional customization. 
        Prepares the question for display and interaction by assembling option widgets and setting up observers for user responses.
        
        Parameters:
            description (str): The question text.
            answer (str): The correct answer to the ANS question, indicates the left option or right option.
            description_img (str, optional): URL or path to an optional image to display with the question. Defaults to None.
            description_style (str): CSS style for the question text. Defaults to "color:red; font-size: 30px".
            timeout (int, optional): The maximum time for answering the question. Defaults to -1, infinite time.

        Returns:
            None
        """
        
        # Initialize base class.
        super().__init__(description, description_img, description_style, timeout)
        
        # Assign attributes.
        self.timeout = timeout
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
        
        # Attach event handler to buttons for submission recording, answer checking and time calculation.
        def on_button_click(b):
            self.submission = b.description
            self.check_answer()
                
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
                        <div style='display:grid; place-items: center;'>
                        <img src='{fixation_cross}' style='width:310px; height:300px;'>
                        <p style='{self.description_style}'>{self.description}</p>
                        </div>
                        """)
        
        display_html(html_out)
        display(self.options_box)
        
        # Check for submission.
        self.wait_for_submission(timeout=self.timeout)
        
        # Calculate total time if timeout was set.
        self.get_time()

        return

class SpatialReasoningQuestion(Question):  
    """
    A class to represent a Spatial Reasoning question, extending the base Question class.

    Spatial Reasoning questions are designed to assess a participant's ability to understand the spatial relations among objects.

    Attributes:
        options (dict): A mapping of option descriptions to their image paths, used to present multiple choice options to the user.
        answer (int): The correct answer to the Spatial Reasoning question, typically represented as the index or key corresponding to the correct option in the `options` dictionary.
        Inherits all attributes from the 'Question' class, including 'description', 'description_img', 'description_style', and timing-related attributes.
    """
    
    def __init__(self, description, options, answer, description_img=None, description_style="color:red; font-size: 30px", timeout=-1):
        """
        Initializes a SpatialReasoningQuestion object with a description, the options, the correct answer, and optional customization.
        Prepares the question for display and interaction by assembling option widgets and setting up observers for user responses.

        Parameters:
            description (str): The text describing the spatial reasoning task.
            options (dict): A mapping of option labels to their associated image paths, used to present choices to the user.
            answer (int): The index or key of the correct option in the `options` dictionary.
            description_img (str, optional): An optional URL or path to a background or contextual image for the question. Defaults to None.
            description_style (str): CSS styling for the question text, allowing customization of its appearance. Defaults to "color:red; font-size: 30px".
            timeout (int, optional): The maximum time for answering the question. Defaults to -1, infinite time.

        Returns:
            None
        """
        
        # Initialize base class.
        super().__init__(description, description_img, description_style, timeout)
        
        # Assign attributes.
        self.timeout = timeout
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
        
        # Sort the directionary of options.
        sorted_options = sorted(self.options)
        
        for option in sorted_options:
            
            # Create image widget and checkbox for each option.
            img_path = option
            image = widgets.Image(
                value=open(img_path, 'rb').read(),
                format='png',
                width=400,
                height=400,
            )
            checkbox = widgets.Checkbox(description=option[-5])
            
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
        
        # Attach event handler to checkboxes for submission recording, answer checking and time calculation.
        def on_checkbox_click(description, change):
            if change['new']==True:
                self.submission = description
                self.check_answer()
                
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
        
        # Check for submission.
        self.wait_for_submission(timeout=self.timeout)
        
        # Calculate total time if timeout was set.
        self.get_time()

        print(self.total_time)
        
        return

class MathsAbilityQuestion(Question):  
    """
    A class to represent a Mathematics Ability question, extending the base Question class.

    Mathematics Ability questions are designed to assess a participant's ability to understand and apply mathematical concepts and procedures within short time.
    
    Attributes:
        calc_steps (list): A sequential list of steps that guide the user through the calculation process required to solve the question. Each step is presented as a string.
        answer (str): The correct answer to the Mathematics Ability question. This can be a numerical value, a mathematical expression, or any string that correctly represents the solution.
        Inherits all attributes from the 'Question' class, including 'description', 'description_img', 'description_style', and any other attributes related to question presentation and interaction handling.
    """
    
    def __init__(self, description, calc_steps, answer, description_img=None, description_style="color:red; font-size: 30px", timeout=-1):
        """
        Initializes a MathsAbilityQuestion object with a description, the options, the correct answer, and optional customization.
        Prepares the question for display and interaction by assembling option widgets and setting up observers for user responses.

        Parameters:
            description (str): The text description of the question.
            calc_steps (list): The sequential steps needed to solve the question.
            answer (str): The correct answer to the question.
            description_img (str, optional): Optional image to accompany the question description.
            description_style (str): CSS styling for the question description.
            timeout (int, optional): The maximum time for answering the question. Defaults to -1, infinite time.

        Returns:
            None
        """
        
        # Initialize base class.
        super().__init__(description, description_img, description_style, timeout)
        
        # Assign attributes.
        self.timeout = timeout
        self.calc_steps = calc_steps
        self.answer = answer
        

        # Create input widgets, and setup response observers.
        self.assemble_input_widgets()
        self.setup_observers()
 
        return

    def assemble_input_widgets(self):
        """
        Prepares interactive input box.

        Parameters:
            None

        Returns:
            None
        """
        
        # Create input widget and checkbox for each option.
        self.text_input = widgets.Text(description="=")
        
        self.button = widgets.Button(description="Submit")
        
        # Combine input and button into a horizontal box.
        self.input_box = widgets.HBox([self.text_input, self.button])
        
        return

    def setup_observers(self):
        """
        Initializes observers for user interactions with option widgets.

        Parameters:
            None

        Returns:
            None
        """
        
        # Attach event handler to button for submission recording, answer checking and time calculation.
        def on_button_click(b):
            self.submission = self.text_input.value
            self.check_answer()
            
        self.button.on_click(on_button_click)
            
        return
    
    def show_calc_steps(self):
        """
        Displays each calculation step sequentially.
        
        Parameter:
            None
        
        Returns:
            None
        """

        # Display each calculation step for 2 seconds.
        for step in self.calc_steps:
            clear_output(wait=True)
            html_out = HTML(f"<span style='color:red; font-size: 30px'>{step}</span>")
            display_html(html_out)
            time.sleep(2)
        
        return

    def display_question(self):
        """
        Inherits the initial display behavior from the base class, then show calculation steps sequentially.

        Parameters:
            None

        Returns:
            None
        """
        
        # Display initial question.
        super().display_question()
        
        # Pause.
        time.sleep(2)
        
        # Display calculation steps.
        self.show_calc_steps()
        
        # Clear Previous content.
        clear_output()
        
        # Record the current time as the start time.
        self.start_time = time.time()
        
        # Display input box.
        display(self.input_box)
        
        # Check for submission.
        self.wait_for_submission(timeout=self.timeout)

        # Calculate total time if timeout was set.
        self.get_time()
        
        return
    
class MemoryQuestion(Question):  
    """
    Represents a Memory Question within a quiz.

    Memory Questions are crafted to assess a participant's ability to recall and recognize information or patterns previously presented.
    
    Attributes:
        sub_questions (list): A list of tuples, each containing a sub-question description and its options.
        answer_list (list): A list of integers, each representing the correct answer index for the corresponding sub-question.
        correctness_list (list): A list tracking the correctness of responses to sub-questions.
        Inherits attributes from the 'Question' class for basic question properties and display customization.
    """
    
    def __init__(self, description, sub_questions, answer_list, description_img=None, description_style="color:red; font-size: 30px"):
        """
        Initializes a MemoryQuestion object with a description, the options, the correct answer, and optional customization.
        Prepares the question for display and interaction by assembling option widgets and setting up observers for user responses.
        
        Parameters:
            description (str): Description of the main question or task.
            sub_questions (list): Sub-questions with their options.
            answer_list (list): Correct answers for each sub-question.
            description_img (str, optional): Image related to the main question.
            description_style (str): CSS style for customizing the question's appearance.

        Returns:
            None
        """
        
        # Initialize base class.
        super().__init__(description, description_img, description_style)
        
        # Assign attributes.
        self.sub_questions = sub_questions
        self.answer_list = answer_list
        self.correctness_list = []

        # Create option widgets, and setup response observers.
        self.assemble_input_widgets()
        self.setup_observers()
 
        return

    def assemble_input_widgets(self):
        """
        Prepares interactive widgets for sub questions.

        Parameters:
            None

        Returns:
            None
        """
        
        # Initialize lists for question, option widgets and answers.
        self.q_n_a_list = []
        
        for idx in range(len(self.sub_questions)):
            
            # Package sub-questions, their options, and answers together.
            sub_question = self.sub_questions[idx]
            question = sub_question[0]
            options = widgets.RadioButtons(
                options=[sub_question[1], sub_question[2], sub_question[3],sub_question[4]],
                disabled=False
            )
            answer = self.answer_list[idx]
            
            self.q_n_a_list.append([question, options, answer])
        
        return

    def setup_observers(self):
        """
        Initializes observers for user interactions with option widgets.

        Parameters:
            None

        Returns:
            None
        """
        
        # Attach event handler to radiobuttons for submission recording, answer checking and time calculation.
        def on_radio_click(answer, change):
            if change['type'] == 'change' and change['name'] == 'value':
                self.answer = answer
                self.submission = change["new"]
                self.check_answer()
                self.correctness_list.append(self.correctness)
                
        for q_n_a in self.q_n_a_list:
            options = q_n_a[1]
            answer = q_n_a[2]
            callback = partial(on_radio_click, answer)
            options.observe(callback, names="value")
            
        return
    
    def show_sub_questions(self):
        """
        Displays each sub questions sequentially.
        
        Parameter:
            None
        
        Returns:
            None
        """
        
        # Display each sub questions until answered.
        for q_n_a in self.q_n_a_list:
            self.submission = None
            clear_output(wait=True)
            question = q_n_a[0]
            html_out = HTML(f"<span>{question}</span>")
            options = q_n_a[1]
            display_html(html_out)
            display(options)
            self.wait_for_submission(timeout=self.timeout)
            
            # Calculate total time if timeout was set.
            self.get_time()
        return            

    def display_question(self):
        """
        Inherits the initial display behavior from the base class, then show sub questions sequentially.

        Parameters:
            None

        Returns:
            None
        """
        
        # Display initial question.
        super().display_question()
        
        # Pause.
        time.sleep(2)
        
        # Record the current time as the start time.
        self.start_time = time.time()
        
        # Display questions in sequence.
        self.show_sub_questions()
        
        return