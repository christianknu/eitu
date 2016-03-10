# EITU: Empty rooms at ITU

Tired of running in circles at ITU trying to find an empty room for group work or studying?

[EITU](https://eitu.github.io) gives you an overview of empty rooms at a glance, and lets you know how long they will be empty for. There is also a handy list of first-come first-serve glass boxes.

## What kind of sorcey is this?!

- EITU runs hourly on [AWS Lambda](https://aws.amazon.com/lambda/details/)
- EITU pulls iCalendar data from [TimeEdit](https://timeedit.itu.dk/)
- EITU commits the changes to [GitHub Pages](https://pages.github.com/)

## How to run

- Clone the repository
- Make sure you have Python 2.7 installed
- `cd functions/eitu`
- `pip install -r requirements.txt`
- `python main.py`
- `open index.html`

## How to deploy

If you wish to deploy EITU on AWS Lambda you will need to install and configure [Apex](https://github.com/apex). You will also need a GitHub token with access to your repository of choice. When I deploy EITU with Apex I run this command standing in the root folder: `apex deploy -e GITHUB_TOKEN=<my GitHub token>`
