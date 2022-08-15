from App import db, app, UserMixin

friends = db.Table('friends',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('friend_id', db.Integer, db.ForeignKey('user.id'))
)

cart = db.Table('cart',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'))
)

library = db.Table('library',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'))
)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(80), nullable=False)
    def __init__(self, name, description, image, price, genre):
        self.name = name
        self.description = description
        self.image = image
        self.price = price
        self.genre = genre

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(128))
    security_question = db.Column(db.String(80))
    security_answer = db.Column(db.String(80))

    in_cart = db.relationship('Game',
        secondary=cart,
        #primaryjoin=(cart.c.user_id == id),
        #secondaryjoin=(cart.c.game_id == id),
        backref=db.backref('cart', lazy='dynamic'),
        lazy='dynamic')

    Library = db.relationship('Game',
        secondary=library,
        backref=db.backref('library', lazy='dynamic'),
        lazy='dynamic')

    is_friends = db.relationship('User',
        secondary=friends,
        primaryjoin=(friends.c.user_id == id),
        secondaryjoin=(friends.c.friend_id == id),
        backref=db.backref('friends', lazy='dynamic'),
        lazy='dynamic')

    def __init__(self, username, password, security_question, security_answer):
        self.username = username
        self.password = password
        self.security_question = security_question
        self.security_answer = security_answer
    def __repr__(self):
        return f"{self.username}, {self.password}, {self.security_question}, {self.security_answer}"