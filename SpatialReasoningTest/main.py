import cube_constructor as cc
import ipywidgets as widgets
import question_constructor as qc
import SRQuestion_generator as sg
import data_interaction as di
import numpy as np
from IPython.display import display, Image, clear_output, HTML, Javascript
from jupyter_ui_poll import ui_events
import time
from functools import partial

image_list, options_list, answer_list, grid_size_list = sg.SRQuestion_bank(60)

event_info = {
    'type': '',
    'description': '',
}

data_dict = {
    "consent":False,
    "user_id":None,
    "age":None,
    "gender":None,
    "total_score":0,
    "total_time":0,
    "question_3d_image_list":image_list,
    "question_options_list":options_list,
    "question_answer_list":answer_list,
    "grid_size_list":grid_size_list,
    "score_list":[],
    "time_list":[]
}

def wait_for_submission(timeout=-1, interval=0.001, max_rate=4000, allow_interupt=True):
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
    # Start time count.
    start_wait = time.time()

    # Resent event info.
    event_info['type'] = ""
    event_info['description'] = ""
    
    n_proc = int(max_rate*interval)+1

    with ui_events() as ui_poll:
        keep_looping = True
        while keep_looping == True:
            
            # process UI events
            ui_poll(n_proc)

            # end loop if we have waited more than the timeout period
            if (timeout != -1) and (time.time() > start_wait + timeout):
                keep_looping = False

            # end loop if submission appears
            if allow_interupt==True and event_info["description"] != "":
                keep_looping = False

            # add pause before looping to check submission again
            time.sleep(interval)

    return


def consent_submission(b):
    event_info["description"] = b.description
    if b.description == "Yes":
        data_dict["consent"] = True
        
def enforce_uppercase_and_length(text, change):
    new_value = change.new.upper()[:4]  # 转换为大写并限制长度为4
    text.value = new_value

def form_submission(id_input, age_input, gender_input, sports_input, tiredness_input, b):
    # 这里应该有代码来处理或存储用户输入的数据
    event_info["description"] = b.description
    data_dict["user_id"] = id_input.value
    data_dict["age"] = age_input.value
    data_dict["gender"] = gender_input.value
    data_dict["sports"] = sports_input.value
    data_dict["tiredness"] = tiredness_input.value
    


def opening():
    display(HTML("""
    <div style="display: grid; place-items: center;"">
    <div>
    <h3>Please read:</h3>
    <p>We wish to record your response data to an anonymised public data repository.</p>
    <p>Your data will be used for educational teaching purposes practising data analysis and visualisation.</p>
    <p>Please click <b>Yes</b> below if you consent to the upload.</p>
    </div>
    </div>
    """))
    
    # 创建按钮来处理用户的同意/不同意
    btn_yes = widgets.Button(description="Yes", button_style="success")
    btn_no = widgets.Button(description="No", button_style="danger")
    btns_yn = widgets.HBox([btn_yes, btn_no], layout=widgets.Layout(justify_content="center"))
    display(btns_yn)
    btn_yes.on_click(consent_submission)
    btn_no.on_click(consent_submission)
    wait_for_submission()
    clear_output(wait=True)
    if data_dict["consent"] == True:
        display(HTML("""
        <div style="display: grid; place-items: center;">
        <h3>Enter your anonymised ID & personal information</h3>
        <div>
        <h4>Please read the following instructions</h4>
        <p>To generate an anonymous 4-letter unique user identifier please enter:</p>
        <ul>
            <li>Two letters based on the initials (first and last name) of a childhood friend</li>
            <li>Two letters based on the initials (first and last name) of a favourite actor / actress</li>
        </ul>
        <p>e.g., if your friend was Charlie Brown and film star was Tom Cruise, then your ID would be CBTC</p>
        </div>
        </div>
        """))
        id_input = widgets.Text(description="User ID:", layout=widgets.Layout(width="70%"))
        callback = partial(enforce_uppercase_and_length, id_input)
        id_input.observe(callback, names="value")
        age_input = widgets.IntText(description="Age:", layout=widgets.Layout(width="70%"))
        gender_input = widgets.Dropdown(options=['Male', 'Female', 'Other'], description='Gender:', layout=widgets.Layout(width="70%"))
        sports_input = widgets.Dropdown(options=["Frequently(>5 days per week)", "Often(3-4 days per week)", "Sometime(1-2 days per week)", "Never(0 days per week)"], description='How often do you do sports:', layout=widgets.Layout(width="70%"))
        tiredness_input = widgets.IntSlider(min=0, max=10, step=1, description="How tired you are:", layout=widgets.Layout(width="70%"))
        btn_submit = widgets.Button(description="Submit", button_style='info')
        callback = partial(form_submission, id_input, age_input, gender_input, sports_input, tiredness_input)
        btn_submit.on_click(callback)
        form = widgets.VBox([id_input, age_input, gender_input, sports_input, tiredness_input, widgets.HBox([btn_submit], layout=widgets.Layout(justify_content="center"))], layout=widgets.Layout(margin="0 35%"))
        display(form)
        wait_for_submission()

    else:
        display(HTML("<p>No problem, we hope you have a nice day!</p>"))
    
    return data_dict

def percentile_rank_calculator(total_score):
    score_list = np.array(di.get_data(["total_score"],"1-MsGe9J7Ym4NIiC8q0eOTXgge_PqV7G0mxZE4U-r2RM")["total_score"]).astype(int)
    count = sum(1 for score in score_list if score < total_score)
    index = count
    percentage = (index / len(score_list)) * 100
    return percentage

def ending():
    clear_output(wait=True)
    total_score = data_dict["total_score"]
    total_questions = len(data_dict["question_answer_list"])
    percentile_rank = percentile_rank_calculator(total_score)
    display(HTML(f"""
    <div style="display: grid; place-items: center;"">
        <h2>Thank you for taking the test!</h2>
        <p>You have got <strong>{total_score}/{total_questions}</strong>.</p>
        <p>You have beaten <strong>{percentile_rank}%</strong> of people in dataset.</p>
        <h3>Wish you a nice day!</h3>
    </div>
    """))
    
    return

def main():
    question_list = []
    for idx in range(len(answer_list)):
        question = qc.SpatialReasoningQuestion(description="Which of the views (a-d) can not be made by rotating the cube arrangement shown?",
                                               description_img=image_list[idx],
                                               options=options_list[idx],
                                               answer=answer_list[idx],
                                               timeout=25
                                              )
        question_list.append(question)
    opening()
    if data_dict["consent"]:
        clear_output(wait=True)
        for idx in range(len(question_list)):
            qc.set_progress_indicator(question_list[idx], len(question_list))
            qc.update_progress_bar(idx+1)
            question_list[idx].display_question()
            print(question_list[idx].submission)
            time.sleep(1)
            clear_output(wait=True)
        
        for question in question_list:
            if question.correctness:
                data_dict["total_score"] += 1
                data_dict["score_list"].append(1)
            else:
                data_dict["score_list"].append(0)
            data_dict["total_time"] += question.get_time()
            data_dict["time_list"].append(question.get_time())
            
        di.send_data(data_dict, "1FAIpQLSeg0mO4taHmaOFavbHc4yxajewiUt-IiqVT1h63rf7_kGNmBQ")
        ending()
        
main()