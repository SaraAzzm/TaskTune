# TaskTune

**TaskTune** is a task management web application that combines productivity and emotional tracking, helping users understand how feelings impact productivity and the potential effects of their emotional state. Users can add tasks with or without deadlines, record their emotions for each task, and access detailed productivity statistics and emotional insights.

# Features

### Flexible Task Management

Users can easily add, edit, complete, and delete tasks as needed.

- **Adding Tasks:** Providing a deadline is optional, offering flexibility for tasks without specific time constraints. Additionally, users select an emotion from a predefined list to reflect how they feel about the task being added.

- **Editing Tasks:** Users can edit any field in a task, including adding, removing, or extending a deadline.  

- **Completing Tasks:** Once a task is completed, it can be marked as such. Tasks with deadlines can still be marked complete, even if they are past the due date. 

- **Deleting Tasks:** A confirmation prompt appears when the user presses the delete button, ensuring tasks are not deleted accidentally.  

### Search and Filter

Easily search for tasks by title or apply filters to view tasks due today, tasks with deadlines, or tasks without deadlines, ensuring quick access to relevant information.

### Emotional Statistics and Indicators

Users can gain valuable emotional insights through the [**Emotional Productivity Score (EPS)**](#what-is-eps), which reflects the emotional quality of the their productivity. The app calculates the EPS based on the emotions recorded for each task, offering a clearer understanding of how feelings impact productivity.

Additionally, users can view a breakdown of their task completion in relation to their emotional state. Indicators highlight how certain emotions may affect task performance. This feature helps users recognize patterns and adjust their approach to tasks for better productivity.

The statistics page contains a dedicated section offering resources to learn about the impact of emotions on productivity and strategies to manage their work effectively while maintaining their well-being.

### Productivity Statistics

View detailed statistics to gain a comprehensive insight into productivity. The app displays the following key productivity metrics:

- **Total Tasks Completed**: Percenatge of all completed tasks.
- **Tasks Completed On Time**: Percentage of tasks that were completed before their deadline (only for tasks that have deadlines).
- **Tasks Completed Past Due Date**: Percentage of tasks that were completed after their deadline.
- **Current Tasks with Deadlines**: Percentage of tasks that have a deadline and are not yet completed.
- **Current Tasks without Deadlines**: Percentage of tasks that do not have a deadline and are still pending.
- **Current Overdue Tasks**: Percentage of tasks that have passed their deadline and have not yet been marked as completed.

These statistics provide valuable insights into overall productivity, helping understand how well tasks and deadlines are being managed.

### Task History

A dedicated history page allows users to view their completed tasks and track their progress over time. It displays the completion date for each task and highlights tasks completed past their due dates by showing the completion date in red.

# What is EPS?

TaskTune uses the **Emotional Productivity Score (EPS)** to provide insights into the user's emotional state and its correlation with productivity. Here's how EPS is calculated:

1. **Emotional Input:** Users select their emotions for each task from a predefined list (e.g., anxious, indifferent, excited). These emotions are assigned numeric values: 

   - Positive: `+1`  
   - Neutral: `0`  
   - Negative: `-1`  

2. **Scoring Algorithm:** The EPS is calculated by summing the emotional values of all completed tasks and dividing by the total number of completed tasks.  

3. **Insights:** The EPS score is categorized into ranges (low, medium, high), with one indicator reflecting the EPS score alone, and another indicator reflecting the correlation between the EPS score and task completion.

The EPS system helps users reflect on their productivity patterns and emotional well-being.

# User Interface Design

### Task Display

- **Overdue Tasks Highlighting:** Overdue tasks are visually highlighted in red. This makes it easy for users to spot tasks that have missed their deadline.
- **Task Order:** Tasks are sorted such that overdue tasks are displayed first, followed by tasks that are on time or without deadlines.

### User Feedback for Empty States

- **No Tasks Available:** When there are no tasks in the system or the task list is empty, a message will display to let the user know there are no tasks to show.
- **No Results from Filtering:** If the user applies a filter and no tasks match the criteria, a message will display indicating no tasks were found for the current filter.
- **No Completed Tasks Yet:** In the History page, if the user has not completed any tasks yet, a message will show letting them know they have no completed tasks.

### Statistics Table Handling

- **Empty Data Representation:** In the statistics tables, if no data is available to calculate percentages (e.g., if the user has not completed any tasks yet), dashes ("--") will be displayed in place of percentages. This ensures a uniform and clear presentation, even when there are no results.

# Technologies Used

- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Backend:** Python (Flask Framework)
- **Database:** SQLite

# Acknowledgment 

TaskTune is my final project created after completing [Harvard's CS50x course](https://cs50.harvard.edu/x/). This project applies many of the technologies and skills I learned throughout the course, including web development, backend programming, and database management.
