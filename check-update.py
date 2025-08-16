#!/usr/bin/env python3

from dotenv import load_dotenv
import subprocess
import git
import os

load_dotenv()

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("REPO_NAME")

REPO_URL = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{REPO}.git"

# REPO_URL = "https://github.com/swati-d-bajpai/git_assignment_HeroVired.git"
LOCAL_REPO_PATH = "/mnt/c/Users/Admin/Documents/GitHub/python/gitassignment/git_assignment_HeroVired"
LAST_COMMIT_FILE = "last_commit.txt"

def clone_or_pull():
    if not os.path.exists(LOCAL_REPO_PATH):
        print("Cloning repository...")
        git.Repo.clone_from(REPO_URL, LOCAL_REPO_PATH)
    else:
        print("Pulling latest changes...")
        # repo = git.Repo(LOCAL_REPO_PATH)
        # origin = repo.remotes.origin
        # origin.pull()

        # subprocess.run(["git", "stash"], cwd=LOCAL_REPO_PATH, check=True)
        subprocess.run(
            ["git", "pull","--no-rebase", REPO_URL],
            cwd=LOCAL_REPO_PATH,
            check=True
        )
        # subprocess.run(["git", "stash", "pop"], cwd=LOCAL_REPO_PATH, check=True)


def get_latest_commit():
    repo = git.Repo(LOCAL_REPO_PATH)
    return repo.head.commit.hexsha

def read_last_commit():
    if os.path.exists(LAST_COMMIT_FILE):
        with open(LAST_COMMIT_FILE, "r") as f:
            return f.read().strip()
    return None

def write_last_commit(sha):
    with open(LAST_COMMIT_FILE, "w") as f:
        f.write(sha)

def main():
    clone_or_pull()
    latest_commit = get_latest_commit()
    last_commit = read_last_commit()

    if latest_commit != last_commit:
        print("New commit detected. Deploying...")
        os.system("./deploy.sh")
        write_last_commit(latest_commit)
    else:
        print("No new commits found.")

if __name__ == "__main__":
    main()
