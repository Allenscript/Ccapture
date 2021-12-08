import wx

import CcaptureFrame

if __name__ == '__main__':
    app = wx.App()
    main_win = CcaptureFrame.MainWindow(None)
    size = wx.GetDisplaySize()
    main_win.Move(size.x-380,size.y-180)
    main_win.Show()

    app.MainLoop()