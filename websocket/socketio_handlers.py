from flask_socketio import SocketIO, join_room, emit
from flask import session , current_app
import base64 , os ,time
from converter import cov_ppt , add_animations , add_background_music
from websocket.utils import allowed_file , allowed_audio_file , save_base64_file
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
        sid = session['sid']
        ppt_file_data = data['ppt_file_data']
        ppt_file_name = secure_filename(data['ppt_name'])
        if not allowed_file(filename=ppt_file_name):
            emit('file_upload_error',{"message":"invalid File!"},to=f"user_{sid}")
            return 400
        ppt_path = save_base64_file(ppt_file_data, ppt_file_name, current_app.config['UPLOAD_FOLDER'])
        audio_file_data = data.get('audio_file')
        audio_path = None
        if audio_file_data:
            audio_file_name = secure_filename(data['audio_name'])
            audio_path = save_base64_file(audio_file_data, audio_file_name, current_app.config['UPLOAD_FOLDER'])
        
        emit('upload_complete', {'status': 200})

        quality = data.get('quality')
        effect = data.get('effect')

        video_name = os.path.splitext(ppt_file_name)[0] + '.mp4'
        video_path = os.path.join(current_app.config['CONVERTED_FOLDER'], video_name)

        cov_ppt(ppt_path, video_path,resol=quality,effect_id=effect,id=sid)

        if audio_path:
            print("Audio File")
            emit('alert', {'message': f'Convert Successfull, Adding Audio'},to=f"user_{sid}")
            output_path = os.path.join(current_app.config['CONVERTED_FOLDER'], f'{os.path.splitext(ppt_file_name)[0]}_with_audio.mp4')
            add_background_music(video_path, audio_path, output_path)
            emit("convert_success",{"message":f"convert successfully {ppt_file_name}",'type':'success',"file_link":f'{os.path.splitext(ppt_file_name)[0]}_with_audio.mp4'},to=f"user_{sid}")     
        else:
            print("no Audio File")
            emit("convert_success",{"message":f"convert successfully {ppt_file_name}",'type':'success',"file_link":video_name},to=f"user_{sid}")     

    except Exception as e:
        import traceback; traceback.print_exc();
        raise e
    
@socketio.on_error_default
def error_handler(e):
    sid = session.get('sid')
    if sid:
        return emit('error',f"{e}",to=f"user_{sid}")