#!/usr/bin/env python

# Import libs
import gi, requests, json, urllib3
gi.require_version('WebKit', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import WebKit as webkit


# Load settings from settings.json
with open ("settings.json", "r") as settings_json:
    settings = json.load(settings_json)


# Terminal colors for error messages and other info
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Check if this is the latest version.
with open ("info.json", "r") as local_info:
    local_proj_info = json.load(local_info)

local_version = str(local_proj_info['version'])

http = urllib3.PoolManager()
r = http.request('GET', 'https://raw.githubusercontent.com/olback/simple-python-browser/master/info.json')
github_proj_info = json.loads(r.data.decode('utf-8'))

if (str(github_proj_info['version']) == local_version):
    print (bcolors.OKGREEN + 'Your browser is up to date! ' + bcolors.ENDC + str(github_proj_info['version']))
else:
    print (bcolors.WARNING + '\nBrowser not up to date, please download the latest version from\n'+ github_proj_info['project_link'] + bcolors.FAIL + '\nCurrent version: '+ bcolors.ENDC + local_version + bcolors.OKGREEN + '\nNew version: '+ bcolors.ENDC + str(github_proj_info['version']))


# Actual browser
class SimpleWebView():

    def __init__(self):
        # Create window
        self.window = gtk.Window()
        self.window.set_icon_from_file(settings['icon'])
        self.window.connect('destroy', lambda w: gtk.main_quit())
        self.window.set_default_size(settings['window_width'], settings['window_height'])

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
        self.nav.pack_start(self.address_bar, expand=True, fill=True, padding=5)

        # Create view for webpage
        self.view = gtk.ScrolledWindow()
        self.wv = webkit.WebView()

        # Webview settings
        wvs = webkit.WebSettings()
        wvs.set_property('user-agent', settings['ua'])

        self.wv.set_settings(wvs)
        self.wv.open(settings['start_url'])
        self.wv.connect('title-changed', self.change_title)
        self.wv.connect('load-committed', self.change_url)
        self.view.add(self.wv)

        # Add everything and initialize
        self.container = gtk.VBox()
        if settings['enable_nav'] == "true":
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
