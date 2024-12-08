from burp import IBurpExtender, IHttpListener
from RequestViewerGUI2 import RequestViewerGUI

class BurpExtender(IBurpExtender, IHttpListener):
    def __init__(self):
        self.gui = RequestViewerGUI()

    def registerExtenderCallbacks(self, callbacks):
        self.helpers = callbacks.getHelpers()
        callbacks.registerHttpListener(self)

    def processHttpMessage(self, toolFlag, messageIsRequest, message):
        if messageIsRequest:
            request = message.getRequest()
            requestInfo = self.helpers.analyzeRequest(request)
            headers = requestInfo.getHeaders()
            body = request[requestInfo.getBodyOffset():].tostring()
            self.gui.setRequestData(headers, body)
        else:
            return

if __name__ == '__main__':
    pass
