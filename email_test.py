import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import random


def send_mail(name_x, name_y, cid_x, cid_y, template_path, csv_file):

    # Generating Random Number
    ran = random.randint(1000,9999)

    # Reading the CSV file
    # csv_file = "Test - Form Responses 2.csv"
    df = pd.read_csv(csv_file)

    # Adding column 'certificateID' to CSV
    try:
        df["certificateID"]
    except KeyError:
        df["certificateID"] = [""] * len(df)
    
    # Adding column 'emailsent' to CSV
    try:
        df["emailsent"]
    except KeyError:
        df['emailsent'] = [""] * len(df)

    # Adding column 'event' to CSV
    df["event"] = ["TechNehathon"] * len(df)

    # Adding column 'eventtype' to CSV
    df["eventtype"] = ["Hackathon"] * len(df)


    font = ImageFont.truetype("tahoma.ttf", size=40)
    font1 = ImageFont.truetype("tahoma.ttf", size=10)
    font2 = ImageFont.truetype("tahoma.ttf", size=30)
    font3 = ImageFont.truetype("tahoma.ttf", size=20)


    # Output Folder
    output_folder = 'desired path'

    flag = False
    if all(df["emailsent"]):
        print("All emails were  already sent successfully!")
        flag = True

    # Loop through each row in the Excel data
    for index, row in df.iterrows():
        # Send the email only if 'emailsent' is not 'success'
        if row["emailsent"] != "success":
            # Customize the positioning based on your template
            df.at[index, 'certificateID'] = ran
            template = Image.open(template_path)
            draw = ImageDraw.Draw(template)
            x2, y2 = 290, 320  # coordinates event
            x3, y3 = 590, 475  # coordinates date

            # Accessing data using correct column names
            certificate_text = f"{row['Roll Number']}-{row['Name (On Certificate)']}"
            draw.text((name_x, name_y), certificate_text, font=font, fill='black')
            draw.text((cid_x, cid_y), str(ran), font=font1, fill='black')
            draw.text((x2, y2), row['event'], font=font2, fill='black')
            draw.text((x3, y3), "12-12-23", font=font3, fill='black')



            # Save the modified template as a PDF
            pdf_name = f'{row["Roll Number"]}-{row["Name (On Certificate)"]}.pdf'
            pdf_path = output_folder + '/' + pdf_name
            template.save(pdf_path, 'PDF')

            # Email sending code with attachment
            email_sender = 'email address'
            email_password = "App Password not usual password"
            email_receiver = row['Email']

            # Set the subject and body of the email
            subject = 'Check out Your Certificate Now!'
            body = "Your certificate has arrived"

    
            # if row['emailsent'] != 'success':
            # Set up the email message
            message = MIMEMultipart()
            message['From'] = email_sender
            message['To'] = email_receiver
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))

            # Attach the PDF file
            with open(pdf_path, 'rb') as attachment_file:
                pdf_attachment = MIMEApplication(attachment_file.read(), _subtype="pdf")
                pdf_attachment.add_header('Content-Disposition', 'attachment', filename=pdf_name)
                message.attach(pdf_attachment)

            # Log in and send the email
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls()
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, message.as_string())

                
                # Update Excel Status
                df.at[index, 'emailsent'] = 'success'
                ran += 1
                print(f"Emails Sent Successfully for {email_receiver}")

    # Update Excel file with the transaction status
    df.to_csv(csv_file, index=False)
    if not flag:
        print("All Mails Sent Successfully !")
