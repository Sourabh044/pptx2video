import win32com.client
import time
import pythoncom
import os
from flask_socketio import emit
from moviepy.editor import VideoFileClip, AudioFileClip

msoMedia = 16	#Media
msoPicture	= 13	#Picture
msoAnimEffectFade = 1
msoAnimEffectBounce = 26
msoAnimEffectZoom =	23
msoAnimTriggerAfterPrevious = 3


def isMediaType(shape):
    return shape.Type == msoMedia or shape.Type == msoPicture

def add_animations(presentation):
    previous_shape = None
    for slide in presentation.Slides:
        max_delay = 0
        for shape in slide.Shapes:
            if shape.HasTextFrame and shape.TextFrame.HasText:
                paragraphs = shape.TextFrame.TextRange.Paragraphs()
                print("Effect added to Text")
                for i in range(1, paragraphs.Count + 1):
                    # paragraph = paragraphs(i)
                    effect = slide.TimeLine.MainSequence.AddEffect(
                        shape,
                        msoAnimEffectZoom,
                        0,
                        msoAnimTriggerAfterPrevious
                    )
                    effect.Timing.TriggerDelayTime = (i - 1) * 1  # Delay each paragraph by 0.5 seconds
                    max_delay = max(max_delay, effect.Timing.TriggerDelayTime + 1)  # Assume each effect lasts 1 second
            elif isMediaType(shape):  # Shape is a media object (e.g., picture, video, etc.)
                print("Effect added to Media")
                effect = slide.TimeLine.MainSequence.AddEffect(
                    shape,
                    msoAnimEffectZoom,
                    0,
                    msoAnimTriggerAfterPrevious
                )
                effect.Timing.TriggerDelayTime = max_delay if max_delay > 0 else max_delay +1
                max_delay += 1  # Assume each media effect lasts 1 second
            previous_shape = shape
        slide.SlideShowTransition.AdvanceOnTime = True
        slide.SlideShowTransition.AdvanceTime = max_delay + 10
    return presentation

def cov_ppt(src, dst, resol,id):
    pythoncom.CoInitialize()
    PowerPoint = win32com.client.Dispatch('PowerPoint.Application')
    presentation = PowerPoint.Presentations.Open(src, WithWindow=False)
    # PowerPoint.Visible = True
    emit('alert', {'message': f'Adding Animations..'},to=f"user_{id}")
    presentation = add_animations(presentation)
    emit('alert', {'message': f'Creating Video...'},to=f"user_{id}")
    presentation.CreateVideo(dst, VertResolution=resol)
    emit('alert', {'message': f'Saving Video...'},to=f"user_{id}")
    while True:
        time.sleep(1)
        try:
            os.rename(dst, dst)
            print(src + ' has been successfully converted!')
            break
        except Exception:
            pass
    PowerPoint.Quit()
    print('exiting function')
    return

def add_background_music(video_path, audio_path, output_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path).subclip(0, video_clip.duration)
    video_with_audio = video_clip.set_audio(audio_clip)
    video_with_audio.write_videofile(output_path, codec="libx264", audio_codec="aac")

if __name__ == "__main__":
    print("Please enter the desired video resolution")
    resol = 720
    while resol not in [480, 720, 1080, 2160]:
        resol = int(input("You can only choose from [480, 720, 1080, 2160]: "))
    
    # audio_path = input("Please provide the path to the background music file: ")
    audio_path = "audio\\audio.mp3"
    ppt_srcs = os.listdir('ppt\\')
    print("Starting conversion!")
    start_time = time.time()
    for ppt_src in ppt_srcs:
        ppt_path = os.getcwd() + '\\ppt\\' + ppt_src
        video_path = os.getcwd() + '\\video\\' + ppt_src[:-5] + '.mp4'
        output_path = os.getcwd() + '\\video_with_audio\\' + ppt_src[:-5] + '_with_audio.mp4'
        
        cov_ppt(ppt_path, video_path, resol)
        # add_background_music(video_path, audio_path, output_path)
    
    end_time = time.time()
    print('The entire conversion process took: ' + str(end_time - start_time) + ' seconds')
    input("Press any key to exit...")
