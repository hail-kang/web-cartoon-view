from flask import Flask, render_template, jsonify, request, url_for, redirect
import json
import os
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
    except Exception as e:
        print(e)
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
    except Exception as e:
        print(e)
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
    except Exception as e:
        print(e)
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
    db = None
    try:
        db = db_connect()
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = 'select * from cartoon where cartoonid=%s'
            cursor.execute(sql, cartoonid)
            cartoon = cursor.fetchone()

            sql = 'select * from story where cartoonid=%s order by number desc'
            cursor.execute(sql, cartoonid)
            storylist = cursor.fetchall()

            sql = 'select g.name \
                    from cartoon_genre cg \
                    join genre g on cg.genreid=g.genreid \
                    where cg.cartoonid=%s'
            cursor.execute(sql, cartoonid)
            genre = cursor.fetchall()
        if db != None:
            db.close()
        return render_template('storylist.html', cartoon=cartoon, storylist=storylist, genre=genre)
    except Exception as e:
        print(e)
        if db != None:
            db.close()
        return 'error'

@app.route('/cartoon/<int:cartoonid>/story/<int:number>')
def view_story(cartoonid, number):
    inspect = f'C:/Users/강하일/Desktop/storage/cartoon/{cartoonid}/{number}'
    files = next(os.walk(inspect))[2]
    files.sort(key=lambda name : int(name[:name.find('.')]))
    return render_template('story.html', cartoonid=cartoonid, number=number, images=files)

@app.route('/cartoon/<int:cartoonid>/story/<int:number>/cut/<string:arrange>')
def image_cut(cartoonid, number, arrange):
    path = f'C:/Users/강하일/Desktop/storage/cartoon/{cartoonid}/{number}/{arrange}'
    with open(path, 'rb') as f:
        result = f.read()
    return result

@app.route('/admin')
def view_admin():
    db = None
    try:
        db = db_connect()
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = 'select * from cartoon'
            cursor.execute(sql)
            cartoon = cursor.fetchall()
        if db != None:
            db.close()
        return render_template('admin.html', cartoon=cartoon)
    except Exception as e:
        print(e)
        if db != None:
            db.close()
        return 'error'

@app.route('/admin/addcartoon')
def view_addcartoon():
    db = None
    try:
        db = db_connect()
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = 'select authorid, name from author'
            cursor.execute(sql)
            author = cursor.fetchall()
        if db != None:
            db.close()
        return render_template('addcartoon.html', author=author)
    except Exception as e:
        print(e)
        if db != None:
            db.close()
        return 'error'

@app.route('/api/addcartoon', methods=['POST'])
def api_addcartoon():
    db = None
    try:
        db = db_connect()
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            isaddauthor = request.form.get('isaddauthor')
            author = request.form.get('author')
            authorid = request.form.get('authorid')
            if isaddauthor:
                sql = 'insert into author(name) values(%s)'    
                cursor.execute(sql, author)

                sql = 'select last_insert_id() authorid'
                cursor.execute(sql)
                authorid = cursor.fetchone().get('authorid')

            title = request.form.get('title')
            complete = request.form.get('complete')
            plaform = request.form.get('platform')
            sql = 'insert into cartoon(title, complete, platform, authorid) values(%s, %s, %s, %s)'
            cursor.execute(sql, (title, complete, plaform, authorid))

            sql = 'select last_insert_id() cartoonid'
            cursor.execute(sql)
            cartoonid = cursor.fetchone().get('cartoonid')
            
            db.commit()

        if db != None:
            db.close()

        thumbnail = request.files.get('thumbnail')
        if thumbnail != None:
            thumbnail.save(f'C:/Users/강하일/Desktop/storage/thumbnail/{cartoonid}.jpg')
        return render_template('addcartoon.html', author=author)
    except Exception as e:
        print(e)
        if db != None:
            db.close()
        return 'error'

    return redirect('/admin')

if __name__ == "__main__":
    app.run('127.0.0.1', '8080')