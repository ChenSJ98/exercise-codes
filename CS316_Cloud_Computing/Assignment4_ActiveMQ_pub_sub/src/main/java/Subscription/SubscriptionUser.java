package Subscription;

import org.apache.activemq.ActiveMQConnection;
import org.apache.activemq.ActiveMQConnectionFactory;
import org.apache.activemq.advisory.DestinationSource;
import org.apache.activemq.command.ActiveMQTopic;

import javax.jms.*;
import javax.swing.text.DateFormatter;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Set;

public class SubscriptionUser {
    private String username;
    private String password;
    private String URL;
    private int id;
    ConnectionFactory connectionFactory;
    Connection connection;
    Session session;
    Destination destination;
    public SubscriptionUser(String username, String password, String url, int id) {
        this.username = username;
        this.password = password;
        this.URL = url;
        this.id = id;
        connectionFactory = new ActiveMQConnectionFactory(username, password, URL);
    }

    public Set<ActiveMQTopic> getAllTopics() {
        try {
            connection = connectionFactory.createConnection();
            connection.start();
            DestinationSource ds = ((ActiveMQConnection)connection).getDestinationSource();
            Set<ActiveMQTopic> allTopics = ds.getTopics();
            return allTopics;
        } catch (JMSException e) {
            e.printStackTrace();
        } finally {
            close(connection, session);
        }
        return null;
    }

    private static void close(Connection connection, Session session) {
        if(connection != null) {
            try {
                connection.close();
            } catch (JMSException e) {
                e.printStackTrace();
            }
        }
        if(session != null) {
            try {
                session.close();
            } catch (JMSException e) {
                e.printStackTrace();
            }
        }
    }

    public boolean publishContent(String username, String topic, String content) {
        try {
            connection = connectionFactory.createConnection();
            connection.start();
            session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
            destination = session.createTopic(topic);
            MessageProducer producer = session.createProducer(destination);
            producer.setDeliveryMode(DeliveryMode.PERSISTENT);
            sendMessage(username, producer, content);
        } catch (JMSException e) {
            e.printStackTrace();
            return false;
        } finally {
            close(connection, session);
        }

        return true;
    }

    private void sendMessage(String username, MessageProducer producer, String content) throws JMSException {
        String date;
        Date dt = new Date();
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        date = sdf.format(dt);
        TextMessage message = session.createTextMessage(date + " By " + username + ":\n" + content);
        producer.send(message);
    }

    public boolean subscribeTopic(int id, String topic) {
        try {
            connection = connectionFactory.createConnection();
            connection.setClientID(String.valueOf(id));
            connection.start();
            session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
            destination = session.createTopic(topic);
            Topic jmsTopic = session.createTopic(topic);

            session.createDurableSubscriber(jmsTopic, "user_" + id + "_" + topic);

        } catch (JMSException e) {
            e.printStackTrace();
            return false;
        } finally {
            close(connection, session);
        }
        return true;

    }

    public void displayMessages(List<String> topics)  {
        try {
            connection = connectionFactory.createConnection();
            connection.setClientID(String.valueOf(id));
            connection.start();
            System.out.println();
            for (String topic : topics) {
                System.out.println("topic: " + topic);
                System.out.println("----------------------------");
                session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
                MessageConsumer messageConsumer = session.createDurableSubscriber(new ActiveMQTopic(topic), "user_"+id + "_" + topic);
                while(true) {
                    Message msg = messageConsumer.receive(10);
                    if(msg == null) {
                        break;
                    }
                    if(msg instanceof TextMessage) {
                        System.out.println("~" + ((TextMessage)msg).getText());
                        System.out.println();
                    }
                    msg.acknowledge();
                }
                session.close();
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            close(connection, session);
        }
    }

}
