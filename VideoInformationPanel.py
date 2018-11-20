import wx

class VideoInformationPanel( wx.Panel ):

    # Constructor
    def __init__( self, parent ):

        # Call parent constructor
        wx.Panel.__init__( self, parent, size = wx.Size( 300, 300 ) )

        # Define attributes
        self.sizer_v = wx.BoxSizer( wx.VERTICAL )
        self.txt_source = wx.StaticText( self )
        self.txt_frames = wx.StaticText( self )
        self.txt_width = wx.StaticText( self )
        self.txt_height = wx.StaticText( self )
        self.txt_fps = wx.StaticText( self )
        self.txt_time = wx.StaticText( self )

        # Configure panel
        self.SetSizer( self.sizer_v )

        # Configure sizer
        self.sizer_v.Add( self.txt_source )
        self.sizer_v.Add( self.txt_frames )
        self.sizer_v.Add( self.txt_width )
        self.sizer_v.Add( self.txt_height )
        self.sizer_v.Add( self.txt_fps )
        self.sizer_v.Add( self.txt_time )

    # Public methods
    def updateInformation( self, videoSource ):
        self.txt_source.SetLabel( f"Source: { videoSource.source }" )
        self.txt_frames.SetLabel( f"Frame: { videoSource.frameNumber + 1 } / { videoSource.frames }" )
        self.txt_width.SetLabel( f"Width: { videoSource.width }" )
        self.txt_height.SetLabel( f"Height: { videoSource.height }" )
        self.txt_fps.SetLabel( f"FPS: { videoSource.fps }" )
        self.txt_time.SetLabel( f"Elapsed: { round( videoSource.time ) }s" )
