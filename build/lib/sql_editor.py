
import wx


__version__='0.0.1'

def main():
    # Next, create an application object.
    app = wx.App()
    
    # Then a frame.
    frm = wx.Frame(None, title="Hello World")
    
    # Show it.
    frm.Show()
    
    # Start the event loop.
    app.MainLoop()   

if __name__ == '__main__':
    main()