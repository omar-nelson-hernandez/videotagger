import cv2
import numpy as np
import wx
from VideoInformationPanel import VideoInformationPanel
import wx.lib.agw.buttonpanel as bp
from TaggingPanel import TaggingPanel

class VideoContainer( wx.Panel ):

    # Constructor
    def __init__( self, parent ):

        # Call constructor of parent
        wx.Panel.__init__( self, parent )

        # Define class attributes
        self.videoDrawingPanel = wx.Panel( self )
        self.videoSource = None
        self.updateFrameTimer = wx.Timer( self.videoDrawingPanel )
        self.bmpFrame = None
        self.sizer_v = wx.BoxSizer( wx.VERTICAL )
        self.trackbar = wx.Slider( self )
        self.sizer_h = wx.BoxSizer( wx.HORIZONTAL )
        self.vip = VideoInformationPanel( self )
        self.tp = TaggingPanel( self )

        # Button bar
        self.mediaControls = bp.ButtonPanel( self, wx.ID_ANY )
        self.play = bp.ButtonInfo( self.mediaControls, wx.ID_ANY, text = "PLAY" )
        self.mediaControls.AddButton( self.play )
        self.pause = bp.ButtonInfo( self.mediaControls, wx.ID_ANY, text = "PAUSE" )
        self.mediaControls.AddButton( self.pause )
        self.forward = bp.ButtonInfo( self.mediaControls, wx.ID_ANY, text = "FORWARD" )
        self.mediaControls.AddButton( self.forward )
        self.backward = bp.ButtonInfo( self.mediaControls, wx.ID_ANY, text = "BACKWARD" )
        self.mediaControls.AddButton( self.backward )

        # Define events
        self.videoDrawingPanel.Bind( wx.EVT_TIMER, self.onNextFrame, self.updateFrameTimer )
        self.videoDrawingPanel.Bind( wx.EVT_PAINT, self.onPaint )
        self.trackbar.Bind( wx.EVT_SLIDER, self.onSlider, self.trackbar )
        #  self.Bind( wx.EVT_SIZE, self.onResize )
        self.videoDrawingPanel.Bind( wx.EVT_SIZE, self.onResizeVideoPanel )
        self.mediaControls.Bind( wx.EVT_BUTTON, self.onPlay, self.play )
        self.mediaControls.Bind( wx.EVT_BUTTON, self.onPause, self.pause )
        self.mediaControls.Bind( wx.EVT_BUTTON, self.onForward, self.forward )
        self.mediaControls.Bind( wx.EVT_BUTTON, self.onBackward, self.backward )

        # Configure video drawing panel
        self.videoDrawingPanel.SetDoubleBuffered( True )

        # Configure video container panel
        self.SetSizer( self.sizer_h )

        # Configure sizer
        self.sizer_v.Add( self.videoDrawingPanel, 1, wx.EXPAND )
        self.sizer_v.Add( self.mediaControls, 0, wx.EXPAND )
        self.sizer_v.Add( self.trackbar, 0, wx.EXPAND )

        self.sizer_h.Add( self.sizer_v, 1, wx.EXPAND )
        self.sizer_h.Add( self.vip, 1, wx.EXPAND )
        self.sizer_h.Add( self.tp, 1, wx.EXPAND )

        self.mediaControls.DoLayout()

    # Private methods
    #  def onResize( self, evt ):
        #  clientWidth = self.GetClientSize()[0]
        #  self.trackbar.SetSize( clientWidth - 220, -1 )

        #  evt.Skip()

    def onPlay( self, evt ):
        self.videoPlay()

    def onPause( self, evt  ):
        self.videoPause()

    def onForward( self, evt ):
        if self.videoSource.frameNumber < self.videoSource.frames:
            self.updateFrame( self.videoSource.frameNumber + 1 )

    def onBackward( self, evt ):
        if self.videoSource.frameNumber > 0:
            self.updateFrame( self.videoSource.frameNumber - 1 )

    def onResizeVideoPanel( self, evt ):
        if self.videoSource:
            if self.videoSource.frames == self.videoSource.frameNumber:
                newFrame = self.videoSource.frameNumber - 1
            else:
                newFrame = self.videoSource.frameNumber
            self.updateFrame( newFrame )

    def onSlider( self, evt ):
        trackbarPosition = evt.EventObject.GetValue()
        if self.videoSource.frameNumber != trackbarPosition:
            self.updateFrame( trackbarPosition )

    def updateFrame( self, frameNumber ):
        if self.videoSource:
            status, frame = self.videoSource.read( frameNumber )
            self.updateVideo( status, frame )

    def onNextFrame( self, evt ):
        status, frame = self.videoSource.read()
        self.updateVideo( status, frame )

    def updateVideo( self, status, frame ):
        if status:
            npVideoFrame = np.copy( frame )
            height, width = npVideoFrame.shape[ : 2 ]
            displayWidth, displayHeight = self.videoDrawingPanel.GetSize()
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

            imgWorking = cv2.resize( npVideoFrame, ( resizeWidth, resizeHeight ) )
            imgWorking = cv2.cvtColor( imgWorking, cv2.COLOR_BGR2RGB )
            height, width = imgWorking.shape[ : 2 ]
            self.bmpFrame = wx.Bitmap.FromBuffer( width, height, imgWorking.tostring() )
            self.videoDrawingPanel.Refresh()

            # Adjust trackabr
            self.trackbar.SetValue( self.videoSource.frameNumber )
            # Adjust VideoInformationPanel
            self.vip.updateInformation( self.videoSource )

    def onPaint( self, evt ):
        if self.bmpFrame:
            wx.BufferedPaintDC( self.videoDrawingPanel, self.bmpFrame )

        evt.Skip()

    # Public methods
    def videoPlay( self ):
        if self.videoSource:
            self.updateFrameTimer.Start( 1000 / self.videoSource.fps )

    def videoPause( self ):
        self.updateFrameTimer.Stop()

    def setVideoSource( self, videoSource ):
        self.videoSource = videoSource

        # Configure slider for this video source
        self.trackbar.SetRange( 0, self.videoSource.frames - 1 )
        self.trackbar.SetValue( 0 )

        # Configure VideoInformationPanel from VideoSource
        self.vip.updateInformation( videoSource )

        # Pass the video source to the tagging panel in order to fetch information from it
        self.tp.setVideoSource( videoSource )
