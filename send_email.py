from email.mime.text import MIMEText
import smtplib

def send_email(email, weight, average_weight, height, average_height, count, bmi_):
    from_email="your_email"
    from_password="your_password"
    to_email=email
    
    if bmi_<18.5:
        wstr="UnderWeight"
    elif bmi_>=18.5 and bmi_<24.9:
        wstr="Normal"
    elif bmi_>25 and bmi_<29.9:
        wstr="OverWeight"
    elif bmi_>30 and bmi_<34.9:
        wstr="Obese"
    elif bmi_>35:
        wstr="Extremely Obese"
    
    
        
    subject="BMI Survey Data"
    message="Hey there, Your BMI is <strong>%s</strong>. You are <strong>%s</strong>.<br> Your Weight is <strong>%s</strong>.<br> Your height is <strong>%s</strong>.<br> Average weight of all is <strong>%s</strong> <br> Average height of all is <strong>%s</strong> and that is calculated out of <strong>%s</strong> people. <br> Thanks!" % (bmi_, wstr ,weight, height, average_weight, average_height, count)

    msg=MIMEText(message, 'html')
    msg['Subject']=subject
    msg['To']=to_email
    msg['From']=from_email

    gmail=smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)
