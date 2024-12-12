from burp import IBurpExtender, IHttpListener
from RequestViewerGUI2 import RequestViewerGUI

class BurpExtender(IBurpExtender, IHttpListener):
    def registerExtenderCallbacks(self, callbacks):
        self.helpers = callbacks.getHelpers()
        callbacks.registerHttpListener(self)
        self.gui = RequestViewerGUI(self.helpers)

    def processHttpMessage(self, toolFlag, messageIsRequest, message):
        if messageIsRequest:
            request = message.getRequest()
            requestInfo = self.helpers.analyzeRequest(request)
            headers = requestInfo.getHeaders()
            body = request[requestInfo.getBodyOffset():].tostring()
            self.gui.setRequestData(headers, body, message)
        else:
            response = message.getResponse()
            if response is not None:
                responseInfo = self.helpers.analyzeResponse(response)

                print("Response received:")
                if "image/x-icon" in self.helpers.bytesToString(response).encode('ascii', 'ignore').decode('ascii'):
                    print("skip")
                else:
                    print(self.helpers.bytesToString(response).encode('ascii', 'ignore').decode('ascii'))
