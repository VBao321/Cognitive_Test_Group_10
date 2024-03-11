import numpy as np

def create_random_MathQuestion(num_steps, num_range=(100,10)):
    operations = ['+', '-', '\u00D7', '\u00F7']
    equation = [str(np.random.randint(1, num_range[0]+1))]
    result = int(equation[0])

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
            while num == 0 or result % num != 0:
                num = np.random.randint(1, num_range[1]+1)
            result /= num

        equation.append(f"{operation}{num}")
        
    result = str(result)    
    
    return equation, result

def MathQuestion_bank(seed):
    np.random.seed(seed)
    equation_list = []
    answer_list = []
    for level in range(3):
        for idx in range(5):
            question = create_random_MathQuestion(level+2, ((idx+1)*10,idx+10))
            equation_list.append(question[0])
            answer_list.append(question[1])
    
    return equation_list, answer_list
