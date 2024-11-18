import os
import pandas as pd
import numpy as np
import csv
import time
from datetime import datetime
import subprocess
import shutil
from git import Repo, exc
from logger import loggingObject

logger = loggingObject()


def giveTimeStamp():
    tsObj = time.time()
    return datetime.fromtimestamp(tsObj).strftime('%Y-%m-%d %H:%M:%S')


def deleteRepo(dirName, reason="Unknown", base_dir=None):
    """Deletes the repository directory if it exists."""
    if base_dir:
        dirName = os.path.join(base_dir, dirName)

    logger.info(f"::{reason}:: Deleting {dirName}")
    try:
        if os.path.exists(dirName):
            shutil.rmtree(dirName)
            logger.info(f"Deleted {dirName}")
        else:
            logger.info(f"{dirName} does not exist, skipping.")
    except OSError as e:
        logger.error(f"Failed to delete {dirName}. Error: {e}")


def dumpContentIntoFile(content, filePath):
    """Dumps content into a file and returns the size of the file."""
    logger.info(f"Dumping content into {filePath}")
    try:
        with open(filePath, 'w') as file:
            file.write(content)
        file_size = str(os.stat(filePath).st_size)
        logger.info(f"Content written to {filePath}. File size: {file_size} bytes.")
        return file_size
    except Exception as e:
        logger.error(f"Error dumping content into file {filePath}: {e}")
        raise


def makeChunks(the_list, size_):
    """Splits a list into chunks of the given size."""
    for i in range(0, len(the_list), size_):
        yield the_list[i:i + size_]


def cloneRepo(repo_name, target_dir):
    """Clones a Git repository into the specified directory."""
    cmd_ = f"git clone {repo_name} {target_dir}"
    try:
        logger.info(f"Cloning repo {repo_name} into {target_dir}...")
        subprocess.check_output(['bash', '-c', cmd_])
        logger.info(f"Cloned repo {repo_name} into {target_dir} successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error cloning repo {repo_name}: {e}")


def checkPythonFile(path2dir):
    """Checks if specific Python packages are used in the files within the directory."""
    usageCount = 0
    patternDict = ['sklearn', 'h5py', 'gym', 'rl', 'tensorflow', 'keras', 'tf', 'stable_baselines', 'tensorforce',
                   'rl_coach', 'pyqlearning', 'MAMEToolkit', 'chainer', 'torch', 'chainerrl']
    for root_, dirnames, filenames in os.walk(path2dir):
        for file_ in filenames:
            full_path_file = os.path.join(root_, file_)
            if os.path.exists(full_path_file) and (file_.endswith('.py') or file_.endswith('.ipynb')):
                with open(full_path_file, 'r', encoding='latin-1') as f:
                    pythonFileContent = f.read().split('\n')
                    pythonFileContent = [z_.lower() for z_ in pythonFileContent if z_ != '\n']
                    for content_ in pythonFileContent:
                        for item_ in patternDict:
                            if item_ in content_:
                                usageCount += 1
                                print(f"Pattern found in {full_path_file}: {content_}")
    return usageCount


def days_between(d1_, d2_):
    """Calculates the number of days between two datetime objects."""
    return abs((d2_ - d1_).days)


def getDevEmailForCommit(repo_path_param, hash_):
    """Gets the developer's email from a specific commit hash."""
    author_emails = []
    cdCommand = f"cd {repo_path_param} ; "
    commitCountCmd = f"git log --format='%ae' {hash_}^!"
    command2Run = cdCommand + commitCountCmd

    try:
        logger.info(f"Fetching email for commit {hash_} in {repo_path_param}")
        author_emails = subprocess.check_output(['bash', '-c', command2Run]).decode('utf-8').split('\n')
        author_emails = [email.strip() for email in author_emails if '@' in email]
        author_emails = list(np.unique(author_emails))
        logger.info(f"Found {len(author_emails)} unique developer emails for commit {hash_}.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error fetching commit email for {hash_}: {e}")
    return author_emails


