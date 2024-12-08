from javax.swing import JFrame, JPanel, JTextArea, JScrollPane, JLabel, JTextField, JComboBox, JButton
from java.awt import BorderLayout, Color, Dimension, FlowLayout, Font
from javax.swing.border import EmptyBorder

class RequestViewerGUI:
    def __init__(self, headers, body):
        self.headers = headers
        self.body = body
        
    def show_request_in_gui(self):
        frame = JFrame("Request Details")
        frame.setSize(1000, 600)
        frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
        frame.setResizable(False)

        panel_top = JPanel()
        panel_top.setLayout(BorderLayout())
        panel_top.setBorder(EmptyBorder(10, 10, 10, 10))
        
        top_label = JLabel("Your Request")
        top_label.setFont(Font("Arial", Font.BOLD, 16)) 
        top_label.setForeground(Color.BLACK)
        top_label.setBorder(EmptyBorder(10, 0, 10, 0))
        panel_top.add(top_label, BorderLayout.NORTH)

        text_area1 = JTextArea()
        text_area1.setEditable(False)
        request_data = "\n".join(self.headers) + "\n\n" + self.body
        text_area1.setText(request_data)
        scroll_pane1 = JScrollPane(text_area1)
        panel_top.add(scroll_pane1, BorderLayout.CENTER)
        panel_top.setPreferredSize(Dimension(1500, 260))

        panel_middle = JPanel()
        panel_middle.setLayout(BorderLayout())
        panel_middle.setBorder(EmptyBorder(10, 10, 10, 10)) 
        text_area2 = JTextArea()
        text_area2.setEditable(True)
        text_area2.setText("--None--")
        scroll_pane2 = JScrollPane(text_area2)
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

        button1 = JButton("Encrypt")
        button2 = JButton("Decrypt")
        
        button1.addActionListener(lambda e: self.encrypt_action(text_field, dropdown))
        button2.addActionListener(lambda e: self.decrypt_action(text_field, dropdown))
        
        panel_bottom_right.add(button1)
        panel_bottom_right.add(button2)

        panel_bottom.add(panel_bottom_left, BorderLayout.WEST)
        panel_bottom.add(panel_bottom_right, BorderLayout.EAST)

        frame.add(panel_top, BorderLayout.NORTH)
        frame.add(panel_middle, BorderLayout.CENTER)
        frame.add(panel_bottom, BorderLayout.SOUTH)

        frame.setVisible(True)

    def encrypt_action(self, text_field, dropdown):
        print("KEY = ", str(text_field.getText()))
        print("Algorithm = ", str(dropdown.getSelectedItem()))


    def decrypt_action(self, text_field, dropdown):
        print("KEY = ", str(text_field.getText()))
        print("Algorithm = ", str(dropdown.getSelectedItem()))
