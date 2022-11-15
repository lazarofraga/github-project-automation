from dotenv import load_dotenv
from github import Github
import os
import shutil
import subprocess

cwd = os.getcwd()
if not os.path.exists(f'{cwd}/.env'):
    raise Exception("Missing .env file. Please see README.")
load_dotenv()
project_name = os.getenv('PROJECT_NAME')
github_access_token = os.getenv('GITHUB_ACCESS_TOKEN')
github_username = os.getenv('GITHUB_USERNAME')
github_project_path = f"https://github.com/{github_username}/{project_name}.git"
github_email = os.getenv("GITHUB_EMAIL")
local_project_path = os.getenv('LOCAL_PATH')


def create_github_repo():
    user = Github(github_access_token).get_user()
    repo = user.create_repo(project_name)
    return repo


def configure_git_globally():
    subprocess.run(['git', 'config', '--global',
                   'user.name', f'\"{github_username}\"'])
    subprocess.run(['git', 'config', '--global',
                   'user.email', f'\"{github_email}\"'])


def init_local_repo():
    os.chdir(local_project_path)
    if not os.path.exists(f'{local_project_path}/.git'):
        print(f"Initializing local git in {local_project_path}")
        os.chdir(local_project_path)
        subprocess.run(['git', 'init'])


def create_gitignore():
    if not os.path.exists(f'{local_project_path}/.gitignore'):
        print(f"Creating .gitignore in {local_project_path}")
        shutil.copyfile(f'{cwd}/files/.gitignore',
                        f'{local_project_path}/.gitignore')
        os.chdir(local_project_path)
        subprocess.run(['git', 'add', '.gitignore'])


def create_readme():
    if not os.path.exists(f'{local_project_path}/README.md'):
        os.chdir(local_project_path)
        with open(f'{local_project_path}/README.md', 'a') as file:
            file.write(f'# {project_name}')
        subprocess.run(['git', 'add', 'README.md'])


def precommit_hooks():
    if not os.path.exists(f'{local_project_path}/.pre-commit-config.yaml'):
        shutil.copyfile(f'{cwd}/files/.pre-commit-config.yaml',
                        f'{local_project_path}/.pre-commit-config.yaml')
    p = subprocess.run(['docker', '-v'])
    if p.returncode != 0:
        raise Exception(
            'Please install docker and current user to docker group')
    os.chdir(local_project_path)
    subprocess.run(['pre-commit', 'autoupdate'])
    subprocess.run(['pre-commit', 'install'])


def push_to_github(github_username, project_name):
    os.chdir(local_project_path)
    subprocess.run(['git', 'commit', '-m', '\"first commit\"'])
    subprocess.run(['git', 'branch', '-M', 'main'])
    subprocess.run(['git', 'remote', 'add', 'origin',
                   f'https://github.com/{github_username}/{project_name}.git'])
    subprocess.run(['git', 'push', '-u', 'origin', 'main'])


if __name__ == "__main__":
    configure_git_globally()
    init_local_repo()
    create_gitignore()
    create_readme()
    precommit_hooks()
    repo = create_github_repo()
    push_to_github(github_username, project_name)
