import cv2
import numpy as np

class VideoSource():

    # Constructor
    def __init__( self, source = 0, frameNumber = 0 ):
        # Save parameters into local variables
        self.source = source
        self.frameNumber = frameNumber
        print( f"[Video] Source: { self.source }" )
        print( f"[Video] Frame number: { self.frameNumber }" )

        # Create capture object
        self.capture = cv2.VideoCapture( self.source )

        # Get size properties
        self.width = int( round( self.capture.get( cv2.CAP_PROP_FRAME_WIDTH ) ) )
        self.height = int( round( self.capture.get( cv2.CAP_PROP_FRAME_HEIGHT ) ) )
        print( f"[Video] Width: { self.width }" )
        print( f"[Video] Height: { self.height }" )

        # Get total frames
        self.frames = int( round( self.capture.get( cv2.CAP_PROP_FRAME_COUNT ) ) )
        print( f"[Video] Total frames: { self.frames }" )

        # Get FPS
        self.fps = self.capture.get( cv2.CAP_PROP_FPS )
        print( f"[Video] FPS: { self.fps }" )

        # Move to the correct frame when the source is a video file
        if source != 0:
            if ( frameNumber > 0 ) and ( frameNumber < self.frames ):
                self.capture.set( cv2.CAP_PROP_POS_FRAMES, frameNumber )

        # Why?
        self.frameNumber = int( round( self.capture.get( cv2.CAP_PROP_POS_FRAMES ) ) )
        print( f"[Video] Frame number: { self.frameNumber }" )

        # Get position in msec
        self.time = self.capture.get( cv2.CAP_PROP_POS_MSEC ) / 1000.0
        print( f"[Video] Msec: { self.time }" )

    # Read method
    def read( self, frameNumber = None ):
        if frameNumber is not None:
            if frameNumber > -1 and frameNumber < self.frames:
                print( f"[Video] Seeking frame { frameNumber }" )
                self.capture.set( cv2.CAP_PROP_POS_FRAMES, frameNumber )
            else:
                print( f"[Video] Invalid frame number: { frameNumber }" )
                return (False, np.zeros( self.height, self.width, 3 ))

        # Get new frame number and position in msec
        self.frameNumber = int( round( self.capture.get( cv2.CAP_PROP_POS_FRAMES ) ) )
        self.time = self.capture.get( cv2.CAP_PROP_POS_MSEC ) / 1000.0

        status, img = self.capture.read()
        return ( status, img )

    # Define accesors
    def getSource():
        return self.source

    def getWidth():
        return self.width

    def getHeight():
        return self.height

    def getFrames():
        return self.frames

    def getFps():
        return self.fps

    def getFrameNumber():
        return self.frameNumber

    def getTime():
        return self.time
