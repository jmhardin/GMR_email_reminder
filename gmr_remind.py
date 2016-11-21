import requests, json, datetime, urllib2, httplib, os

authKey = "getUrOwn" #find it on gmr-site
gameName = "Our Awesome Game" #must be exact
#make your own - must turn on less secure app access on this account
reminder_user = "username@gmail.com"#Change the smtp below if you want to use something other than gmail, gmail will require that you explicitly enable this
reminder_pwd = "yourpass"


#GMR doesn't return steam names, so must input emails by turn order
turn_emails = []
turn_emails.append("email1@domain.com")
turn_emails.append("email2@otherdomain.org")


playerID = ""
mygames = []

#API and such stolen from intermaxim at http://steamcommunity.com/groups/multiplayerrobot/discussions/0/371918937280157414/ and http://pastebin.com/ZK2CjfJM

#Shamelessly stolen
def start():  
    print "...checking authKey and getting playerID..."
    r = requests.get('http://multiplayerrobot.com/api/' +
                     'Diplomacy/AuthenticateUser?authKey=' + authKey)
    global playerID
    playerID = r.text
    #TODO validate playerID --> should be 64bit integer
    print playerID
    print authKey
    update(False);       

def update(raw):
    global mygames
    print "...updating game overview..."
    print '------------start of list----------'
    r = requests.get('http://multiplayerrobot.com/api/Diplomacy/' +
                     'GetGamesAndPlayers?playerIDText=' + playerID +
                     '&authKey=' + authKey)
    
    if raw == True:
        print r.text
        return

    mygames = []
    answer = json.loads(r.text)
    #list my current turns
    counter = 1
    for game in answer["Games"]:
	if (str(game["Name"]) == gameName):
            cturn = int(game["CurrentTurn"]["PlayerNumber"])
            print cturn
            send_email(turn_emails[cturn])
            
    print '------------end of list----------'
#stolen from http://stackoverflow.com/questions/10147455/how-to-send-an-email-with-gmail-as-provider-using-python
def send_email(recipient):
    import smtplib

    
    gmail_user = reminder_user
    gmail_pwd = reminder_pwd
    FROM = reminder_user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = "%s - Turn Reminder" % (gameName)
    TEXT = "You have not yet submitted your turn in %s, this is a reminder to do so.  Thank you (generated automatically)" % (gameName)

    

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
#    print message
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"

start()
