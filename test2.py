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
        
        from EncryptDecrypt import AESECB, AESCBC, AESGCM, RSA
        rsa = RSA()
        
        private_key_base64 = "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7UeHP17+W7KUx9NsFt2rPzItAkrMVkZ3xuVfZdOVI26o73E70Ft9Q0rPnugRyNMDGNVuWeT6Nr0+iJ9a4I5ZsYXpwffubrJBPvO/B/X3vUr0jtMOEqWbIx/Yo2EtfwxF3r74PfGp0n7jwqzebjujWV2Yy9xL6Q5ZN62Gsm52ftOob7a+ypfaFGqm3HSHCBoFjkHO/RaIEGM4phk84YR3BoaYbuaz3gVf7F0oOQ8WR6kwuhgFplGpOVd/JA++mjsLS7OKvzzl2gc1Tqv65su0ggrht9F5nUdP6ICOwAnTVUS2uYRTwzuCu5gR4ac1qa5MatyjHk4KQJ6QzIUW5Th8BAgMBAAECggEALnqnSsCwZ90JMmecrwLvbGdHCDs+V3Q92hxQqYMBX34t89N6/cLtH2tgu3djIgln6eaUdrZX6KUe38/9zcv6x6K6VE5WT67WUgrB/QMOrAL+Lm1sdC7qc5h2QnVE4pqO64E+ai5HZe+53nHFhwJDUOf30l6PJWz+zw/AOSmVx2oaW7V3TygNvuF24PqyQsIuM8wtK/vkAjxy95Agg2PkuWk1PK3wcJ2u9+ed+Ghe6R05s+0Vpr8U0rR8HsuA8uYy9MTXDh5LmKBMYsk0KZD/C/RVkwiCbfzMYWvwG3sGanTp8wg/rk72Ld3NWIhvmsBG4+3idWCVjASUVdWibj8JyQKBgQDeHNqLqh7UbKbK4UV06j2wLsl5OWfVxd2z9fFEO6HnHawianJoehygdztQgxZSECW3SQ9IjDsQeGhbyRC0nA2OnQ55yGL2DOyPZM622c6S0MkgbudL9+sC0ReACzIIxxiy07oh2mSbe7u7qyAJfyKvzjAIaJI3dp9g+RlEUb5BPQKBgQDX5hwPB9ZcIczsP74S4UU1dL/pHeiQ4hrv0mqvm8X5Hv1F841qR4ETdX4ibVT121N1GgAhkG0vhcrmcUGcFqXa8SGoUvq7P0Srqo8whh3h+Zc0DknnBE7r827FAwIvuM+uo/2H9SH+6VECEpE+Lo4fQHTr+asoiPcL3GbqAUApFQKBgDUl7l2xLYNjJF4znW0mh/BaobcyN1h96lkfpsXPByTIguIRWqMJZUQ4g6b2Vyb32i6Leu6/L3r3dPFRoX+2P8A6cLZPbu61lP2S/6vdXoLfFuF96DbTchbQdbEb/LMBATX5V/a1zZEvAHMdtaLQGzq6OeApNaOz7NtFf/hLHx15AoGAHCFMSJ0RzgFNbP7FKjqVxOhIVPxjn/UF43d8FRNr0RC7mVCpfU6Bv+JQI/Yw2rPQBPL1T2o8/7MkA7CABvFgfM1sQD1Hk/wjW2amr4DaBeZ6T/sIoAQMsGuQZDUHJOakkLGnR/6lhkwqFOYMbJiuRd4lHdXy+h4WakI2Woj9Lh0CgYEAkBav3k+8+AwzNVqoEXK57XnuupOg+InOX3fL4PMBlCxeSNsLIGRTQ/rGk2i9RfQKEOyHI8o2tZBgBDia5Ph3TMamrEv0VbGf/SuObPghpNYTuj0Z9QrEwYnUWvDqT+1Agrsqzb11bAF6NaBRY3ZoN8N9JYJOZGhlbTqU59olGBI="  
        public_key_base64 = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAu1Hhz9e/luylMfTbBbdqz8yLQJKzFZGd8blX2XTlSNuqO9xO9BbfUNKz57oEcjTAxjVblnk+ja9PoifWuCOWbGF6cH37m6yQT7zvwf1971K9I7TDhKlmyMf2KNhLX8MRd6++D3xqdJ+48Ks3m47o1ldmMvcS+kOWTethrJudn7TqG+2vsqX2hRqptx0hwgaBY5Bzv0WiBBjOKYZPOGEdwaGmG7ms94FX+xdKDkPFkepMLoYBaZRqTlXfyQPvpo7C0uzir885doHNU6r+ubLtIIK4bfReZ1HT+iAjsAJ01VEtrmEU8M7gruYEeGnNamuTGrcox5OCkCekMyFFuU4fAQIDAQAB"  
        plaintext = "id=B6403348"

        public_key = rsa.load_public_key_from_base64(public_key_base64)
        private_key = rsa.load_private_key_from_base64(private_key_base64)
        #print(private_key_base64)

        ciphertext = rsa.encryptRAW(public_key, plaintext)
        decrypted_text = rsa.decryptRAW(private_key, ciphertext)
        #print("cipher:",ciphertext)
        #print("decrypt:",decrypted_text)
        

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