from App import db, app, StringField, PasswordField, HiddenField, SubmitField, DataRequired, FlaskForm, SelectField

class LoginForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Submit")

class resetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class SignupForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    password = StringField('Password', [DataRequired()])
    security_question_choices = ['What is your favorite color?', 'What is your favorite food?', 
    'What is your favorite movie?', 'What is your favorite book?', 'What is your favorite sport?', 
    'What is your favorite band?', 'Who is your favorite artist?', 'What is your favorite game?']
    security_questions = [(choice,choice) for choice in security_question_choices]
    security_question = SelectField(label='Security Question Options', choices=security_questions, validators=[DataRequired()])
    security_answer = StringField('Security Question Answer', [DataRequired()])
    submit = SubmitField('Submit')
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.user = None

class AddFriendForm(FlaskForm):
    username = StringField('Username', [DataRequired()], render_kw={"placeholder": "Enter The Username of the friend you want to add"})
    submitadd = SubmitField('Add Friend')

class RemoveForm(FlaskForm):
    removeID = HiddenField('RemoveID')
    submitrem = SubmitField('Remove')

class AddGameForm(FlaskForm):
    name = StringField('Game Name', [DataRequired()], render_kw={"placeholder": "Enter The Name of the game you want to add"})
    description = StringField('Game Description', [DataRequired()], render_kw={"placeholder": "Enter The Description of the game you want to add"})
    image = StringField('Game Image', [DataRequired()], render_kw={"placeholder": "Enter The URL Image of the game you want to add"})
    price = StringField('Game Price', [DataRequired()], render_kw={"placeholder": "Enter The Price of the game you want to add"})
    genre = StringField('Game Genre', [DataRequired()], render_kw={"placeholder": "Enter The Genre of the game you want to add"})
    submit = SubmitField('Add Game')

class StoreForm(FlaskForm):
    search = StringField('Search', [DataRequired()], render_kw={"placeholder": "Search for a title"})
    searchSubmit = SubmitField('Search')

class addCartForm(FlaskForm):
    addID = HiddenField('AddID')
    submitadd = SubmitField('Add to Cart')

class CartForm(FlaskForm):
    choice_options = ['Myself', 'A Friend']
    options = [(choice,choice) for choice in choice_options]
    recepient = SelectField('Who is this purchase for?', choices=options, validators=[DataRequired()])
    submit = SubmitField('Checkout')

class CheckoutForm(FlaskForm):
    card = StringField('Credit Card Number', [DataRequired()], render_kw={"placeholder": "Enter Your Credit Card Number"})
    exp = StringField('Expiration Date', [DataRequired()], render_kw={"placeholder": "Enter Your Expiration Date"})
    cvv = StringField('CVV', [DataRequired()], render_kw={"placeholder": "Enter Your CVV"})
    submit = SubmitField('Complete Purchase')

class ChooseFriendForm(FlaskForm):
    friendID = HiddenField('FriendID')
    submit = SubmitField('Select')