from flask import *
import base64
import os
# import io
from werkzeug.utils import secure_filename
import datetime

app = Flask(__name__)

cur_path = os.path.dirname(__file__)
uploads_dir = os.path.join(cur_path, '/instance/uploaded/')

print(cur_path)
#new_path = os.path.relpath('uploaded', cur_path)


@app.route('/')
def upload():
    return render_template("file_upload_form.html")


@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        f = request.files['image']

        f.save(os.path.join(uploads_dir, secure_filename(f.filename)))
       # if f and allowed_file(f.filename):
       #     filename = secure_filename(f.filename)
       #     byte_io = io.BytesIO()
       #     byte_io.write(f.read())
       #     byte_io.seek(0)
       #     response = make_response(send_file(byte_io,mimetype='image/jpg'))
       #     response.headers['Content-Transfer-Encoding']='base64'
       #     return response

        return render_template("success.html", name=f.filename)


@app.route('/upload', methods=['POST'])
def upload_base64_file():
    data = request.get_json()
    if data is None:
        print("No valid request body, json missing!")
        return jsonify({'error': 'No valid request body, json missing!'})
    else:
        img_data = data['image'].split(",")[1].encode()
        ft = open(str(datetime.datetime.now())+".png", 'wb')
        ft.write(base64.decodebytes(img_data))
        ft.close()
        return jsonify({'code': '200', 'msg': 'ok'})


if __name__ == '__main__':
    app.run(debug=True)
