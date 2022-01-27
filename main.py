import pandas as pd
import os
import smtplib
from getpass import getpass
from email.message import EmailMessage

# Importing the PIL library
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


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

# credentials of sender and address of receiver
sender_address = 'emailforclasses22@gmail.com'
sender_password = getpass('Enter password: ')

pwd = os.getcwd()

# change coordinates to your liking (where the text should be placed) 
bottom_right_corner = (1250, 550)
top_left_corner = (200, 400)


# open CSV file in read mode
df = pd.read_csv("responses/sample_names.csv")

for index, row in df.iterrows():
    name = row['Name']

    # format name properly
    name = name.strip().title()

    # Open the image 
    img = Image.open('certs/cert.png')
    
    # Call draw Method to add 2D graphics in an image
    I1 = ImageDraw.Draw(img)
    
    # Adjusting font size based on String length
    font_size = bottom_right_corner[1] - top_left_corner[1]
    font_size = font_size - int(len(name) * 2.4)
    
    # Custom font style and font size
    myFont = ImageFont.truetype('certs/DancingScript.ttf', font_size)
    
    # Find size of the font in pixels
    x, y = I1.textsize(name, font=myFont)
    
    X = bottom_right_corner[0] - top_left_corner[0]
    Y = bottom_right_corner[1] - top_left_corner[1]
    
    x = (X - x) / 2 + top_left_corner[0]
    y = (Y - y) / 2 + bottom_right_corner[1]
    
    # Add Text to an image
    I1.text((x, y), name, font=myFont, fill=(193, 175, 83))
    
    # Save the edited image
    im = img.convert('RGB')
    im.save(pwd + '/certs/pdfs/' + name + '.pdf', "PDF", resolution=100.0)
    print("Created: " + name + "-cert.pdf")


    # use other fields from each row
    email = row['Email Address']
    quiz_1 = row['Quiz-1 Score']
    quiz_2 = row['Quiz-2 Score']
    quiz_3 = row['Quiz-3 Score']
    quiz_4 = row['Quiz-4 Score']
    assignment = row['Final Assignment']

    receiver_address = email

    # adding a subject, from address and to addess
    message = EmailMessage()
    message['Subject'] = 'Test Email'
    message['From'] = sender_address
    message['To'] = receiver_address

    # body of the mail
    body = f'''Hello {name},

Thank You for participating in the Python Training Sessions conducted and organised by Coding Club JNTUHCEH.

Here is a summary of your scores:
Quiz - 1: {quiz_1}
Quiz - 2: {quiz_2}
Quiz - 3: {quiz_3}
Quiz - 4: {quiz_4}
Final assignment: {assignment}

As a reward of your efforts, here is your certificate!

Thank you {name}
- Coding Club JNTUHCEH


'''

    message.set_content(body)

    # setting the path
    path = f'certs/pdfs/{name}.pdf'

    # opening the file in 'rb' mode
    # and reading in the binary data
    pdf = open(path, 'rb')
    file_data = pdf.read()
    file_name = os.path.basename(pdf.name)
    pdf.close()

    # add the binary data as an attachment
    message.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)

    # send the email using the SMTP Library
    session = smtplib.SMTP('smtp.gmail.com', 587) # use gmail with port
    session.starttls() # enable security
    session.login(sender_address, sender_password) # login with mail_id and password

    session.send_message(message)
    session.quit()

    print(f'Mail Sent to {receiver_address}')
