package RmiUtility;

import java.rmi.Remote;
import java.rmi.RemoteException;
import java.util.List;

public interface ServerAction extends Remote{
    int login(String username, String password) throws RemoteException;
    boolean register(String username, String password) throws RemoteException;
    boolean subscribeTopic(int userId, String topic) throws RemoteException;
    List<String> getSubscribedTopics(int userId) throws RemoteException;
    int getIdByUsername(String username) throws RemoteException;
}