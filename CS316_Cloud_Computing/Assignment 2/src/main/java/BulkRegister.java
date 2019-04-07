package main.java;
import MyRMI.LocateSimpleRegistry;
import MyRMI.RemoteObjectRef;
import MyRMI.SimpleRegistry;
import main.java.RmiUtility.ServerAction;
import java.util.Vector;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.UUID;

public class BulkRegister implements Runnable{
    private static AtomicInteger RMIcounter = new AtomicInteger();
    private static AtomicInteger appCounter = new AtomicInteger();
    public static void main(String[] args) {
        int N = 60000;
        Vector<Thread> threads = new Vector<>();
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

        try {
            //Registry reg = LocateRegistry.getRegistry("localhost",1099);
            SimpleRegistry sr = LocateSimpleRegistry.getRegistry("localhost",2099);
            //int t = (new Random()).nextInt(2000);
            //sleep(t);
            if(sr == null) {
                System.out.println("sr null!");
                return;
            }
            RemoteObjectRef ror = sr.lookup("Server");
            RMIcounter.getAndIncrement();
            if(ror == null) {
                System.out.println("ror null!");
                return;
            }
            ServerAction myStub = (ServerAction) ror.localise();

            boolean result = myStub.register(username, password);
            if(result){
                //System.out.println(Thread.currentThread().getId() + "Congratulations, you have successfully signed up as a user!");
                appCounter.getAndIncrement();
            } else {
                System.out.println(Thread.currentThread().getId() + "Error! It seems the username exists");
            }

        } catch (Exception e) {
            System.out.println("BR error:" + e.toString());
            e.printStackTrace();
        }

    }
}
