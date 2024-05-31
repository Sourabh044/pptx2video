def allowed_file(filename):
    # Check if the file has a .pptx extension
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pptx'