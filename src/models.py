from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(250), unique=False, nullable=False)
    last_name = db.Column(db.String(250), unique=False, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    phone_number = db.Column(db.BigInteger, unique=False, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    appointments = db.relationship('Appointment', backref='user', lazy=True) 
    # above db creates a relationship between the user and in this case, appointments. One to many relationship with user_id - one user can have multiple appointments 


    def __repr__(self):
        return '<User %r>' % self.email
      

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "password": self.password, # serialized for testing purpose, remove when ready to launch 
            "appointments": list(map(lambda x: x.serialize(), self.appointments)) # one to many relationship 
        
            # do not serialize the password, its a security breach
        }
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=False, nullable=False)
    startDate = db.Column(db.DateTime, unique=False, nullable=False)
    endDate = db.Column(db.DateTime, unique=False, nullable=False)
    location = db.Column(db.String(250), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    # above creates a relatinships between appointment and user. This will show a user only its private data and not everyone elses. 

    def __repr__(self):
        return '<Appointment %r>' % self.title

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "startDate": self.startDate,
            "endDate": self.endDate,
            "location": self.location,
        }
       

