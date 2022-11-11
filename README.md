# Github Project Automation

This project automates create a Github repo, configuring git locally and setting up basic pre-commit hooks and a gitignore file. This is particular to how I usually start a project which is why I'm making assumptions like:
1. You never have git configured properly
2. You're not ever already using git when you decide to put your project on Github

## What's included

* Create GitHub Repo
* Create Local Repo
* Install gitleaks, 
* Create a README

## Requirements

* Python 3
* PIP
* Docker

## Getting Started

Clone this repo
Create `.env` file:

```
PROJECT_NAME=""
GITHUB_USERNAME=""
LOCAL_PATH=""
GITHUB_ACCESS_TOKEN=""
GITHUB_EMAIL=""
```

```
pip install -r requirements.txt
python3 create.py
```
## TODO

* Dockerize it
* Make it a little more easily customizable
* Test on a brand new VM