import re

def isProperUsername(username):
    if len(username) > 16 or len(username) < 3  \
    or username.isnumeric() or username[0].isnumeric():
        return False
    else:
        return True
    
def isProperEmail(email):
    if len(email.split('@')) < 2 or len(email.split('.')) < 2:
        return False
    return True

def isProperPassword(password):
    if bool(re.search('[A-Z]', password)) and \
    bool(re.search('[a-z]', password)) and \
    bool(re.search('[0-9]', password)) and \
    (len(password) >= 6 and len(password) <= 16):
        return True
    return False

def isValidSsn(ssn):
    return True if len(str(ssn)) is 9 and ssn.isnumeric() \
        else False

def isValidPhonenumber(pnumber):
    return True if len(pnumber) is 10 and pnumber.isnumeric() \
        else False

def isValidMemberid(memberid):
    return True if len(memberid) is 10 and memberid.isnumeric() \
        else False

def isValidGroupNumber(groupnumber):
    return True if len(str(groupnumber)) > 2 and len(str(groupnumber)) <= 16 else False

def checkAvailable(available):
    if available is '1' or available is '0':
        return True
    return False