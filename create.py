from dotenv import load_dotenv
from github import Github
import os
import shutil
import subprocess


def create_github_repo(github_access_token, project_name):
    user = Github(github_access_token).get_user()
    repo = user.create_repo(project_name)
    return repo


def configure_git_globally(github_username, github_email):
    subprocess.run(['git', 'config', '--global',
                   'user.name', f'\"{github_username}\"'])
    subprocess.run(['git', 'config', '--global',
                   'user.email', f'\"{github_email}\"'])


def init_local_repo(local_project_path):
    os.chdir(local_project_path)
    if not os.path.exists(f'{local_project_path}/.git'):
        print(f"Initializing local git in {local_project_path}")
        os.chdir(local_project_path)
        subprocess.run(['git', 'init'])


def create_gitignore(local_project_path, cwd):
    if not os.path.exists(f'{local_project_path}/.gitignore'):
        print(f"Creating .gitignore in {local_project_path}")
        shutil.copyfile(f'{cwd}/files/.gitignore',
                        f'{local_project_path}/.gitignore')
        os.chdir(local_project_path)
        subprocess.run(['git', 'add', '.gitignore'])


def create_readme(local_project_path):
    if not os.path.exists(f'{local_project_path}/README.md'):
        os.chdir(local_project_path)
        with open(f'{local_project_path}/README.md', 'a') as file:
            file.write(f'# {project_name}')
        subprocess.run(['git', 'add', 'README.md'])


def precommit_hooks(local_project_path, cwd):
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
    configure_git_globally(github_username, github_email)
    init_local_repo(local_project_path)
    create_gitignore(local_project_path, cwd)
    create_readme(local_project_path)
    precommit_hooks(local_project_path, cwd)
    repo = create_github_repo(github_access_token, project_name)
    push_to_github(github_username, project_name)
