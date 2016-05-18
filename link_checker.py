import subprocess
import smtplib
from email.mime.text import MIMEText as text

websites = ['http://andersenlab.org/', 'https://elegansvariation.org/']

for website in websites:
  cmd = ['linkchecker', website]
  output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0].split('\n\n')

  urls = [x for x in output if x[0:3] == "URL"]
  broken_links = set()

  if urls:
    for url in urls:
      local_url = url.split('\n')[0].split('`')[1]
      if local_url not in broken_links:
        broken_links.add(local_url)

    server = smtplib.SMTP('smtp.mail.com', 111)

    server.ehlo()
    server.starttls()

    server.ehlo()
    server.login("test.com", "hello")

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    m = "Hey,\n" + "Iowa sucks and these links are not working in "+ website +":\n\t" + '\n\t'.join(broken_links)
    recipients = ["a@gmail.com", "b@gmail.com"]
    message = text(m)
    message['From'] = "abc@gmail.com"
    message['To'] = ", ".join(recipients)
    message['Subject'] = "Broken links in " + website

    server.sendmail("abc@gmail.com", recipients, message.as_string())
    server.quit()
