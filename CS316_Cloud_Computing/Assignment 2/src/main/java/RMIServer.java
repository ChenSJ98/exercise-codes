package main.java;

import MyRMI.LocateSimpleRegistry;
import MyRMI.SimpleRegistry;
import main.java.RmiUtility.ServerAction;
import main.java.RmiUtility.ServerActionImpl;

import java.rmi.Naming;
import java.rmi.registry.LocateRegistry;

public class RMIServer {
    public RMIServer(){}
    public static void main(String[] args) {
        try {
	        SimpleRegistry reg = LocateSimpleRegistry.getRegistry("localhost",2099);
            ServerAction server = new ServerActionImpl();
            System.out.println("Get simple reg");
            reg.rebind("Server", server, "localhost", 1234);
            //Naming.rebind("noobServer",server);
            System.out.println("noob server is up and running");
        } catch ( Exception e) {
            System.out.println("Server throws exception: " + e.toString() );
        }
    }
}
