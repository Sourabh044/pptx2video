import os
from flask import Flask ,render_template ,send_from_directory
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from websocket.socketio_handlers import socketio
from converter.utils import Effects
load_dotenv()

def create_app():
    app = Flask('pptx2video')
    app.config['SECRET_KEY']=os.environ['SECRET_KEY']
    app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, os.environ['UPLOAD_FOLDER'])  # Folder to save uploaded files
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit
    app.config['CONVERTED_FOLDER'] = os.path.join(app.static_folder, os.environ['CONVERTED_FOLDER'])
    CSRFProtect(app)
    socketio.init_app(app=app)
    return app

app = create_app()
# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['CONVERTED_FOLDER']):
    os.makedirs(app.config['CONVERTED_FOLDER'])

@app.route('/',methods=['get'])
def hompage():
    return render_template('convert.html',title='Convert',effects=Effects)


@app.route('/get-file/<path:filename>')
def download_link(filename):
   return send_from_directory(directory=app.config['CONVERTED_FOLDER'], path=filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
