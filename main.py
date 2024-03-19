from question_constructor import Question, ANSQuestion, MathQuestion, MemoryQuestion, SpatialReasoningQuestion
from ANSQuestion_generator import ANSQuestion_bank
from MathQuestion_generator import MathQuestion_bank
from MemoryQuestion_generator import MemoryQuestion_bank
from SRQuestion_generator import SRQuestion_bank
from data_interaction import get_data, send_data
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tk_html_widgets import HTMLLabel
import numpy as np
import time
import os
import threading

def test_instruction(frame, instruction):
    """
    Creates and places an instruction label and a timer label within a given frame.
    
    Parameters:
        frame (tk.Frame): The parent frame where the labels will be displayed.
        instruction (str): The HTML content to be displayed in the instruction label.
    
    Returns:
        tuple: A tuple containing the instruction label and timer label objects.
    """
    
    # Create instruction label.
    instruction_label = HTMLLabel(frame, html=instruction, width=75, height=20)
    instruction_label.configure(bg="white")
    
    # Create a timer label.
    timer_label = HTMLLabel(frame, html="<h3 style='background-color:white;'>Questions not loaded yet...</h3>", width=75)
    timer_label.configure(bg="white")
    
    # Organize the labels. 
    instruction_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    timer_label.place(relx=0.5, rely=1, anchor=tk.CENTER)
    
    return instruction_label, timer_label

def test_set_up():
    """
    Sets up the instructions for different test sections and initializes question banks and labels.
    
    Parameters:
        None
    
    Returns:
        None
    """
    
    # Instructions setup for ANS, Math, Memory, and Spatial Reasoning tests.
    ANST_instruction = f"""
    <div style="display:grid; place-items:center; background-color:white;">
    <h2>ANS Test</h2>
    <div style='font-size:12px;'>
    <p>The test challenges participants to select the image with a higher count of randomly placed dots by pressing the according arrow key<strong>LEFT / RIGHT</strong>.</p>
    <p>These images flash on the screen for a duration of 0.75 seconds, with a 3-second time limit given for each response.</p>
    <p>Between each question, there is a 1.5-second interval to prepare for the next one.</p>
    <p>Participant's accuracy and response are recorded.</p>
    </div>
    </div>
    """
    
    MathT_instruction = f"""
    <div style="display:grid; place-items:center; background-color:white;">
    <h2>Math Test</h2>
    <div style='font-size:12px;'>
    <p>The test comprises 15 mathematical questions, each involving a sequence of calculation steps displayed for 2 seconds per step.</p>
    <p>Participants are required to memorize these steps and input the final calculation result after the steps are no longer visible.</p>
    <p>Between each question, there is a 1.5-second interval to prepare for the next one.</p>
    p>Participant's accuracy and response are recorded.</p>
    </div>
    </div>
    """
    
    MemoryT_instruction = f"""
    <div style="display:grid; place-items:center; background-color:white;">
    <h2>Memory Test</h2>
    <div style='font-size:12px;'>
    <p>The Memory Test is structured around four main questions, each comprising a matrix of images.</p>
    <p>Participants are tasked with memorizing as many details as possible about the colors and relative positions of the images within a 20-second timeframe.</p>
    <p>Following this memorization phase, participants answer five related questions each with a 15-second time limit to test their recall of the images.</p>
    p>Participant's accuracy and response are recorded.</p>
    </div>
    </div>
    """
    
    SRT_instruction = f"""
    <div style="display:grid; place-items:center; background-color:white;">
    <h2>Spatial Reasoning Test</h2>
    <div style='font-size:12px;'>
    <p>Participants are presented with a series of 9 spatial reasoning questions, each involving a randomly generated three-dimensional cybe arrangement.</p>
    <p>The task is to identify, from four options (A, B, C, D), which two-dimensional image cannot be obtained by rotating the given three-dimensional figure.</p>
    <p>A time limit of 25 seconds is allocated for answering each question, aiming to assess not only accuracy but also the speed of spatial reasoning.</p>
    p>Participant's accuracy and response are recorded.</p>
    </div>
    </div>
    """
    
    # Create instruction labels for each test.
    ANST_labels = test_instruction(ANSTest_frame, ANST_instruction)
    MathT_labels = test_instruction(MathTest_frame, MathT_instruction)
    MemoryT_labels = test_instruction(MemoryTest_frame, MemoryT_instruction)
    SRT_labels = test_instruction(SRTest_frame, SRT_instruction)
    
    # Load question banks for each test.
    image_list, num_points_list, answer_list= ANSQuestion_bank(60)
    ANST_dict["question_image_list"]=image_list
    ANST_dict["num_left_list"]=[nums[0] for nums in num_points_list]
    ANST_dict["num_right_list"]=[nums[1] for nums in num_points_list]
    ANST_dict["ratio_list"] = [nums[0] / nums[1] for nums in num_points_list]
    ANST_dict["question_answer_list"]=answer_list
    ANSTest(ANSTest_frame, ANST_labels)
    
    equation_list, answer_list = MathQuestion_bank(60)
    MathT_dict["question_equation_list"]=equation_list
    MathT_dict["question_answer_list"]=answer_list
    MathTest(MathTest_frame, MathT_labels)
    
    question_list = MemoryQuestion_bank()
    MemoryT_dict["description_image_list"]= [question[0] for question in question_list]
    MemoryT_dict["question_description_list"]= [subquestion[0] for question in question_list for subquestion in question[1]]
    MemoryT_dict["question_option_list"]= [subquestion[1] for question in question_list for subquestion in question[1]]
    MemoryT_dict["question_answer_list"]= [subquestion[2] for question in question_list for subquestion in question[1]]
    MemoryT_dict["question_image_list"]= [subquestion[3] for question in question_list for subquestion in question[1]]
    MemoryTest(MemoryTest_frame, MemoryT_labels)
    
    image_list, options_list, answer_list, grid_size_list = SRQuestion_bank(60)
    SRT_dict["question_3d_image_list"]=image_list
    SRT_dict["question_options_list"]=options_list
    SRT_dict["question_answer_list"]=answer_list
    SRT_dict["grid_size_list"]=grid_size_list
    SRTest(SRTest_frame, SRT_labels)
    
    return

