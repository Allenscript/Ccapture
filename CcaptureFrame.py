
import wx
import wx.xrc
import images
# import datetime

from win32.lib import win32con
import win32gui, win32print
 
 
def get_real_resolution():
    """获取真实的分辨率"""
    hDC = win32gui.GetDC(0)
    wide = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    high = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    return (wide,high)
###########################################################################
## Class MainWindow
###########################################################################

class MainWindow ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Ccapture", pos = wx.DefaultPosition, size = wx.Size( 370,107 ),style=wx.CLIP_CHILDREN|wx.CLOSE_BOX ) #style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
                                                                                                                        #596,374       style=wx.CLIP_CHILDREN|wx.CLOSE_BOX ) #                                     
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetIcon(images.AppIcon.GetIcon())

		self.status = customStatusBar(self)
		self.SetStatusBar(self.status)
		self.status.SetStatusText(u"抓取状态：", 0)

		self.display = get_real_resolution()
		self.monitor = (wx.GetDisplaySize().x,wx.GetDisplaySize().y)
		self.zone1 = (0,0)
		self.zone2 = get_real_resolution()

		self.recToolbar = self.CreateToolBar( wx.TB_HORIZONTAL, wx.ID_ANY )

		self.selectBtn = wx.Button( self.recToolbar, wx.ID_ANY, u"设置选区", wx.DefaultPosition, wx.Size(62,25 ), 0 )
		self.recToolbar.AddControl( self.selectBtn )

		self.saveBtn = wx.Button( self.recToolbar, wx.ID_ANY, u"选择保存路径", wx.DefaultPosition, wx.Size(82,25 ), 0 )
		self.recToolbar.AddControl( self.saveBtn )

		self.recordBtn = wx.Button( self.recToolbar, wx.ID_ANY, u"开启记录", wx.DefaultPosition, wx.Size(62,25 ), 0 )
		self.recToolbar.AddControl( self.recordBtn )

		self.helpBtn = wx.BitmapButton( self.recToolbar, wx.ID_ANY, images.Help.GetBitmap(), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		self.recToolbar.AddControl( self.helpBtn )

		self.m_staticText2 = wx.StaticText( self.recToolbar, wx.ID_ANY, u"视频PPT抓取工具", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.recToolbar.AddControl(self.m_staticText2)

		self.closeBtn = wx.BitmapButton( self.recToolbar, wx.ID_ANY, images.Close.GetBitmap(), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		self.recToolbar.AddControl( self.closeBtn )

		self.recToolbar.Realize()
		bSizer1 = wx.BoxSizer( wx.VERTICAL)#HORIZONTAL )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"当前未设置选区", wx.DefaultPosition,wx.Size(340,14 ), 0 )

		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"当前未设置保存路径", wx.DefaultPosition,wx.Size(340,14 ), 0 )
		

		bSizer1.Add( self.m_staticText3, 0, wx.ALL, 5 )
		# bSizer1.Add( ( 60, 0), 0, wx.EXPAND, 5 )
		bSizer1.Add( self.m_staticText4, 0, wx.ALL, 5 )

		self.SetSizer( bSizer1 )
		self.Layout()
		self.Centre( wx.BOTH )

		# Connect Events
		self.selectBtn.Bind( wx.EVT_BUTTON, self.selectZone )
		self.saveBtn.Bind( wx.EVT_BUTTON, self.OnSaveBtn )
		self.helpBtn.Bind( wx.EVT_BUTTON, self.Help )
		self.closeBtn.Bind( wx.EVT_BUTTON, self.close )
		self.Bind(wx.EVT_LEFT_DOWN, self.OnPanelLeftDown)
		self.Bind(wx.EVT_MOTION, self.OnPanelMotion)
		self.Bind(wx.EVT_LEFT_UP, self.OnPanelLeftUp)
		self.lastIMG = None
		self.grabBmp = self.Get_Screen_Bmp()
	def __del__( self ):
		pass
	def setLabel(self,str):
		self.m_staticText3.SetLabel(str)
		pass
	def close(self,event):
		wx.Exit()
	def OnSaveBtn(self, event):

		dlg = wx.DirDialog(self,u"选择文件夹",style=wx.DD_DEFAULT_STYLE)
		if dlg.ShowModal() == wx.ID_OK:
			self.path = dlg.GetPath()
			self.m_staticText4.SetLabel('路径: '+self.path)
		dlg.Destroy()

	def OnPanelLeftDown(self, event):
		pos = event.GetPosition()
		x, y = self.ClientToScreen(pos)
		ox, oy = self.GetPosition()
		dx = x - ox
		dy = y - oy
		self.delta = ((dx, dy))
 
	def OnPanelMotion(self, event):
		if event.Dragging() and event.LeftIsDown():
			mouse=wx.GetMousePosition()
			self.Move((mouse.x-self.delta[0],mouse.y-self.delta[1]))
 
	def OnPanelLeftUp(self, event):
		# if self.frame.HasCapture():
		# 	self.frame.ReleaseMouse()
		pass

	def selectZone( self, event ):
		event.Skip()

	def saveimg( self, event ):
		event.Skip()

	def Get_Screen_Bmp(self):
		screen = wx.ScreenDC()
		width,height = get_real_resolution()
		scale = width/wx.GetDisplaySize().x
		bmp = wx.Bitmap(width, height)
		mem = wx.MemoryDC(bmp)
		mem.Blit(0, 0, width, height, screen, 0, 0)
		bmp=bmp.ConvertToImage().Scale(width/scale,height/scale)
		bmp=bmp.ConvertToBitmap()
		return bmp

class GrabFrame(wx.Frame):
    def __init__(self, frame):
        
        x,y = get_real_resolution()
        wx.Frame.__init__(self, frame, wx.NewId(), pos = (0, 0),
                          size= wx.Size(x-100,y-100), style=wx.NO_BORDER | wx.STAY_ON_TOP)
        
        self.firstPoint = wx.Point(0, 0)#记录截图的第一个点
        self.lastPoint  = wx.Point(0, 0)#记录截图的最后一个点
        self.Started = False            #记录是否按下鼠标左键
        self.frame = frame
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.On_Mouse_LeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.On_Mouse_LeftUp)
        self.Bind(wx.EVT_MOTION, self.On_Mouse_Move)

        
    def OnPaint(self, evt):
        dc = wx.GCDC(wx.BufferedPaintDC(self))
        self.PaintUpdate(dc)

    def PaintUpdate(self, dc):
        rect = self.GetClientRect()
        color = wx.Colour(0, 0, 0, 120)
 
        #设置绘制截图区域时矩形的点
        minX, minY = min(self.firstPoint.x, self.lastPoint.x), min(self.firstPoint.y, self.lastPoint.y)
        maxX, maxY = max(self.firstPoint.x, self.lastPoint.x), max(self.firstPoint.y, self.lastPoint.y)
 
        #画出整个屏幕的截图
        dc.DrawBitmap(self.frame.grabBmp, 0, 0)
 
        #画出阴影部分（截取的部分不需要画）
        dc.SetPen(wx.Pen(color))
        dc.SetBrush(wx.Brush(color))
        dc.DrawRectangle(0, 0, maxX, minY)
        dc.DrawRectangle(maxX, 0, rect.width - maxX, maxY)
        dc.DrawRectangle(minX, maxY, rect.width - minX, rect.height - maxY)
        dc.DrawRectangle(0, minY, minX, rect.height - minY)
 
        if(self.Started == True):
 
            #画出截图区域的边框
            dc.SetPen(wx.Pen(wx.Colour(255, 0, 0)))
            dc.SetBrush(wx.Brush(color, wx.TRANSPARENT))
            dc.DrawRectangle(minX, minY, maxX - minX, maxY - minY)
 
            #显示信息
            dc.SetBrush(wx.Brush(wx.Colour(255,0,0)))
            dc.DrawRectangleList([
                (minX - 2, minY - 2, 5, 5),
                (maxX / 2 + minX / 2 - 2, minY - 2, 5, 5),
                (maxX - 2, minY - 2, 5, 5),
                (maxX - 2, maxY / 2 + minY / 2 - 2, 5, 5),
                (maxX - 2, maxY - 2, 5, 5),
                (maxX / 2 + minX / 2 - 2, maxY - 2, 5, 5),
                (minX - 2, maxY - 2, 5, 5),
                (minX - 2, maxY / 2 + minY / 2 - 2, 5, 5)
                ])
            color = wx.Colour(0,0,0,180)
            dc.SetPen(wx.Pen(color))
            dc.SetBrush(wx.Brush(color, wx.SOLID))
            w,h = 140, 43
            s = u'区域大小：'+str(maxX - minX)+'*'+str(maxY - minY)
            
            s += u'\n鼠标位置：（'+str(self.lastPoint.x)+','+str(self.lastPoint.y)+')'
            lab = s.replace('\n','\t')
            self.frame.setLabel("选区: "+lab)
            dc.DrawRectangle(minX, minY-h-5 if minY -5 > h else minY+5, w, h)
            dc.SetTextForeground(wx.Colour(255,255,255))
            dc.DrawText(s, minX+5, (minY-h-5 if minY-5 > h else minY + 5)+5)
 
 
 
    def On_Mouse_LeftDown(self, evt):
        self.Started = True
        self.firstPoint = evt.GetPosition()
        self.lastPoint = evt.GetPosition()
        
    def On_Mouse_LeftUp(self, evt):
        if(self.Started):
            self.lastPoint = evt.GetPosition()
            if(self.firstPoint.x == self.lastPoint.x)&(self.firstPoint.y == self.lastPoint.y):
                wx.MessageBox(u"区域设置不正确", "Error", wx.OK | wx.ICON_ERROR, self)
                self.Started = False
                self.firstPoint = wx.Point(0, 0)#记录截图的第一个点
                self.lastPoint  = wx.Point(0, 0)#记录截图的最后一个点
                
            else:
                self.frame.bmp = self.frame.grabBmp.GetSubBitmap(wx.Rect(
                    min(self.firstPoint.x, self.lastPoint.x),
                    min(self.firstPoint.y, self.lastPoint.y),
                    abs(self.firstPoint.x - self.lastPoint.x),
                    abs(self.firstPoint.y - self.lastPoint.y)
                    ))
                self.frame.zone1 = (self.firstPoint.x,self.firstPoint.y)
                self.frame.zone2 = ( self.lastPoint.x, self.lastPoint.y)
                self.Close()
                self.frame.Show()
        
    def On_Mouse_Move(self, evt):
        if(self.Started):
            self.lastPoint = evt.GetPosition()
            self.NewUpdate()
 
    def NewUpdate(self):
        self.RefreshRect(self.GetClientRect(), True)
        self.Update()

class customStatusBar(wx.StatusBar):
    def __init__(self, parent):
        wx.StatusBar.__init__(self,parent,-1)
        self.SetFieldsCount(2)
        self.SetStatusWidths([-1,-3])
        self.count=0
        print(parent.GetSize())
