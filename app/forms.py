from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class TradingForm(FlaskForm):
    user_name = StringField('User Name', validators=[DataRequired()])
    pokemon_trade_in_id = IntegerField('Pokemon Trade In ID', validators=[DataRequired()])
    pokemon_trade_out_id = IntegerField('Pokemon Trade Out ID', validators=[DataRequired()])
    tradeButton = SubmitField('Trade')
