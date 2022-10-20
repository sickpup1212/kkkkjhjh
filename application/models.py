from application import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1200), unique=True)
    email = db.Column(db.String(1200), unique=True)
    hashy = db.Column(db.LargeBinary(1200), unique=True)
    tstamp = db.Column(db.String(200), unique=True)

    def __repr__(self):
        return '<User %r>' % self.username

class Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1200), nullable=False)
    chip_total = db.Column(db.Integer, nullable=False)
    current_wager = db.Column(db.Integer, nullable=True)
    hands_played = db.Column(db.Integer, nullable=True)
    hands_won = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Stats %r>' % self.chip_total




