from burp import IBurpExtender, IHttpListener, IContextMenuFactory
from javax.swing import JMenuItem
from java.util import ArrayList
from RequestViewerGUI import RequestViewerGUI

class BurpExtender(IBurpExtender, IHttpListener, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("Send to Extension")
        
        callbacks.registerContextMenuFactory(self)
        print("[+] Extension loaded successfully with context menu!")

    def createMenuItems(self, invocation):
        menu_list = ArrayList()
        menu_item = JMenuItem("Send to My Extension", actionPerformed=lambda x: self.handleMenuAction(invocation))
        menu_list.add(menu_item)
        return menu_list

    def handleMenuAction(self, invocation):
        selected_messages = invocation.getSelectedMessages()
        for message_info in selected_messages:
            request = message_info.getRequest()
            analyzed_request = self._helpers.analyzeRequest(request)
            headers = analyzed_request.getHeaders()
            body = request[analyzed_request.getBodyOffset():].tostring()

            gui = RequestViewerGUI(headers, body)
            gui.show_request_in_gui()
