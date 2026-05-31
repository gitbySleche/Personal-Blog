import os
import json
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/article')
def article():

    return render_template('article_template.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():

    if request.method == 'GET' and os.path.exists('Articles.json'):

        with open('Articles.json', 'r') as file:
            data = json.load(file)
        
        article_titles = []

        for id in data['Articles']:
            
            article_titles.append(id, data['Articles'][id]['Article Title'])

        return render_template('admin.html', article_titles=article_titles)
    
    else:
        return render_template('admin.html')

@app.route('/admin/new', methods=['GET', 'POST'])
def new():

    if request.method =='GET':
        return render_template('article_form.html')
    
    else:
        if os.path.exists('Articles.json'):

            with open('Articles.json', 'r') as file:
                data = json.load(file)

        else:
            data = {'Articles': {}}

    if data['Articles'] == {}:
        new_id = 1

    else:
        keys_list = list(data['Articles'].keys())
        new_id = str(int(keys_list[-1]) + 1)
    
    title = request.form['title']
    date = request.form['date']
    text = request.form['text']
    data['Articles'][new_id] = {'Article Title':title, 'Date of publishing':date, 'Content':text}

    with open('Articles.json', 'w') as file:
        json.dump(data, file, indent=4)

    return render_template('article_form.html')

@app.route('/admin/edit', methods=['GET', 'POST'])
def edit():
    



if __name__ == '__main__':
    app.run(debug=True)
