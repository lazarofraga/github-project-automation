from dotenv import load_dotenv
from github import Github
import os
import shutil
import subprocess

load_dotenv()
project_name = os.getenv('PROJECT_NAME')
github_access_token = os.getenv('GITHUB_ACCESS_TOKEN')
github_username = os.getenv('GITHUB_USERNAME')
github_project_path =f"https://github.com/{github_username}/{project_name}.git"
github_email = os.getenv("GITHUB_EMAIL")
local_project_path = os.getenv('LOCAL_PATH')
cwd = os.getcwd()

def precommit_hooks():
    shutil.copyfile(f'{cwd}/files/.pre-commit-config.yaml', f'{local_project_path}/.pre-commit-config.yaml')
    os.chdir(local_project_path)
    subprocess.run(['pre-commit', 'autoupdate'])
    subprocess.run(['pre-commit', 'install'])

def create_github_repo():
    user = Github(github_access_token).get_user()
    repo = user.create_repo(project_name)

def init_local_repo():
    shutil.copyfile(f'{cwd}/files/.gitignore', f'{local_project_path}/.gitignore')
    os.chdir(local_project_path)
    subprocess.run(['git', 'config', '--global', 'user.name', f'\"{github_username}\"'])
    subprocess.run(['git', 'config', '--global', 'user.email', f'\"{github_email}\"'])
    subprocess.run(['git', 'init'])
    subprocess.run(['git', 'add', '.gitignore'])
    if not os.path.exists(f'{local_project_path}/README.md'):
        subprocess.run(['echo', '\"# ${PROJECT_NAME}\"', '>>', 'README.md'])
        subprocess.run(['git', 'add', 'README.md'])
    subprocess.run(['git', 'commit', '-m', '\"first commit\"'])
    subprocess.run(['git', 'branch', '-M', 'main'])
    subprocess.run(['git', 'remote', 'add', 'origin', f'https://github.com/{github_username}/{project_name}.git'])
    subprocess.run(['git', 'push', '-u', 'origin', 'main'])

create_github_repo()
init_local_repo()
# Check for docker for pre-commit hooks
p = subprocess.run(['docker', '-v'])
if p.returncode != 0:
    raise Exception( 'Please install docker and current user to docker group' )
precommit_hooks()