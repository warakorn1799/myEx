from burp import IBurpExtender, IHttpListener, IBurpExtenderCallbacks
from RequestViewerGUI2 import RequestViewerGUI
import time
#from EncryptDecrypt import AESECB, AESCBC, AESGCM

class BurpExtender(IBurpExtender, IHttpListener):
    def registerExtenderCallbacks(self, callbacks):
        self.helpers = callbacks.getHelpers()
        callbacks.registerHttpListener(self)
        self.gui = RequestViewerGUI(self.helpers)
        
        #aes_cipher = AESCBC(192)
        #plaintext = "Hello world"
        #print("Plaintext:", plaintext)
        
        # Encrypt
        #ciphertext = aes_cipher.encrypt(plaintext)
        #print("Ciphertext: {}".format(str(ciphertext)))
        
        # Decrypt
        #decrypted_text = aes_cipher.decrypt(ciphertext)
        #print("Decrypted: {}".format(str(decrypted_text)))

    def processHttpMessage(self, toolFlag, messageIsRequest, message):
	if toolFlag == IBurpExtenderCallbacks.TOOL_PROXY or toolFlag == IBurpExtenderCallbacks.TOOL_REPEATER:
	    if messageIsRequest:
                request = message.getRequest()
                requestInfo = self.helpers.analyzeRequest(request)
                headers = requestInfo.getHeaders()
                body = request[requestInfo.getBodyOffset():].tostring()
                self.gui.setRequestData(headers, body, message)
                self.waitForEncryptButtonPress()
            else:
                response = message.getResponse()
                if response is not None:
		    responseInfo = self.helpers.analyzeResponse(response)
                    responseHeaders = responseInfo.getHeaders()
                    responseBodyOffset = responseInfo.getBodyOffset()
                    responseBody = response[responseBodyOffset:].tostring()
		    self.gui.setResponseData(responseHeaders, responseBody, response)
		    self.waitForSendButtonPress()
	else:
            print("Pass Because it not from Proxy")

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
