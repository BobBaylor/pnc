#----------------------------------------------------------------------
# A wrapper around my pnc.py module
#----------------------------------------------------------------------

import wx
import pnc
import  wx.lib.filebrowsebutton as filebrowse

class MyFrame(wx.Frame):
    """
    This is MyFrame.  It just shows a few controls on a wxPanel,
    and has a simple menu.

    Use this file inFileBtn
    Write this root name TextEntry 
    and starting number TextEntry
    To here outDirRootButton
    Optional subdirectory TextEntry
    Move the input file there, too CheckBox
    """
    def __init__(self, parent, title):
        wide = 860
        wx.Frame.__init__(self, parent, wx.ID_ANY, title,
                          pos=(150, 150), size=(wide, 270))
        # make a minimalist menu bar
        self.CreateStatusBar()
        menuBar = wx.MenuBar()
        menu1 = wx.Menu()
        menu1.Append(101,'&Close','Close this frame')
        self.SetMenuBar( menuBar )
        self.Bind(wx.EVT_MENU, self.Close, id=101)

        # Now create the Panel to put the other controls on.
        self.panel = wx.Panel(self,wx.ID_ANY)
        # Use a sizer to layout the controls, stacked vertically and with
        # a 6 pixel border around each
        space = 6
        sflags = wx.ALL
        sizer = wx.BoxSizer( wx.VERTICAL )
        x = self
        # sizer.Add(self.panel, wx.EXPAND )
        # and a few controls
        text = wx.StaticText(x, -1, "Browse to the .pnc file, choose a root and folder name, and press Do It!")
        text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        text.SetSize(text.GetBestSize())
        sizer.Add( text,                  0, sflags, space)
       
        self.inFileBtn = filebrowse.FileBrowseButton(x, -1, size=(wide-10, -1), 
            changeCallback = self.fbbCallback, labelText='Use this PNC file')
        self.inFileBtn.SetValue( '/Users/guy/Downloads/JpegData.PNC')
        sizer.Add( self.inFileBtn,        0, sflags, space)

        self.outDirRootButton = filebrowse.DirBrowseButton(x, -1, size=(wide-10, -1),  
            changeCallback = self.outDirRootButtonCallback, labelText='To put JPG files here') 
        # self.outDirRootButton.SetValue( '/Users/guy/Pictures' )
        self.outDirRootButton.SetValue( '/Users/guy/python/test' )
        
        # self.outDirRootButton.callCallback = False
        sizer.Add( self.outDirRootButton, 0, sflags, space)
 
                # file name root and starting number 
        hsizer = wx.BoxSizer( wx.HORIZONTAL )
        l1 = wx.StaticText(x, -1, "Optional new dir:")
        hsizer.Add( l1,                    0, sflags, space )

        self.mkDirCtrl = wx.TextCtrl( x, -1, '')              
        hsizer.Add( self.mkDirCtrl,     0, sflags, space )
 
        l2 = wx.StaticText(x, -1, "Filename root:")
        hsizer.Add( l2,                    0, sflags, space )

        self.fileRootCtrl = wx.TextCtrl( x, -1, 'gcam')              
        hsizer.Add( self.fileRootCtrl,     0, sflags, space )
 
        l3 = wx.StaticText(x, -1, "File number start:")
        hsizer.Add( l3,                    0, sflags, space )

        self.fileNumCtrl = wx.TextCtrl( x, -1, '0')              
        hsizer.Add( self.fileNumCtrl,      0, sflags, space )
        sizer.Add( hsizer,                0, sflags, space)

        self.cb = wx.CheckBox( x, -1, 'Move Input file, too')
        sizer.Add( self.cb,               0, sflags, space)

               # bind the button events to handlers
        hsizer2 = wx.BoxSizer( wx.HORIZONTAL )
        funbtn = wx.Button(x, -1, "Do it")
        self.Bind(wx.EVT_BUTTON, self.OnFunButton, funbtn)
        hsizer2.Add( funbtn,                0, sflags, space)
        btn = wx.Button(x, -1, "Close")
        self.Bind(wx.EVT_BUTTON, self.OnTimeToClose, btn)
        hsizer2.Add( btn,                   0, sflags, space)
        # self.result = wx.TextCtrl(x, -1, '')
        # hsizer2.Add( self.result,                   0, sflags, space)

        sizer.Add( hsizer2,                0, sflags, space)
        
        self.SetSizer(sizer)
        

    def OnTimeToClose(self, evt):
        """Event handler for the button click."""
        # print "See ya later!"
        self.Close()

    def OnFunButton(self, evt):
        """Event handler for the button click."""
        self.SetStatusText( 'working...')
        # self.delay(0.1) working doesn't show in the panel.. wtf?
        print ''
        oDir = self.outDirRootButton.GetValue()
        mkDir = self.mkDirCtrl.GetValue()
        if len( mkDir ) > 0:
            oDir = oDir + '/'
            oDir = oDir + mkDir
        fNum = int( self.fileNumCtrl.GetValue() )
        # print self.inFileBtn.GetValue(), ' to ', oDir
        # print 'With', self.cb.GetValue(),  self.fileRootCtrl.GetValue(), '%04d' % fNum 
        bIsOk = pnc.getPhotos(self.inFileBtn.GetValue(),oDir,self.fileRootCtrl.GetValue(),fNum,self.cb.GetValue())
        if bIsOk:
            self.SetStatusText( 'Done!')
        else:
            self.SetStatusText( 'Failed')

    def fbbCallback(self, evt):
        # print('FileBrowseButton: %s\n' % evt.GetString())
        pass

    def outDirRootButtonCallback(self, evt):
        # print('outDirButton: %s\n' % evt.GetString())
        pass

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, "Panasonic .PNC to .JPG converter")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True
        
# app = MyApp(redirect=True)
app = MyApp()
app.MainLoop()

