import os
import base64
def allowed_file(filename):
    # Check if the file has a .pptx extension
    # name ,ext = os.path.splitext(filename)
    # return ext.lower() == 'pptx'
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pptx'



def allowed_audio_file(filename):
    # Check if the file has a .pptx extension
    name ,ext = os.path.splitext(filename)
    return ext == 'mp3'
    # return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'mp3'


def save_base64_file(data, filename, folder):
    filepath = os.path.join(folder, filename)
    with open(filepath, "wb") as fh:
        fh.write(base64.b64decode(data.split(',')[1]))
    return filepath