package Subscription;

import org.apache.activemq.ActiveMQConnection;
import org.apache.activemq.ActiveMQConnectionFactory;
import org.apache.activemq.advisory.DestinationSource;
import org.apache.activemq.command.ActiveMQTopic;

import javax.jms.*;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Set;

public class SubscriptionUser {
    private String username;
    private int id;
    private ConnectionFactory connectionFactory;
    private Connection connection;
    private Session session;
    private Destination destination;

    public SubscriptionUser(String username, String password, String url, int id) {
        this.username = username;
        this.id = id;
        connectionFactory = new ActiveMQConnectionFactory(username, password, url);
    }

    /**
     * Get all the topics currently on ActiveMQ server.
     * @return All topics.
     */
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

    /**
     * Publish content on a topic.
     * @param topic
     * @param content
     * @return Return true on operation success.
     */
    public boolean publishContent(String topic, String content) {
        try {
            connection = connectionFactory.createConnection();
            connection.start();
            session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
            destination = session.createTopic(topic);
            MessageProducer producer = session.createProducer(destination);
            producer.setDeliveryMode(DeliveryMode.PERSISTENT);
            sendMessage(producer, content);
        } catch (JMSException e) {
            e.printStackTrace();
            return false;
        } finally {
            close(connection, session);
        }

        return true;
    }

    private void sendMessage(MessageProducer producer, String content) throws JMSException {
        /* construct text message including date, author and content */
        String date;
        Date dt = new Date();
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        date = sdf.format(dt);
        TextMessage message = session.createTextMessage(date + " By " + username + ":\n" + content);

        producer.send(message);
    }

    /**
     * Subscribe a topic.
     * @param topic
     * @return Return true on operation success.
     */
    public boolean subscribeTopic(String topic) {
        try {
            connection = connectionFactory.createConnection();
            connection.setClientID(String.valueOf(id));
            connection.start();
            session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
            destination = session.createTopic(topic);
            Topic jmsTopic = session.createTopic(topic);

            /* Subscriber name for each topic should be different, otherwise it will be overrode. */
            session.createDurableSubscriber(jmsTopic, "user_" + id + "_" + topic);
        } catch (JMSException e) {
            e.printStackTrace();
            return false;
        } finally {
            close(connection, session);
        }
        return true;

    }

    /**
     * Checks and displays all subscribed messages on the given list of topics.
     * @param topics All topics that the user subscribed. This is get from the remote database.
     */
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
