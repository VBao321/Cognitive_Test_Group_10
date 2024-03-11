import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
import time

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
    
    def __init__(self, display_region, description, description_img_path=None, timeout=-1,):
        """
        Initializes the Question object with description, optional image, and style.

        Parameters:
            description (str): The question text.
            description_img_path (str, optional): URL or path to an optional image to display with the question. Defaults to None.
            description_style (str): CSS style for the question text. Defaults to "color:red; font-size: 30px".
            timeout (int, optional): The maximum time for answering the question. Defaults to -1, infinite time.
        
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
        
        self.assemble_description_widgets()

        return
    
    def assemble_description_widgets(self):
        description_frame = tk.Frame(self.frame, width=600, height=400, bg="white")
        description_frame.grid(row=0, column=0)
        if self.description_img_path != None:
            self.description_img = ImageTk.PhotoImage(Image.open(self.description_img_path).resize((300,300), Image.ANTIALIAS))
            self.description_box = tk.Label(description_frame, image=self.description_img, text=self.description, compound="top", bg="white", wraplength=600, font=("Helvetica", 12, "bold"))
        else:
            self.description_box = tk.Label(description_frame, text=self.description, bg="white", wraplength=600, font=("Helvetica", 12, "bold"))

        self.description_box.pack()
    
    def display_question(self):
        """
        Displays the question text with optional image and applies specified style. Marks the question as shown and starts timing from this point.
        
        Parameters:
            None
        
        Returns:
            None
        """
        
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

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
            float or str: Depending on the question's state, it returns either the time elapsed in seconds or a message. For unshown questions, it returns a message indicating timing hasn't started. For shown but unanswered questions, it returns the time elapsed since the question was displayed. For answered questions, it returns the total time taken to answer the question.
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
            # Return calculated total time
            return self.total_time
        
    def check_timeout(self):
        if self.shown == True:
            if self.timeout != -1 and self.get_time() > self.timeout:
                self.time_up = True
                self.total_time = self.timeout
                self.frame.destroy()
            
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

    def __init__(self, display_region, description, options, answer, description_img_path=None, timeout=-1):
        """
        Initializes a SpatialReasoningQuestion object with a description, the options, the correct answer, and optional customization.
        Prepares the question for display and interaction by assembling option widgets and setting up observers for user responses.

        Parameters:
            description (str): The text describing the spatial reasoning task.
            options (dict): A mapping of option labels to their associated image paths, used to present choices to the user.
            answer (int): The index or key of the correct option in the `options` dictionary.
            description_img_path (str, optional): An optional URL or path to a background or contextual image for the question. Defaults to None.
            description_style (str): CSS styling for the question text, allowing customization of its appearance. Defaults to "color:red; font-size: 30px".
            timeout (int, optional): The maximum time for answering the question. Defaults to -1, infinite time.

        Returns:
            None
        """

        # Initialize base class.
        super().__init__(display_region, description, description_img_path, timeout)

        # Assign attributes.
        self.timeout = timeout
        self.options = options
        self.answer = answer

        # Create option widgets, and setup response observers.
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
            self.check_answer()
            self.frame.destroy()

        sorted_options = sorted(self.options)
        
        options_frame = tk.Frame(self.frame, width=500, height=450, bg="white")
        options_frame.grid(row=1, column=0)
        
        self.img_a = ImageTk.PhotoImage(Image.open(sorted_options[0]).resize((200,200), Image.ANTIALIAS))
        self.img_b = ImageTk.PhotoImage(Image.open(sorted_options[1]).resize((200,200), Image.ANTIALIAS))
        self.img_c = ImageTk.PhotoImage(Image.open(sorted_options[2]).resize((200,200), Image.ANTIALIAS))
        self.img_d = ImageTk.PhotoImage(Image.open(sorted_options[3]).resize((200,200), Image.ANTIALIAS))
        
        option_img_a = tk.Label(options_frame, image=self.img_a, bg="white")
        option_img_b = tk.Label(options_frame, image=self.img_b, bg="white")
        option_img_c = tk.Label(options_frame, image=self.img_c, bg="white")
        option_img_d = tk.Label(options_frame, image=self.img_d, bg="white")
        
        style = ttk.Style()
        style.configure('White.TRadiobutton', background='white')
        
        radio_button_a = ttk.Radiobutton(options_frame, text="a", value="a", variable=self.submission, command=on_radio_button_changed, style='White.TRadiobutton')
        radio_button_b = ttk.Radiobutton(options_frame, text="b", value="b", variable=self.submission, command=on_radio_button_changed, style='White.TRadiobutton')
        radio_button_c = ttk.Radiobutton(options_frame, text="c", value="c", variable=self.submission, command=on_radio_button_changed, style='White.TRadiobutton')
        radio_button_d = ttk.Radiobutton(options_frame, text="d", value="d", variable=self.submission, command=on_radio_button_changed, style='White.TRadiobutton')
        
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
    
    ANS questions typically involve tasks that require estimation or comparison of quantities, suitable for assessing numerical cognition without relying on exact numerical operations.
    
    Attributes:
        answer (int): The correct answer to the ANS question, indicating the participant's choice. It should be 0 for selecting the option on the left or 1 for selecting the option on the right.
        Inherits all attributes from the 'Question' class, including 'description', 'description_img', 'description_style', and timing-related attributes.
    """
    
    def __init__(self, display_region, description, answer, description_img_path=None, timeout=-1):
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
        super().__init__(display_region, description, description_img_path, timeout)
        
        # Assign attributes.
        self.timeout = timeout
        self.answer = answer
        
        return
    
    def update_fixation_cross(self):
        self.description_img = ImageTk.PhotoImage(Image.open("./ANS_Test/Figures/Fixation_cross.png").resize((300,300), Image.ANTIALIAS))
        self.description_box.configure(image=self.description_img)
        
    def assemble_keyboard_listener(self):
        def on_key_press(event):
            if event.keysym == "Left":
                self.submission.set("Left")
            elif event.keysym == "Right":
                self.submission.set("Right")
            self.check_answer()
            self.frame.destroy()
        
        self.start_time = time.time()
        self.frame.bind("<Key>", on_key_press)
        self.frame.focus_set()

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
        
        self.update_fixation_cross()
        
        self.assemble_keyboard_listener()

        return
    
