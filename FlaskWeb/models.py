from FlaskWeb import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False, default='none')
    last_name = db.Column(db.String(20), nullable=False, default='none')
    email = db.Column(db.String(120), nullable=False, default='none')
    imagefile = db.Column(db.String(20), nullable=False, default='none')
    rollno = db.Column(db.String(20), nullable=False, default = '0')
    birthday = db.Column(db.String(120), nullable=False, default='0')
    department = db.Column(db.String(20), nullable=False,unique=False, default='none')

    def __repr__(self):
        return f"User('Name : {self.first_name} {self.last_name}', 'Roll No. : {self.rollno}')"


