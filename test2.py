from burp import IBurpExtender, IHttpListener, IBurpExtenderCallbacks
from RequestViewerGUI2 import RequestViewerGUI
import time
from Queue import Queue

class BurpExtender(IBurpExtender, IHttpListener):
    def registerExtenderCallbacks(self, callbacks):
        self.helpers = callbacks.getHelpers()
        callbacks.registerHttpListener(self)
        self.gui = RequestViewerGUI(self.helpers)
        self.message_queue = Queue()
        self.is_processing_request = False
        self.is_processing_response = False

    def processHttpMessage(self, toolFlag, messageIsRequest, message):
        if toolFlag == IBurpExtenderCallbacks.TOOL_PROXY or toolFlag == IBurpExtenderCallbacks.TOOL_REPEATER:
            if messageIsRequest:
                if not self.is_processing_request:
                    self.is_processing_request = True
                    self.message_queue.put(('request', message))
                    self.processQueue()
                else:
                    print("Request discarded because processing is already ongoing")
            else:
                if not self.is_processing_response:
                    self.is_processing_response = True
                    self.message_queue.put(('response', message))
                    self.processQueue()
                else:
                    print("Response discarded because processing is already ongoing")
        else:
            print("Skipped because it's not from Proxy or Repeater")

    def processQueue(self):
        while not self.message_queue.empty():
            message_type, message = self.message_queue.get()
            self.handleMessage(message_type, message)
        self.is_processing_request = False
        self.is_processing_response = False

    def handleMessage(self, message_type, message):
        if message_type == 'request':
            self.handleRequest(message)
        elif message_type == 'response':
            self.handleResponse(message)

    def handleRequest(self, message):
        request = message.getRequest()
        requestInfo = self.helpers.analyzeRequest(request)
        headers = requestInfo.getHeaders()
        body = request[requestInfo.getBodyOffset():].tostring()
        self.gui.setRequestData(headers, body, message)
        self.waitForEncryptButtonPress()

    def handleResponse(self, message):
        response = message.getResponse()
        if response is not None:
            responseInfo = self.helpers.analyzeResponse(response)
            responseHeaders = responseInfo.getHeaders()
            responseBodyOffset = responseInfo.getBodyOffset()
            responseBody = response[responseBodyOffset:].tostring()
            self.gui.setResponseData(responseHeaders, responseBody, message)
            self.waitForSendButtonPress()

    def waitForEncryptButtonPress(self):
        while True:
            if self.gui.isEncryptButtonPressed():
                self.gui.resetEncryptButton()
                break
            else:
                time.sleep(1)

    def waitForSendButtonPress(self):
        while True:
            if self.gui.isSendButtonPressed():
                self.gui.resetSendButton()
                break
            else:
                time.sleep(1)

    def unRegisterExtenderCallbacks(self, callbacks):
        callbacks.unregisterHttpListener(self)
