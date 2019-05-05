package Subscription;

import javax.jms.JMSException;
import javax.jms.Message;
import javax.jms.MessageListener;
import javax.jms.TextMessage;

public class MyListener implements MessageListener {
    @Override
    public void onMessage(Message message) {
        System.out.println("recv message:");
        try {
            System.out.println(((TextMessage)message).getText());
            System.out.println();
        } catch (JMSException e) {
            e.printStackTrace();
        }
    }
}