def ANSTest(ANSTest_frame, ANST_labels):
    """
    Executes the Approximate Number System (ANS) Test within the specified frame.

    Parameters:
        ANSTest_frame (tk.Frame): The frame where the ANS Test will be conducted.
        ANST_labels (tuple): Contains instruction and timer labels for the test.

    Returns:
        None
    """
    
    # Initialize form and sheet IDs for data submission.
    form_id = "1FAIpQLSdQBeIh23TI9CEyO_nF8QEGxjZlCJNStkaCH1WhxvwlQBHSqQ"
    sheet_id = "19uvDxv2Vhb7-bVsUtOyiaTfbkiMAfMGp1R7FqhDixho"
    
    # Initialize list to store question objects.
    question_list = []
    
    # Background threading to manage test sequence and timing.
    def background():
        """
        Manages the sequence of displaying ANS Test questions to the participant.
        
        Parameters:
            None
            
        Returns:
            None
        """
        
        # Wait until the test frame is viewable.
        while ANSTest_frame.winfo_viewable() == 0:
            time.sleep(0.1)
        
        # Countdown 5 seconds before starting the test.
        for t in range(5):
            ANST_labels[1].set_html(f"<h3>Test will start in {5-t} seconds.</h3>")
            time.sleep(1)
        ANST_labels[0].place_forget()
        ANST_labels[1].place_forget()
        
        # Initialize the test sequence, and progress indicator.
        idx = 1
        question_num = 64
        bar_description = tk.Label(progress_indicator, text=f"Q {idx}/{question_num} :", bg="white")
        progress_bar = ttk.Progressbar(progress_indicator, orient="horizontal", length=100, mode="determinate")
        timer = tk.Label(progress_indicator, text="Question not fully displayed", font=("Helvetica", 12), bg="white")
        bar_description.grid(row=0, column=0)
        progress_bar.grid(row=0, column=1)
        timer.grid(row=1, column=0, columnspan=2)
        
        # Update time and question index as test progresses.
        while idx <= question_num:
            question = question_list[idx-1]
            if question.shown == False:
                question.display_question()
            elif question.correctness != None or question.time_up==True:
                time.sleep(1.5)
                idx += 1
                bar_description["text"] = text=f"Q {idx}/{question_num} :"
                progress_bar["value"] = idx*100/question_num
                timer["text"] = "Question not fully displayed"
            else:
                timer["text"] = f"You have {question.timeout-question.get_time():.1f} seconds left"
                question.check_timeout()
                
        # Remove progress indicator.
        progress_indicator.destroy()
        
        # Send data and get result.
        get_result(ANSTest_frame, question_list, ANST_dict, form_id, sheet_id)
        
        # Let result displays for 3 seconds.
        time.sleep(3)
        
        # Remove the frame when the backrgound thread ends.
        return root.after(0, ANSTest_frame.destroy)
    
    # Fetch question bank and setup questions.
    for i in range(len(ANST_dict["question_image_list"])):
        question = ANSQuestion(ANSTest_frame,
                                  "Press the left or right arrow key based on which image has more dots after dots disappear.",
                                  ANST_dict["question_answer_list"][i],
                                  ANST_dict["question_image_list"][i],
                                  timeout=3)
        question_list.append(question)
        
    # Setup progress indicators.
    progress_indicator = tk.Frame(ANSTest_frame, bg="white")
    progress_indicator.place(relwidth=0.5)
    
    # Start background thread.
    threading.Thread(target=background, daemon=True).start()
    
    return

