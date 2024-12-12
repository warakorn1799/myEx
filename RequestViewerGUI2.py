from javax.swing import JFrame, JPanel, JTextArea, JScrollPane, JLabel, JTextField, JComboBox, JButton, JToggleButton
from java.awt import BorderLayout, Color, Dimension, FlowLayout, Font
from javax.swing.border import EmptyBorder
import time

class RequestViewerGUI:
    def __init__(self, helpers):
        self.helpers = helpers
        self.initialize_gui()
        self.updatedRequest = None
        self.message = None
        self.encryptButtonPressed = False

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

        dropdown = JComboBox(["AES", "RSA", "ECC"])
        dropdown.setFont(font)

        panel_bottom_left.add(label_input)
        panel_bottom_left.add(text_field)
        panel_bottom_left.add(label_dropdown)
        panel_bottom_left.add(dropdown)

        panel_bottom_right = JPanel()
        panel_bottom_right.setLayout(FlowLayout(FlowLayout.RIGHT, 10, 10))
        panel_bottom_right.setBackground(Color.GRAY)

        button2 = JButton("Encrypt")
        button1 = JToggleButton("Decrypt off")

        button2.addActionListener(lambda e: self.encrypt_action(text_field, dropdown))
        button1.addActionListener(lambda e: self.decrypt_action(button1, text_field, dropdown))

        panel_bottom_right.add(button1)
        panel_bottom_right.add(button2)

        panel_bottom.add(panel_bottom_left, BorderLayout.WEST)
        panel_bottom.add(panel_bottom_right, BorderLayout.EAST)

        self.frame.add(panel_top, BorderLayout.NORTH)
        self.frame.add(panel_middle, BorderLayout.CENTER)
        self.frame.add(panel_bottom, BorderLayout.SOUTH)

        self.frame.setVisible(True)

    def isEncryptButtonPressed(self):
        return self.encryptButtonPressed

    def resetEncryptButton(self):
        self.encryptButtonPressed = False
        
    def encrypt_action(self, text_field, dropdown):
        if self.updatedRequest and self.message:
            self.message.setRequest(self.updatedRequest)
            print("Updated request sent:")
            print(self.helpers.bytesToString(self.updatedRequest))
            self.encryptButtonPressed = True 
        else:
            print("No updated request available to send.")

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

        header.add("Origin: www.example.com")

        self.updatedRequest = self.helpers.buildHttpMessage(header, body)
        self.message = message
        #time.sleep(300)
        # self.message.setRequest(self.updatedRequest)
        print("setRequestData Done")
