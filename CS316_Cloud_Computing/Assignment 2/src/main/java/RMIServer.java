package main.java;

import main.java.RmiUtility.ServerAction;
import main.java.RmiUtility.ServerImpl;

import java.rmi.Naming;
import java.rmi.registry.LocateRegistry;

public class RMIServer {
    public RMIServer(){}
    public static void main(String[] args) {
        try {
	        LocateRegistry.createRegistry(1099);
            ServerAction server = new ServerImpl();
            Naming.rebind("noobServer",server);
            System.out.println("noob server is up and running");
        } catch ( Exception e) {
            System.out.println("Server throws exception: " + e.toString() );
        }
    }
}