def MathTest(MathTest_frame, MathT_labels):
    """
    Initiates and manages the Math Test within the specified frame.

    Parameters:
        MathTest_frame (tk.Frame): The frame for the Math Test interface.
        MathT_labels (tuple): Tuple containing instruction and timer labels for the test.

    Returns:
        None
    """
    
    # Initialize form and sheet IDs for data submission.
    form_id = "1FAIpQLSeJ4SykSiZi5Y4_NnOtj2hLKR9jYYWd-mZSDHQWoIr39uH_1A"
    sheet_id = "1QJy2MaWVaj95mrJ-kCtuIzV-2a1hcpL2N0a2yeb33-8"

    # Initialize list to store question objects.
    question_list = []
    
    # Background threading to manage test sequence and timing.
    def background():
        """
        Manages the sequence of Math Test questions, displaying each for a set duration.
        
        Parameters:
            None
            
        Returns:
            None
        """
        
        # Wait until the test frame is viewable.
        while MathTest_frame.winfo_viewable() == 0:
            time.sleep(0.1)
            
        # Countdown 5 seconds before starting the test.
        for t in range(5):
            MathT_labels[1].set_html(f"<h3>Test will start in {5-t} seconds.</h3>")
            time.sleep(1)
        MathT_labels[0].place_forget()
        MathT_labels[1].place_forget()
        
        # Initialize the test sequence, and progress indicator.
        idx = 1
        question_num = len(question_list)
        bar_description = tk.Label(progress_indicator, text=f"Q {idx}/{question_num} :", bg="white")
        progress_bar = ttk.Progressbar(progress_indicator, orient="horizontal", length=100, mode="determinate")
        timer = tk.Label(progress_indicator, text="Question not fully displayed", font=("Helvetica", 12), bg="white")
        bar_description.grid(row=0, column=0)
        progress_bar.grid(row=0, column=1)
        timer.grid(row=1, column=0, columnspan=2)
        
        # Update time and question index as test progresses.
        while idx <= question_num:
            question = question_list[idx-1]
            if question.shown == False:
                question.display_question()
            elif question.correctness != None or question.time_up==True:
                idx += 1
                bar_description["text"] = text=f"Q {idx}/{question_num} :"
                progress_bar["value"] = idx*100/question_num
                timer["text"] = "Question not fully displayed"
            else:
                timer["text"] = f"You have {question.timeout-question.get_time():.1f} seconds left"
                question.check_timeout()
                
        # Remove progress indicator.
        progress_indicator.destroy()
        
        # Send data and get result.
        get_result(MathTest_frame, question_list, MathT_dict, form_id, sheet_id)
        
        # Let result displays for 3 seconds.
        time.sleep(3)
        
        # Remove the frame when the backrgound thread ends.
        return root.after(0, MathTest_frame.destroy)
    
    # Fetch question bank and setup questions.
    for i in range(len(MathT_dict["question_equation_list"])):
        question = MathQuestion(MathTest_frame,
                                "Remember the calculation steps shown in sequence, write the final result after they vanish.",
                                MathT_dict["question_equation_list"][i],
                                MathT_dict["question_answer_list"][i],
                                timeout=15)
        question_list.append(question)

    # Setup progress indicators.
    progress_indicator = tk.Frame(MathTest_frame, bg="white")
    progress_indicator.place(relwidth=0.5)
    
    # Start background thread.
    threading.Thread(target=background, daemon=True).start()
    
    return

