import cv2
import numpy as np
import wx
import wx.lib.agw.buttonpanel as bp

class VideoPanel( wx.Panel ):

    # Constructor
    def __init__( self, parent, video ):
        # Call constructor of parent
        wx.Panel.__init__( self, parent )

        # Get video source parameter
        self.video = video

        # Setup timer to update video frames
        self.playTimer = wx.Timer( self )
        self.Bind( wx.EVT_TIMER, self.onNextFrame, self.playTimer )
        self.playTimer.Start( 1000 / self.video.fps )

        self.SetDoubleBuffered( True )

        # Bitmap to display on the wx.Panel
        self.bmpVideo = None

        # Paint event
        self.Bind( wx.EVT_PAINT, self.onPaint )


    # Next frame event handler
    def onNextFrame( self, evt ):
        status, frame = self.video.read()
        self.updateVideo( status, frame )

    def updateVideo( self, status, frame ):
        if status:
            self.npFrame = np.copy( frame )
            height, width = self.npFrame.shape[ : 2 ]
            displayWidth, displayHeight = self.GetSize()
            aspectRatio = height * 1.0 / width
            areaWidth = displayWidth * int( round( displayWidth * aspectRatio ) )
            areaHeight = displayHeight * int( round( displayHeight / aspectRatio ) )

            if areaWidth >= areaHeight:
                if int( round( displayWidth * aspectRatio ) ) <= displayHeight:
                    resizeWidth = displayWidth
                    resizeHeight = int( round( displayWidth * aspectRatio ) )
                else:
                    resizeHeight = displayHeight
                    resizeWidth = int( round( displayHeight / aspectRatio ) )
            else:
                if int( round( displayHeight / aspectRatio ) ) <= displayWidth:
                    resizeHeight = displayHeight
                    reiszeWidth = int( round( displayHeight / aspectRatio ) )
                else:
                    resizeWidth = displayWidth
                    resizeHeight = int( round( displayWidth * aspectRatio ) )

            self.imgWorking = cv2.resize( self.npFrame, ( resizeWidth, resizeHeight ) )
            self.imgWorking = cv2.cvtColor( self.imgWorking, cv2.COLOR_BGR2RGB )
            height, width = self.imgWorking.shape[ : 2 ]
            self.bmpVideo = wx.Bitmap.FromBuffer( width, height, self.imgWorking.tostring() )
            self.Refresh()

    def onPaint( self, evt ):
        if self.bmpVideo:
            wx.BufferedPaintDC( self, self.bmpVideo )

        evt.Skip()

