# EITU: Empty rooms at ITU

Tired of running in circles at [ITU](https://itu.dk/) trying to find an empty room for group work or studying?

[EITU](https://eitu.dk) gives you an overview of empty rooms at a glance, and lets you know how long they will be empty for. There is also a handy list of first-come first-serve glass boxes.

## How to run

- Clone the repository
- Make sure you have Python >= 3.5 installed
- `pip install -r requirements.txt`
- `python src/main.py`
- `open index.html`


## Development & Deployment flow

In the repo we will be working with initially two main branches:
- master
- develop

### Development
All development should happen on the 'develop' branch using feature branches for each feature developed.
When starting on a new feature do the following:

1. Make a new branch from 'develop' called 'feature/FEATURE-NAME', replacing FEATURE-NAME with the correct feature NAME
2. Do all the development in that branch
3. When done, create a pull request to the 'develop' branch


### Deployment
The 'master' branch is protected in the sense that, you can only pull request to it, and another member has to approve the pull request in order for it to be merged.
Deployment is done by making a pull request from 'develop' to 'master', NEVER from other branches.
