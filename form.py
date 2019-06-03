from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email

class login(FlaskForm):
    user=StringField(u'用户名')
    password=PasswordField(u'密码',validators=[DataRequired(message= u'密码不能为空')])
    submit=SubmitField(u'登录')
