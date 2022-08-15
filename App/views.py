from App import db, app, loginManager, check_password_hash, generate_password_hash, login_user, logout_user, current_user, loginManager, session, redirect, url_for, render_template, flash, login_required
from App.models import User, Game
from App.forms import AddFriendForm, RemoveForm, AddGameForm, StoreForm, CartForm, CheckoutForm, ChooseFriendForm, LoginForm, SignupForm, StoreForm, resetPasswordForm
@loginManager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

#login page (Default)
@app.route('/', methods=['GET', 'POST'])
def login():
    db.create_all()
    form = LoginForm()
    if form.is_submitted():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
			# Check the hash
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home', username=user.username))
            elif form.password.data == '':
                flash('Password is required')
            else:
                flash("Wrong Password - Try Again!")
        elif form.username.data == '':
            flash('Username is required')
        else:
            flash("That User Doesn't Exist! Try Again...")
    return render_template('login.html', form=form)

#signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup = SignupForm()
    if signup.is_submitted():
        user = User.query.filter_by(username=signup.username.data).first()
        if user is not None:
            flash("User Already Exists!")
        elif signup.username.data == '':
            flash('Username cannot be blank')
        elif signup.password.data == '':
            flash("Password cannot be blank")
        elif signup.security_answer.data == '':
            flash("Security Answer cannot be blank")
        else:
            hashed_password = generate_password_hash(signup.password.data, "sha256")
            print(signup.security_question.data)
            user = User(signup.username.data, hashed_password, signup.security_question.data, signup.security_answer.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login', logoutCheck=False))
    return render_template('signup.html', signup=signup)

#forgot password
@app.route('/forgotPassword', methods=['GET', 'POST'])
def forgotPassword():
    login = LoginForm()
    signup = SignupForm()
    if login.is_submitted():
        user = User.query.filter_by(username=login.username.data).first()
        if user != None:
            if user.security_answer == signup.security_answer.data and user.security_question == signup.security_question.data:
                session['username'] = user.username
                return redirect(url_for('resetPassword'))
            else:
                flash("Wrong Security Answer!")
        else:
            flash("User Doesn't Exist!")
    return render_template('forgotPassword.html', signup=signup, login=login)
    

#reset password
@app.route('/resetPassword', methods=['GET', 'POST'])
def resetPassword():
    username = session['username']
    reset = resetPasswordForm()
    user = User.query.filter_by(username=session['username']).first()
    print(user.username)
    if user:
        print(user.username)
        if reset.is_submitted():
            session['username'] = None
            print(user.username)
            password = reset.password.data
            if password == '':
                flash("Password cannot be blank")
            else:
                user.password = generate_password_hash(password, "sha256")
                db.session.commit()
                flash("Password Changed!")
                return redirect(url_for('login'))
        else:
            return render_template('resetPassword.html', reset=reset)
    else:
        flash("You need to confirm your identity before resetting your password!")
        return redirect(url_for('forgotPassword'))
    return render_template('resetPassword.html', reset=reset, username=username)

#home library
@app.route('/home/<username>', methods=['GET', 'POST'])
@login_required
def home(username):
    user = User.query.filter_by(username=username).first()
    library = user.Library.all()
    return render_template('home.html',username=username, library=library)

#store 
@app.route('/store', methods=['GET', 'POST'])
@login_required
def store():
    games = Game.query.all()
    store = StoreForm()
    
    return render_template('store.html', username=current_user.username, games=games, store=store)

#add to cart
@app.route('/addToCart/<gameID>', methods=['GET', 'POST'])
@login_required
def addToCart(gameID):
    game = Game.query.filter_by(id=gameID).first()
    if game:
        user = User.query.filter_by(username=current_user.username).first()
        if user:
            print(user.in_cart)
            if game not in current_user.in_cart:
                current_user.in_cart.append(game)
                db.session.commit()
                flash("Game Added to Cart!")
                return redirect(url_for('store'))
            else:
                flash("Game Already in Cart!")
                return redirect(url_for('store'))

        else:
            flash("User Doesn't Exist!")
    else:
        flash("Game Doesn't Exist!")
        return redirect(url_for('store'))

#cart page
@app.route('/cart/<username>', methods=['GET', 'POST'])
@login_required
def Cart(username):
    removeform = RemoveForm()
    cartform = CartForm()
    friendFlag = False
    try:
        games = current_user.in_cart
        games[0]
        if cartform.validate_on_submit():
            if cartform.recepient.data == 'A Friend':
                friendFlag = True
            else:
                friendFlag = False
            return redirect(url_for('checkout', username=username, friendFlag=friendFlag, id=current_user.id))
        if removeform.validate_on_submit() and removeform.submitrem.data:
                game = Game.query.filter_by(id=removeform.removeID.data).first()
                if game:
                    games.remove(game)
                    db.session.commit()
                    flash("Game Removed from Cart!")
                    return redirect(url_for('Cart', username=username))

        return render_template('cart.html', username=username, games=games, removeform=removeform, cart=cartform)
    except:
        print('oops')
        flash("Your Cart is Empty!")
        return redirect(url_for('store', username=username))

#checkout page
@app.route('/checkout/<username>/gift/<friendFlag>/<id>', methods=['GET', 'POST'])
@login_required
def checkout(username, friendFlag, id):
    checkoutform = CheckoutForm()
    choosefriendform = ChooseFriendForm()
    transactionFlag = True
    friend = User.query.filter_by(id=id).first()
    if friendFlag == 'True':
        friendFlag = True
    else:
        friendFlag = False
    
    if friendFlag:
        if choosefriendform.validate_on_submit():
            friend = User.query.filter_by(id=choosefriendform.friendID.data).first()
            if friend:
                return redirect(url_for('checkout', username=current_user.username,id=friend.id, friend=friend, checkout=checkoutform, friendFlag=friendFlag, user=current_user, choosefriendform=choosefriendform))
            else:
                flash("Error: User Doesn't Exist!")
                return redirect(url_for('checkout', username=current_user.username, friend=friend, checkout=checkoutform, friendFlag=friendFlag, user=current_user, choosefriendform=choosefriendform))
        
        if checkoutform.is_submitted():
            if friend != current_user:
                for game in current_user.in_cart:
                    print(friend.Library)
                    if game not in friend.Library:
                        friend.Library.append(game)
                        current_user.in_cart.remove(game)
                    else:
                        flash(game.name + " is already in " + friend.username + "'s Library!")
                        transactionFlag = False
                if transactionFlag:
                    flash("Transaction Complete! Games Added to " + friend.username + "'s Library!")
                    db.session.commit()
                    return redirect(url_for('home', username=username))
                else:
                    return redirect(url_for('Cart', username=username))
            else:
                flash("Please Select a Friend!")
    else:
        if checkoutform.is_submitted():
            for game in current_user.in_cart:
                if game not in current_user.Library:
                    current_user.Library.append(game)
                    current_user.in_cart.remove(game)
                else:
                    flash(game.name + " is already in your Library!")
                    transactionFlag = False
            if transactionFlag:
                flash("Transaction Complete! Games Added to your Library!")
                db.session.commit()
                return redirect(url_for('home', username=current_user.username))
            else:
                return redirect(url_for('Cart', username=current_user.username))
    return render_template('checkout.html', username=current_user.username, id=id, friend=friend, checkout=checkoutform, friendFlag=friendFlag, user=current_user, choosefriendform=choosefriendform)


#add game to store
@app.route('/addGame', methods=['GET', 'POST'])
@login_required
def addGame():
    addGame = AddGameForm()
    if addGame.is_submitted():
        game = Game.query.filter_by(name=addGame.name.data).first()
        if game:
            flash("Game Already Exists!")
        elif addGame.name.data == '':
            flash('Game Name cannot be blank')
        else:
            game = Game(addGame.name.data, addGame.description.data, addGame.image.data, addGame.price.data, 
                        addGame.genre.data)
            db.session.add(game)
            db.session.commit()
            return redirect(url_for('store'))
    return render_template('addGame.html', addGame=addGame)


#community
@app.route('/community/<username>', methods=['GET', 'POST'])
@login_required
def community(username):
    addform = AddFriendForm()
    removeform = RemoveForm()
    if addform.validate_on_submit() and addform.submitadd.data:
        user = User.query.filter_by(username=addform.username.data).first()
        if user:
            if current_user.username != user.username:
                if user not in current_user.is_friends:
                    current_user.is_friends.append(user)
                    db.session.commit()
                    flash("Friend Added!")
                    return redirect(url_for('community', username=username, form=addform))
                else:
                    flash("You are already friends!")
            else:
                flash("You cannot add yourself as a friend!")
        else:
            flash("User Doesn't Exist!")
    return render_template('community.html', username=username, addform=addform, removeform=removeform, user=current_user)

@app.route('/removeFriend/<friendID>', methods=['GET', 'POST'])
@login_required
def removeFriend(friendID):
    print(friendID)
    user = User.query.filter_by(id=friendID).first()
    if user:
        if user in current_user.is_friends:
            current_user.is_friends.remove(user)
            db.session.commit()
            flash("Friend Removed!")
            return redirect(url_for('community', username=current_user.username))
        else:
            flash("You are not friends with this user!")
    else:
        flash("User Doesn't Exist!")
    return redirect(url_for('community', username=current_user.username))
        


@app.route('/changePassword', methods=['GET', 'POST'])
@login_required
def changePassword():
    login = LoginForm()
    user = User.query.filter_by(username=current_user.username).first()
    if login.is_submitted():
        if login.password.data == '':
            flash("Password cannot be blank")
        else:
            user.password = generate_password_hash(login.password.data, "sha256")
            db.session.commit()
            flash("Password Changed!")
            return redirect(url_for('home', username=current_user.username))
    return render_template('changePassword.html', login=login, username=current_user.username)

#logout
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('You have been logged out')
    return redirect(url_for('login'))
