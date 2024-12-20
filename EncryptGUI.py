from javax.swing import JDialog, JTextArea, JButton, JPanel, JScrollPane, JOptionPane
from java.awt import BorderLayout, FlowLayout, Color

class EncryptGUI:
    def __init__(self, helpers, message, updatedRequest, header, body):
        self.helpers = helpers
        self.message = message
        self.updatedRequest = updatedRequest
        self.encryptButtonPressed = False

        self.dialog = JDialog()
        self.dialog.setTitle("Jython GUI Example")
        self.dialog.setSize(400, 300)
        self.dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE)
        self.dialog.setModal(True)

        self.text_area = JTextArea(10, 30)
        self.text_area.setLineWrap(True)
        self.text_area.setEditable(False)
        request_data = header + "\n\n" + body
        self.text_area.setText(request_data)
        scroll_pane = JScrollPane(self.text_area)

        self.button1 = JButton("Close", actionPerformed=self.button1_action)
        self.button2 = JButton("Send", actionPerformed=self.button2_action)

        button_panel = JPanel()
        button_panel.setLayout(FlowLayout(FlowLayout.RIGHT))
        button_panel.setBackground(Color.GRAY)
        button_panel.add(self.button1)
        button_panel.add(self.button2)

        text_panel = JPanel()
        text_panel.setLayout(BorderLayout())
        text_panel.add(scroll_pane, BorderLayout.CENTER)

        self.dialog.add(text_panel, BorderLayout.CENTER)
        self.dialog.add(button_panel, BorderLayout.SOUTH)

    def start(self):
        self.dialog.setVisible(True)

    def isSendButtonPressed(self):
        return self.encryptButtonPressed

    def resetSendButton(self):
        self.encryptButtonPressed = False

    def button1_action(self, event):
        self.dialog.dispose()

    def button2_action(self, event):
        if self.updatedRequest and self.message:
            self.message.setRequest(self.updatedRequest)
            self.encryptButtonPressed = True
            self.dialog.dispose()
        else:
            print("No updated request available to send.")
