package main.java.RmiUtility;

import main.java.dao.UserDao;

import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

public class ServerImpl extends UnicastRemoteObject implements ServerAction {
    public ServerImpl() throws RemoteException{
        super();
    };
    public boolean login (String username, String password) throws RemoteException{
        UserDao userDao = new UserDao();
        return userDao.login_authenticate(username, password);
    }
    public boolean register(String username, String password) throws RemoteException{
        UserDao userDao = new UserDao();
        return userDao.register_user(username, password);
    }
}