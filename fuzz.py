
import random
import string
import pandas as pd
import ast
from FAME-ML.lint_engine import getDataLoadCount
from FAME-ML.py_parser import checkLoggingPerData
from empirical.frequency import giveTimeStamp, getAllSLOC

def generate_random_python_file():
    '''Generate random string content resembling a Python file.'''
    content = "\n".join(
        f"def func_{i}():\n    return {random.randint(1, 100)}"
        for i in range(random.randint(1, 10))
    )
    return content

def fuzz_getDataLoadCount():
    '''Fuzz test getDataLoadCount with random Python content.'''
    try:
        with open("temp_test.py", "w") as f:
            f.write(generate_random_python_file())
        result = getDataLoadCount("temp_test.py")
        print(f"getDataLoadCount: {result}")
    except Exception as e:
        print(f"getDataLoadCount failed: {e}")

def fuzz_checkLoggingPerData():
    '''Fuzz test checkLoggingPerData with a random AST object.'''
    try:
        tree = ast.parse(generate_random_python_file())
        result = checkLoggingPerData(tree, "random_func")
        print(f"checkLoggingPerData: {result}")
    except Exception as e:
        print(f"checkLoggingPerData failed: {e}")

def fuzz_giveTimeStamp():
    '''Fuzz test giveTimeStamp without inputs.'''
    try:
        result = giveTimeStamp()
        print(f"giveTimeStamp: {result}")
    except Exception as e:
        print(f"giveTimeStamp failed: {e}")

def fuzz_getAllSLOC():
    '''Fuzz test getAllSLOC with a random DataFrame.'''
    try:
        df = pd.DataFrame({
            "FILE_FULL_PATH": [
                ''.join(random.choices(string.ascii_lowercase, k=10))
                for _ in range(random.randint(1, 100))
            ]
        })
        result = getAllSLOC(df)
        print(f"getAllSLOC: {result}")
    except Exception as e:
        print(f"getAllSLOC failed: {e}")

if __name__ == "__main__":
    fuzz_getDataLoadCount()
    fuzz_checkLoggingPerData()
    fuzz_giveTimeStamp()
    fuzz_getAllSLOC()
