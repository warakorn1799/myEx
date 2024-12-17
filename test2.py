from burp import IBurpExtender, IHttpListener
from RequestViewerGUI2 import RequestViewerGUI
import time
from EncryptDecrypt import AESECB

class BurpExtender(IBurpExtender, IHttpListener):
    def registerExtenderCallbacks(self, callbacks):
        self.helpers = callbacks.getHelpers()
        callbacks.registerHttpListener(self)
        self.gui = RequestViewerGUI(self.helpers)

        aes_cipher = AESECB(192)
        plaintext = "Hello world"
        print("Plaintext:", plaintext)

        # Encrypt
        ciphertext = aes_cipher.encrypt(plaintext)
	print("Ciphertext: {}".format(str(ciphertext)))

        # Decrypt
        decrypted_text = aes_cipher.decrypt(ciphertext)
	print("Decrypted: {}".format(str(decrypted_text)))

    def processHttpMessage(self, toolFlag, messageIsRequest, message):
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

                print("Response received:")
                print(self.helpers.bytesToString(response).encode('ascii', 'ignore').decode('ascii'))

    def waitForEncryptButtonPress(self):
        while True:
            if self.gui.isEncryptButtonPressed():
                self.gui.resetEncryptButton()
                break
            else:
                time.sleep(1)

    def unRegisterExtenderCallbacks(self, callbacks):
        callbacks.unregisterHttpListener(self)
