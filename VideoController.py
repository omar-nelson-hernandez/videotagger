from VideoContainer import VideoContainer
from VideoSource import VideoSource
import wx

print( "[MAIN] Initializing application..." )
app = wx.App( False )
print( "[MAIN] Creating main frame..." )
frame = wx.Frame( None, title = "VideoTagger" )

print( "[MAIN] Creating VideoContainer inside main frame..." )
vc = VideoContainer( frame )
print( "[MAIN] Creating VideoSource..." )
video = VideoSource( "test.mp4" )

print( "[MAIN] Setting video source for VideoContainer" )
vc.setVideoSource( video )

print( "[MAIN] Show main frame and main loop..." )
frame.Show()
app.MainLoop()
