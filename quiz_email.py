import pandas as pd
import smtplib
from getpass import getpass
from email.message import EmailMessage


# handle quiz - 1
quiz_1 = pd.read_csv('responses/1.csv')
emails_1 = quiz_1[['Email Address', 'Score']]
emails_1.rename(columns={'Score': 'Quiz-1 Score'}, inplace=True)
# emails_1['Email Address'].str.lower()


# handle quiz - 2
quiz_2 = pd.read_csv('responses/2.csv')
emails_2 = quiz_2[['Email Address', 'Name', 'Score']]
emails_2.rename(columns={'Score': 'Quiz-2 Score'}, inplace=True)
# emails_2['Email Address'].str.lower()

# merge quiz_1 and quiz_2 on common emails
emails_names = pd.merge(emails_1, emails_2, how='inner', on='Email Address')
emails_names.to_csv('responses/Quiz 1 & 2 participants.csv')


# handle quiz - 3
quiz_3 = pd.read_csv('responses/3.csv')
quiz_3.rename(columns={'Name (Actual name that you want on the certificate)': 'Name', 'Score': 'Quiz-3 Score'}, inplace=True)
emails_3 = quiz_3[['Email Address', 'Quiz-3 Score', 'Name']]
emails_names.drop(columns=['Name'], inplace=True)
# emails_3['Email Address'].str.lower()

# merge emails_names and quiz_3 on common emails
emails_names = pd.merge(emails_names, emails_3, how='inner', on='Email Address')


# handle quiz - 4
quiz_4 = pd.read_csv('responses/4.csv')
quiz_4.rename(columns={'Name (Actual name that you want on the certificate)': 'Name', 'Score': 'Quiz-4 Score'}, inplace=True)
emails_4 = quiz_4[['Email Address', 'Quiz-4 Score', 'Name']]
emails_names.drop(columns=['Name'], inplace=True)
# emails_4['Email Address'].str.lower()

# merge emails_names and quiz_3 on common emails
emails_names = pd.merge(emails_names, emails_4, how='inner', on='Email Address')

name_confirmations = pd.read_csv('responses/Final Name Confirmations.csv')

emails_names = pd.merge(emails_names, name_confirmations, how='left', on='Email Address')

emails_names['Name (Actual name that you want on the certificate)'].fillna(emails_names['Name'], inplace=True)
emails_names.drop(columns=['Name'], inplace=True)
emails_names.rename(columns={'Name (Actual name that you want on the certificate)': 'Name',}, inplace=True)

cols = ['Email Address', 'Name', 'Quiz-1 Score', 'Quiz-2 Score', 'Quiz-3 Score', 'Quiz-4 Score']
emails_names = emails_names[cols]
emails_names['Email Address'] = emails_names['Email Address'].str.lower()

emails_names.to_excel('responses/Quizzes.xlsx')
emails_names.to_csv('responses/Quizzes.csv')

# credentials of sender and address of receiver
sender_address = 'ccjntuhceh@gmail.com'
sender_password = getpass('Enter password: ')


# open CSV file in read mode
df = pd.read_csv("responses/Quiz 1,2,3,4.csv")

for index, row in df.iterrows():
    name = row['Name']
    email = row['Email Address']
    quiz_1 = row['Quiz-1 Score']
    quiz_2 = row['Quiz-2 Score']
    quiz_3 = row['Quiz-3 Score']
    quiz_4 = row['Quiz-4 Score']

    receiver_address = email

    # adding a subject, from address and to addess
    message = EmailMessage()
    message['Subject'] = 'Python Training Quiz Results'
    message['From'] = sender_address
    message['To'] = receiver_address

    # body of the mail
    body = f'''Hello {name},

Thank You for attempting all the quizzes.

Here is a summary of your scores:
Quiz - 1: {quiz_1}
Quiz - 2: {quiz_2}
Quiz - 3: {quiz_3}
Quiz - 4: {quiz_4}

Thank you {name}!
- Coding Club JNTUHCEH


'''

    message.set_content(body)

    # send the email using the SMTP Library
    session = smtplib.SMTP('smtp.gmail.com', 587) # use gmail with port
    session.starttls() # enable security
    session.login(sender_address, sender_password) # login with mail_id and password

    session.send_message(message)
    session.quit()

    print(f'Mail Sent to {receiver_address}')
