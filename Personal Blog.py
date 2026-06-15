import os
import json
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secret_key'

def article_list():

    with open('Articles.json', 'r') as file:
        data = json.load(file)
        
    article_titles = []

    for id in data['Articles']:
        article_titles.append((id, data['Articles'][id]['Article Title'], data['Articles'][id]['Date of Publishing'] ))
    
    return article_titles

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'password':
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))
 
@app.route('/')
def home():

    if os.path.exists('Articles.json'):
        return render_template('home.html', article_titles=article_list())
    
    return render_template('home.html')

@app.route('/article/<id>')
def article(id):

    with open('Articles.json', 'r') as file:
        data = json.load(file)

    article_title = data['Articles'][id]['Article Title']
    article_date = data['Articles'][id]['Date of Publishing']
    article_content = data['Articles'][id]['Content']

    return render_template('article.html', title=article_title, date=article_date, content=article_content)

@app.route('/admin', methods=['GET', 'POST'])
def admin():

    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'GET' and os.path.exists('Articles.json'):

        article_titles = article_list()
        
        if article_titles == []:
            return render_template('admin.html') 

        return render_template('admin.html', article_titles=article_titles)
    
    elif request.method == 'POST': #article deletion confirmation
        
        confirmation = request.form['confirmation']
        if confirmation == 'Yes':
            
            id = request.form['article_id']

            with open('Articles.json', 'r') as file:
                data = json.load(file)

            data['Articles'].pop(id)

            with open('Articles.json', 'w') as file:
                json.dump(data, file, indent=4)

            return redirect(url_for('admin'))
        
        elif confirmation == 'No':
            
            return redirect(url_for('admin'))
        
    return render_template('admin.html')

@app.route('/admin/new', methods=['GET', 'POST'])
def new():

    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method =='GET':
        return render_template('new_article.html')
    
    else:
        if os.path.exists('Articles.json'):

            with open('Articles.json', 'r') as file:
                data = json.load(file)

        else:
            data = {'Articles': {}}

    if data['Articles'] == {}:
        new_id = '1'

    else:
        keys_list = list(data['Articles'].keys())
        new_id = str(int(keys_list[-1]) + 1)
    
    title = request.form['title']
    date = request.form['date']
    text = request.form['text']
    data['Articles'][new_id] = {'Article Title':title, 'Date of Publishing':date, 'Content':text}
    new_article = data['Articles'][new_id]['Article Title']

    with open('Articles.json', 'w') as file:
        json.dump(data, file, indent=4)
    
    return render_template('new_article.html', Publish=new_article)

@app.route('/admin/edit', methods=['POST'])
def edit():
    
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    with open('Articles.json', 'r') as file:
        data = json.load(file)

    id = request.form['article_id']
    title = data['Articles'][id]['Article Title']
    date = data['Articles'][id]['Date of Publishing']
    content = data['Articles'][id]['Content']
    
    return render_template('edit_article.html', title=title, date=date, content=content, id=id)

@app.route('/admin/update', methods=['POST'])
def update():

    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    id = request.form['article_id']
    title = request.form['title']
    date = request.form['date']
    text = request.form['text']

    with open('Articles.json', 'r') as file:
        data = json.load(file)
    
    data['Articles'][id]['Article Title'] = title
    data['Articles'][id]['Date of Publishing'] = date
    data['Articles'][id]['Content'] = text

    with open('Articles.json', 'w') as file:
        json.dump(data, file, indent=4)
    
    return render_template('edit_article.html', title=title, date=date, content=text, changes_saved=title)

@app.route('/admin/delete_confirmation', methods=['POST'])
def delete_confirmation():

    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    id = request.form['article_id']
    article_titles = article_list()
    
    return render_template('admin.html', article_titles=article_titles, confirmation=True, delete_id=id)


if __name__ == '__main__':
    app.run(debug=True)
