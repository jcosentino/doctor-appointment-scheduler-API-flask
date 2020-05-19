import pytest
from API.routes.validation import isProperUsername, \
                              isProperEmail, \
                              isProperPassword, \
                              isProperSecurityQuestion, \
                              isProperSecurityAnswer, \
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
    invalid_username5 = 'User123' # capital letter
    invalid_username6 = 'usEr123' # capital letter
    invalid_username7 = '' # empty
    assert isProperUsername(valid_username1) is True
    assert isProperUsername(invalid_username1) is False
    assert isProperUsername(invalid_username2) is False
    assert isProperUsername(invalid_username3) is False
    assert isProperUsername(invalid_username4) is False
    assert isProperUsername(invalid_username5) is False
    assert isProperUsername(invalid_username6) is False
    assert isProperUsername(invalid_username7) is False

def test_isProperEmail():
    valid_email1 = 'test@example.com'
    invalid_email1 = 'testexample.com' # no @ symbol
    invalid_email2 = 'test!*%#@example.com' # invalid symbols
    invalid_email3 = 'test!@example.com' # invalid symbol
    invalid_email4 = '' # empty
    assert isProperEmail(valid_email1) is True
    assert isProperEmail(invalid_email1) is False
    assert isProperEmail(invalid_email2) is False
    assert isProperEmail(invalid_email3) is False
    assert isProperEmail(invalid_email4) is False

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

def test_isProperSecurityQuestion():
    valid_id1 = 1
    valid_id2 = 2
    valid_id3 = 3
    invalid_id1 = 'test' # wrong type
    invalid_id2 = 4 # out of range
    invalid_id3 = 0 # out of range
    assert isProperSecurityQuestion(valid_id1) is True
    assert isProperSecurityQuestion(valid_id2) is True
    assert isProperSecurityQuestion(valid_id3) is True
    assert isProperSecurityQuestion(invalid_id1) is False
    assert isProperSecurityQuestion(invalid_id2) is False
    assert isProperSecurityQuestion(invalid_id3) is False

def test_isProperSecurityAnswer():
    valid_answer1 = 'Here is a valid answer'
    invalid_answer1 = '' # no text
    invalid_answer2 = 'abc' # too short
    invalid_answer3 = 'abcdefghijklmnopqrstuvwxyz1234567890\
                       abcdefghijklmnopqrstuvwxyz1234567890\
                       abcdefghijklmnopqrstuvwxyz1234567890\
                       abcdefghijklmnopqrstuvwxyz1234567890' # too long
    assert isProperSecurityAnswer(valid_answer1) is True
    assert isProperSecurityAnswer(invalid_answer1) is False
    assert isProperSecurityAnswer(invalid_answer2) is False
    assert isProperSecurityAnswer(invalid_answer3) is False

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