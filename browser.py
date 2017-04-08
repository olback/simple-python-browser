#!/usr/bin/env python

start_url = "https://example.com/"                          # Default: "https://example.com"
window_width = 360                                          # Default: 360
window_height = 600                                         # Default: 600
icon = "icon.ico"                                           # Default: "icon.ico"
enable_nav = 1                                              # Enable navigation? Default: 1
ua = ""                                                     # Web user-agent. Default: ""

import gi
gi.require_version('WebKit', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import WebKit as webkit

class SimpleWebView():

    def __init__(self):
        # Create window
        self.window = gtk.Window()
        self.window.set_icon_from_file(icon)
        self.window.connect('destroy', lambda w: gtk.main_quit())
        self.window.set_default_size(window_width, window_height)

        # Create navigation bar
        self.nav = gtk.HBox()

        self.back = gtk.ToolButton(gtk.STOCK_GO_BACK)
        self.forward = gtk.ToolButton(gtk.STOCK_GO_FORWARD)
        self.refresh = gtk.ToolButton(gtk.STOCK_REFRESH)
        self.address_bar = gtk.Entry()

        self.back.connect('clicked', self.go_back)
        self.forward.connect('clicked', self.go_forward)
        self.refresh.connect('clicked', self.refresh_page)
        self.address_bar.connect('activate', self.load_page)

        # Buttons and url-field
        self.nav.pack_start(self.back, expand=False, fill=False, padding=0)
        self.nav.pack_start(self.forward, expand=False, fill=False, padding=0)
        self.nav.pack_start(self.refresh, expand=False, fill=False, padding=0)
        self.nav.pack_start(self.address_bar, expand=False, fill=False, padding=0)

        # Create view for webpage
        self.view = gtk.ScrolledWindow()
        self.wv = webkit.WebView()

        # Webview set_settings
        wvs = webkit.WebSettings()
        wvs.set_property('user-agent', ua)

        self.wv.set_settings(wvs)
        self.wv.open(start_url)
        self.wv.connect('title-changed', self.change_title)
        self.wv.connect('load-committed', self.change_url)
        self.view.add(self.wv)

        # Add everything and initialize
        self.container = gtk.VBox()
        if enable_nav == 1:
            self.container.pack_start(self.nav, expand=False, fill=False, padding=0)
        self.container.pack_start(self.view, expand=True, fill=True, padding=0)

        self.window.add(self.container)
        self.window.show_all()
        gtk.main()

    def load_page(self, widget):
        add = self.address_bar.get_text()
        if add.startswith('http://') or add.startswith('https://'):
            self.wv.open(add)
        else:
            add = 'https://' + add
            self.address_bar.set_text(add)
            self.wv.open(add)

    def change_title(self, widget, frame, title):
        self.window.set_title(title)

    def change_url(self, widget, frame):
        uri = frame.get_uri()
        self.address_bar.set_text(uri)

    def go_back(self, widget):
        self.wv.go_back()

    def go_forward(self, widget):
        self.wv.go_forward()

    def refresh_page(self, widget):
        self.wv.reload()

initialize = SimpleWebView()
