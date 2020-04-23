import re

def isProperUsername(username):
    if len(username) > 16 or len(username) < 3  \
    or username[0].isnumeric() or re.search('[^a-zA-Z0-9]', username):
        return False
    else:
        return True
    
def isProperEmail(email):
    if len(email.split('@')) < 2:
        return False
    return True

def isProperPassword(password):
    if bool(re.search('[A-Z]', password)) and \
    bool(re.search('[a-z]', password)) and \
    bool(re.search('[0-9]', password)) and \
    (len(password) >= 6 and len(password) <= 16):
        return True
    return False

def isProperSecurityQuestion(id):
    if id >= 1 and id <= 3:
        return True
    return False

def isProperSecurityAnswer(answer):
    if len(answer) >= 6 and len(answer) <= 80:
        return True
    return False

def isValidSsn(ssn):
    return True if len(str(ssn)) == 9 and ssn.isnumeric() \
        else False

def isValidPhonenumber(pnumber):
    return True if len(pnumber) == 10 and pnumber.isnumeric() \
        else False

def isValidMemberid(memberid):
    return True if len(memberid) == 10 and memberid.isnumeric() \
        else False

def isValidGroupNumber(groupnumber):
    return True if len(str(groupnumber)) > 2 and \
                   len(str(groupnumber)) <= 16 and \
                    str(groupnumber).isnumeric() \
                else False

def checkAvailable(available):
    if available == '1' or available == '0':
        return True
    return False