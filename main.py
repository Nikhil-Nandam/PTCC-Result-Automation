import pandas as pd

# handle quiz - 1
quiz_1 = pd.read_csv('responses/Quiz - 1 (Responses).csv')
emails_1 = quiz_1[['Email Address', 'Score']]
emails_1.rename(columns={'Score': 'Quiz-1 Score'}, inplace=True)

# handle quiz - 2
quiz_2 = pd.read_csv('responses/Quiz - 2 (Responses).csv')
emails_2 = quiz_2[['Email Address', 'Name', 'Score']]
emails_2.rename(columns={'Score': 'Quiz-2 Score'}, inplace=True)

# merge quiz_1 and quiz_2 on common emails
emails_names = pd.merge(emails_1, emails_2, how='inner', on='Email Address')
emails_names.to_csv('responses/Quiz 1 & 2 participants.csv')

# handle quiz - 3
quiz_3 = pd.read_csv('responses/Quiz - 3 (Responses).csv')
quiz_3.rename(columns={'Name (Actual name that you want on the certificate)': 'Name', 'Score': 'Quiz-3 Score'}, inplace=True)
emails_3 = quiz_3[['Email Address', 'Quiz-3 Score', 'Name']]
emails_names.drop(columns=['Name'], inplace=True)

# merge emails_names and quiz_3 on common emails
emails_names = pd.merge(emails_names, emails_3, how='inner', on='Email Address')

# required columns
cols = ['Email Address', 'Name', 'Quiz-1 Score', 'Quiz-2 Score', 'Quiz-3 Score']
emails_names = emails_names[cols]

emails_names.to_csv('responses/Quiz 1,2,3 participants.csv')
