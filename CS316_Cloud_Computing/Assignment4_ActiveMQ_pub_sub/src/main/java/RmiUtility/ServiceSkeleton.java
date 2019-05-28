package RmiUtility;

import MyRMI.Message;

import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.concurrent.LinkedBlockingDeque;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

public class ServiceSkeleton {
    public ServiceSkeleton(){}
    public void run(int port) throws IOException, ClassNotFoundException, NoSuchMethodException, InvocationTargetException, IllegalAccessException, InstantiationException {
        ServerSocket serverSocket = new ServerSocket(port, 10000);
        System.out.println("Server Skeleton is running");
        ThreadPoolExecutor executor = new ThreadPoolExecutor(5,12, 200, TimeUnit.MICROSECONDS, new LinkedBlockingDeque<Runnable>());

        while(true) {
            Socket socket = serverSocket.accept();
            SkeletonThread t = new SkeletonThread(socket);
            executor.execute(t);
        }
    }
    static class SkeletonThread implements Runnable {
        Socket socket;
        SkeletonThread(Socket socket) {
            this.socket = socket;
        }
        @Override
        public void run() {
            try {
                ObjectInputStream oIn= new ObjectInputStream(socket.getInputStream());
                ObjectOutputStream oOut = new ObjectOutputStream(socket.getOutputStream());
                Message m = (Message) oIn.readObject();

                Class<?> classType = Class.forName(m.getServiceName()+"Impl");
                Method method = classType.getMethod(m.getMethodName(),m.getArgTypes());
                Object result = method.invoke(classType.newInstance(),m.getParams());
                m.setResult(result);

                oOut.writeObject(m);
                oIn.close();
                oOut.close();
                socket.close();

            } catch (Exception e) {
                //System.out.println(e.toString());
                e.printStackTrace();
            }

        }
    }
}
