from flask import Blueprint, request, jsonify
from ..validation import isProperSecurityQuestion, isProperSecurityAnswer, isProperPassword
from db.global_db import db
from db.models.user import User
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

security_question = Blueprint('security_question', __name__)

@security_question.route('/changeSecQues/<int:userid>', methods=['PATCH'])
def changeSecQues(userid):
      if request.method == 'PATCH':
            sec_ques_num = int(request.get_json().get('sec_ques_num'))
            user = User.query.filter_by(userid=userid).first()
            if isProperSecurityQuestion(sec_ques_num):
                  user.sec_ques_num = sec_ques_num
                  user.lastUpdated = datetime.now()
                  db.session.commit()
                  return jsonify('Security question has been updated!')
            else:
                  return jsonify('Security question could not be updated.')
      else:
            return jsonify('Unsupported HTTP method!')

@security_question.route('/changeSecAns/<int:userid>', methods=['PATCH'])
def changeSecAns(userid):
      if request.method == 'PATCH':
            sec_ques_ans = request.get_json().get('sec_ques_ans')
            user = User.query.filter_by(userid=userid).first()
            if isProperSecurityAnswer(sec_ques_ans):
                  user.sec_ques_ans = generate_password_hash(sec_ques_ans)
                  user.lastUpdated = datetime.now()
                  db.session.commit()
                  return jsonify('Security answer has been updated!')
            else:
                  return jsonify('Security answer could not be updated.')
      else:
            return jsonify('Unsupported HTTP method!')

@security_question.route('/forgotPassword', methods=['PATCH'])
def forgotPassword():
      if request.method == 'PATCH':
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            sec_ques_ans = data.get('sec_ques_ans')
            user = User.query.filter_by(email=email).first()
            if user is None or \
               check_password_hash(user.sec_ques_ans, sec_ques_ans) is False:
                  return jsonify('Email or Security Question is incorrect!')
            elif isProperPassword(password) is False:
                  return jsonify('Invalid password!')
            else:
                  user.password = generate_password_hash(password)
                  user.lastUpdated = datetime.now()
                  db.session.commit()
                  return jsonify('Password has been updated!') 
      else:
            return jsonify('Unsupported HTTP method!')
