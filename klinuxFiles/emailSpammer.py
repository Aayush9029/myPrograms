import smtplib

print('''
                                  
   ___  ___ _ __   __ _ _ __ ___  _ __ ___   ___ _ __ 
  / _ \/ __| '_ \ / _` | '_ ` _ \| '_ ` _ \ / _ \ '__|
 |  __/\__ \ |_) | (_| | | | | | | | | | | |  __/ |   
  \___||___/ .__/ \__,_|_| |_| |_|_| |_| |_|\___|_|   
           | |                                        
           |_|                                        

                mySite: aayush.wtf

''')


def main():
    who = input('''
    Type Email or emails to spam 
    (seperate emails by comma) eg:
    ---------------------------------------------------
    hey@hotmail.com, spameme@gmail.com, yolo@yahoo.com
    ---------------------------------------------------

    => ''')

    # list of email_id to send the mail
    li = who.split(',')
    print('\n')
    print(f"target/s: {li}")
    print('\n')
    messageToSpam = input('Type a message to spam: ')
    print('\n')
    userName = input('your email id?: ')
    print('\n')
    password = input('your password?: ')
    print('\n')
    howManyTimes = int(input('how many times should i spam? (default 10): '))
    print('\n')

    spam(userName, password, li, messageToSpam, howManyTimes)


def spam(yourEmail, yourPass, listOfEmails, message="testing..", howManyTimes=100):
    for _ in range(howManyTimes):
        for email in listOfEmails:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(yourEmail, yourPass)
            print(f"sending {message} to {email}")
            s.sendmail("sent from iPhone", email, message)
            s.quit()
    ask = input("Press R to spam again: ")
    if ask.lower() == 'r':
        main()


# remove this if this is a part of toolkit
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n   cya later...")
