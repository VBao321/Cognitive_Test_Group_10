def MemoryQuestion_bank():
    """
    Creates and returns a structured list of memory test questions with associated images to memory, answer options, and correct answers.
    
    Parameters:
        None
    
    Returns:
        questions (list): A list containing question sets, where each set includes an image path and a list of questions with their details.
    """
    questions = [
        [
            "./Memory_Test/Figures/Description_img/MemoryQ_1.png",
            [
                ["What is the color of the star?", ["Red", "Purple", "Yellow", "Green"], "Red", None],
                ["What shape is underneath the pentagon?", ["Star", "Circle", "Rectangle", "Square"], "Rectangle", None],
                ["Which shape has the color yellow?", ["Triangle", "Square", "Pentagon", "Plus"], "Triangle", None],
                ["What shape is in between the triangle and the diamond?", ["Diamond", "Circle", "Triangle", "Octagon"], "Circle", None],
                ["What shape is located at this location?", ["Square", "Pentagon", "Rectangle", "Star"], "Star", "./Memory_Test/Figures/Subquestion_img/MemoryQ_1.png"]
            ]
        ],
        [
            "./Memory_Test/Figures/Description_img/MemoryQ_2.png",
            [
                ["What is the color of the smiley face?", ["Blue", "Purple", "Red", "Yellow"], "Purple", None],
                ["How many arrows are there?", ["1", "0", "3", "2"], "2", None],
                ["Which way is the arrow in the higlighted box is facing?", ["Up", "Down", "Left","Right"], "Up", "./Memory_Test/Figures/Subquestion_img/MemoryQ_2.png"],
                ["What color is the heart?", ["Green", "Pink", "Yellow", "Black"], "Yellow", None],
                ["Which shape has the color green?", ["Lightning", "Moon", "Hexagon", "Square"], "Square", None]
            ]
        ],
        [
            "./Memory_Test/Figures/Description_img/MemoryQ_3.png",
            [
                ["What shape is inside the pentagon?", ["Pentagon", "Heart", "Smiley Face", "Circle"], "Heart", None],
                ["What color is the lightning?", ["Blue", "Red", "Green", "Grey"], "Green", None],
                ["Which way is the arrow inside the diamond is facing?", ["Right", "Down", "Up", "Left"], "Left", None],
                ["How many smiley faces are there in the image?", ["1", "4", "0", "2"], "1", None],
                ["What color is the triangle?", ["Cyan", "Red", "Pink", "Black"], "Pink", None]
            ]            
        ],
        [
            "./Memory_Test/Figures/Description_img/MemoryQ_4.png",
            [
                ["What number is inside the diamond?", ["11", "7", "0", "1"], "7", None],
                ["What color is the number inside the square has?", ["Blue", "Green", "Brown", "Yellow"], "Yellow", None],
                ["Which number is inside the heart?", ["1", "11", "10", "9"], "10", None],
                ["What color does the number 5 has?", ["Orange", "White", "Black", "Green"], "Orange", None],
                ["What color is the star?", ["Orange", "Red", "Black", "Green"], "Black", None]
            ]
        ],
    ]
    
    return questions