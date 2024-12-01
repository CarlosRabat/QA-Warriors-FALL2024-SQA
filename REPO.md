# Activities and Leassons Learned

## Task 1: Create a Git hook to extract Security Weaknesses to a CSV File

- While doing this task we learned how to attached a hook on a repository. The pre-commit file calls the Bandit tool that does a JSON report and then it calls a python script that takes the reports and extracts the information that we think was most valuable and makes a csv file. Another thing that we learned was that in order to make the pre-commit work we needed to make all the files executable. Furthermore, we can add linters to this hook to make our code to a certain standard.

## Task 3: Integrate forensics by modifying 5 Python methods of your choice

- For this task, we integrated forensics by modifying five Python methods in `mining.py`. We created a new class, `logger.py`, with a method `loggingObject()` that sets up logging using the logging module. The logger is configured to store logs in a file (`QA-WARRIORS.log`) with a format that includes timestamps, log levels, and method names. We then integrated this logger into the five modified methods to capture events like function calls, exceptions, and key processing steps. Through implementing forensics, we learned how logging can greatly aid in debugging. It allows for easier identification of where and when something goes wrong in the application. The detailed timestamp and log level give context to each logged event, making it easier to trace any issues and understand the application flow.

## Task 4: Continous Integratrion

- For the continous integration we used Codacy with default settings. Codacy is a static analysis tool that reviews the code to ensure high quality code, the tool analyzes the code when it gets pushed into the repo and blocks the merge if it finds any problems.
