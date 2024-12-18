from javax.swing import JFrame, JPanel, JTextArea, JScrollPane, JLabel, JTextField, JComboBox, JButton, JToggleButton
from java.awt import BorderLayout, Color, Dimension, FlowLayout, Font
from javax.swing.border import EmptyBorder
import time
from EncryptGUI import EncryptGUI
from EncryptDecrypt import AESECB, AESCBC, AESGCM

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
        self.gui = EncryptGUI('', '', '', '', '')

    def initialize_gui(self):
        self.frame = JFrame("Request Details")
        self.frame.setSize(1000, 600)
        self.frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
        self.frame.setResizable(True)

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

        text_field = JTextField(30)
        text_field.setFont(font)

        label_dropdown = JLabel("Select an Algorithm")
        label_dropdown.setFont(font)
        label_dropdown.setForeground(Color.WHITE)

        dropdown = JComboBox(["RSA", "AES(ECB)", "AES(CBC)", "AES(GCM)"])
        dropdown.setFont(font)
        dropdown.addActionListener(lambda e: self.onSelection(e))

        panel_bottom_left.add(label_input)
        panel_bottom_left.add(text_field)
        panel_bottom_left.add(label_dropdown)
        panel_bottom_left.add(dropdown)

        panel_bottom_right = JPanel()
        panel_bottom_right.setLayout(FlowLayout(FlowLayout.RIGHT, 10, 10))
        panel_bottom_right.setBackground(Color.GRAY)

        button2 = JButton("Encrypt/Send")
        button1 = JToggleButton("Decrypt off")

        button2.addActionListener(lambda e: self.encrypt_action(text_field, dropdown))
        button1.addActionListener(lambda e: self.decrypt_action(button1, text_field, dropdown))

        panel_bottom_right.add(button1)
        panel_bottom_right.add(button2)

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

        label_me = JLabel("IV")
        label_me.setFont(font)
        label_me.setForeground(Color.WHITE)

        self.text_field2 = JTextField(30)
        self.text_field2.setFont(font)
        self.text_field2.setEnabled(False)
        self.text_field2.setBackground(Color.LIGHT_GRAY)

        panel_bottom_label.add(label_me)
        panel_bottom_label.add(self.text_field2)

        panel_bottom.add(panel_bottom_label, BorderLayout.SOUTH)

        self.frame.add(panel_top, BorderLayout.NORTH)
        self.frame.add(panel_middle, BorderLayout.CENTER)
        self.frame.add(panel_bottom, BorderLayout.SOUTH)

        self.frame.setVisible(True)

    def onSelection(self, event):
        dropdown = event.getSource()
        selectedItem = dropdown.getSelectedItem()
        print("Algorithm selected:", selectedItem)

        if selectedItem == "AES(CBC)" or selectedItem == "AES(GCM)":
            self.text_field2.setEnabled(True)
            self.text_field2.setBackground(Color.WHITE)
        else:
            self.text_field2.setEnabled(False)
            self.text_field2.setBackground(Color.LIGHT_GRAY)

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

    def encrypt_action(self, text_field, dropdown):
        if self.updatedRequest and self.message:
            self.gui = EncryptGUI(self.helpers, self.message, self.updatedRequest, self.header, self.body)
            self.gui.start()
	    self.updatedRequest= None
	    self.message = None
	elif self.updatedResponse and self.response:
            self.encryptButtonPressed = True
        else:
            from javax.swing import JOptionPane
            JOptionPane.showMessageDialog(
                None,
                "No Request data found. Please ensure a request is selected or available.",
                "Error",
                JOptionPane.ERROR_MESSAGE
            )

    def decrypt_action(self, button, text_field, dropdown):
        if text_field.getText() == "":
            print("0")
            if button.isSelected():
                button.setSelected(False)
                button.setText("Decrypt off")
        else:
            if button.isSelected():
                print("1")
                button.setText("Decrypt on")
                button.setSelected(True)

        	selectedItem = dropdown.getSelectedItem()
		if selectedItem == "AES(CBC)":
		    key = "zM56kZa2aF43jHIaOLEiNGDp0Yj1V1QD"
                    iv = "mZ3B9oXMbNDf7mmMZOHckw=="
                    plaintext = "Hello World"

                    aes = AESCBC()

                    ciphertext = aes.encrypt(plaintext, key, iv)
                    print("Encrypted:", ciphertext)

                    decrypted_text = aes.decrypt(ciphertext, key, iv)
                    print("Decrypted:", decrypted_text) 
            else:
                print("0")
                button.setText("Decrypt off")
                button.setSelected(False)

    def setRequestData(self, header, body, message):
        request_data = "\n".join(header) + "\n\n" + body
	request_data = (self.helpers.bytesToString(request_data).encode('ascii', 'ignore').decode('ascii'))
        self.text_area1.setText(request_data)

	self.top_label.setText("Your Request")

        self.header = header
        self.body = body
        header.add("Origin: www.example.com")

        self.updatedRequest = self.helpers.buildHttpMessage(header, body)
        self.message = message

    def setResponseData(self, header, body, response):
	response_data = "\n".join(header).encode('utf-8', 'ignore').decode('utf-8') + "\n\n" + body.encode('utf-8', 'ignore').decode('utf-8')
	response_data = (self.helpers.bytesToString(response_data).encode('ascii', 'ignore').decode('ascii'))
        self.text_area1.setText(response_data)

	self.top_label.setText("Your Response")

        self.header = header
        self.body = body

        self.updatedResponse = self.helpers.buildHttpMessage(header, body)
        self.response = response
