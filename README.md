# Secret-Santa-App
This is a Python program to manage a Secret Santa gift exchange. It allows users to add participants, assign Secret Santa pairs, and send email notifications to each participant with their Secret Santa assignment.

## Features

- **Add Participants**: Enter new participants with names and email addresses.
- **List Participants**: View all current participants.
- **Delete Participant**: Remove a participant from the list.
- **Send Secret Santa Emails**: Assign Secret Santas randomly and email each participant with their assignment.
- **Data Storage**: Save participant data in a CSV file and manage historical records.

## Requirements

- Python 3.x
- Google API credentials for Gmail API
- Required Python libraries:
  - `google-auth`
  - `google-auth-oauthlib`
  - `google-auth-httplib2`
  - `google-api-python-client`
  - `base64`
 
## Setup

1. **Install Dependencies**

   Install the required Python libraries using pip:

   ```bash
   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

2. **Google API Credentials**

Create a Google Cloud project and enable the Gmail API.
Download the credentials.json file from the Google Developer Console and place it in the project directory.

3. **OAuth Token**

When you run the program for the first time, it will create a token.json file which stores the OAuth tokens. This allows the application to access your Gmail account.

## Usage
  
Run the application using:

  python secret_santa.py


Follow the menu options to manage participants and send Secret Santa emails.

# Code Overview

## Classes

`Account`
Manages basic account operations.

## Attributes:
account_number: The account's unique identifier.
balance: The account balance.

## Methods:
__init__(self, account_number, balance=0.0): Initializes the account with an account number and optional balance.
deposit(self, amount): Deposits a specified amount into the account.
withdraw(self, amount): Withdraws a specified amount from the account.
get_balance(self): Returns the current balance.
__str__(self): Returns a string representation of the account.
CurrentAccount, SavingsAccount, BusinessAccount
Inherit from Account and represent different types of bank accounts.

## Functions
get_participants()
Prompts the user to input participant names and emails, returning a list of participants.

assign_secret_santa(participants)
Randomly assigns Secret Santas ensuring that no participant is assigned to themselves. Returns a dictionary mapping givers to receivers.

save_to_csv(participants)
Saves participant data to a CSV file named secret_santa.csv.

send_email(giver, receiver)
Uses the Gmail API to send an email to the giver informing them of their Secret Santa recipient.

add_participants()
Adds new participants to the existing list, updates the CSV file.

list_participants()
Displays all participants currently in the CSV file.

delete_participant()
Allows the user to delete a participant by specifying their index from the list.

send_secret_santa_emails()
Assigns Secret Santas, sends out the assignment emails, and renames the CSV file with a timestamp.

## Main Function
The main() function provides a menu-driven interface for the user to interact with the application, handling user choices and executing corresponding functions.

# Contact
For any queries, please contact bruno.bucci@hotmail.com