def MemoryTest(MemoryTest_frame, MemoryT_labels):
    """
    Conducts the Memory Test, displaying images and questions to assess the participant's recall ability.

    Parameters:
        MemoryTest_frame (tk.Frame): Frame dedicated to the Memory Test.
        MemoryT_labels (tuple): Instruction and timer labels for guiding the participant.

    Returns:
        None
    """
    
    # Initialize form and sheet IDs for data submission.
    form_id = "1FAIpQLSe84e3y21rKnMHL0_j1qVyVIPc8Z4vsnmTLkQrDK77vXx4xRg"
    sheet_id = "1Gb0oRYE3iq47QvIrLnrEC7vypCDfn5QccEqoWORhNWs"

    # Initialize list to store question objects.
    question_list = []
    subquestion_list = []
    
    # Background threading to manage test sequence and timing.
    def background():
        """
        Manages the display and timing of Memory Test questions.
        
        Parameters:
            None
            
        Returns:
            None
        """
        
        # Wait until the test frame is viewable.
        while MemoryTest_frame.winfo_viewable() == 0:
            time.sleep(0.1)
        
        # Countdown 5 seconds before starting the test.
        for t in range(5):
            MemoryT_labels[1].set_html(f"<h3>Test will start in {5-t} seconds.</h3>")
            time.sleep(1)
        MemoryT_labels[0].place_forget()
        MemoryT_labels[1].place_forget()
        
        # Initialize the test sequence, and progress indicator.
        i = 1
        idx = 1
        question_num = len(subquestion_list)
        bar_description = tk.Label(progress_indicator, text=f"Q {idx}/{question_num} :", bg="white")
        progress_bar = ttk.Progressbar(progress_indicator, orient="horizontal", length=100, mode="determinate")
        timer = tk.Label(progress_indicator, text="Question not fully displayed", font=("Helvetica", 12), bg="white")
        bar_description.grid(row=0, column=0)
        progress_bar.grid(row=0, column=1)
        timer.grid(row=1, column=0, columnspan=2)
        
        # Update time and question index as test progresses.
        while idx <= question_num:
            
            # Display a question (an image for memorization).
            question = question_list[int(idx/5)]
            if question.shown == False:
                question.display_question()
            else:
                timer["text"] = f"You have {question.timeout-question.get_time():.1f} seconds left"
                question.check_timeout()
            if question.time_up == True:
                
                # Follow by five related subquestions.
                while i <= 5:
                    subquestion = subquestion_list[idx-1]
                    if subquestion.shown == False:
                        subquestion.display_question()
                    elif subquestion.correctness != None or subquestion.time_up==True:
                        i += 1
                        idx += 1
                        bar_description["text"] = text=f"Q {idx}/{question_num} :"
                        progress_bar["value"] = idx*100/question_num
                        timer["text"] = "Question not fully displayed"
                    else:
                        timer["text"] = f"You have {subquestion.timeout-subquestion.get_time():.1f} seconds left"
                        subquestion.check_timeout()
                
                # Reset i for next 5 subquestions.
                i = 1
        
        # Remove progress indicator.
        progress_indicator.destroy()
        
        # Send data and get result.
        get_result(MemoryTest_frame, subquestion_list, MemoryT_dict, form_id, sheet_id)
        
        # Let result displays for 3 seconds.
        time.sleep(3)
        
        # Remove the frame when the backrgound thread ends.
        return root.after(0, MemoryTest_frame.destroy)

    # Fetch question bank and setup questions.
    for i in range(len(MemoryT_dict["description_image_list"])):
        question =Question(MemoryTest_frame,
                             "You will have 20s to remember this picture.",
                             MemoryT_dict["description_image_list"][i],
                             timeout=20)
        question_list.append(question)
    
    # Fetch subquestion bank and setup subquestions.
    for i in range(len(MemoryT_dict["question_image_list"])):
        subquestion = MemoryQuestion(MemoryTest_frame,
                                        MemoryT_dict["question_description_list"][i],
                                        MemoryT_dict["question_option_list"][i],
                                        MemoryT_dict["question_answer_list"][i],
                                        MemoryT_dict["question_image_list"][i],
                                        timeout=10)
        subquestion_list.append(subquestion)

    # Setup progress indicators.
    progress_indicator = tk.Frame(MemoryTest_frame, bg="white")
    progress_indicator.place(relwidth=0.5)
    
    # Start background thread.
    threading.Thread(target=background, daemon=True).start()
    
    return

