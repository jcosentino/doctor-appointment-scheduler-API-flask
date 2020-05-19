import re

def isProperUsername(username):
    if username is None: return False
    usernameLength = len(username)
    pattern = '[^a-z0-9]'
    return (usernameLength <= 16 and usernameLength >= 3
            and username[0].isnumeric() is False
            and re.search(pattern, username) is None)
    
def isProperEmail(email):
    return not (str(email) == 'None' or len(email.split('@')) < 2 or
        (email != re.sub(r'[^a-zA-Z0-9@.]', "", email)))

def isProperPassword(password):
    return (bool(re.search('[A-Z]', password)) and
            bool(re.search('[a-z]', password)) and
            bool(re.search('[0-9]', password)) and
            (len(password) >= 6 and len(password) <= 16))

def isProperSecurityQuestion(id):
    return str(id).isnumeric() and id > 0 and id < 4

def isProperSecurityAnswer(answer):
    return len(answer) >= 6 and len(answer) <= 80

def isValidSsn(ssn):
    return len(str(ssn)) == 9 and ssn.isnumeric()

def isValidPhonenumber(pnumber):
    return len(pnumber) == 10 and pnumber.isnumeric()

def isValidMemberid(memberid):
    return len(memberid) == 10 and memberid.isnumeric()

def isValidGroupNumber(groupnumber):
    return (len(str(groupnumber)) > 2 and
            len(str(groupnumber)) <= 16 and
            str(groupnumber).isnumeric())

def checkAvailable(available):
    return available == '1' or available == '0'
