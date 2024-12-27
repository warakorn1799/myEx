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
        self.index = 0
        self.processing_lock = threading.Lock()  # Add a lock to synchronize queue processing

    def processHttpMessage(self, toolFlag, messageIsRequest, message):
        if toolFlag == IBurpExtenderCallbacks.TOOL_PROXY or toolFlag == IBurpExtenderCallbacks.TOOL_REPEATER:
            self.index += 1
            if messageIsRequest:
                self.messageQueue.put(('request', message, self.index))
            else:
                self.messageQueue.put(('response', message, self.index))
            self.processQueue()
    
    def processQueue(self):
        with self.processing_lock:  # Acquire lock before processing
            if not self.messageQueue.empty():
                item = self.messageQueue.get()
                messageType, message, index = item
                if messageType == 'request':
                    print("Processed request:", message, "at index", self.index)
                    self.handleRequest(message)
                elif messageType == 'response':
                    print("Processed response:", message, "at index", self.index)
                    self.handleResponse(message)
                self.index += 1

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