import os
import csv
import random
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
import base64

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Step 1: Get information from the user
def get_participants():
    participants = []
    print("Enter the participants' names and emails. Type 'done' when finished.")
    while True:
        name = input("Enter name (or type 'done' to finish): ")
        if name.lower() == 'done':
            break
        email = input("Enter email (or type 'done' to finish): ")
        if email.lower() == 'done':
            break
        participants.append({"name": name, "email": email})
    return participants

# Step 2: Assign Secret Santa
def assign_secret_santa(participants):
    givers = participants[:]
    receivers = participants[:]
    
    # Shuffle until no one is assigned to themselves
    valid_assignment = False
    while not valid_assignment:
        random.shuffle(receivers)
        valid_assignment = all(giver["email"] != receiver["email"] for giver, receiver in zip(givers, receivers))

    assignments = {giver["email"]: receiver for giver, receiver in zip(givers, receivers)}
    return assignments

# Step 3: Save data in a .csv file
def save_to_csv(participants):
    filename = "secret_santa.csv"
    fieldnames = ["name", "email"]

    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for participant in participants:
            writer.writerow(participant)
    
    return filename

# Step 4: Send email using Gmail API
def send_email(giver, receiver):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    message_text = (
        f"Hi {giver['name']},\n\n"
        f"You have been chosen as the Secret Santa for {receiver['name']} ({receiver['email']}).\n\n"
        f"Happy gifting!"
    )
    message = MIMEText(message_text)
    message['to'] = giver['email']
    message['subject'] = 'Your Secret Santa Assignment'
    message['from'] = 'your-email@gmail.com'  # Replace with your email

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {'raw': raw}

    message = (service.users().messages().send(userId="me", body=body)
               .execute())
    print(f"Email sent to {giver['email']} with message ID: {message['id']}")

def add_participants():
    participants = get_participants()
    if len(participants) > 0:
        file_name = save_to_csv(participants)
        print(f"Participants' data saved to {file_name}")
    else:
        print("No participants added.")

def send_secret_santa_emails():
    filename = "secret_santa.csv"
    
    if not os.path.exists(filename):
        print("No participants found.")
        return
    
    participants = []
    with open(filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            participants.append(row)
    
    if len(participants) < 2:
        print("At least two participants are required for Secret Santa.")
        return
    
    assignments = assign_secret_santa(participants)

    for giver_email, receiver in assignments.items():
        giver = next(participant for participant in participants if participant["email"] == giver_email)
        send_email(giver, receiver)
        print(f"{giver['name']} will give a gift to {receiver['name']}.")

    new_filename = "processed_secret_santa.csv"
    if os.path.exists(filename):
        if not os.path.exists(new_filename):
            os.rename(filename, new_filename)
            print(f"File renamed to {new_filename}")
        else:
            print(f"File {new_filename} already exists, no renaming needed")

def main():
    while True:
        print("\nSecret Santa Menu")
        print("1. Add Participants")
        print("2. Send Secret Santa Emails")
        print("3. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            add_participants()
        elif choice == '2':
            send_secret_santa_emails()
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()
