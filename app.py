from flask import Flask, render_template,request,Blueprint
from flask_login import login_required, current_user
from .models import History
from . import db
app = Flask(__name__)
main =  Blueprint('main', __name__)
@main.route('/')
def index():
	return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
	return render_template('profile.html', name=current_user.name)

@main.route('/bmi-calculator', methods=['GET', 'POST'])
@login_required
def bmi():
	bmi = ''
	state = ''
	if request.method == 'POST' and 'weight' in request.form:
		try:
			weight = float(request.form.get('weight'))
			height = float(request.form.get('height'))
			assert(height>0 and weight>0)
			bmi = calc_bmi(weight, height)
			state = comment(bmi)
			if state!='Invalid BMI':
				history=History(bmi=bmi, id_user=current_user.id)
				db.session.add(history)
				db.session.commit()
		except:
			bmi=None
			state=None
	return render_template("bmi_calculator.html",
							bmi=bmi, state=state)

def calc_bmi(weight, height):
	return round((weight / ((height / 100) ** 2)), 2)

def comment(bmi):
	if bmi<16:
		return 'Severe Thinness'
	elif 16<=bmi<17:
		return 'Moderate Thinness'
	elif 17<=bmi<18.5:
		return 'Mild Thinness'
	elif 18.5<=bmi<25:
		return 'Normal'
	elif 25<=bmi<30:
		return 'Overweight'
	elif 30<=bmi<35: 
		return 'Obese Class I'
	elif 35<=bmi<40: 
		return 'Obese Class II'
	elif bmi>40: 
		return 'Obese Class III'
	else: 
		return 'Invalid BMI'



@main.route('/history')
@login_required
def history():
	user_id = current_user.id
	history = History.query.filter_by(id_user=user_id).all()
	labels = [i for i in range(1,len(history)+1)]
	values = []
	for record in history:
		values.append(record.bmi)
	return render_template('history.html', values=values, labels=labels, name=current_user.name)

if __name__ == '__main__':
	app.run(debug=True)