def SRTest(SRTest_frame, SRT_labels):
    """
    Manages the Spatial Reasoning Test, challenging participants with questions about 3D object rotations.

    Parameters:
        SRTest_frame (tk.Frame): The frame to display the Spatial Reasoning Test.
        SRT_labels (tuple): Instruction and timer labels for the test.

    Returns:
        None
    """
    
    # Initialize form and sheet IDs for data submission.
    form_id = "1FAIpQLScVhZDFl3MBSRnaANngjmYk_5Ej0icxzYqc2ZlyPkcw2MrcFw"
    sheet_id = "1DBMUZZLjtrP1ZDCP7AH0vBK-nyn_AuGgGjFKrsik8M4"

    # Initialize list to store question objects.
    question_list = []
    
    # Background threading to manage test sequence and timing.
    def background():
        """
        Manages the display and timing of Reasoning Test questions.
        
        Parameters:
            None
            
        Returns:
            None
        """
        
        # Wait until the test frame is viewable.
        while SRTest_frame.winfo_viewable() == 0:
            time.sleep(0.1)
            
        # Countdown 5 seconds before starting the test.
        for t in range(5):
            SRT_labels[1].set_html(f"<h3>Test will start in {5-t} seconds.</h3>")
            time.sleep(1)
        SRT_labels[0].place_forget()
        SRT_labels[1].place_forget()
        
        # Initialize the test sequence, and progress indicator.
        idx = 1
        question_num = len(question_list)
        bar_description = tk.Label(progress_indicator, text=f"Q {idx}/{question_num} :", bg="white")
        progress_bar = ttk.Progressbar(progress_indicator, orient="horizontal", length=100, mode="determinate")
        timer = tk.Label(progress_indicator, text="Question not fully displayed", font=("Helvetica", 12), bg="white")
        bar_description.grid(row=0, column=0)
        progress_bar.grid(row=0, column=1)
        timer.grid(row=1, column=0, columnspan=2)
        
        # Update time and question index as test progresses.
        while idx <= question_num:
            question = question_list[idx-1]
            if question.shown == False:
                question.display_question()
            elif question.correctness != None or question.time_up==True:
                idx += 1
                bar_description["text"] = text=f"Q {idx}/{question_num} :"
                progress_bar["value"] = idx*100/question_num
                timer["text"] = "Question not fully displayed"
            else:
                timer["text"] = f"You have {question.timeout-question.get_time():.1f} seconds left"
                question.check_timeout()
        
        # Remove progress indicator.
        progress_indicator.destroy()
        
        # Send data and get result.
        get_result(SRTest_frame, question_list, SRT_dict, form_id, sheet_id)
        
        # Let result displays for 3 seconds.
        time.sleep(3)
        
        # Remove the frame when the backrgound thread ends.
        return root.after(0, SRTest_frame.destroy)

    # Fetch question bank and setup questions.
    for i in range(len(SRT_dict["question_3d_image_list"])):
        question = SpatialReasoningQuestion(SRTest_frame,
                                               "Which of the views (a-d) can not be made by rotating the cube arrangement shown?",
                                               SRT_dict["question_options_list"][i],
                                               SRT_dict["question_answer_list"][i],
                                               SRT_dict["question_3d_image_list"][i],
                                               timeout=25)
        question_list.append(question)
    
    # Setup progress indicators.
    progress_indicator = tk.Frame(SRTest_frame, bg="white")
    progress_indicator.place(relwidth=0.5)
    
    # Start background thread.
    threading.Thread(target=background, daemon=True).start()
    
    return

def get_consent(consent_frame):
    """
    Displays consent information and collects participant's consent response.
    
    Parameters:
        consent_frame (tk.Frame): The frame where consent information and response buttons will be placed.
    
    Returns:
        None
    """
    
    # Create consent label with HTML content.
    consent_text = """
    <div style="display:grid; place-items:center; background-color:white;">
    <h2>Please read:</h2>
    <div style='font-size:12px;'>
    <p>We wish to record your response data to an anonymised public data repository.</p>
    <p>Your data will be used for educational teaching purposes practising data analysis and visualisation.</p>
    <p>Please click <b>Yes</b> below if you consent to the upload.</p>
    </div>
    </div>
    """
    consent_label = HTMLLabel(consent_frame, html=consent_text, height=12)
    consent_label.configure(bg="white")
    
    # update consent value upon button click.
    def consent_submission(consent):
        """
        Processes the participant's consent response.

        Parameters:
            consent (bool): The participant's consent response, where True indicates consent and False indicates refusal.

        Returns:
            None
        """
        consent_frame.destroy()
        main_dict["consent"]=consent
    
    # Create "Yes" and "No" buttons for consent.
    yes_btn = tk.Button(consent_frame, text="Yes", width=15, command=lambda: consent_submission(True), font=("Helvetica", 15), bg="#28a745", fg="white")
    no_btn = tk.Button(consent_frame, text="No", width=15, command=lambda: consent_submission(False), font=("Helvetica", 15), bg="#dc3545", fg="white")
    
    # Organize the consent widgets.
    consent_label.grid(row=0, column=0, columnspan=2)
    yes_btn.grid(row=1, column=0, sticky="E")
    no_btn.grid(row=1, column=1, sticky="W")
    
    return

