from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


news_list = []


user_likes = {}


chat_messages = []


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    nickname = request.args.get('nickname')  
    return render_template('home.html', nickname=nickname, news_list=news_list, user_likes=user_likes)

@app.route('/news_form/<nickname>', methods=['GET', 'POST'])
def news_form(nickname):
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        file = request.files['image']
        image_url = None

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_url = 'uploads/' + filename 

        news_item = {
            'title': title,
            'text': text,
            'image_url': image_url, 
            'nickname': nickname,
            'likes': 0  
        }
        news_list.append(news_item)

        return redirect(url_for('home', nickname=nickname))

    return render_template('news_form.html', nickname=nickname)

@app.route('/like/<int:news_index>', methods=['POST'])
def like(news_index):
    nickname = request.args.get('nickname')  

    if nickname not in user_likes:
        user_likes[nickname] = set()

    if news_index not in user_likes[nickname]:
        news_list[news_index]['likes'] += 1  
        user_likes[nickname].add(news_index)  

    return redirect(url_for('home', nickname=nickname))

@app.route('/chat/<nickname>', methods=['GET', 'POST'])
def chat(nickname):
    if request.method == 'POST':
        message = request.form['message']
        chat_messages.append({'nickname': nickname, 'message': message})
    
    return render_template('chat.html', nickname=nickname, chat_messages=chat_messages)

if __name__ == '__main__':
    app.run(debug=True)
