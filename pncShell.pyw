"""
A wrapper around my pnc.py module
"""

import os.path

import wx
import wx.lib.filebrowsebutton as filebrowse

import pnc

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
        menu_bar = wx.MenuBar()
        menu1 = wx.Menu()
        menu1.Append(101, '&Close', 'Close this frame')
        self.SetMenuBar(menu_bar)
        self.Bind(wx.EVT_MENU, self.Close, id=101)

        # Now create the Panel to put the other controls on.
        self.panel = wx.Panel(self, wx.ID_ANY)
        # Use a sizer to layout the controls, stacked vertically and with
        # a 6 pixel border around each
        space = 6
        sflags = wx.ALL
        sizer = wx.BoxSizer(wx.VERTICAL)
        # x = self
        # sizer.Add(self.panel, wx.EXPAND )
        # and a few controls
        text = wx.StaticText(self, -1, "Browse to the .pnc file, choose a root and folder name, and press Do It!")         #pylint: disable=line-too-long
        text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        text.SetSize(text.GetBestSize())
        sizer.Add(text, 0, sflags, space)

        self.btn_infile = filebrowse.FileBrowseButton(self, -1, size=(wide-10, -1),
                                                      changeCallback=self.cback_infile,
                                                      labelText='Use this PNC file')
        self.btn_infile.SetValue('/Users/guy/Downloads/JpegData.PNC')
        sizer.Add(self.btn_infile, 0, sflags, space)

        self.file_browse_root = filebrowse.DirBrowseButton(self, -1, size=(wide-10, -1),
                                                           changeCallback=self.cback_file_root,         #pylint: disable=line-too-long
                                                           labelText='To put JPG files here')
        # self.file_browse_root.SetValue( '/Users/guy/Pictures' )
        self.file_browse_root.SetValue('/Users/guy/python/test')

        # self.file_browse_root.callCallback = False
        sizer.Add(self.file_browse_root, 0, sflags, space)

                # file name root and starting number
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(wx.StaticText(self, -1, "Optional new dir:"), 0, sflags, space)

        self.tc_out_dir = wx.TextCtrl(self, -1, '')
        hsizer.Add(self.tc_out_dir, 0, sflags, space)

        hsizer.Add(wx.StaticText(self, -1, "Filename root:"), 0, sflags, space)

        self.tc_out_fname = wx.TextCtrl(self, -1, 'gcam')
        hsizer.Add(self.tc_out_fname, 0, sflags, space)

        # hsizer.Add(wx.StaticText(self, -1, "File number start:"), 0, sflags, space)

        sizer.Add(hsizer, 0, sflags, space)

        self.cb_move_file = wx.CheckBox(self, -1, 'Move Input file, too')
        sizer.Add(self.cb_move_file, 0, sflags, space)

               # bind the button events to handlers
        hsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        funbtn = wx.Button(self, -1, "Do it")
        self.Bind(wx.EVT_BUTTON, self.evh_doit, funbtn)
        hsizer2.Add(funbtn, 0, sflags, space)
        btn = wx.Button(self, -1, "Close")
        self.Bind(wx.EVT_BUTTON, self.evh_close, btn)
        hsizer2.Add(btn, 0, sflags, space)
        sizer.Add(hsizer2, 0, sflags, space)
        self.SetSizer(sizer)


    def evh_close(self, evt):             #pylint: disable=unused-argument
        """Event handler for the button click."""
        self.Close()

    def evh_doit(self, evt):               #pylint: disable=unused-argument
        """Event handler for the button click."""
        self.SetStatusText('working...')
        print ''
        out_dir = self.file_browse_root.GetValue()
        out_new_dir = self.tc_out_dir.GetValue()
        out_dir = os.path.join(out_dir, out_new_dir)
        b_success = pnc.get_photos(self.btn_infile.GetValue(),
                                   out_dir, self.tc_out_fname.GetValue(),
                                   self.cb_move_file.GetValue())
        if b_success:
            self.SetStatusText('Done!')
        else:
            self.SetStatusText('Failed')

    def cback_infile(self, evt):               #pylint: disable=unused-argument
        """ dummy callback  """
        pass

    def cback_file_root(self, evt):  #pylint: disable=unused-argument
        """ dummy callback  """
        pass

class MyApp(wx.App):
    """ a simple GUI """
    def OnInit(self):      #pylint: disable=invalid-name
        """ let's get this party started  """
        frame = MyFrame(None, "Panasonic .PNC to .JPG converter")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True

# app = MyApp(redirect=True)
app = MyApp()              #pylint: disable=invalid-name
app.MainLoop()