def get_info(info_frame):
    """
    Displays fields for participants to enter their personal information and an anonymized ID.

    Parameters:
        info_frame (tk.Frame): The frame where the information form is to be displayed.

    Returns:
        None
    """
    
    def info_submission():
        """
        Collects the user's input from the information form and stores it in the main_dict, and destroy the frame.

        Parameters:
            None
            
        Returns:
            None
        """
        
        # Retrieve and store each piece of information from the form in the main dictionary.
        main_dict["user_id"]=id_input.get()
        main_dict["gender"]=gender_input.get()
        main_dict["age"]=age_input.get()
        main_dict["sports"]=sports_input.get()
        main_dict["tiredness"]=tiredness_input.get()
        
        # Destroy the info frame to move to the next part of the application.
        info_frame.destroy()
        
        return
    
    def enforce_policy(*args):
        """
        Enforces input policy for the user ID field (No more than 4 characters, all uppercase).

        Parameters:
            *args: Arbitrary argument list. Not directly used but necessary for compatibility with Tkinter's trace callback signature.

        Returns:
            None
        """
        
        # Retrieve the current value of the user ID input field.
        value = user_id.get()
        
        # Enforce maximum 4 uppercase characters for user ID.
        user_id.set(value[:4].upper())
            
        return
    
    # Display instructions for entering personal information.
    instruction = """
        <div style="display: grid; place-items: center; background-color:white;">
        <h2>Enter your anonymised ID & personal information</h2>
        <div style='font-size:12px;'>
        <h4>Please read the following instructions</h4>
        <p>To generate an anonymous 4-letter unique user identifier please enter:</p>
        <ul>
            <li>Two letters based on the initials (first and last name) of a childhood friend</li>
            <li>Two letters based on the initials (first and last name) of a favourite actor / actress</li>
        </ul>
        <p>e.g., if your friend was Charlie Brown and film star was Tom Cruise, then your ID would be CBTC</p>
        <h4>For tiredness measurement we use the Karolinska Sleepiness Scale</h4>
        <ul>
            <li>Extrmely alert - 1</li>
            <li>Very Alert     - 2</li>
            <li>Alert          - 3</li>
            <li>Rather alert   - 4</li>
            <li>Neither alert or sleepy - 5</li>
            <li>Some signs of sleepiness - 6</li>
            <li>Sleepy but no effort to keep awake - 7</li>
            <li>Sleepy but some effort to keep awake - 8</li>
            <li>Very sleepy, great effort to keep awake, fighting sleep - 9</li>
            <li>Extremely sleepy, can't keep awake - 10</li>
        </ul>
        </div>
        </div>
        """
    
    instruction_label = HTMLLabel(info_frame, html=instruction, height=32)
    instruction_label.configure(bg="white")
    instruction_label.grid(row=0, column=0, columnspan=2)
    
    # Create input fields for personal information.
    user_id = tk.StringVar()
    user_id.trace_add("write", enforce_policy)
    
    id_label = tk.Label(info_frame, text="User ID:", bg="white", font=("Helvetica", 12))
    id_input = tk.Entry(info_frame, textvariable=user_id, width=22, bg="white", font=("Helvetica", 12))
    
    gender_label = tk.Label(info_frame, text="Gender:", bg="white", font=("Helvetica", 12))
    gender_input = ttk.Combobox(info_frame, values=["Male", "Female", "Other"], width=20, font=("Helvetica", 12))
    
    age_label = tk.Label(info_frame, text="Age:", bg="white", font=("Helvetica", 12))
    age_input = tk.Spinbox(info_frame, from_=0, to=120, width=21, bg="white", font=("Helvetica", 12))
    
    sports_label = tk.Label(info_frame, text="How often you do sports:", bg="white", font=("Helvetica", 12))
    sports_input = ttk.Combobox(info_frame, values=["Frequently(>5 days per week)", "Often(3-4 days per week)", "Sometime(1-2 days per week)", "Never(0 days per week)"], width=20, font=("Helvetica", 12))
    
    tiredness_label = tk.Label(info_frame, text="How tired you are:", bg="white", font=("Helvetica", 12))
    tiredness_input = tk.Scale(info_frame, from_=0, to=10, orient="horizontal", resolution=1, length=200, bg="white", font=("Helvetica", 12))
    
    submission_btn = tk.Button(info_frame, text="Submit", width=15, command=info_submission, font=("Helvetica", 15), bg="#28a745", fg="white")
    
    # Organize the widgets.
    id_label.grid(row=1, column=0, sticky="E")
    id_input.grid(row=1, column=1, sticky="W", pady=5)
    gender_label.grid(row=2, column=0, sticky="E")
    gender_input.grid(row=2, column=1, sticky="W", pady=5)
    age_label.grid(row=3, column=0, sticky="E")
    age_input.grid(row=3, column=1, sticky="W", pady=5)
    sports_label.grid(row=4, column=0, sticky="E")
    sports_input.grid(row=4, column=1, sticky="W", pady=5)
    tiredness_label.grid(row=5, column=0, sticky="E")
    tiredness_input.grid(row=5, column=1, sticky="W", pady=5)
    submission_btn.grid(row=6, column=0, columnspan=2, pady=5)
    
    return

