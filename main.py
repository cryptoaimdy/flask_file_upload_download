import os
# import magic
import urllib.request
from config import app
from flask import Flask, flash, request, redirect, render_template, jsonify,send_file
from werkzeug.utils import secure_filename
import time
import webbrowser
import mysql.connector 


conn = mysql.connector.connect(user='root', password='***',
                              host='localhost',
                              database='hrms',
                              auth_plugin='mysql_native_password')

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx', 'mp4'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
    file_path = app.config['UPLOAD_FOLDER']+'/' + filename
    # webbrowser.open(filepath)
    return send_file(file_path, as_attachment=True, attachment_filename='')
    return redirect('/')

# @app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
# def download_file(filename):
#     file_path = app.config['UPLOAD_FOLDER']+'/' + filename
#     return send_file(file_path, as_attachment=True, attachment_filename='')
#     return redirect('/')

# @app.route('/return-files/<filename>')
# def return_files_tut(filename):
#     file_path = app.config['UPLOAD_FOLDER'] + filename
#     return send_file(file_path, as_attachment=True, attachment_filename='')



def processFile(filename):
    file_list = filename.split('.')
    file_time = int(round(time.time() * 1000))
    unique_file_name = file_list[0] + str(file_time)
    final_file_name = unique_file_name + '.' + file_list[1]
    return final_file_name

def push_in_db(filename, userid = 101):
    cursor = conn.cursor()
    sql = "insert into filestorage(userid, filename) values (%s, %s)"
    val = (userid, filename)
    cursor.execute(sql, val)
    conn.commit()
    if cursor.rowcount > 0:
        result = 'Added filename into DB'
    return cursor.rowcount




@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            filename = processFile(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            db_insert_count = push_in_db(filename)
            if db_insert_count > 0:
                flash(path)
                # flash('{}'.format(request.host)+'/uploads/'+filename)
                return redirect('/')
                # return redirect('/uploads/'+ filename)
            else:
                flash('Could not insert into DB')
                return redirect('/')
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)


if __name__ == "__main__":
    app.run()