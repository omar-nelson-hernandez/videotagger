import wx

class TaggingPanel( wx.Panel ):

    # Constructor
    def __init__( self, parent ):

        # Call parent constructor
        wx.Panel.__init__( self, parent )

        # Define attributes
        self.availableTags = wx.ListBox( self, wx.ID_ANY, size = wx.Size( 100, 300 ) )
        self.openTags = wx.ListBox( self, wx.ID_ANY, size = wx.Size( 100, 300 ) )
        self.taggedItems = wx.ListBox( self, wx.ID_ANY, size = wx.Size( 100, 300 ) )
        self.sizer_h = wx.BoxSizer( wx.HORIZONTAL )
        self.sizer_v = wx.BoxSizer( wx.VERTICAL )
        self.start = wx.Button( self, label = "Start" )
        self.stop = wx.Button( self, label = "Stop" )
        self.btnSizer =  wx.BoxSizer( wx.HORIZONTAL )
        self.btnLoadTags = wx.Button( self, label = "Load tags" )
        self.btnExportTags = wx.Button( self, label = "Export tags" )

        #self.SetBackgroundColour( ( 11, 11, 11 ) )

        # Define events
        self.Bind( wx.EVT_BUTTON, self.onStart, self.start )
        self.Bind( wx.EVT_BUTTON, self.onStop, self.stop )
        self.Bind( wx.EVT_BUTTON, self.onLoadTags, self.btnLoadTags )
        self.Bind( wx.EVT_BUTTON, self.onExportTags, self.btnExportTags )

        # Configure panel
        self.SetSizer( self.sizer_v )

        # Configure sizer
        self.sizer_h.Add( self.availableTags )
        self.sizer_h.Add( self.openTags )
        self.sizer_h.Add( self.taggedItems )

        self.btnSizer.Add( self.start )
        self.btnSizer.Add( self.stop )
        self.btnSizer.Add( self.btnLoadTags )
        self.btnSizer.Add( self.btnExportTags )

        self.sizer_v.Add( self.sizer_h, 3, wx.EXPAND )
        self.sizer_v.Add( self.btnSizer, 1, wx.EXPAND )

    # Private methods
    def onExportTags( self, evt ):
        with wx.FileDialog( self, "Export tags to file...", style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT ) as fileDialog:

            # User cancelled the curren operation
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            # User chose a file
            with open( fileDialog.GetPath(), "w" ) as outFile:
                for tag in range( 0, self.taggedItems.GetCount() ):
                    outFile.write( self.taggedItems.GetString( tag ) + "\n" )

    def onLoadTags( self, evt ):
        with wx.FileDialog( self, "Load tags from file...", style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST ) as fileDialog:

            # User cancelled current operation
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            # User chose a file
            with open( fileDialog.GetPath() ) as tagFile:
                for line in tagFile:
                    self.availableTags.InsertItems( [ line.rstrip( "\n" ) ], 0 )

    def onStart( self, evt ):
        tagSelected = self.availableTags.GetSelection()
        print( f"[TaggingPanel] (Start BTN) Current selection: { tagSelected }" )
        if tagSelected < 0:
            dlg = wx.MessageDialog( message = "No tag selected", caption = "Error!", parent = self )
            dlg.ShowModal()
            dlg.Destroy()
        else:
            tag = self.availableTags.GetString( tagSelected )
            frame = str( self.videoSource.frameNumber )
            print( f"[TaggingPanel] (Start BTN) Tag open: <{ tag }> on frame <{ frame }>" )
            self.openTags.InsertItems( [ tag + "," + frame ], 0 )


    def onStop( self, evt ):
        closingTag = self.openTags.GetSelection()
        if closingTag < 0:
            dlg = wx.MessageDialog( message = "No alredy open tag selected", caption = "Error!", parent = self )
            dlg.ShowModal()
            dlg.Destroy()
        else:
            tag = self.openTags.GetString( closingTag )
            frame = str( self.videoSource.frameNumber )
            print( f"[TaggingPanel] (Stop BTN) Tag closing: <{ tag }> on frame <{ frame }>" )
            self.taggedItems.InsertItems( [ tag + "," + frame  ], 0 )

            # Remove item from open tags
            self.openTags.Delete( closingTag )

    # Public methods
    def setVideoSource( self, videoSource ):
        self.videoSource = videoSource