def percentile_rank_calculator(total_score, sheet_id):
    """
    Calculates the percentile rank of a participant's score compared to scores retrieved from a data sheet.

    Parameters:
        total_score (int): The participant's total score to be ranked.
        sheet_id (str): The ID for the google spreadsheet containing score data.

    Returns:
        percentage (float): The percentile rank of the participant's score.
    """
    
    # Retrieve the list of scores from the spreadsheet identified by sheet_id.
    score_list = np.array(get_data(["total_score"], sheet_id)["total_score"]).astype(int)
    
    if len(score_list) != 0:
            
        # Count the number of scores less than the participant's score.
        index = sum(1 for score in score_list if score < total_score)

        # Calculate the percentile rank.
        percentage = (index / len(score_list)) * 100
    
    # Recurse until google sheet update data.
    else:
        return percentile_rank_calculator(total_score, sheet_id)
    
    return percentage

def get_result(frame, question_list, Test_dict, form_id, sheet_id):
    """
    Displays the test results, sending data for storage and calculating percentile rank.

    Parameters:
        frame (tk.Frame): The frame to display the test results.
        question_list (list): List of Question objects used in the test.
        Test_dict (dict): Dictionary holding test-related data.
        form_id (str): ID for the form where results are sent.
        sheet_id (str): ID for the sheet used for percentile rank calculation.

    Returns:
        None
    """
    
    # Display uploading message before data fully uploadeed.
    uploading_label = f"""
    <h3 style="text-align: center; background-color: white">Data is uploading...</h3>
    """
    uploading_label = HTMLLabel(frame, html=uploading_label, height=12)
    uploading_label.pack()
    uploading_label.configure(bg="white")
    
    # Calculate scores and compile result summary.
    for question in question_list:
        if question.correctness:
            Test_dict["total_score"] += 1
            Test_dict["score_list"].append(1)
        else:
            Test_dict["score_list"].append(0)
        Test_dict["total_time"] += question.get_time()
        Test_dict["time_list"].append(question.get_time())
    
    # Send test data and display results in the provided frame.
    if send_data(main_dict|Test_dict, form_id):
        
        total_score = Test_dict["total_score"]
        total_questions = len(Test_dict["question_answer_list"])
        percentile_rank = percentile_rank_calculator(total_score, sheet_id)
        result = f"""
        <div style="text-align: center; background-color: white; font-size: 12px;">
        <p>You have got <strong>{total_score}/{total_questions}</strong>.</p>
        <p>You have beaten <strong>{percentile_rank}%</strong> of people in dataset.</p>
        </div>
        """

        result_label = HTMLLabel(frame, html=result, height=12)
        
        # Replace uploading message with results.
        uploading_label.pack_forget()
        result_label.pack()
        result_label.configure(bg="white")
    
    return