def getDevDayCount(full_path_to_repo, branchName='master', explore=1000):
    """Returns various stats related to commits and developers in a repository."""
    repo_emails = []
    all_commits = []
    all_time_list = []

    logger.info(f"Collecting developer stats for {full_path_to_repo} on branch {branchName}")

    if os.path.exists(full_path_to_repo):
        repo_ = Repo(full_path_to_repo)
        try:
            all_commits = list(repo_.iter_commits(branchName))
        except exc.GitCommandError:
            logger.error(f"Error accessing commits in {full_path_to_repo}: Branch {branchName} not found.")
            return 0, 0, 0, 0

        for commit_ in all_commits:
            commit_hash = commit_.hexsha
            emails = getDevEmailForCommit(full_path_to_repo, commit_hash)
            repo_emails.extend(emails)

            timestamp_commit = commit_.committed_datetime
            str_time_commit = timestamp_commit.strftime('%Y-%m-%d')
            all_time_list.append(str_time_commit)

    all_day_list = [datetime(int(x_.split('-')[0]), int(x_.split('-')[1]), int(x_.split('-')[2]), 12, 30) for x_ in
                    all_time_list]
    try:
        min_day = min(all_day_list)
        max_day = max(all_day_list)
        ds_life_days = days_between(min_day, max_day)
        logger.info(f"Repository lifetime in days: {ds_life_days}")
    except (ValueError, TypeError) as e:
        logger.error(f"Error calculating repo lifetime: {e}")
        ds_life_days = 0

    ds_life_months = round(ds_life_days / 30.0, 5)
    return len(repo_emails), len(all_commits), ds_life_days, ds_life_months


def getPythonFileCount(path2dir):
    """Counts the number of Python files in the given directory."""
    return len([file_ for _, _, filenames in os.walk(path2dir) for file_ in filenames if
                file_.endswith('.py') or file_.endswith('.ipynb')])


def cloneRepos(repo_list, dev_threshold=3, python_threshold=0.10, commit_threshold=25, base_dir=None):
    """Clones a list of repositories and performs various checks on them."""
    counter = 0
    str_ = ''
    all_list = []

    for repo_batch in repo_list:
        for repo_ in repo_batch:
            counter += 1
            print(f"Cloning {repo_}")
            dirName = os.path.join(base_dir, repo_.split('/')[-2] + '@' + repo_.split('/')[-1])
            cloneRepo(repo_, dirName)

            checkPattern = 0
            dev_count, python_count, commit_count, age_months = 0, 0, 0, 0
            flag = True
            all_fil_cnt = sum([len(files) for _, _, files in os.walk(dirName)])
            python_count = getPythonFileCount(dirName)

            if all_fil_cnt <= 0:
                deleteRepo(dirName, 'NO_FILES', base_dir)
                flag = False
            elif python_count < (all_fil_cnt * python_threshold):
                deleteRepo(dirName, 'NOT_ENOUGH_PYTHON_FILES', base_dir)
                flag = False
            else:
                dev_count, commit_count, age_days, age_months = getDevDayCount(dirName)
                if dev_count < dev_threshold:
                    deleteRepo(dirName, 'LIMITED_DEVS', base_dir)
                    flag = False
                elif commit_count < commit_threshold:
                    deleteRepo(dirName, 'LIMITED_COMMITS', base_dir)
                    flag = False

            if flag:
                checkPattern = checkPythonFile(dirName)
                if checkPattern == 0:
                    deleteRepo(dirName, 'NO_PATTERN', base_dir)
                    flag = False

            print('#' * 100)
            str_ += f"{counter},{repo_},{dirName},{checkPattern},{dev_count},{flag}\n"
            tup = (counter, dirName, dev_count, all_fil_cnt, python_count, commit_count, age_months, flag)
            all_list.append(tup)
            print(f"Processed {counter} repos so far")

            if counter % 100 == 0:
                dumpContentIntoFile(str_, 'tracker_completed_repos.csv')
                pd.DataFrame(all_list).to_csv('PYTHON_BREAKDOWN.csv',
                                              header=['INDEX', 'REPO', 'DEVS', 'FILES', 'PYTHON_FILES', 'COMMITS',
                                                      'AGE_MONTHS', 'FLAG'], index=False, encoding='utf-8')

            if counter % 1000 == 0:
                print(str_)

            print('#' * 100)
        print('*' * 10)


if __name__ == '__main__':
    # Set the base directory for cloning repos (or use an environment variable)
    base_dir = os.getenv('REPOS_DIR', './repos')  # You can specify a different base directory here

    repos_df = pd.read_csv('PARTIAL_REMAINING_GITHUB.csv', sep='delimiter')
    print(repos_df.head())
    list_ = np.unique(repos_df['url'].tolist())
    
    t1 = time.time()
    print('Started at:', giveTimeStamp() )
    print('*'*100 )

    
    print('Repos to download:', len(list_)) 
    ## need to create chunks as too many repos 
    chunked_list = list(makeChunks(list_, 100))  ### list of lists, at each batch download 1000 repos 
    cloneRepos(chunked_list)


    print('*'*100 )
    print('Ended at:', giveTimeStamp() )
    print('*'*100 )
    t2 = time.time()
    time_diff = round( (t2 - t1 ) / 60, 5) 
    print('Duration: {} minutes'.format(time_diff) )
    print( '*'*100  )  