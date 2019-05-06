

import MyRMI.LocateSimpleRegistry;
import MyRMI.RemoteObjectRef;
import MyRMI.SimpleRegistry;
import RmiUtility.ServerAction;
import Subscription.SubscriptionUser;
import org.apache.activemq.ActiveMQConnection;
import org.apache.activemq.command.ActiveMQTopic;

import javax.jms.JMSException;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.util.List;
import java.util.Scanner;

public class RMIClient {
    private static ServerAction myStub = null;
    public RMIClient(){}
    private static SubscriptionUser subscriptionUser;
    private static final String activeMqUrl = ActiveMQConnection.DEFAULT_BROKER_URL;
    public static void main(String[] args) {
        try {
            Registry reg = LocateRegistry.getRegistry("localhost",1099);
            SimpleRegistry sr = LocateSimpleRegistry.getRegistry("localhost",2099);
            RemoteObjectRef ror = sr.lookup("Server");

            myStub = (ServerAction) ror.localise();

            int quit = 0;
            while(true){
                System.out.println("Welcome");
                System.out.println("\n==============MENU==============");
                System.out.println("1. Login\n2. Register\n3. Quit");
                System.out.println("==============MENU==============\n");
                Scanner scanner = new Scanner(System.in);
                int x = scanner.nextInt();
                switch (x) {
                    case 1:
                        login();
                        break;
                    case 2:
                        register();
                        break;
                    case 3:
                        quit = 1;
                        break;
                    default: {
                        System.out.println("Invalid Choice!");
                    }
                }
                if(quit == 1)
                    break;
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
        return;
    }

    /**
     * Performs login authentication and displays user menu.
     * @throws RemoteException
     */
    private static void login() throws RemoteException {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Username: ");
        String username = scanner.next();
        System.out.print("Password: ");
        String password = scanner.next();
        System.out.println("Authenticating...");
        int id = myStub.login(username, password);
        if (id > 0) {
            System.out.println("Login success!");
            subscriptionUser = new SubscriptionUser(username, password, activeMqUrl, id);
            displayUserMenu(id, username);
        } else {
            System.out.println("Login fail! Please check your credentials");
        }
    }

    /**
     * Displays all the subscribed messages of user with the given id.
     * @param id userId
     */
    private static void displayMessages(int id) {
        System.out.println("\n============MESSAGES============");
        try {
            System.out.println("Fetching messages...");
            List<String> topics = myStub.getSubscribedTopics(id);
            System.out.println("Your Messages:");
            subscriptionUser.displayMessages(topics);
        } catch (Exception e) {
            e.printStackTrace();
        }
        System.out.println("============MESSAGES============\n");

    }

    /**
     * Displays user menu for the given user.
     * @param id
     * @param username
     */
    private static void displayUserMenu(int id, String username) {
        System.out.println("Welcome back, "+username);
        displayMessages(id);
        while(true) {
            System.out.println("\n==============MENU==============");
            System.out.println("1. Publish Content\n2. Subscribe Topics\n3. Check new message.\n4. Quit\n");
            System.out.println("==============MENU==============\n");
            int opt;
            Scanner in = new Scanner(System.in);
            opt = in.nextInt();
            switch(opt) {
                case 1 :
                    publishContent();
                    break;
                case 2:
                    subscribeTopics(id);
                    break;
                case 3:
                    displayMessages(id);
                    break;
                case 4:
                    break;
                default:
                    System.out.println("invalid option!");
                    continue;
            }
            if(opt == 4)
                break;
        }
    }

    /**
     * Displays user interface for subscribing topics.
     * @param id
     */
    private static void subscribeTopics(int id) {
        Scanner in = new Scanner(System.in);
        while (true) {
            System.out.println();
            displayAllTopics();
            System.out.println("Enter the topic that you want to subscribe. Enter 'q' to quit");
            String topic = in.nextLine();
            if(topic.equals("q"))
                break;
            subscriptionUser.subscribeTopic(topic);
            try {
                if(myStub.subscribeTopic(id, topic))
                    System.out.println("You have successfully subscribed to "+ topic +"!");
            } catch (RemoteException e) {
                e.printStackTrace();
            }

        }


    }

    /**
     * Displays all topics currently available on ActiveMQ server.
     */
    private static void displayAllTopics() {
        System.out.println("All topics:");
        int count = 0;
        for(ActiveMQTopic topic : subscriptionUser.getAllTopics()) {
            try {
                System.out.println("topic #" + count + ": " + topic.getTopicName());
                count++;
            } catch (JMSException e) {
                e.printStackTrace();
            }
        }

    }

    /**
     * Displays user interface for publishing content.
     */
    private static void publishContent() {

        int opt;
        Scanner in = new Scanner(System.in);
        while(true) {
            System.out.println("\n==============MENU==============");
            System.out.println("1. Publish a comment on a topic");
            System.out.println("2. Quit");
            System.out.println("==============MENU==============\n");
            opt = in.nextInt();
            switch (opt) {
                case 1:
                    displayAllTopics();
                    publishOnTopic();
                    break;
                case 2:
                    break;
                default:
                    System.out.println("Invalid option!");
            }
            if(opt == 2)
                break;
        }
    }

    /**
     * Displays user interface for publishing a piece of content on a specific topic.
     */
    private static void publishOnTopic() {
        Scanner in = new Scanner(System.in);
        System.out.println("Please enter topic and comment, press 'q' to quit.");
        System.out.println("If you enter a non-exist topic, it will be created.");
        System.out.println("Topic:");
        String topic = in.nextLine();
        System.out.println("Content:");
        String content = in.nextLine();
        if(subscriptionUser.publishContent(topic, content))
            System.out.println("Comment successfully published!");
    }

    /**
     * Displays user interface for registration.
     */
    private static void register(){
        Scanner scanner = new Scanner(System.in);
        try{
            System.out.print("Username: ");
            String username = scanner.next();
            System.out.print("Password: ");
            String password = scanner.next();
            System.out.println("Processing...");
            if(myStub.register(username, password)){
                System.out.println("Congratulations, you have successfully signed up as a user!");
                subscribeTopics(myStub.getIdByUsername(username));
            } else {
                System.out.println("Error! It seems the username exists");
            }
        } catch(Exception e) {
            e.printStackTrace();
        }
    }
}