def opening(root):
    """
    Initiates the opening frames of the application, including displaying consent and collecting participant information.

    Parameters:
        root (tk.Tk): The root window of the application where the frames will be placed.

    Returns:
        None
    """
    
    # Create frames for consent and personal information forms.
    consent_frame = tk.Frame(root, bg="white")
    info_frame = tk.Frame(root, bg="white")
    
    # Add frames to the frames list, awaiting display.
    frames.append(consent_frame)
    frames.append(info_frame)
    
    # initialize the two opening frames.
    get_consent(consent_frame)
    get_info(info_frame)
    
    return

def ending(root):
    """
    Concludes the test sequence by displaying the closing messages to the participant.

    Parameters:
        root (tk.Tk): The root window of the application where the results and messages will be displayed.

    Returns:
        None
    """
    
    ending_frame = tk.Frame(root, bg="white", width=600, height=800)
    frames.append(ending_frame)
    
    closing_text = f"""
    <div style="text-align: center; background-color:white;"">
    <h2>Thank you for taking the test!</h2>
    <h2>Wish you a nice day!</h2>
    <p style="font-size: 12px;">Please contact <strong>a.fedorec@ucl.ac.uk</strong> if you have any questions or concerns.</p>
    </div>
    """

    closing_label = HTMLLabel(ending_frame, html=closing_text, height=12)
    closing_label.pack()
    closing_label.configure(bg="white")
    
    return

# The entry point of application.
if __name__ == "__main__":

    def switch_frame():
        """
        Switches between different test frames based on their visibility and participant consent. Exits application if consent is False.
        
        Parameters:
            None
            
        Returns:
            None
        """
        
        # Display new frame until the previous one has been destroyed.
        for frame in frames:
            frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            while frame.winfo_exists() == 1:
                
                # Exit the application if consent is False.
                if main_dict["consent"] == False:
                    root.after(0, root.destroy)
        
        return
    
    # Dictionary to hold the main participant data.
    main_dict = {
        "consent":None,
        "user_id":None,
        "age":None,
        "gender":None,
        "sports":None,
        "tiredness":None,
    }

    # Dictionaries to hold test-specific data.
    ANST_dict = {
        "total_score":0,
        "total_time":0,
        "question_image_list":[],
        "num_left_list":[],
        "num_right_list":[],
        "ratio_list":[],
        "question_answer_list":[],
        "score_list":[],
        "time_list":[]
    }

    MathT_dict = {
        "total_score":0,
        "total_time":0,
        "question_equation_list":[],
        "question_answer_list":[],
        "score_list":[],
        "time_list":[]
    }

    MemoryT_dict = {
        "total_score":0,
        "total_time":0,
        "description_image_list":[],
        "question_image_list":[],
        "question_answer_list":[],
        "score_list":[],
        "time_list":[]
    }

    SRT_dict = {
        "total_score":0,
        "total_time":0,
        "question_3d_image_list":[],
        "question_options_list":[],
        "question_answer_list":[],
        "grid_size_list":[],
        "score_list":[],
        "time_list":[]
    }
    
    # List to hold the test frames for display management.
    frames=[]
    
    # Set up the main application window.
    root = tk.Tk()
    root.configure(bg='white')
    root.attributes('-topmost', True)
    root.title("Cognitive Test")
    window_size = (800, 900)

    # Position the window in the center of the screen.
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (window_size[0] / 2)
    y = (screen_height / 2) - (window_size[1] / 2)
    root.geometry('%dx%d+%d+%d' % (window_size[0], window_size[1], x, y))
    
    # Create opening frames for consent and participant info.
    opening(root)
    
    # Create the test frames and append them to the frames list for later display.
    ANSTest_frame = tk.Frame(root, bg="white", width=600, height=900)
    frames.append(ANSTest_frame)
    MathTest_frame = tk.Frame(root, bg="white", width=600, height=900)
    frames.append(MathTest_frame)
    MemoryTest_frame = tk.Frame(root, bg="white", width=600, height=900)
    frames.append(MemoryTest_frame)
    SRTest_frame = tk.Frame(root, bg="white", width=600, height=900)
    frames.append(SRTest_frame)

    # Create ending frame for final messages display.
    ending(root)

    # Start the test setup in a background thread.
    threading.Thread(target=test_set_up, daemon=True).start()

    # Start frame switching in a background thread.
    threading.Thread(target=switch_frame, daemon=True).start()

    # Start the application event loop
    root.mainloop()