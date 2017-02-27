import smtplib

server = smtplib.SMTP('smtp.gmail.com', 587)
print("smtp set")
server.starttls()
print("start ttls")
server.login("priyanshubhatnagar1851996@gmail.com", "Dimpo@22")
print("login complete")

msg = "YOUR MESSAGE!"
server.sendmail("priyanshubhatnagar1851996@gmail.com", "rashika2014@gmail.com", msg)
print("Sent")
server.quit()