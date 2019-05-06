

import MyRMI.LocateSimpleRegistry;
import MyRMI.SimpleRegistry;
import RmiUtility.ServerAction;
import RmiUtility.ServerActionImpl;


public class RMIServer {
    public RMIServer(){}
    public static void main(String[] args) {
        try {
	        SimpleRegistry reg = LocateSimpleRegistry.getRegistry("localhost",2099);
            ServerAction server = new ServerActionImpl();
            System.out.println("Get simple reg");
            reg.rebind("Server", server, "localhost", 1234);
            System.out.println("noob server is up and running");
        } catch ( Exception e) {
            System.out.println("Server throws exception: " + e.toString() );
        }
    }
}
