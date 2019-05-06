
import MyRMI.LocateSimpleRegistry;
import MyRMI.RemoteObjectRef;
import MyRMI.SimpleRegistry;
import RmiUtility.ServerAction;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.UUID;

/**
 * A test class that simulates high concurrency rmi invocation.
 */
public class BulkRegister implements Runnable{
    private static AtomicInteger rmiCounter = new AtomicInteger();
    private static AtomicInteger appCounter = new AtomicInteger();
    static CountDownLatch latch;
    static CountDownLatch done;
    public static void main(String[] args) {
        int N = 100;
        ExecutorService service = Executors.newCachedThreadPool();
        latch  = new CountDownLatch(1);
        done = new CountDownLatch(N);
        rmiCounter.set(0);
        appCounter.set(0);
        for(int i = 0; i < N; i++) {
            service.execute(new BulkRegister());
        }
        latch.countDown();
        try {
            done.await();
            service.shutdown();
            System.out.println("successful RMI connections:"+ rmiCounter.get() +"/" + N);
            System.out.println("successful APP connections:"+ appCounter.get() +"/" + N);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }


    }

    @Override
    public void run() {

        /* use uuid as an unique random string */
        String username = String.valueOf(UUID.randomUUID());
        String password = String.valueOf(UUID.randomUUID());

        try {
            latch.await();
            SimpleRegistry sr = LocateSimpleRegistry.getRegistry("localhost",2099);
            if(sr == null) {
                System.out.println("sr null!");
                return;
            }
            RemoteObjectRef ror = sr.lookup("Server");
            rmiCounter.getAndIncrement();
            if(ror == null) {
                System.out.println("ror null!");
                return;
            }
            ServerAction myStub = (ServerAction) ror.localise();

            boolean result = myStub.register(username, password);
            if(result){
                System.out.println(Thread.currentThread().getId() + "Congratulations, you have successfully signed up as a user!");
                appCounter.getAndIncrement();
            } else {
                System.out.println(Thread.currentThread().getId() + "Error! It seems the username exists");
            }

        } catch (Exception e) {
            System.out.println("BR error:" + e.toString());
            e.printStackTrace();
        } finally{
            done.countDown();
        }

    }
}