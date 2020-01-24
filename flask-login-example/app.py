import flask
import flask_login
import flask_wtf
import wtforms

app = flask.Flask(
        __name__,
        template_folder='templates')

app.secret_key = b'jugemjugemgokonosurikirekaijarisuigyono'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

class LoginForm(flask_wtf.FlaskForm):
    user_id = wtforms.StringField(
            'user_id',
            [wtforms.validators.DataRequired(), wtforms.validators.Length(min=3, max=20)])
    password = wtforms.PasswordField(
            'password',
            [wtforms.validators.DataRequired(), wtforms.validators.Length(min=4, max=20)])

@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' ログイン '''
    form = LoginForm(flask.request.form)

    # validationチェック
    if form.validate_on_submit():
        # 通常はDB等で認証しますが割愛してハードコーディング
        if form.user_id.data == 'scott' and form.password.data == 'tiger':
            # ログインの実行
            user = User(form.user_id.data)
            flask_login.login_user(user)
            # ログインに成功したらmemberページへ飛びます
            return flask.redirect('/member')
        else:
            # ログイン失敗のメッセージを書いたり
            pass

    # GET時やログイン
    return flask.render_template(
            'login.html',
            form=form)

@app.route('/logout', methods=['GET'])
def logout():
    ''' ログアウト '''
    flask_login.logout_user()
    return 'ログアウトしました'

@app.route('/', methods=['GET'])
def index():
    ''' トップページ（ログイン不要） '''
    return '''<h1>top page</h1><p><a href="/login">ログイン</a><p><a href="/member">メンバー</a><p><a href="/logout">ログアウト</a>'''

@app.route('/member', methods=['GET'])
@flask_login.login_required
def member():
    ''' 会員ページ（要ログイン） '''
    return '会員ページ'

@login_manager.unauthorized_handler
def unauthorized():
    return flask.redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)

