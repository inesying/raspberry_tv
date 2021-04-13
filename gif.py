

import os
import time
from PIL import Image, ImageOps

class Frame:
    def __init__(self, duration=0):
        self.duration = duration
        self.image = None

class AnimatedGif:
    def __init__(self, ShowImage,Xstart=0,Ystart=0, width=240, height=240, folder=None):
        self._frame_count = 0
        self._loop = 0
        self._index = 0
        self._duration = 0
        self._gif_files = []
        self._gif_files_size=-1
        self._frames = []
        self._height=height
        self._width=width
        self._Xstart=Xstart
        self._Ystart=Ystart
        self._ShowImage = ShowImage
        if folder is not None:
            self.load_files(folder)
            self.run()
 
    def advance(self):
        self._index = (self._index + 1) % len(self._gif_files)
 
    def back(self):
        self._index = (self._index - 1 + len(self._gif_files)) % len(self._gif_files)
 
    def load_files(self, folder):
        gif_files = [f for f in os.listdir(folder) if f.endswith(".gif")]
        for gif_file in gif_files:
            image = Image.open(gif_file)
            # Only add animated Gifs
            if image.is_animated:
                self._gif_files.append(gif_file)
                self._gif_files_size+=1
 
        print("Found", self._gif_files)
        if not self._gif_files:
            print("No Gif files found in current folder")
            exit()  # pylint: disable=consider-using-sys-exit
 
    def preload(self):
        image = Image.open(self._gif_files[self._index])
        print("Loading {}...".format(self._gif_files[self._index]))
        if "duration" in image.info:
            self._duration = image.info["duration"]
        else:
            self._duration = 0
        if "loop" in image.info:
            self._loop = image.info["loop"]
        else:
            self._loop = 1
        self._frame_count = image.n_frames
        self._frames.clear()
        for frame in range(self._frame_count):
            image.seek(frame)
            # Create blank image for drawing.
            # Make sure to create image with mode 'RGB' for full color.
            frame_object = Frame(duration=self._duration)
            if "duration" in image.info:
                frame_object.duration = image.info["duration"]
            frame_object.image = ImageOps.pad(  # pylint: disable=no-member
                image.convert("RGB"),
                (self._width, self._height),
                method=Image.NEAREST,
                color=(0, 0, 0),
                centering=(0.5, 0.5),
            )
            self._frames.append(frame_object)
 
    def play(self):
        self.preload()
 
        # Check if we have loaded any files first
        if not self._gif_files:
            print("There are no Gif Images loaded to Play")
            return False
        while True:
            for frame_object in self._frames:
                start_time = time.monotonic()
                image=frame_object.image
                image = image.rotate(180).resize((240, 240))
                image=image.transpose(Image.FLIP_LEFT_RIGHT)
                self._ShowImage(image,self._Xstart,self._Ystart)

                while time.monotonic() < (start_time + frame_object.duration / 1000):
                    pass
        

 
            
            if self._loop > 0:
                self._loop -= 1
            if self._gif_files_size==self._index:
                return True
            if self._loop==0:
                self._index+=1
                return False
            
 
    def run(self):
        while True:
            auto_advance = self.play()
            if auto_advance:
                self.advance()

