package RmiUtility;


import dao.UserDao;

import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.util.List;

public class ServerActionImpl extends UnicastRemoteObject implements ServerAction {
    UserDao dao;
    public ServerActionImpl() throws RemoteException{
        super();
        dao = new UserDao();
    };
    public int login (String username, String password) {
        System.out.println("Incoming login request");

        return dao.login_authenticate(username, password);
    }
    public boolean register(String username, String password) {
        System.out.println("Incoming register request");

        return dao.register_user(username, password);
    }

    @Override
    public boolean subscribeTopic(int userId, String topic) {
        return dao.subscribeTopic(userId, topic);
    }

    @Override
    public List<String> getSubscribedTopics(int userId) {
        return dao.getSubscribedTopics(userId);
    }

    @Override
    public int getIdByUsername(String username) {
        return dao.getIdByUsername(username);
    }


}