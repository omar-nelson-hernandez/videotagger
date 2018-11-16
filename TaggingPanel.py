import wx

class TaggingPanel( wx.Panel ):

    # Constructor
    def __init__( self, parent ):

        # Call parent constructor
        wx.Panel.__init__( self, parent )

        # Define attributes
        self.availableTags = wx.ComboBox( self, wx.ID_ANY, choices = [ "tag1", "tag2" ] )
        self.taggedItems = wx.ListBox( self, wx.ID_ANY, choices = [ "tagged1", "tagged2" ] )
        self.sizer_h = wx.BoxSizer( wx.HORIZONTAL )
        self.sizer_v = wx.BoxSizer( wx.VERTICAL )
        self.start = wx.Button( self, label = "Start" )
        self.stop = wx.Button( self, label = "Stop" )
        self.btnSizer =  wx.BoxSizer( wx.HORIZONTAL )
        self.activeTag = None

        # Define events
        self.Bind( wx.EVT_BUTTON, self.onStart, self.start )
        self.Bind( wx.EVT_BUTTON, self.onStop, self.stop )

        # Configure panel
        self.SetSizer( self.sizer_v )

        # Configure sizer
        self.sizer_h.Add( self.availableTags )
        self.sizer_h.Add( self.taggedItems )

        self.btnSizer.Add( self.start )
        self.btnSizer.Add( self.stop )

        self.sizer_v.Add( self.sizer_h, 3, wx.EXPAND )
        self.sizer_v.Add( self.btnSizer, 1, wx.EXPAND )

    # Private methods
    def onStart( self, evt ):
        tagSelected = self.availableTags.GetSelection()
        print( f"[TaggingPanel] (Start BTN) Current selection: { tagSelected }" )
        if tagSelected < 0:
            dlg = wx.MessageDialog( message = "No tag selected", caption = "Error!", parent = self )
            dlg.ShowModal()
            dlg.Destroy()
        else:
            self.activeTag = tagSelected
            print( f"[TaggingPanel] (Start BTN) Tag open" )


    def onStop( self, evt ):
        if self.activeTag >= 0:
            print( f"[TaggingPanel] (Stop BTN) Tag closing" )
            tag = self.availableTags.GetString( self.activeTag )
            frame = self.videoSource.frameNumber
            self.taggedItems.InsertItems( [ tag + " -> " + str( frame ) ], 0 )
            self.activeTag = None

    # Public methods
    def setVideoSource( self, videoSource ):
        self.videoSource = videoSource
