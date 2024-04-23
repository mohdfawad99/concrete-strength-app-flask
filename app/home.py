from flask import Blueprint, render_template, request, redirect, url_for, session

from app.functions.predict import get_concrete_strength, wc_ratio_ranges

bp = Blueprint("home", __name__)



@bp.route("/", methods=("POST", "GET"))
def home():
    result = 'Enter appropriate values to get concrete strength'

    if request.method == 'POST' and request.form:
        mix_proportion = request.form['mix_proportion']
        concrete_grade = request.form.get('concrete-grade')
        wc_ratio = request.form['wc_ratio']
        result = get_concrete_strength(mix_proportion, concrete_grade, wc_ratio)

        session['concrete_grades']=list(wc_ratio_ranges.keys())
        session['wc_ratio_ranges']=wc_ratio_ranges
        session['result']=result
        session['post_data_processed']=True
        return redirect(url_for('home.home'))

    try:
        concrete_grades = session.pop('concrete_grades')
        wc_ratio_range = session.pop('wc_ratio_ranges')
        result = session.pop('result')
        post_data_processed = session.pop('post_data_processed')
    except:
        concrete_grades = list(wc_ratio_ranges.keys())
        wc_ratio_range = wc_ratio_ranges
        result = result
        post_data_processed=False

    return render_template('home/home.html', concrete_grades=concrete_grades, wc_ratio_ranges=wc_ratio_range, result=result, post_data_processed=post_data_processed)