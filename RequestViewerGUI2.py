from javax.swing import JFrame, JPanel, JTextArea, JScrollPane, JLabel, JTextField, JComboBox, JButton, JToggleButton, JOptionPane
from java.awt import BorderLayout, Color, Dimension, FlowLayout, Font
from javax.swing.border import EmptyBorder
from EncryptGUI import EncryptGUI
from EncryptDecrypt import AESECB, AESCBC, AESGCM


class RequestViewerGUI:
    def __init__(self, helpers):
        self.helpers = helpers
        self.updatedRequest = None
        self.updatedResponse = None
        self.message = None
        self.response = None
        self.sendButtonPressed = False
        self.encryptButtonPressed = False
        self.header = None
        self.decryptOn = False
        self.algorithm = None
        self.key = None
        self.iv = None
        self.gui = EncryptGUI('', '', '', '', '')
        self.initialize_gui()

    def initialize_gui(self):
        self.frame = JFrame("Request Details")
        self.frame.setExtendedState(JFrame.MAXIMIZED_BOTH)
        self.frame.setSize(1400, 800)
        self.frame.setResizable(False)

        panel_top = JPanel(BorderLayout())
        panel_top.setBorder(EmptyBorder(10, 10, 10, 10))

        self.top_label = JLabel("Your Request")
        self.top_label.setFont(Font("Arial", Font.BOLD, 16))
        self.top_label.setForeground(Color.BLACK)
        self.top_label.setBorder(EmptyBorder(10, 0, 10, 0))
        panel_top.add(self.top_label, BorderLayout.NORTH)

        self.text_area1 = JTextArea("--None--", editable=False)
        scroll_pane1 = JScrollPane(self.text_area1)
        panel_top.add(scroll_pane1, BorderLayout.CENTER)
        panel_top.setPreferredSize(Dimension(1500, 260))

        panel_middle = JPanel(BorderLayout())
        panel_middle.setBorder(EmptyBorder(10, 10, 10, 10))

        self.text_area2 = JTextArea("--None--", editable=True)
        scroll_pane2 = JScrollPane(self.text_area2)
        panel_middle.add(scroll_pane2, BorderLayout.CENTER)
        panel_middle.setPreferredSize(Dimension(1500, 260))

        panel_bottom_left = JPanel(FlowLayout(FlowLayout.LEFT, 10, 10))
        panel_bottom_left.setBackground(Color.GRAY)
        font = Font("Arial", Font.PLAIN, 14)

        label_key = JLabel("KEY")
        label_key.setFont(font)
        label_key.setForeground(Color.WHITE)

        text_field = JTextField(30)
        text_field.setFont(font)

        label_pri = JLabel("Encrypt KEY")
        label_pri.setFont(font)
        label_pri.setForeground(Color.WHITE)

        pri_field = JTextField(30)
        pri_field.setFont(font)

        panel_bottom_left.add(label_key)
        panel_bottom_left.add(text_field)
        panel_bottom_left.add(label_pri)
        panel_bottom_left.add(pri_field)

        panel_bottom_right = JPanel(FlowLayout(FlowLayout.RIGHT, 10, 10))
        panel_bottom_right.setBackground(Color.GRAY)

        button_encrypt = JButton("Encrypt/Send")
        button_decrypt = JToggleButton("Decrypt off")

        button_encrypt.addActionListener(lambda e: self.encrypt_action(text_field))
        button_decrypt.addActionListener(lambda e: self.decrypt_action(button_decrypt, text_field))

        panel_bottom_right.add(button_decrypt)
        panel_bottom_right.add(button_encrypt)

        panel_bottom = JPanel(BorderLayout())
        panel_bottom.setBackground(Color.GRAY)
        panel_bottom.setBorder(EmptyBorder(10, 10, 10, 10))
        panel_bottom.setPreferredSize(Dimension(1000, 80))

        panel_bottom.add(panel_bottom_left, BorderLayout.WEST)
        panel_bottom.add(panel_bottom_right, BorderLayout.EAST)

        panel_bottom_label = JPanel(FlowLayout(FlowLayout.LEFT, 18, 0))
        panel_bottom_label.setBackground(None)

        label_iv = JLabel("IV")
        label_iv.setFont(font)
        label_iv.setForeground(Color.WHITE)

        self.text_field2 = JTextField(30, editable=False)
        self.text_field2.setFont(font)
        self.text_field2.setBackground(Color.LIGHT_GRAY)

        label_algo = JLabel("Select an Algorithm")
        label_algo.setFont(font)
        label_algo.setForeground(Color.WHITE)

        dropdown = JComboBox(["RSA", "AES(ECB)", "AES(CBC)", "AES(GCM)"])
        dropdown.setFont(font)
        dropdown.addActionListener(self.onSelection)

        panel_bottom_label.add(label_iv)
        panel_bottom_label.add(self.text_field2)
        panel_bottom_label.add(label_algo)
        panel_bottom_label.add(dropdown)

        self.frame.getContentPane().add(panel_top, BorderLayout.NORTH)
        self.frame.getContentPane().add(panel_middle, BorderLayout.CENTER)
        self.frame.getContentPane().add(panel_bottom, BorderLayout.SOUTH)
        self.frame.getContentPane().add(panel_bottom_label, BorderLayout.WEST)
