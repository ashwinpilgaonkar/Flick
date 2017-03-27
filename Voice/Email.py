import smtplib

def mail(TO, SUB, CONTENT):
    From = "priyanshubhatnagar1851996@gmail.com"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    print("smtp set")
    server.starttls()
    print("start ttls")
    server.login(From, "PASSWORD")
    print("login complete")

    server.sendmail(From, TO, CONTENT)
    print("Sent")
    server.quit()