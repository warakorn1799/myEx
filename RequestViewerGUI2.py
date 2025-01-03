from java.lang import IllegalArgumentException
from javax.crypto import Cipher, BadPaddingException, IllegalBlockSizeException
from java.security import InvalidKeyException
from javax.swing import JFrame, JPanel, JTextArea, JScrollPane, JLabel, JTextField, JComboBox, JButton, JToggleButton, JOptionPane
from java.awt import BorderLayout, Color, Dimension, FlowLayout, Font
from javax.swing.border import EmptyBorder
from java.util import ArrayList
from java.util import Base64
import time
import re
from EncryptGUI import EncryptGUI
from EncryptDecrypt import AESECB, AESCBC, AESGCM, RSA
from java.awt.event import KeyEvent, KeyListener

class PlaceholderDocument(KeyListener):
    def __init__(self, textField, placeholder):
        self.textField = textField
        self.placeholder = placeholder
        self.isPlaceholder = True
        self.textField.addKeyListener(self)

    def keyPressed(self, event):
        if event.getKeyCode() != KeyEvent.VK_ENTER and self.isPlaceholder:
            self.textField.setText('')
            self.textField.setForeground(Color.BLACK)
            self.isPlaceholder = False

    def keyReleased(self, event):
        if not self.textField.getText():
            self.textField.setText(self.placeholder)
            self.textField.setForeground(Color.GRAY)
            self.isPlaceholder = True

    def keyTyped(self, event):
        pass
    
