from flask import render_template, request
from flask_table import Table, Col
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pythondb import pythondb_bp
from pythondb.model import Users, Emails, PhoneNumbers
from models import menus


# Declare your Users table
class UserTable(Table):
    UserID = Col('UserID')
    username = Col('username')
    password = Col('Password')


# Declare your  emailtable
class EmailTable(Table):
    UserID = Col('UserID')
    email_address = Col('email_address')


# Declare your  phone numbers table
class PNTable(Table):
    UserID = Col('UserID')
    phone_number = Col('phone_number')


# connects default URL to a function
@pythondb_bp.route('/')
def databases():
    # fill the Users table
    users = Users.query.all()
    records = []
    for user in users:
        user_dict = {'id': user.UserID, 'name': user.username, 'password': user.password}
        # associate emails with user
        emails = Emails.query.all()
        for email in emails:
            if user_dict['id'] == email.UserID:
                user_dict['emails'] = email.email_address
        # associate phone numbers with user
        phone_numbers = PhoneNumbers.query.all()
        for pn in phone_numbers:
            if user_dict['id'] == pn.UserID:
                user_dict['phone_numbers'] = pn.phone_number
        # add record to list
        records.append(user_dict)
    return render_template("pythondb/index.html", table=records, menus=menus)


# if input url used, use the input html
@pythondb_bp.route('/input/', methods=["GET", "POST"])
def input():
    if request.form:
        engine = create_engine('sqlite:///models/myDB.db', echo=True)  # relative path within project
        Session = sessionmaker(bind=engine)
        session = Session()
        print("UserID: " + str(request.form.get("ID")))
        email = Emails(email_address=request.form.get("email"), UserID=request.form.get("ID"))
        session.add(email)
        print(session)
        session.commit()
        phone_number = PhoneNumbers(phone_number=request.form.get("phone_number"), UserID=request.form.get("ID"))
        session.add(phone_number)
        session.commit()
    return render_template("pythondb/index.html", menus=menus)


# if email url, show the email table
@pythondb_bp.route('/emails/')
def emails():
    # fill the table with emails only
    records = []
    emails = Emails.query.all()
    for email in emails:
        user_dict = {}
        user_dict['id'] = email.UserID
        user_dict['emails'] = email.email_address
        records.append(user_dict)
    return render_template("pythondb/index.html", table=records, menu=menus)


# if phones url, shjow phones table
@pythondb_bp.route('/phones/')
def phones():
    # fill the table with phone numbers only
    records = []
    phone_numbers = PhoneNumbers.query.all()
    for phone in phone_numbers:
        user_dict = {}
        user_dict['id'] = phone.UserID
        user_dict['phone_numbers'] = phone.phone_number
        records.append(user_dict)
    return render_template("pythondb/index.html", table=records, menu=menus)


# CRUD delete
@pythondb_bp.route('/delete/')
def delete():
    return render_template("pythondb/index.html", table=pntable, menu=menus)

