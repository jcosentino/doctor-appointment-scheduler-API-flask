import pytest
from routes.validation import isProperUsername, \
                              isProperEmail, \
                              isProperPassword, \
                              isValidSsn, \
                              isValidPhonenumber, \
                              isValidMemberid, \
                              isValidGroupNumber, \
                              checkAvailable \

def test_isProperUsername():
    valid_username1 = 'user123'
    invalid_username1 = 'user12345678901234567890' # too long
    invalid_username2 = 'ab' # too short
    invalid_username3 = '1user123' # begins withnumeric
    invalid_username4 = 'user123!#' # special characters
    assert isProperUsername(valid_username1) is True
    assert isProperUsername(invalid_username1) is False
    assert isProperUsername(invalid_username2) is False
    assert isProperUsername(invalid_username3) is False
    assert isProperUsername(invalid_username4) is False

def test_isProperEmail():
    valid_email1 = 'test@example.com'
    invalid_email = 'testexample.com' # no @ symbol
    assert isProperEmail(valid_email1) is True
    assert isProperEmail(invalid_email) is False

def test_isProperPassword():
    valid_password1 = 'Password1'
    invalid_password1 = 'Password' # no numbers
    invalid_password2 = 'password' # no uppercase letters
    invalid_password3 = 'PASSWORD' # no lowercase letters
    invalid_password4 = 'p' # too long
    invalid_password5 = 'Password12345678901234567890' # too short
    assert isProperPassword(valid_password1) is True
    assert isProperPassword(invalid_password1) is False
    assert isProperPassword(invalid_password2) is False
    assert isProperPassword(invalid_password3) is False
    assert isProperPassword(invalid_password4) is False
    assert isProperPassword(invalid_password5) is False

def test_isValidSsn():
    valid_ssn1 = '123456789'
    invalid_ssn1 = '1' # too short
    invalid_ssn2 = '12345678901234567890' # too long
    invalid_ssn3 = '123456789x' # not numeric
    assert isValidSsn(valid_ssn1) is True
    assert isValidSsn(invalid_ssn1) is False
    assert isValidSsn(invalid_ssn2) is False
    assert isValidSsn(invalid_ssn3) is False

def test_isValidPhonenumber():
    valid_pNumber1 = '7185551234'
    invalid_pNumber1 = '71855512345' # too long
    invalid_pNumber2 = '718555' # too short
    invalid_pNumber3 = 'testpnumber' # not numeric
    assert isValidPhonenumber(valid_pNumber1) is True
    assert isValidPhonenumber(invalid_pNumber1) is False
    assert isValidPhonenumber(invalid_pNumber2) is False
    assert isValidPhonenumber(invalid_pNumber3) is False

def test_isValidMemberid():
    valid_memberid1 = '1234567890'
    invalid_memberid1 = '123456789000' # too long
    invalid_memberid2 = '12345' # too short
    invalid_memberid3 = '123456789x' # not numeric
    assert isValidMemberid(valid_memberid1) is True
    assert isValidMemberid(invalid_memberid1) is False
    assert isValidMemberid(invalid_memberid2) is False
    assert isValidMemberid(invalid_memberid3) is False

def test_isValidGroupNumber():
    valid_groupNumber1 = 123456789
    invalid_groupNumber1 = 1 # too short
    invalid_groupNumber2 = 12345678901234567890 # too long
    invalid_groupNumber3 = 'testgroupnumber' # not numeric
    assert isValidGroupNumber(valid_groupNumber1) is True
    assert isValidGroupNumber(invalid_groupNumber1) is False
    assert isValidGroupNumber(invalid_groupNumber2) is False
    assert isValidGroupNumber(invalid_groupNumber3) is False

def test_checkAvailable():
    available0 = '0'
    available1 = '1'
    invalid_available1 = '2' # not 0 or 1
    invalid_available2 = 'x' # not 0 or 1
    assert checkAvailable(available0) is True
    assert checkAvailable(available1) is True
    assert checkAvailable(invalid_available1) is False
    assert checkAvailable(invalid_available2) is False