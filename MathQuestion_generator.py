import numpy as np

def create_random_MathQuestion(num_steps, num_range=(100,10)):
    """
    Generates a random math equation and its result.

    Parameters:
        num_steps (int): The number of operations to include in the equation.
        num_range (tuple): A tuple of two integers, defining the range of values for the operands.
                           The first element is the maximum for addition and subtraction,
                           and the second is the maximum for multiplication and division.

    Returns:
        tuple: A tuple containing two elements:
            1. equation (list): A list of strings representing the equation steps.
            2. result (str): A string representing the final result of the equation.
    """
    
    # Define the operations list.
    operations = ['+', '-', '\u00D7', '\u00F7']
    
    # Start the equation list with a random number.
    equation = [str(np.random.randint(1, num_range[0]+1))]
    
    # Initialize result with the first number.
    result = int(equation[0])

    # Randomly choose an operation & update the result.
    for step in range(num_steps-1):
        operation = np.random.choice(operations)

        if operation == '+':
            num = np.random.randint(1, num_range[0]+1)
            result += num
        elif operation == '-':
            num = np.random.randint(1, num_range[0]+1)
            result -= num
        elif operation == '\u00D7':
            num = np.random.randint(2, num_range[1]+1)
            result *= num
        else:
            num = np.random.randint(2, num_range[1]+1)
            
            # Ensure division is possible without remainder.
            while num == 0 or result % num != 0:
                num = np.random.randint(1, num_range[1]+1)
            result /= num
            
        # Add the operation and number to the equation list.
        equation.append(f"{operation}{num}")
    
    # Convert the result to int then to string.
    result = str(int(result))
    
    return equation, result

def MathQuestion_bank(seed):
    """
    Generates a bank of random math questions and their answers, based on specified seed.

    Parameters:
        seed (int): A seed for the random number generator to ensure reproducibility.

    Returns:
        tuple: A tuple containing two lists:
            1. equation_list (list): A list of equations for each question, where each equation is represented as a list of strings detailing the steps.
            2. result (str): A list of strings indicating the final results of the equations.
    """
    
    # Set random seed.
    np.random.seed(seed)
    equation_list = []
    answer_list = []
    
    # Generate questions for three levels of difficulty.
    for level in range(3):
        for idx in range(5):
            question = create_random_MathQuestion(level+2, ((idx+1)*10,idx+10))
            equation_list.append(question[0])
            answer_list.append(question[1])
    
    return equation_list, answer_list