class MathQuestion(Question):
    """
    A class to represent an Approximate Number System (ANS) question, extending the base Question class.
    
    ANS questions typically involve tasks that require estimation or comparison of quantities, suitable for assessing numerical cognition without relying on exact numerical operations.
    
    Attributes:
        answer (int): The correct answer to the ANS question, indicating the participant's choice. It should be 0 for selecting the option on the left or 1 for selecting the option on the right.
        Inherits all attributes from the 'Question' class, including 'description', 'description_img', 'description_style', and timing-related attributes.
    """
    
    def __init__(self, display_region, description, equation, answer, description_img_path=None, timeout=-1):
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
        super().__init__(display_region, description, description_img_path, timeout)
        
        # Assign attributes.
        self.timeout = timeout
        self.equation = equation
        self.answer = answer
        
        self.assemble_calculation_widgets()
        
        return
        
    def assemble_calculation_widgets(self):
        
        def get_submission(event):
            submission = self.entry.get()
            if submission != "":
                self.submission.set(submission)
                self.check_answer()
                self.frame.destroy()
            
            return
        
        calculation_frame = tk.Frame(self.frame, width=500, height=450, bg="white")
        calculation_frame.grid(row=1, column=0)
        
        self.calculation_box = tk.Label(calculation_frame, bg="white", anchor="center", font=("Helvetica", 24, "bold"))
        
        equal_label = tk.Label(calculation_frame, text="=", bg="white", font=("Helvetica", 12))
        
        self.entry = tk.Entry(calculation_frame, width=22, bg="white", font=("Helvetica", 12), state='disabled')
        self.entry.bind("<Return>", get_submission)
        
        self.calculation_box.grid(row=0, column=0, columnspan=2)
        equal_label.grid(row=1, column=0)
        self.entry.grid(row=1, column=1)
    
    def update_calculation_box(self):
        
        for calculation in self.equation:
            self.calculation_box.configure(text=calculation)
            time.sleep(2)
            
        return
    
    def enable_entry(self):
        self.start_time = time.time()
        
        self.entry.configure(state="normal")
        self.entry.focus_set()
        
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
        self.update_calculation_box()
        
        self.calculation_box.destroy()
        
        self.enable_entry()

        return
    
    
class MemoryQuestion(Question):
    """
    A class to represent an Approximate Number System (ANS) question, extending the base Question class.
    
    ANS questions typically involve tasks that require estimation or comparison of quantities, suitable for assessing numerical cognition without relying on exact numerical operations.
    
    Attributes:
        answer (int): The correct answer to the ANS question, indicating the participant's choice. It should be 0 for selecting the option on the left or 1 for selecting the option on the right.
        Inherits all attributes from the 'Question' class, including 'description', 'description_img', 'description_style', and timing-related attributes.
    """
    
    def __init__(self, display_region, description, options, answer, description_img_path=None, timeout=-1):
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
        super().__init__(display_region, description, description_img_path, timeout)
        
        # Assign attributes.
        self.timeout = timeout
        self.options = options
        self.answer = answer
        
        self.assemble_option_widgets()
        
        return
        
    def assemble_option_widgets(self):
        
        def on_button_clicked(submission):
            self.submission.set(submission)
            self.check_answer()
            self.frame.destroy()
        
        options_frame = tk.Frame(self.frame, width=500, height=450, bg="white")
        options_frame.grid(row=1, column=0)
        
        button_a = tk.Button(options_frame, text=self.options[0], command=lambda: on_button_clicked(self.options[0]), bg="white", font=("Helvetica", 12), width=25)
        button_b = tk.Button(options_frame, text=self.options[1], command=lambda: on_button_clicked(self.options[1]), bg="white", font=("Helvetica", 12), width=25)
        button_c = tk.Button(options_frame, text=self.options[2], command=lambda: on_button_clicked(self.options[2]), bg="white", font=("Helvetica", 12), width=25)
        button_d = tk.Button(options_frame, text=self.options[3], command=lambda: on_button_clicked(self.options[3]), bg="white", font=("Helvetica", 12), width=25)
        
        
        button_a.grid(row=0, column= 0, padx=5, pady=5)
        button_b.grid(row=0, column= 1, padx=5, pady=5)
        button_c.grid(row=1, column= 0, padx=5, pady=5)
        button_d.grid(row=1, column= 1, padx=5, pady=5)
        
        return