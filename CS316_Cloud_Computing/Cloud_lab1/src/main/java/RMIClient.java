package main.java;

import main.java.RmiUtility.ServerAction;

import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.util.Scanner;

public class RMIClient {
    private static ServerAction stub = null;
    public RMIClient(){}
    public static void main(String[] args) {
        try {
            Registry reg = LocateRegistry.getRegistry("localhost",1099);
            stub = (ServerAction) reg.lookup("noobServer");
            //a simple command-line interface
            System.out.println("Welcome");
            int quit = 0;
            while(true){
                System.out.println("1. Login 2. Register 3.Quit");
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
            System.out.print("Client exception thrown: "+e.toString());
        }

    }

    private static void login() throws RemoteException {
        Scanner scanner = new Scanner(System.in);
        String username = "";
        String password = "";
        System.out.print("Username: ");
        username = scanner.next();
        System.out.print("Password: ");
        password = scanner.next();
        System.out.println("Authenticating...");
        if (stub.login(username, password)) {
            System.out.println("Login success!");
        } else {
            System.out.println("Login fail! Please check your credentials");
        }
    }

    private static void register(){
        Scanner scanner = new Scanner(System.in);
        try{
            Registry reg = LocateRegistry.getRegistry("localhost",1099);
            stub = (ServerAction) reg.lookup("noobServer");
            String username = "";
            String password = "";
            System.out.print("Username: ");
            username = scanner.next();
            System.out.print("Password: ");
            password = scanner.next();
            System.out.println("Processing...");
            if(stub.register(username, password)){
                //System.out.println("Congratulations, you have successfully signed up as a user!");
            } else {
                System.out.println("Error! It seems the username exists");
            }
        } catch(Exception e) {
            e.printStackTrace();
        }
    }
}
