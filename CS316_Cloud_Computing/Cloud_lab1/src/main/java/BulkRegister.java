package main.java;
import main.java.RmiUtility.ServerAction;

import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.UUID;

public class BulkRegister implements Runnable{
    private static AtomicInteger RMIcounter = new AtomicInteger();
    private static AtomicInteger appCounter = new AtomicInteger();
    static CountDownLatch latch;
    static CountDownLatch done;
    public static void main(String[] args) {
        int N = 30000;
        ExecutorService service = Executors.newCachedThreadPool();
        latch  = new CountDownLatch(1);
        done = new CountDownLatch(N);
        RMIcounter.set(0);
        appCounter.set(0);
        for(int i = 0; i < N; i++) {
            service.execute(new BulkRegister());
        }
        latch.countDown();
        try {
            done.await();
            service.shutdown();
            System.out.println("successful RMI connections:"+ RMIcounter.get() +"/" + N);
            System.out.println("successful APP connections:"+ appCounter.get() +"/" + N);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }


    }


    @Override
    public void run() {
        String username = String.valueOf(UUID.randomUUID());
        String password = String.valueOf(UUID.randomUUID());
        try{
            latch.await();
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
        } finally{
            done.countDown();
        }

    }
}
