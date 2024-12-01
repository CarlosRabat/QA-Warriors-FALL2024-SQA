# Activities and Leassons Learned

## Task 1: Create a Git hook to extract Security Weaknesses to a CSV File

- While doing this task we learned how to attached a hook on a repository. The pre-commit file calls the Bandit tool that does a JSON report and then it calls a python script that takes the reports and extracts the information that we think was most valuable and makes a csv file. Another thing that we learned was that in order to make the pre-commit work we needed to make all the files executable. Furthermore, we can add linters to this hook to make our code to a certain standard.

## Task 4: Continous Integratrion

- For the continous integration we used Codacy with default settings. Codacy is a static analysis tool that reviews the code to ensure high quality code, the tool analyzes the code when it gets pushed into the repo and blocks the merge if it finds any problems.