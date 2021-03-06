import subprocess
import smtplib
import sys
from email.mime.text import MIMEText as text

websites = ["https://elegansvariation.org", "http://andersenlab.org"]

for website in websites:
  cmd = ['linkchecker', website]
  process = subprocess.Popen( cmd, stdout=subprocess.PIPE )
  output = process.communicate()[0].split('\n\n')
  
  urls = [x for x in output if x[0:3] == "URL"]
  broken_links = set()
  counter = 0
  if urls:
    for url in urls:
      pieces = url.split("\n")
      broken_url = pieces[0].split(' ')[-1]
      parent = " ".join(pieces[2].split(' ')[2:])
      error = " ".join(pieces[-1].split(' ')[-4:])
      print error
      msg = "The following link " + broken_url + " is broken in parent url " + parent + " of source code with "+ error +".\n\n"
      if url not in broken_links:
        broken_links.add(msg)

  if broken_links:
    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.ehlo()
    server.starttls()

    server.ehlo()
    server.login("andersenlablinkchecker@gmail.com", "cegwas123")

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    m = "Hey,\n" + "This is your daily link checker and these links are not working on "+ website.strip("https://") +":\n\n\t" + '\n\t'.join(broken_links) 
    recipients = ["danielecook@gmail.com"]
    message = text(m)
    message['From'] = "andersenlablinkchecker@gmail.com"
    message['To'] = ", ".join(recipients)
    message['Subject'] = "Broken links in " + website

    server.sendmail("andersenlablinkchecker@gmail.com", recipients, message.as_string())
    server.quit()
