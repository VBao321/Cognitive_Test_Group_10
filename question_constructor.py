import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
import time

class Question:
    """
    A class to represent a question with optional image, customizable display style, and timing functionality.
    
    Attributes:
        frame (tk.Frame): The container frame for the question display within the GUI.
        description (str): The text of the question.
        description_img_path (str, optional): The file path to an optional image associated with the question.
        description_img (ImageTk.PhotoImage, optional): The optional image displayed with the question, loaded from description_img_path.
        timeout (int, optional): The time limit for the question in seconds. A value of -1 indicates no time limit.
        time_up (bool): Indicator of whether the time limit for answering the question has been exceeded.
        answer (str): The correct answer to the question.
        submission (tk.StringVar): The user's submitted answer.
        correctness (bool): Indicates whether the submitted answer is correct.
        shown (bool): Tracks whether the question has been displayed to the user.
        total_time (float): The total time taken by the user to answer the question, measured from when the question is displayed to when the answer is submitted.
        start_time (float): The timestamp when the question was displayed.
        end_time (float): The timestamp when the answer was submitted or when the time was checked last.
        elapsed_time (float): The time elapsed from displaying the question to the current moment or to the submission of the answer.

    """
    
    def __init__(self, display_region, description, description_img_path=None, timeout=-1,):
        """
        Initializes the Question object with display_region, description, optional image path, and timeout.

        Parameters:
            display_region (tk.Frame): The GUI region where the question will be displayed.
            description (str): The text of the question.
            description_img_path (str, optional): Path to an optional image to be displayed with the question. Defaults to None.
            timeout (int, optional): The maximum time in seconds allowed for answering the question. Defaults to -1, indicating no time limit.
        
        Returns:
            None
        """
        
        # Assign attributes.
        self.frame = tk.Frame(display_region, bg="white")
        self.description = description
        self.description_img_path = description_img_path
        self.description_img = None
        self.description_box = None
        self.timeout=timeout
        self.description_img = None
        self.time_up = False
        self.answer = None
        self.submission = tk.StringVar()
        self.correctness = None
        self.shown = False
        self.total_time = None
        
        # Create description widgets.
        self.assemble_description_widgets()

        return
    
    def assemble_description_widgets(self):
        """
        Prepares and places the text and optional image components within the question's frame.
        
        Parameters:
            None
            
        Returns:
            None
        """
        
        # Create a sub-frame for the question description and optional image.
        description_frame = tk.Frame(self.frame, width=600, height=450, bg="white")
        description_frame.grid(row=0, column=0)
        
        # If an image path is provided, load the image, otherwise the text only.
        if self.description_img_path != None:
            self.description_img = ImageTk.PhotoImage(Image.open(self.description_img_path).resize((340,340), Image.ANTIALIAS))
            self.description_box = tk.Label(description_frame, image=self.description_img, text=self.description, compound="top", bg="white", wraplength=600, font=("Helvetica", 12, "bold"))
        else:
            self.description_box = tk.Label(description_frame, text=self.description, bg="white", wraplength=600, font=("Helvetica", 12, "bold"))
            
        # Display the text (and optionally image) within the frame.
        self.description_box.pack()
    
    def display_question(self):
        """
        Displays the question text with optional image and applies specified style. Marks the question as shown and starts timing from this point.
        
        Parameters:
            None
        
        Returns:
            None
        """
        
        # Place the question's frame in the center of its display region.
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Mark the question as shown.
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
        if self.submission.get() != "":
            if self.answer == self.submission.get():
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
            float or str: Depending on the question's state, it returns either the time elapsed in seconds or a message. For unshown questions, it returns a message indicating timing hasn't started. For shown but unanswered questions with in time limit, it returns the time elapsed since the question was displayed. For answered questions, it returns the total time taken to answer the question.
        """
        
        # Return warning if question not displayed, else calculate/return time based on submission status.
        if self.shown == False:
            warning = "The question has not been displayed; consequently, the timer has not commenced."
            return warning
        
        elif self.submission.get() == "" and self.time_up == False:
            
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
            # Return calculated total time.
            return self.total_time
        
    def check_timeout(self):
        """
        Checks if the current time exceeds the timeout limit for the question and handles the timeout event.

        Parameters:
            None

        Returns:
            None
        """
        
        # Check if the question has been displayed.
        if self.shown == True:
            
            # Mark time_up as true, set the total_time to the timeout value & remove the question frame from the GUI if the current time exceeds the given time limit .
            if self.timeout != -1 and self.get_time() > self.timeout:
                self.time_up = True
                self.total_time = self.timeout
                self.frame.destroy()
            
        return
    
class SpatialReasoningQuestion(Question):  
    """
    A class to represent a Spatial Reasoning question, extending the base Question class.

    Attributes:
        options (list): A list of image paths used to present according choice options to the user.
        answer (str): The correct answer to the Spatial Reasoning question.
        Inherits all attributes from the 'Question' class.
    """

    def __init__(self, display_region, description, options, answer, description_img_path=None, timeout=-1):
        """
        Initializes a SpatialReasoningQuestion object with question details and display settings.

        Parameters:
            display_region (tk.Frame): The GUI region where the question is to be displayed.
            description (str): The text describing the spatial reasoning task.
            options (list): A list of image paths, each corresponding to a choice option.
            answer (str): The correct option label.
            description_img_path (str, optional): Path to an optional image associated with the question. Defaults to None.
            timeout (int, optional): The maximum time in seconds allowed for answering the question. Defaults to -1, indicating no time limit.

        Returns:
            None
            
        """

        # Initialize base class.
        super().__init__(display_region, description, description_img_path, timeout)

        # Assign attributes.
        self.timeout = timeout
        self.options = options
        self.answer = answer

        # Create option widgets.
        self.assemble_option_widgets()

        return

    def assemble_option_widgets(self):
        """
        Prepares interactive widgets for question options. Options are displayed with associated images.

        Parameters:
            None

        Returns:
            None
        """

        def on_radio_button_changed():
            """
            Check the submitted answer and destroy the question frame upon selection.

            Parameters:
                None

            Returns:
                None
            """
            
            self.check_answer()
            self.frame.destroy()
            
            return
            
        # Sort the options to ensure a consistent order.
        sorted_options = sorted(self.options)
        
        # Create a frame to contain the option images and radio buttons.
        options_frame = tk.Frame(self.frame, width=500, height=450, bg="white")
        options_frame.grid(row=1, column=0)
        
        # Load and option images.
        self.img_a = ImageTk.PhotoImage(Image.open(sorted_options[0]).resize((200,200), Image.ANTIALIAS))
        self.img_b = ImageTk.PhotoImage(Image.open(sorted_options[1]).resize((200,200), Image.ANTIALIAS))
        self.img_c = ImageTk.PhotoImage(Image.open(sorted_options[2]).resize((200,200), Image.ANTIALIAS))
        self.img_d = ImageTk.PhotoImage(Image.open(sorted_options[3]).resize((200,200), Image.ANTIALIAS))
        
        # Place option images in the options frame.
        option_img_a = tk.Label(options_frame, image=self.img_a, bg="white")
        option_img_b = tk.Label(options_frame, image=self.img_b, bg="white")
        option_img_c = tk.Label(options_frame, image=self.img_c, bg="white")
        option_img_d = tk.Label(options_frame, image=self.img_d, bg="white")
        
        # Configure the style for radio buttons.
        style = ttk.Style()
        style.configure('White.TRadiobutton', background='white')
        
        # Create radio buttons for each option.
        radio_button_a = ttk.Radiobutton(options_frame, text="a", value="a", variable=self.submission, command=on_radio_button_changed, style='White.TRadiobutton')
        radio_button_b = ttk.Radiobutton(options_frame, text="b", value="b", variable=self.submission, command=on_radio_button_changed, style='White.TRadiobutton')
        radio_button_c = ttk.Radiobutton(options_frame, text="c", value="c", variable=self.submission, command=on_radio_button_changed, style='White.TRadiobutton')
        radio_button_d = ttk.Radiobutton(options_frame, text="d", value="d", variable=self.submission, command=on_radio_button_changed, style='White.TRadiobutton')
        
        # Organize the radio buttons and images.
        radio_button_a.grid(row=0, column= 0)
        option_img_a.grid(row=1, column= 0)
        radio_button_b.grid(row=0, column= 1)
        option_img_b.grid(row=1, column= 1)
        radio_button_c.grid(row=2, column= 0)
        option_img_c.grid(row=3, column= 0)
        radio_button_d.grid(row=2, column= 1)
        option_img_d.grid(row=3, column= 1)
        
        return
    
class ANSQuestion(Question):
    """
    A class to represent an Approximate Number System (ANS) question, extending the base Question class.
    
    Attributes:
        answer (str): The correct answer to the ANS question. It should be "Left" or "Right".
        Inherits all attributes from the 'Question' class.
    """
    
    def __init__(self, display_region, description, answer, description_img_path=None, timeout=-1):
        """
        Initializes an ANSQuestion object with question details and display settings.
        
        Parameters:
            display_region (tk.Widget): The parent widget where the question will be displayed.
            description (str): The text description of the ANS question.
            answer (str): The correct answer, either "Left" or "Right".
            description_img_path (str, optional): Path to an optional contextual image for the question. Defaults to None.
            timeout (int, optional): The maximum allowed time (in seconds) to answer the question. Defaults to -1 for no limit.

        Returns:
            None
        """
        
        # Initialize base class.
        super().__init__(display_region, description, description_img_path, timeout)
        
        # Assign attributes.
        self.timeout = timeout
        self.answer = answer
        
        return
    
    def update_fixation_cross(self):
        """
        Updates the discription image to show a blank fixation cross.
        
        Parameters:
            None
            
        Returns:
            None
        """
        
        self.description_img = ImageTk.PhotoImage(Image.open("./ANS_Test/Figures/Fixation_cross.png").resize((340,340), Image.ANTIALIAS))
        self.description_box.configure(image=self.description_img)
        
    def assemble_keyboard_listener(self):
        """
        Sets up a keyboard listener to capture the participant's response to the ANS question through key presses.
        
        Parameters:
            None
            
        Returns:
            None
        """
        
        def on_key_press(event):
            
            """
            Set submission for "Left" or "Right" key press, check the answer, and destroy the frame.

            Parameters:
                None

            Returns:
                None
            """
            
            if event.keysym in ["Left", "Right"]:
                self.submission.set(event.keysym)
                self.check_answer()
                self.frame.destroy()
                
            return
        
        # Reset start time upon full display of question to accurately measure response time.
        self.start_time = time.time()
        
        # Bind the key press event to the frame for response capture.
        self.frame.bind("<Key>", on_key_press)
        self.frame.focus_set()

    def display_question(self):
        """
        Displays the question after showing the description and optional image for a brief period.
        
        Inherits the initial display behavior from the base class, then briefly pauses before showing a fixation cross and enable input.

        Parameters:
            None

        Returns:
            None
        """
        
        # Display initial question.
        super().display_question()
        
        # Brief pause before showing the fixation cross.
        time.sleep(0.75)
        
        # Show the fixation cross and set up the keyboard listener for response capture.
        self.update_fixation_cross()
        self.assemble_keyboard_listener()

        return
    
class MathQuestion(Question):
    """
    A class to represent a Math Question, extending the Question class.

    Attributes:
        equation (list): A list containing strings, each representing a part of the math equation or calculation posed to the participant.
        answer (str): The correct answer to the complete math calculation.
        Inherits all attributes from the 'Question' class.
    """
    
    def __init__(self, display_region, description, equation, answer, description_img_path=None, timeout=-1):
        """
        Initializes a MathQuestion object with detailed settings for interaction and display.

        Parameters:
            display_region (tk.Frame): The GUI area where the question is to be shown.
            description (str): A textual description or prompt for the math question.
            equation (list): A list containing strings, each representing a part of the math equation or calculation posed to the participant.
            answer (str): The correct answer to the math problems.
            description_img_path (str, optional): Path to an image related to the question, if applicable. Defaults to None.
            timeout (int, optional): The time limit for responding to the question in seconds. Defaults to -1, indicating no limit.

        Returns:
            None
        """
        
        # Initialize base class.
        super().__init__(display_region, description, description_img_path, timeout)
        
        # Assign attributes.
        self.timeout = timeout
        self.equation = equation
        self.answer = answer
        
        # Create calculation widgets.
        self.assemble_calculation_widgets()
        
        return
        
    def assemble_calculation_widgets(self):
        """
        Prepares interactive widgets for displaying the equation sequence and collecting the participant's answer.
        
        Parameters:
            None
            
        Returns:
            None
        """
        
        def get_submission(event):
            """
            Capture answer submission from entry box and destroy the question frame.

            Parameters:
                None

            Returns:
                None
            """
            
            submission = self.entry.get()
            if submission != "":
                self.submission.set(submission)
                self.check_answer()
                self.frame.destroy()
            
            return
        
        # Create a frame for the equation display and answer input.
        calculation_frame = tk.Frame(self.frame, width=500, height=450, bg="white")
        calculation_frame.grid(row=1, column=0)
        
        # Create label widget to display the equation.
        self.calculation_box = tk.Label(calculation_frame, bg="white", anchor="center", font=("Helvetica", 24, "bold"))
        equal_label = tk.Label(calculation_frame, text="=", bg="white", font=("Helvetica", 12))
        
        # Create entry widget for answer submission.
        self.entry = tk.Entry(calculation_frame, width=22, bg="white", font=("Helvetica", 12), state='disabled')
        self.entry.bind("<Return>", get_submission)
        
        # Organize the label and entry box.
        self.calculation_box.grid(row=0, column=0, columnspan=2)
        equal_label.grid(row=1, column=0)
        self.entry.grid(row=1, column=1)
    
    def update_calculation_box(self):
        """
        Sequentially updates the calculation box with each part of the equation.
        
        parameters:
            None
        Returns:
            None
        """
        
        for calculation in self.equation:
            self.calculation_box.configure(text=calculation)
            time.sleep(2)
            
        return
    
    def enable_entry(self):
        """
        Activates the answer input field and sets it as the focus.
        
        Parameters:
            None
            
        Returns:
            None
        """
        
        # Reset start time upon full display of question to accurately measure response time.
        self.start_time = time.time()
        
        # Enable the entry widget for input and set focus to it.
        self.entry.configure(state="normal")
        self.entry.focus_set()
        
        return
        
    def display_question(self):
        """
        Displays the complete math question to the participant.
        
        Inherits the initial display behavior from the base class, following by showing each part of the equation in sequence, then allows the participant to input their answer.

        Parameters:
            None

        Returns:
            None
        """
        
        # Display initial question.
        super().display_question()
        
        # Show each part of the equation with pauses.
        self.update_calculation_box()
        
        # Remove the calculation box from the display and activate entry box.
        self.calculation_box.destroy()
        self.enable_entry()

        return
    
    
class MemoryQuestion(Question):
    """
    A class to represent a Memory Question within a quiz, extending the Question class.
       
    Attributes:       
        options (list): A list of strings used as choices presented to the participant.
        answer (str): The correct answer to the memory question.
        Inherits all attributes from the Question class.
    """
    
    def __init__(self, display_region, description, options, answer, description_img_path=None, timeout=-1):
        """
        Initializes a MemoryQuestion with specified details for interaction and display.

        Parameters:
            display_region (tk.Frame): The GUI area where the question is to be shown.
            description (str): Text description of the memory task.
            options (list): A list of strings used as available choices for the question.
            answer (str): The correct choice from the options.
            description_img_path (str, optional): Path to an image related to the task. Defaults to None.
            timeout (int, optional): Time limit in seconds to answer. Defaults to -1 for no limit.

        Returns:
            None
        """
        
        # Initialize base class.
        super().__init__(display_region, description, description_img_path, timeout)
        
        # Assign attributes.
        self.timeout = timeout
        self.options = options
        self.answer = answer
        
        # Create option widgets.
        self.assemble_option_widgets()
        
        return
        
    def assemble_option_widgets(self):
        """
        Creates and arranges buttons for each of the provided options.
        
        parameters:
            None
            
        Returns:
            None
        """
        
        def on_button_clicked(submission):
            """
            Set submission for button press, check the answer, and destroy the frame.
            
            Parameters:
                None

            Returns:
                None
            """
            
            self.submission.set(submission)
            self.check_answer()
            self.frame.destroy()
        
        # Set up a frame for the option buttons.
        options_frame = tk.Frame(self.frame, width=500, height=450, bg="white")
        options_frame.grid(row=1, column=0)
        
        # Create option buttons.
        button_a = tk.Button(options_frame, text=self.options[0], command=lambda: on_button_clicked(self.options[0]), bg="white", font=("Helvetica", 12), width=25)
        button_b = tk.Button(options_frame, text=self.options[1], command=lambda: on_button_clicked(self.options[1]), bg="white", font=("Helvetica", 12), width=25)
        button_c = tk.Button(options_frame, text=self.options[2], command=lambda: on_button_clicked(self.options[2]), bg="white", font=("Helvetica", 12), width=25)
        button_d = tk.Button(options_frame, text=self.options[3], command=lambda: on_button_clicked(self.options[3]), bg="white", font=("Helvetica", 12), width=25)
        
        # Organize the option buttons.
        button_a.grid(row=0, column= 0, padx=5, pady=5)
        button_b.grid(row=0, column= 1, padx=5, pady=5)
        button_c.grid(row=1, column= 0, padx=5, pady=5)
        button_d.grid(row=1, column= 1, padx=5, pady=5)
        
        return