class RequestViewerGUI:
    def __init__(self, helpers):
        self.helpers = helpers
        self.initialize_gui()
        self.updatedRequest = None
        self.updatedResponse = None
        self.message = None
        self.response = None
        self.sendButtonPressed = False
        self.encryptButtonPressed = False
        self.header = None
        self.decryptOn = False
        self.algorithm = "RSA"
        self.key = None
        self.EncryptKey = None
        self.iv = None
        self.reqData = None
        self.resData = None
        self.rsaPadding = "RAW"
        self.gui = EncryptGUI('', '', '', '', '')

    def initialize_gui(self):
        self.frame = JFrame("Request Details")
        self.frame.setExtendedState(JFrame.MAXIMIZED_BOTH)
        self.frame.setSize(1400, 800)
        self.frame.setResizable(False)

        panel_top = JPanel()
        panel_top.setLayout(BorderLayout())
        panel_top.setBorder(EmptyBorder(10, 10, 10, 10))

        self.top_label = JLabel("Your Request")
        self.top_label.setFont(Font("Arial", Font.BOLD, 16))
        self.top_label.setForeground(Color.BLACK)
        self.top_label.setBorder(EmptyBorder(10, 0, 10, 0))
        panel_top.add(self.top_label, BorderLayout.NORTH)

        self.text_area1 = JTextArea()
        self.text_area1.setEditable(False)
        self.text_area1.setText("--None--")
        scroll_pane1 = JScrollPane(self.text_area1)
        panel_top.add(scroll_pane1, BorderLayout.CENTER)
        panel_top.setPreferredSize(Dimension(1500, 260))

        panel_middle = JPanel()
        panel_middle.setLayout(BorderLayout())
        panel_middle.setBorder(EmptyBorder(10, 10, 10, 10))

        self.text_area2 = JTextArea()
        self.text_area2.setEditable(True)
        self.text_area2.setText("--None--")
        scroll_pane2 = JScrollPane(self.text_area2)
        panel_middle.add(scroll_pane2, BorderLayout.CENTER)
        panel_middle.setPreferredSize(Dimension(1500, 260))

        panel_bottom_left = JPanel()
        panel_bottom_left.setLayout(FlowLayout(FlowLayout.LEFT, 10, 10))
        panel_bottom_left.setBackground(Color.GRAY)

        font = Font("Arial", Font.PLAIN, 14)

        label_input = JLabel("KEY")
        label_input.setFont(font)
        label_input.setForeground(Color.WHITE)
	
        self.keyField = JTextField(30)
        self.keyField.setFont(font)
        self.keyField.setText('key must be Base64 for AES and RSA (PEM)')
        self.keyField.setForeground(Color.GRAY)

        label_pri = JLabel("Encrypt KEY")
        label_pri.setFont(font)
        label_pri.setForeground(Color.WHITE)
        
        self.pri_field = JTextField(30)
        self.pri_field.setFont(font)

        panel_bottom_left.add(label_input)
        panel_bottom_left.add(self.keyField)
        panel_bottom_left.add(label_pri)
        panel_bottom_left.add(self.pri_field)

        panel_bottom_right = JPanel()
        panel_bottom_right.setLayout(FlowLayout(FlowLayout.RIGHT, 10, 10))
        panel_bottom_right.setBackground(Color.GRAY)

        button_encrypt = JButton("Encrypt/Send")
        button_decrypt = JToggleButton("Decrypt off")

        button_encrypt.addActionListener(lambda e: self.encrypt_action(self.keyField, self.dropdown))
        button_decrypt.addActionListener(lambda e: self.decrypt_action(button_decrypt, self.keyField, self.dropdown))

        panel_bottom_right.add(button_decrypt)
        panel_bottom_right.add(button_encrypt)

        panel_bottom = JPanel()
        panel_bottom.setLayout(BorderLayout())
        panel_bottom.setBackground(Color.GRAY)
        panel_bottom.setBorder(EmptyBorder(10, 10, 10, 10))
        panel_bottom.setPreferredSize(Dimension(1000, 80))

        panel_bottom.add(panel_bottom_left, BorderLayout.WEST)
        panel_bottom.add(panel_bottom_right, BorderLayout.EAST)

        panel_bottom_label = JPanel()
        panel_bottom_label.setLayout(FlowLayout(FlowLayout.LEFT, 18, 0))
        panel_bottom_label.setBackground(None)

        label_iv = JLabel("IV")
        label_iv.setFont(font)
        label_iv.setForeground(Color.WHITE)

        self.text_field2 = JTextField(30)
        self.text_field2.setFont(font)
        self.text_field2.setEnabled(False)
        self.text_field2.setBackground(Color.LIGHT_GRAY)

        label_encryption_scheme = JLabel("Padding Schemes")
        label_encryption_scheme.setFont(font)
        label_encryption_scheme.setForeground(Color.WHITE)
	
        label_dropdown = JLabel("Select an Algorithm")
        label_dropdown.setFont(font)
        label_dropdown.setForeground(Color.WHITE)

        self.dropdown = JComboBox(["RSA", "AES(ECB)", "AES(CBC)", "AES(GCM)"])
        self.dropdown.setFont(font)
        self.dropdown.addActionListener(lambda e: self.onSelection(e))

        self.dropdown_encryption_scheme = JComboBox(["RAW", "RAES-PKCS1-V1_5", "RSA-OAEP(SHA-256)", "RSA-OAEP(SHA-384)","RSA-OAEP(SHA-512)"])
        self.dropdown_encryption_scheme.setFont(font)
        self.dropdown_encryption_scheme.addActionListener(lambda e: self.onSelectionScheme(e))

        panel_bottom_label.add(label_iv)
        panel_bottom_label.add(self.text_field2)
        panel_bottom_label.add(label_dropdown)
        panel_bottom_label.add(self.dropdown)
        panel_bottom_label.add(label_encryption_scheme)
        panel_bottom_label.add(self.dropdown_encryption_scheme)
	
        panel_bottom.add(panel_bottom_label, BorderLayout.SOUTH)

        self.frame.add(panel_top, BorderLayout.NORTH)
        self.frame.add(panel_middle, BorderLayout.CENTER)
        self.frame.add(panel_bottom, BorderLayout.SOUTH)
        self.frame.setVisible(True)
        
        self.keyField.addKeyListener(PlaceholderDocument(self.keyField, "key must be Base64 for AES and RSA (PEM)."))

    def onSelection(self, event):
        #dropdown = event.getSource()
        selectedItem = self.dropdown.getSelectedItem()
        self.algorithm = selectedItem
        if selectedItem == "AES(CBC)" or selectedItem == "AES(GCM)":
            self.keyField.setEnabled(True)
            self.keyField.setBackground(Color.WHITE)
            self.text_field2.setEnabled(True)
            self.text_field2.setBackground(Color.WHITE)
            self.pri_field.setEnabled(False)
            self.pri_field.setBackground(Color.LIGHT_GRAY)
            self.dropdown_encryption_scheme.setEnabled(False)
            self.dropdown.setEnabled(True)
        elif selectedItem == "RSA":
            self.keyField.setEnabled(True)
            self.keyField.setBackground(Color.WHITE)
            self.text_field2.setEnabled(False)
            self.text_field2.setBackground(Color.LIGHT_GRAY)
            self.pri_field.setEnabled(True)
            self.pri_field.setBackground(Color.WHITE)
            self.dropdown_encryption_scheme.setEnabled(True)
            self.dropdown.setEnabled(True)
        else:
            self.keyField.setEnabled(True)
            self.keyField.setBackground(Color.WHITE)
            self.text_field2.setEnabled(False)
            self.text_field2.setBackground(Color.LIGHT_GRAY)
            self.pri_field.setEnabled(False)
            self.pri_field.setBackground(Color.LIGHT_GRAY)
            self.dropdown_encryption_scheme.setEnabled(False)
            self.dropdown.setEnabled(True)

    def onSelectionScheme(self, event):
        dropdown = event.getSource()
        selectedItem = dropdown.getSelectedItem()
        self.rsaPadding = selectedItem

    def isEncryptButtonPressed(self):
        while True:
            if self.gui.isSendButtonPressed():
                self.gui.resetSendButton()
                return True
            else:
                time.sleep(1)

    def resetSendButton(self):
        self.encryptButtonPressed = False

    def isSendButtonPressed(self):
        return self.encryptButtonPressed

    def resetEncryptButton(self):
        self.encryptButtonPressed = False

    def encrypt_action(self, keyField, dropdown):
        if self.updatedRequest and self.message:
            requestDecrypt = self.text_area2.getText()
            if "\n\n" in requestDecrypt:
                header, body = requestDecrypt.split("\n\n", 1)
            else:
                header = requestDecrypt
                body = ""

            header_array_list = ArrayList()
            for line in header.split("\n"):
                header_array_list.add(line)

            body_str = str(body)
            encrypted = body_str
            if self.decryptOn:
                try:
                    if self.algorithm == "AES(ECB)":
                        aes = AESECB()
                        encrypted = aes.encrypt(body_str, self.key)
                    elif self.algorithm == "AES(CBC)":
                        aes = AESCBC()
                        encrypted = aes.encrypt(body_str, self.key, self.iv)
                    elif self.algorithm == "AES(GCM)":
                        aes = AESGCM()
                        encrypted = aes.encrypt(body_str, self.key, self.iv)
                    elif self.algorithm == "RSA":
                        if self.rsaPadding == "RAW":
                            rsa = RSA()
                            self.EncryptKey = re.sub(r'\s+', '', self.EncryptKey)
                            try:
                                Base64.getDecoder().decode(self.EncryptKey)
                            except Exception as e:
                                JOptionPane.showMessageDialog(
                                    None,
                                    "Can't encrypt maybe key is incorrect",
                                    "Error",
                                    JOptionPane.ERROR_MESSAGE
                                )
                                return
                            public_key_base64 = self.EncryptKey
                            public_key = rsa.load_public_key_from_base64(public_key_base64)
                            encrypted = rsa.encryptRAW(public_key, body)
                        elif self.rsaPadding == "RAES-PKCS1-V1_5":
                            rsa = RSA()
                            self.EncryptKey = re.sub(r'\s+', '', self.EncryptKey)
                            try:
                                Base64.getDecoder().decode(self.EncryptKey)
                            except Exception as e:
                                JOptionPane.showMessageDialog(
                                    None,
                                    "Can't encrypt maybe key is incorrect",
                                    "Error",
                                    JOptionPane.ERROR_MESSAGE
                                )
                                return
                            public_key_base64 = self.EncryptKey
                            public_key = rsa.load_public_key_from_base64(public_key_base64)
                            encrypted = rsa.encryptPKCS1(public_key, body)
                        elif self.rsaPadding == "RSA-OAEP(SHA-256)":
                            rsa = RSA()
                            self.EncryptKey = re.sub(r'\s+', '', self.EncryptKey)
                            try:
                                Base64.getDecoder().decode(self.EncryptKey)
                            except Exception as e:
                                JOptionPane.showMessageDialog(
                                    None,
                                    "Can't encrypt maybe key is incorrect",
                                    "Error",
                                    JOptionPane.ERROR_MESSAGE
                                )
                                return
                            public_key_base64 = self.EncryptKey
                            public_key = rsa.load_public_key_from_base64(public_key_base64)
                            encrypted = rsa.encryptOAEP_SHA256(public_key, body)
                        elif self.rsaPadding == "RSA-OAEP(SHA-384)":
                            rsa = RSA()
                            self.EncryptKey = re.sub(r'\s+', '', self.EncryptKey)
                            try:
                                Base64.getDecoder().decode(self.EncryptKey)
                            except Exception as e:
                                JOptionPane.showMessageDialog(
                                    None,
                                    "Can't encrypt maybe key is incorrect",
                                    "Error",
                                    JOptionPane.ERROR_MESSAGE
                                )
                                return
                            public_key_base64 = self.EncryptKey
                            public_key = rsa.load_public_key_from_base64(public_key_base64)
                            encrypted = rsa.encryptOAEP_SHA384(public_key, body)
                        elif self.rsaPadding == "RSA-OAEP(SHA-512)":
                            rsa = RSA()
                            self.EncryptKey = re.sub(r'\s+', '', self.EncryptKey)
                            try:
                                Base64.getDecoder().decode(self.EncryptKey)
                            except Exception as e:
                                JOptionPane.showMessageDialog(
                                    None,
                                    "Can't encrypt maybe key is incorrect",
                                    "Error",
                                    JOptionPane.ERROR_MESSAGE
                                )
                                return
                            public_key_base64 = self.EncryptKey
                            public_key = rsa.load_public_key_from_base64(public_key_base64)
                            encrypted = rsa.encryptOAEP_SHA512(public_key, body)
                except (IllegalBlockSizeException, BadPaddingException, InvalidKeyException, Exception) as e:
                    self.updatedRequest = self.helpers.buildHttpMessage(self.header, self.body)
                    self.gui = EncryptGUI(self.helpers, self.message, self.updatedRequest, self.header, self.body)

                self.updatedRequest = self.helpers.buildHttpMessage(header_array_list, encrypted)
                self.gui = EncryptGUI(self.helpers, self.message, self.updatedRequest, header, encrypted)
            else:
                self.updatedRequest = self.helpers.buildHttpMessage(self.header, self.body)
                self.gui = EncryptGUI(self.helpers, self.message, self.updatedRequest, self.header, self.body)

            self.gui.start()
            if self.gui.isCloseButtonPressed():
                pass
            else:
                self.updatedRequest = None
                self.message = None
                self.reqData = None
                self.resData = None
                self.text_area1.setText("--None--")
                self.text_area2.setText("--None--")
        elif self.updatedResponse and self.response:
            self.encryptButtonPressed = True
            self.updatedResponse = None
            self.reqData = None
            self.resData = None
            self.response = None
            self.text_area1.setText("--None--")
            self.text_area2.setText("--None--")
        else:
            JOptionPane.showMessageDialog(
                None,
                "No Request data found. Please ensure a request is selected or available.",
                "Error",
                JOptionPane.ERROR_MESSAGE
            )

    def decrypt_action(self, button, keyField, dropdown):
        selectedItem = dropdown.getSelectedItem()
        self.key = keyField.getText()
        self.EncryptKey = self.pri_field.getText()
        self.iv = self.text_field2.getText()
        if keyField.getText() == "":
            if button.isSelected():
                button.setSelected(False)
                button.setText("Decrypt off")
                self.decryptOn = False
        elif len(keyField.getText()) not in [16, 24, 32] and (selectedItem == "AES(CBC)" or selectedItem == "AES(GCM)" or selectedItem == "AES(ECB)"):
            JOptionPane.showMessageDialog(
                None,
                "Key must be 16 or 24 or 32 bytes",
                "WARNING",
                JOptionPane.WARNING_MESSAGE
            )
        elif len(self.text_field2.getText()) != 16 and (selectedItem == "AES(CBC)" or selectedItem == "AES(GCM)"):
            JOptionPane.showMessageDialog(
                None,
                "IV must be 16 bytes",
                "WARNING",
                JOptionPane.WARNING_MESSAGE
            )
        else:
            if button.isSelected():
                button.setText("Decrypt on")
                button.setSelected(True)
                self.decryptOn = True
                
                self.keyField.setEnabled(False)
                self.keyField.setBackground(Color.LIGHT_GRAY)
                self.text_field2.setEnabled(False)
                self.text_field2.setBackground(Color.LIGHT_GRAY)
                self.pri_field.setEnabled(False)
                self.pri_field.setBackground(Color.LIGHT_GRAY)
                self.dropdown_encryption_scheme.setEnabled(False)
                self.dropdown.setEnabled(False)
                if self.message is not None or self.response is not None:
                    if self.message is None:
                        self.setResponseData(self.header, self.body, self.response)
                    if self.response is None:
                        self.setRequestData(self.header, self.body, self.message)

            else:
                button.setText("Decrypt off")
                selectedItem = dropdown.getSelectedItem()
                self.onSelection(dropdown)
                button.setSelected(False)
                self.decryptOn = False
                self.text_area2.setText("--None--")

    def setRequestData(self, header, body, message):
        request_data = "\n".join(header) + "\n\n" + body
        request_data = self.helpers.bytesToString(request_data).encode('ascii', 'ignore').decode('ascii')
        self.text_area1.setText(request_data)

        self.top_label.setText("Your Request")

        self.header = header
        self.body = body

        self.updatedRequest = self.helpers.buildHttpMessage(header, body)
        self.message = message
	
        if self.decryptOn:
            try:
                if self.algorithm == "AES(ECB)":
                    aes = AESECB()
                    decrypted_text = aes.decrypt(body, self.key)
                    decrypted_data2 = "\n".join(header) + "\n\n" + decrypted_text
                    decrypted_data2 = self.helpers.bytesToString(decrypted_data2).encode('ascii', 'ignore').decode('ascii')
                elif self.algorithm == "AES(CBC)":
                    aes = AESCBC()
                    decrypted_text = aes.decrypt(body, self.key, self.iv)
                    decrypted_data2 = "\n".join(header) + "\n\n" + decrypted_text
                    decrypted_data2 = self.helpers.bytesToString(decrypted_data2).encode('ascii', 'ignore').decode('ascii')
                elif self.algorithm == "AES(GCM)":
                    aes = AESGCM()
                    decrypted_text = aes.decrypt(body, self.key, self.iv)
                    decrypted_data2 = "\n".join(header) + "\n\n" + decrypted_text
                    decrypted_data2 = self.helpers.bytesToString(decrypted_data2).encode('ascii', 'ignore').decode('ascii')
                elif self.algorithm == "RSA":
                    rsa = RSA()
                    self.key = re.sub(r'\s+', '', self.key)
                    private_key_base64 = self.key

                    try:
                        Base64.getDecoder().decode(private_key_base64)
                    except Exception as e:
                        decrypted_data2 = request_data
                        self.text_area2.setText(decrypted_data2)
                        return

                    private_key = rsa.load_private_key_from_base64(private_key_base64)

                    if self.rsaPadding == "RAW":
                        decrypted_text = rsa.decryptRAW(private_key, body)
                    elif self.rsaPadding == "RAES-PKCS1-V1_5":
                        decrypted_text = rsa.decryptPKCS1(private_key, body)
                    elif self.rsaPadding == "RSA-OAEP(SHA-256)":
                        decrypted_text = rsa.decryptOAEP_SHA256(private_key, body)
                    elif self.rsaPadding == "RSA-OAEP(SHA-384)":
                        decrypted_text = rsa.decryptOAEP_SHA384(private_key, body)
                    elif self.rsaPadding == "RSA-OAEP(SHA-512)":
                        decrypted_text = rsa.decryptOAEP_SHA512(private_key, body)

                    decrypted_data2 = "\n".join(header) + "\n\n" + decrypted_text
                    decrypted_data2 = self.helpers.bytesToString(decrypted_data2).encode('ascii', 'ignore').decode('ascii')

            except (IllegalArgumentException, IllegalBlockSizeException, BadPaddingException, InvalidKeyException, Exception) as e:
                decrypted_data2 = request_data

            self.text_area2.setText(decrypted_data2)


    def setResponseData(self, header, body, response):
        response_data = (
            "\n".join(header).encode("utf-8", "ignore").decode("utf-8")
            + "\n\n"
            + body.encode("utf-8", "ignore").decode("utf-8")
        )
        response_data = (
            self.helpers.bytesToString(response_data)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
        self.text_area1.setText(response_data)
        self.top_label.setText("Your Response")

        self.header = header
        self.body = body
        self.updatedResponse = self.helpers.buildHttpMessage(header, body)
        self.response = response

        if self.decryptOn:
            try:
                if self.algorithm == "AES(ECB)":
                    aes = AESECB()
                    decrypted_text = aes.decrypt(body, self.key)
                    decrypted_data2 = "\n".join(header) + "\n\n" + decrypted_text
                    decrypted_data2 = (self.helpers.bytesToString(decrypted_data2).encode("ascii", "ignore").decode("ascii"))
                elif self.algorithm == "AES(CBC)":
                    aes = AESCBC()
                    decrypted_text = aes.decrypt(body, self.key, self.iv)
                    decrypted_data2 = "\n".join(header) + "\n\n" + decrypted_text
                    decrypted_data2 = (self.helpers.bytesToString(decrypted_data2).encode("ascii", "ignore").decode("ascii"))
                elif self.algorithm == "AES(GCM)":
                    aes = AESGCM()
                    decrypted_text = aes.decrypt(body, self.key, self.iv)
                    decrypted_data2 = "\n".join(header) + "\n\n" + decrypted_text
                    decrypted_data2 = (self.helpers.bytesToString(decrypted_data2).encode("ascii", "ignore").decode("ascii"))
                elif self.algorithm == "RSA":
                    rsa = RSA()
                    self.key = re.sub(r'\s+', '', self.key)
                    private_key_base64 = self.key
                    private_key = rsa.load_private_key_from_base64(private_key_base64)

                    if self.rsaPadding == "RAW":
                        decrypted_text = rsa.decryptRAW(private_key, body)
                    elif self.rsaPadding == "RAES-PKCS1-V1_5":
                        decrypted_text = rsa.decryptPKCS1(private_key, body)
                    elif self.rsaPadding == "RSA-OAEP(SHA-256)":
                        decrypted_text = rsa.decryptOAEP_SHA256(private_key, body)
                    elif self.rsaPadding == "RSA-OAEP(SHA-384)":
                        decrypted_text = rsa.decryptOAEP_SHA384(private_key, body)
                    elif self.rsaPadding == "RSA-OAEP(SHA-512)":
                        decrypted_text = rsa.decryptOAEP_SHA512(private_key, body)

                    decrypted_data2 = "\n".join(header) + "\n\n" + decrypted_text
                    decrypted_data2 = (self.helpers.bytesToString(decrypted_data2).encode("ascii", "ignore").decode("ascii"))
            except (IllegalArgumentException, IllegalBlockSizeException, BadPaddingException, InvalidKeyException, Exception,) as e:
                decrypted_data2 = response_data
                
            self.text_area2.setText(decrypted_data2)
            self.resData = decrypted_data2



