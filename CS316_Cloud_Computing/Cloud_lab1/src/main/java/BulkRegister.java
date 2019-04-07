package main.java;


import main.java.RmiUtility.ServerAction;

import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.util.Random;
import java.util.UUID;
import java.util.Vector;
import java.util.concurrent.atomic.AtomicInteger;

import static java.lang.Thread.sleep;

public class BulkRegister implements Runnable{
    private static AtomicInteger RMIcounter = new AtomicInteger();
    private static AtomicInteger appCounter = new AtomicInteger();
    public static void main(String[] args) {
        int N = 60000;
        Vector<Thread> threads = new Vector<Thread>();
        RMIcounter.set(0);
        appCounter.set(0);
        for(int i = 0; i < N; i++) {
            Thread t = new Thread(new BulkRegister());
            threads.add(t);
            t.start();
        }
        for(Thread t : threads) {
            try {
                t.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        System.out.println("successful RMI connections:"+ RMIcounter.get() +"/" + N);
        System.out.println("successful APP connections:"+ appCounter.get() +"/" + N);

    }

    @Override
    public void run() {
        UUID uuid = UUID.randomUUID();
        String username = String.valueOf(UUID.randomUUID());
        String password = String.valueOf(UUID.randomUUID());
        //System.out.println(username);
        //System.out.println(password);
        try{
            Registry reg = LocateRegistry.getRegistry("localhost",1099);
            ServerAction stub = (ServerAction) reg.lookup("noobServer");
            RMIcounter.getAndIncrement();
            if(stub.register(username, password)){
                System.out.println("Congratulations, you have successfully signed up as a user!");
                appCounter.getAndIncrement();
            } else {
                System.out.println("Error! It seems the username exists");
            }
        } catch(Exception e) {
            e.printStackTrace();
        }

    }
}
