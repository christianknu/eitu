# EITU: Empty rooms at ITU

Tired of running in circles at ITU trying to find an empty class room? EITU is here to help you.

## How

- Every hour EITU is initiated on [AWS Lambda](https://aws.amazon.com/lambda/details/)
- EITU pulls iCalendar data from [TimeEdit](https://timeedit.itu.dk/)
- EITU commits the changes to the [GitHub page](https://eitu.github.io)

## Requirements

- [Apex](https://github.com/apex)
- Python 2.7
