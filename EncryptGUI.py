from javax.swing import JFrame, JTextArea, JButton, JPanel, JScrollPane, JOptionPane
from java.awt import BorderLayout, FlowLayout, Color

class EncryptGUI:
    def __init__(self, helpers, message, updatedRequest, header , body):
        self.helpers = helpers
        self.message = message
        self.updatedRequest = updatedRequest
        self.encryptButtonPressed = False
        print('updatedRequest',updatedRequest)

        self.frame = JFrame("Jython GUI Example")
        self.frame.setSize(400, 300)
        self.frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)

        self.text_area = JTextArea(10, 30)
        self.text_area.setLineWrap(True) 
        request_data = "\n".join(header) + "\n\n" + body
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
        
        self.frame.add(text_panel, BorderLayout.CENTER)
        self.frame.add(button_panel, BorderLayout.SOUTH)
        
        #self.frame.setVisible(True)

    def start(self):
        self.frame.setVisible(True)

    def isSendButtonPressed(self):
        return self.encryptButtonPressed

    def resetSendButton(self):
        self.encryptButtonPressed = False

    def button1_action(self, event):
        x=1
        
    def button2_action(self, event):
        if self.updatedRequest and self.message:
            self.message.setRequest(self.updatedRequest)
            print("Updated request sent:")
            print(self.helpers.bytesToString(self.updatedRequest))
            self.encryptButtonPressed = True
        else:
            print("No updated request available to send.")