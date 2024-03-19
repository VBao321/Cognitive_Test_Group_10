# Cognitive Test Group 10 v2.0.0

This project, developed as part of the BIOS0030 course, is designed to assess various cognitive abilities through a series of tests. Each test focuses on a different aspect of cognitive functioning, providing a comprehensive evaluation of the participants' skills. The repository contains all necessary code to administer these tests.

## Tests Included

The project comprises four distinct tests, each targeting a specific cognitive skill:

1. **ANS Test**: Authored by Lihao Tao, this test evaluates the ability to quickly and accurately estimate the number of items in a visual display.

2. **Math Ability Test**: Developed by Fatin Qistina Mohd Faizal, this test measures mathematical computation skills and the ability to recall and apply sequential calculation steps.

3. **Memory Test**: Created by Hazim Mohammad Tarmizi, this test assesses memory capabilities, focusing on the recall of colors and spatial positions within an image matrix.

4. **Spatial Reasoning Test**: Written by Weiye Bao, this test evaluates the ability to understand three-dimensional space, identifying images that cannot be derived from rotating a given three-dimensional figure.

## Test Details

### ANS Test

The test challenges participants to select the image with a higher count of randomly placed dots. These images flash on the screen for a duration of 0.75 seconds, with a 3-second time limit given for each response. Between each question, there is a 1.5-second interval to prepare for the next one. Participant's accuracy and response time in these quick-paced decisions on number sensing are recorded.

### Math Ability Test

The test comprises 15 mathematical questions, each involving a sequence of calculation steps displayed for 2 seconds per step. Participants are required to memorize these steps and input the final calculation result after the steps are no longer visible. The accuracy of the answers and the time taken to respond are recorded for each question.

### Memory Test

The Memory Test is structured around four main questions, each comprising a matrix of images. Participants are tasked with memorizing as many details as possible about the colors and relative positions of the images within a 20-second timeframe. Following this memorization phase, participants answer five related questions each with a 15-second time limit to test their recall of the images. The test measures both the accuracy of the participants' answers and the time they take to respond.

### Spatial Reasoning Test

Participants are presented with a series of 9 spatial reasoning questions, each involving a randomly generated three-dimensional cube arrangement. The task is to identify, from four options (A, B, C, D), which two-dimensional image cannot be obtained by rotating the given three-dimensional figure. A time limit of 25 seconds is allocated for answering each question, aiming to assess not only accuracy but also the speed of spatial reasoning.

## Data Collection

For each test, participants' accuracy rates and response times are recorded alongside anonymous demographic information, including gender, age, exercise frequency, and fatigue levels (measured using the Karolinska Sleepiness Scale). This data is collected for educational purposes, aiming to practice data analysis and visualization skills within the context of cognitive science.

## Test Dissemination via MyBinder.org

The tests are made accessible online through [mybinder.org](https://mybinder.org), allowing for a wider reach and participation.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/VBao321/Cognitive_Test_Group_10.git/HEAD)

## How to Run - Final Version

1. **Install Required Packages**:
   - Make sure you have the following packages installed:
     - tkinter
     - tk_html_widgets
     - numpy
     - pandas
     - matplotlib
     - BeautifulSoup

2. **Local Installation**:
   - Since the final version utilizes Tkinter GUI, it cannot be displayed on mybinder.org; therefore, you need to install the project locally on your machine.

3. **Open main.ipynb**:
   - After installing all the required packages, navigate to the project directory.
   - Open the main.ipynb file and run the test.

## Software Features

### Integrated User Interface

- Hosted within Python Tkinter GUI for seamless test transitions.

### Comprehensive Test Instructions

- Detailed instructions provided before each test for clarity on test objectives and response methods.

### Randomized Test Questions

- Advanced randomization functions create unique ANS, Math Ability, and Spatial Reasoning Test questions, using seed 60 for consistent reproducibility. This process runs in parallel with user data entry, optimizing test start times.

### Instant Result Feedback

- Immediate feedback on accuracy and percentile ranking after each test.

### User-Friendly UI

- Intuitive Tkinter widgets ensure ease of navigation and interaction.

## Post-v1.0.0 Updates

- Integrated all four tests into a single application using Tkinter GUI, where all interactions are managed through Tkinter widgets.
- Input method for the ANS Test has been updated from clicking buttons to pressing left and right arrow keys.
- Random question generator for Math Ability Test, with seed supports to produce reproducible questions.
- Timer display for every questions.
- Introduced a 5-second instruction display before the start of each test, helping participants understand the test's instructions and objectives.
- Implemented parallel loading of tests to significantly reduce waiting times. While participants input their personal information at the program's startup, tests are loaded in the background. If test content is not fully preloaded by the time the participants completes their personal information, the program will notify the participants and display the respective test's instructions until the content is ready.
