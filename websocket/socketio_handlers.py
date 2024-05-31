from flask_socketio import SocketIO, join_room, emit
from flask import session , current_app
import base64 , os ,time
from converter import cov_ppt , add_animations , add_background_music
from websocket.utils import allowed_file
from werkzeug.utils import secure_filename
socketio = SocketIO(max_http_buffer_size=1024 * 1024 * 50)

# Basic Connection Handlers Socketio
@socketio.on('connect')
def connect():
    print('Connected')

@socketio.on('disconnect')
def disconnect():
    print('disconnected')

@socketio.on('join_room')
def user_join_room(data):
    print(data)
    id = data.get('sid')
    session['sid'] = data.get('sid')
    if id:
        print('joining_id', id)
        join_room(f'user_{id}')
        return {'success': True}
    else:
        {'success': False}

@socketio.on('upload_file')
def handle_upload_file(data):
    try:
        file_name = data['file_name']
        secure_filename_ = secure_filename(file_name)
        resolution = data['quality']
        sid = session['sid']
        if not allowed_file(filename=file_name):
            emit('file_upload_error',{"message":"invalid File!"},to=f"user_{sid}")
            return 400
        file_data = base64.b64decode(data['file_data'].split(',')[1])
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename_)
        name, ext = os.path.splitext(secure_filename_)
        video_name = name+'.mp4'
        video_path = os.path.join(current_app.config['CONVERTED_FOLDER'],video_name)
        with open(file_path, 'wb') as f:
            f.write(file_data)
        emit('alert', {'message': f'File {file_name} successfully uploaded'},to=f"user_{sid}")
        emit('alert', {'message': f'Converting...'},to=f"user_{sid}")
        cov_ppt(src=file_path,dst=video_path,resol=int(resolution),id=sid)
        print("Emitting Final Response")
        emit("convert_success",{"message":f"convert successfully {file_name}",'type':'success',"file_link":video_name},to=f"user_{sid}")     
    except Exception as e:
        import traceback; traceback.print_exc();
        raise e
    
@socketio.on_error_default
def error_handler(e):
    sid = session.get('sid')
    if sid:
        return emit('error',f"{e}",to=f"user_{sid}")