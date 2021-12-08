import wx

import CcaptureFrame


class mainWin(CcaptureFrame.MainWindow):

    def Help(self,event):
        print('into help')
        pass
    def selectZone(self, event):
        self.grabBmp = self.Get_Screen_Bmp()
        gr = CcaptureFrame.GrabFrame(self)
        gr.Show()

    def saveimg(self,event):
        
        screen = wx.ScreenDC()
        scale = self.display[0]/self.monitor[0]
        width = self.zone2[0]-self.zone1[0]
        height = self.zone2[1]-self.zone1[1]

        bmp = wx.Bitmap(int(width*scale), int(height*scale))
        mem = wx.MemoryDC(bmp)
        mem.Blit(0,0, int(width*scale), int(height*scale), screen, int(self.zone1[0]*scale),int(self.zone1[1]*scale))
        bmp.SaveFile("123" + '.png', wx.BITMAP_TYPE_PNG)

if __name__ == '__main__':
    app = wx.App()
    main_win = mainWin(None)
    size = wx.GetDisplaySize()
    main_win.Move(size.x-380,size.y-180)
    main_win.Show()

    app.MainLoop()