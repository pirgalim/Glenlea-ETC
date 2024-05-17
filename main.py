from flask import Flask, render_template, request, redirect, make_response, url_for
import os
import services.ETC as ETC
from forms import InputForm, SelectForm


# remove later
from wtforms import Form, SelectField, SubmitField



app = Flask(__name__)

app.config['SECRET_KEY'] = 'd42c51f24733b869a5916a8c09043624'


@app.route("/")
def my_redirect():   
    return redirect(url_for('test'))
    


class MyForm(Form):
    camera = SelectField('Dropdown', choices=[('', ''), ('asi6200mm', 'ASI6200MM'), ('asi2600mm', 'ASI2600MM')])


@app.route('/test', methods=['GET', 'POST'])
def test():
    
    
    camera_form = MyForm(request.form)
    in_form = InputForm()
    array = [1,2,3,4,5]
    option_selected = False
    
    if request.method == 'POST':
        
        option_selected = True
        
        selected_option = request.form['camera']
        # Process the selected option as needed
        print("Selected option:", selected_option)
        
    return render_template('input.html', camera_form=camera_form, in_form=in_form, array=array, option_selected=option_selected)

























@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    
    in_form = InputForm()
    select_form = SelectForm()
    
    if select_form.is_submitted():
        
        camera = request.form['camera']
        print(camera)
        
        
        
        
        
        # camera = request
        
        new_form = InputForm()
        
        
        
        return render_template('input.html', in_form=in_form, select_form=select_form)
    
    return render_template('input.html', in_form=in_form, select_form=select_form)


    # if in_form.is_submitted():
        
    #     result = request.form
    #     print(result)
    #     return render_template('input.html', in_form=in_form, select_form=select_form)
    
    # return render_template('input.html', in_form=in_form, select_form=select_form)



































# @app.route("/test")
# def test():
        
#     resp = make_response(render_template('index.html'))
    
#     if os.path.exists("static/my_plot.png"):
#         os.remove("static/my_plot.png")
        
#         return resp
#     else:
#         print("The file does not exist")

#     return resp











# @app.route("/", methods = ['GET', 'POST'])
# def get_plot():
        
#     if request.method == "POST":
        
#         params = [request.form['sen_x'], request.form['sen_y'], request.form['px_size'], request.form['q_eff'], request.form['read_noise'],
#                   request.form['gain'], request.form['sen_offset'], request.form['dark_noise'], request.form['full_well']]

        
        
#         if os.path.exists("static/my_plot.png"):
#             os.remove("static/my_plot.png")
#         else:
#             print("The file does not exist")
        
        
#         #camera = ETC.camera(params)
#         ETC.plot_light_curve_SB()
#         #ETC.print_data(camera)

        
#         return render_template('index.html', plot_url = "static/my_plot.png")
    
#     else:   # this is temporary
#         return render_template('index.html')     

    


# @app.route("/hello")
# def run():
#     return render_template('main.html')





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)