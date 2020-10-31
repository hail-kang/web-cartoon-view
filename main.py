from flask import Flask, render_template, jsonify, request
import json
import pymysql

# class CustomFlask(Flask):
#     jinja_options = Flask.jinja_options.copy()
#     jinja_options.update({
#         'block_start_string' : '<%',
#         'block_end_string' : '%>',
#         'variable_start_string' : '%%',
#         'variable_end_string' : '%%',
#         'comment_start_string' : '<#',
#         'comment_end_string' : '#>',
#     })

# app = CustomFlask(__name__)
app = Flask(__name__)

def db_connect():
    return pymysql.connect(
        user='hail', 
        passwd='1234', 
        host='127.0.0.1', 
        db='cartoon_site', 
        charset='utf8'
    )

@app.route('/')
def index():
    db = None
    try:
        db = db_connect()
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = 'select * from cartoon'
            cursor.execute(sql)
            result = cursor.fetchall()

            sql = 'select cg.cartoonid, g.name from cartoon_genre cg join genre g on cg.genreid=g.genreid'
            cursor.execute(sql)
            cartoon_genre = cursor.fetchall()

            for r in result:
                genre = [cg['name'] for cg in cartoon_genre if cg['cartoonid'] == r['cartoonid']]
                r['genre'] = genre
        if db != None:
            db.close()
        return render_template('index.html', items=result)
    except:
        if db != None:
            db.close()
        return 'error'

@app.route('/<string:title>')
def index_title(title):
    db = None
    try:
        db = db_connect()
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = f'select * from cartoon where title like "%{title}%"'
            cursor.execute(sql)
            result = cursor.fetchall()

            sql = f'select cg.cartoonid, g.name \
                    from cartoon_genre cg \
                    join cartoon c on cg.cartoonid=c.cartoonid \
                    join genre g on cg.genreid=g.genreid \
                    where c.title like "%{title}%"'

            cursor.execute(sql)
            cartoon_genre = cursor.fetchall()

            for r in result:
                genre = [cg['name'] for cg in cartoon_genre if cg['cartoonid'] == r['cartoonid']]
                r['genre'] = genre
        if db != None:
            db.close()
        return render_template('index.html', items=result, keyword=title)
    except:
        if db != None:
            db.close()
        return 'error'

@app.route('/api/search', methods=['POST'])
def search():
    title = request.form.get('title')
    author = request.form.get('author')
    complete = request.form.get('complete')
    platform = request.form.get('platform')
    genre = request.form.getlist('genre[]')

    db = None
    try:
        db = db_connect()
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            where = ''
            if title != '':
                where += f' and c.title like %{title}%'
            if author != '':
                where += f' and a.name like %{author}%'
            if complete != 0:
                where += f' and c.complete={complete}'
            if platform != 0:
                where += f' and c.platform={platform}'

            if len(genre) == 1:
                where += f' and exists(select * \
                                        from cartoon_genre cg \
                                        join genre g on cg.genreid=g.genreid \
                                        where g.name="{genre[0]}")'
            elif len(genre) > 1:
                where += f' and exists(select * \
                                        from cartoon_genre cg \
                                        join genre g on cg.genreid=g.genreid \
                                        where g.name in {tuple(genre)})'
            
            sql = f'select c.cartoonid, c.title, c.complete, c.platform, a.name \
                    from cartoon c \
                    join author a on c.authorid=c.authorid \
                    where 1=1' + where
            cursor.execute(sql)
            result = cursor.fetchall()

            sql = f'select cg.cartoonid, g.name \
                    from cartoon_genre cg \
                    join cartoon c on cg.cartoonid=c.cartoonid \
                    join genre g on cg.genreid=g.genreid \
                    where 1=1' + where
            cursor.execute(sql)
            cartoon_genre = cursor.fetchall()

            for r in result:
                genre = [cg['name'] for cg in cartoon_genre if cg['cartoonid'] == r['cartoonid']]
                r['genre'] = genre
        if db != None:
            db.close()
        return jsonify({
            'items' : result
        })
    except:
        if db != None:
            db.close()
        return 'error'

@app.route('/thumbnail/<int:cartoonid>')
def image_thumbnail(cartoonid):
    path = f'C:/Users/강하일/Desktop/storage/thumbnail/{cartoonid}.jpg'
    with open(path, 'rb') as f:
        result = f.read()
    return result

@app.route('/cartoon/<int:cartoonid>')
def view_story_list(cartoonid):

    return render_template('storylist.html')

@app.route('/cartoon/<int:cartoonid>/story/<int:number>')
def view_story(cartoonid, number):
    return render_template('story.html')

if __name__ == "__main__":
    app.run('127.0.0.1', '8080')