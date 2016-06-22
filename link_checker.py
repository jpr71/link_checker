import subprocess
import smtplib
from email.mime.text import MIMEText as text

websites = ["https://www.elegansvariation.org", "http://andersenlab.org"]

for website in websites:
  cmd = ['linkchecker', website]
  output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0].split('\n\n')
  print "output: ", output
  urls = [x for x in output if x[0:3] == "URL"]
  broken_links = set()

  if urls:
    for url in urls:
      local_url = url.split('\n')[0].split('`')[1]

      if local_url not in broken_links:
        broken_links.add(local_url)

    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.ehlo()
    server.starttls()

    server.ehlo()
    server.login("andersenlablinkchecker@gmail.com", "cegwas123")

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    m = "Hey,\n" + "This is your daily link checker and these links are not working on "+ website.strip("https://") +":\n\t" + '\n\t'.join(broken_links)
    recipients = ["danielecook@gmail.com", "joshuapr1@gmail.com"]
    message = text(m)
    message['From'] = "andersenlablinkchecker@gmail.com"
    message['To'] = ", ".join(recipients)
    message['Subject'] = "Broken links in " + website

    server.sendmail("andersenlablinkchecker@gmail.com", recipients, message.as_string())
    server.quit()
