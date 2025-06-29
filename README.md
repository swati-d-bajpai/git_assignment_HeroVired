# git_assignment_HeroVired
# Git Assignment – Hero Vired

This repository contains the implementation of the **Git Assignment** provided by Hero Vired. It demonstrates hands-on usage of Git concepts like branching, pull requests, stash, releases, Git LFS, and collaboration.

---

## 📌 Assignment Features

### ✅ Q1: CalculatorPlus Application (20 Points)
- Implemented basic arithmetic operations: add, subtract, multiply, divide.
- **New Feature**: Added square root functionality using Python’s `math.sqrt()`.
- **Bug Fix**: Updated the `divide()` method to handle divide-by-zero errors using exception handling.
- **Collaboration**: Reviewed a classmate’s repository and added them as a collaborator.
- **Releases**:
  - **Version 1 (v1.0)**: Basic arithmetic operations.
  - **Version 2 (v2.0)**: Added square root feature and divide-by-zero bug fix.

### ✅ Q2: Git LFS Integration (10 Points)
- Created a new branch `lfs`.
- Installed and initialized Git LFS.
- Tracked large files using `.gitattributes`.
- Uploaded a zip file (`large_dataset.zip`) larger than 200MB.
- Verified that the file is properly downloaded after cloning the repository on another machine.
- deleted file

### ✅ Q3: Geometry Calculator with Git Stash (20 Points)
- Created a `geometry-calculator` module to calculate:
  - Area of a circle
  - Area of a rectangle
- Used `git stash` to manage work on multiple features simultaneously.
- Implemented feature branches:
  - `feature/circle-area`
  - `feature/rectangle-area`
- Stashed incomplete work before switching branches.
- Completed each feature and pushed them separately.
- Created pull requests and merged after review.

---

## 🚀 Git Workflow Summary

### Branches Used:
- `main`: Stable codebase
- `dev`: Active development branch
- `feature/sqrt`: For square root feature
- `lfs`: For Git LFS test
- `geometry-calculator`: Base branch for geometry task
- `feature/circle-area`: Circle area implementation
- `feature/rectangle-area`: Rectangle area implementation

### Git Stash Usage:
- Stashed changes before switching between `circle-area` and `rectangle-area` to avoid committing incomplete features:
  ```bash
  git stash
  git stash pop
