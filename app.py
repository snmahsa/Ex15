from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_bcrypt import Bcrypt
from forms import RegistrationForm, LoginForm  , InputForm 
from database import db, User, TrackerInput
from sqlalchemy.exc import IntegrityError
from model.model import prediction_iris
app = Flask(__name__)
app.config['SECRET_KEY'] = '1234$'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db.init_app(app)
bcrypt = Bcrypt(app)

def login_required(f):
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            flash('You need to login first!', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        hash_password = bcrypt.generate_password_hash(password).decode('utf8')
        new_user = User(username=username,password=hash_password)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('Username exist','warning')
            return redirect(url_for('register'))
        else:   
            flash('Register Successfull')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form =  LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username_login = form.username_login.data
        password_login = form.password_login.data
        user_check = User.query.filter_by(username=username_login).first() 
        if user_check and bcrypt.check_password_hash(user_check.password, password_login):
            session['username'] = username_login
            return redirect(url_for('input'))
        
    return  render_template('login.html', form=form)

@app.route('/users')
def show_users():
    users = User.query.all()  
    return render_template('show_users.html', users=users)

@app.route('/input')
@login_required
def input():
    form = InputForm()
    return render_template('input.html', form=form)

@app.route('/predict', methods=['POST','GET'])
@login_required
def predict():
    form = InputForm()
    if request.method == 'POST'  :
        sepal_length = form.sepal_length.data
        sepal_width = form.sepal_width.data
        petal_length = form.petal_length.data
        petal_width = form.petal_width.data
   

        features = [sepal_length, sepal_width, petal_length, petal_width]
        
        predicted_class = int(prediction_iris(features))
        username_login = session['username']
        print(f"------------------- user: {username_login}")
        user_check = User.query.filter_by(username=username_login.lower()).first()
        print(f"------------------- user check: {user_check}")
        match predicted_class:
            case 0:
                result = "Iris-setosa"
                image_link = 'img/setosa.png'
            case 1:
                result = "Iris-versicolor"
                image_link = 'img/versicolor.png'
            case 2:
                result = "Iris-virginica"
                image_link = 'img/virginica.png'


        new_input = TrackerInput(
            user_id=user_check.id,
            result_code = predicted_class,
            result=result,
            sepal_length=sepal_length,
            sepal_width=sepal_width,
            petal_length=petal_length,
            petal_width=petal_width,

        )

        db.session.add(new_input)
        db.session.commit()

        return redirect(url_for('result',predicted_class=result,image_link=image_link))




@app.route('/result')
@login_required
def result():
    predicted_class = request.args.get('predicted_class')
    image_link = request.args.get('image_link')
    return render_template('result.html', predicted_class=predicted_class, image_link=image_link)

@app.route('/history')
@login_required
def history():
    username_login = session['username']
    user_check = User.query.filter_by(username=username_login.lower()).first()
    inputs = TrackerInput.query.filter_by(user_id=user_check.id).all()
    return render_template('history.html', inputs=inputs)

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('index'))

@app.errorhandler(Exception)
def page_not_found(e):
    if hasattr(e, 'code'):
        status_code = e.code
        error_message = {
            400: "Bad request.",
            401: "Authorization required.",
            403: "Access to this resource is forbidden.",
            404: "Ops! Page not found.",
            500: "An internal server error has occurred."
        }.get(status_code, "An unexpected error has occurred.")
    else:
        status_code = 500
        error_message = "An unexpected error has occurred."
    return render_template('error.html', error_message=error_message,status_code=error_message)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(host='0.0.0.0', port=5000, debug=True)