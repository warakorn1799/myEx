from javax.swing import JFrame, JPanel, JTextArea, JScrollPane, JLabel, JTextField, JComboBox, JButton, JToggleButton
from java.awt import BorderLayout, Color, Dimension, FlowLayout, Font
from javax.swing.border import EmptyBorder
import time
from EncryptGUI import EncryptGUI

class RequestViewerGUI:
    def __init__(self, helpers):
        self.helpers = helpers
        self.initialize_gui()
        self.updatedRequest = None
        self.message = None
        self.encryptButtonPressed = False
        self.header = None
        self.gui = EncryptGUI('', '', '', '', '')

    def initialize_gui(self):
        self.frame = JFrame("Request Details")
        self.frame.setSize(1000, 600)
        self.frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
        self.frame.setResizable(False)

        panel_top = JPanel()
        panel_top.setLayout(BorderLayout())
        panel_top.setBorder(EmptyBorder(10, 10, 10, 10))

        top_label = JLabel("Your Request")
        top_label.setFont(Font("Arial", Font.BOLD, 16)) 
        top_label.setForeground(Color.BLACK)
        top_label.setBorder(EmptyBorder(10, 0, 10, 0))
        panel_top.add(top_label, BorderLayout.NORTH)

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

        panel_bottom = JPanel()
        panel_bottom.setLayout(BorderLayout())
        panel_bottom.setBackground(Color.GRAY)
        panel_bottom.setBorder(EmptyBorder(10, 10, 10, 10))
        panel_bottom.setPreferredSize(Dimension(1000, 80))

        self.panel_bottom_left = JPanel()
        self.panel_bottom_left.setLayout(FlowLayout(FlowLayout.LEFT, 10, 10))
        self.panel_bottom_left.setBackground(Color.GRAY)

        font = Font("Arial", Font.PLAIN, 14)

        label_input = JLabel("KEY")
        label_input.setFont(font)
        label_input.setForeground(Color.WHITE)

        text_field = JTextField(30)
        text_field.setFont(font)

        label_dropdown = JLabel("Select an Algorithm")
        label_dropdown.setFont(font)
        label_dropdown.setForeground(Color.WHITE)

        dropdown = JComboBox(["RSA", "AES(CBC)", "AES(CFB)", "AES(GCM)"])
        dropdown.setFont(font)
        dropdown.addActionListener(lambda e: self.onSelection(e))

        self.panel_bottom_left.add(label_input)
        self.panel_bottom_left.add(text_field)
        self.panel_bottom_left.add(label_dropdown)
        self.panel_bottom_left.add(dropdown)

        panel_bottom_right = JPanel()
        panel_bottom_right.setLayout(FlowLayout(FlowLayout.RIGHT, 10, 10))
        panel_bottom_right.setBackground(Color.GRAY)

        button2 = JButton("Encrypt")
        button1 = JToggleButton("Decrypt off")

        button2.addActionListener(lambda e: self.encrypt_action(text_field, dropdown))
        button1.addActionListener(lambda e: self.decrypt_action(button1, text_field, dropdown))

        panel_bottom_right.add(button1)
        panel_bottom_right.add(button2)

        panel_bottom.add(self.panel_bottom_left, BorderLayout.WEST)
        panel_bottom.add(panel_bottom_right, BorderLayout.EAST)

        self.frame.add(panel_top, BorderLayout.NORTH)
        self.frame.add(panel_middle, BorderLayout.CENTER)
        self.frame.add(panel_bottom, BorderLayout.SOUTH)

        self.frame.setVisible(True)
	
        self.font = Font("Arial", Font.PLAIN, 14)

    def onSelection(self, event):
        dropdown = event.getSource()
        selectedItem = dropdown.getSelectedItem()
        print("Algorithm selected:", selectedItem)

        if selectedItem == "AES(CBC)":
            labelIV = JLabel("IV")
            labelIV.setFont(self.font)
            labelIV.setForeground(Color.WHITE)

            text_field2 = JTextField(30)
            text_field2.setFont(self.font)

            self.panel_bottom_left.add(labelIV)
            self.panel_bottom_left.add(text_field2)
        else:
            if labelIV and text_field2:
                self.panel_bottom_left.remove(labelIV)
                self.panel_bottom_left.remove(text_field2)

            self.panel_bottom_left.revalidate()
            self.panel_bottom_left.repaint()

    def isEncryptButtonPressed(self):
        while True:
            if self.gui.isSendButtonPressed():
                self.gui.resetSendButton()
                return True
            else:
                time.sleep(1)

    def resetEncryptButton(self):
        self.encryptButtonPressed = False

    def encrypt_action(self, text_field, dropdown):
        if self.updatedRequest and self.message:
            self.gui = EncryptGUI(self.helpers, self.message, self.updatedRequest, self.header, self.body)
            self.gui.start()
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
            else:
                print("0")
                button.setText("Decrypt off")
                button.setSelected(False)

    def setRequestData(self, header, body, message):
        request_data = "\n".join(header) + "\n\n" + body
        self.text_area1.setText(request_data)

        self.header = header
        self.body = body
        header.add("Origin: www.example.com")

        self.updatedRequest = self.helpers.buildHttpMessage(header, body)
        self.message = message
