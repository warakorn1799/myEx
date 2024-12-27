from burp import IBurpExtender, IHttpListener, IBurpExtenderCallbacks
from RequestViewerGUI2 import RequestViewerGUI
from Queue import Queue
import time
import threading

class BurpExtender(IBurpExtender, IHttpListener):
    def registerExtenderCallbacks(self, callbacks):
        self.helpers = callbacks.getHelpers()
        callbacks.registerHttpListener(self)
        self.gui = RequestViewerGUI(self.helpers)

        self.messageQueue = Queue()
        self.processingLock = threading.Lock()

    def processHttpMessage(self, toolFlag, messageIsRequest, message):
        if toolFlag == IBurpExtenderCallbacks.TOOL_PROXY or toolFlag == IBurpExtenderCallbacks.TOOL_REPEATER:
            if messageIsRequest:
                self.messageQueue.put(('request', message))
            else:
                self.messageQueue.put(('response', message))
            self.processQueue()
    
    def processQueue(self):
        with self.processingLock:
            if not self.messageQueue.empty():
                item = self.messageQueue.get()
                messageType, message = item
                if messageType == 'request':
                    self.handleRequest(message)
                elif messageType == 'response':
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
            self.gui.setResponseData(responseHeaders, responseBody, response)
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