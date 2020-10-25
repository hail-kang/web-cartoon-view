from flask import Flask, render_template

class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update({
        'block_start_string' : '<%',
        'block_end_string' : '%>',
        'variable_start_string' : '%%',
        'variable_end_string' : '%%',
        'comment_start_string' : '<#',
        'comment_end_string' : '#>',
    })

app = CustomFlask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    return render_template('test.html', message='Hello Flask')

if __name__ == "__main__":
    app.run('127.0.0.1', '8080')