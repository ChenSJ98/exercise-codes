package main.java.RmiUtility;

import MyRMI.Message;

import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.net.ServerSocket;
import java.net.Socket;

public class ServiceSkeleton {
    public ServiceSkeleton(){}
    public void run(int port) throws IOException, ClassNotFoundException, NoSuchMethodException, InvocationTargetException, IllegalAccessException {
        ServerSocket serverSocket = new ServerSocket(port);
        System.out.println("Server Skeleton is running");
        while(true) {
            Socket socket = serverSocket.accept();
            ObjectInputStream oIn= new ObjectInputStream(socket.getInputStream());
            ObjectOutputStream oOut = new ObjectOutputStream(socket.getOutputStream());
            Message m = (Message) oIn.readObject();
            System.out.println("Skeleton receives obj");
            Class<?> classType = Class.forName(m.getServiceName()+"Impl");
            System.out.println("Service name: "+m.getServiceName());
            System.out.println("Method name: "+m.getMethodName());
            Method method = classType.getMethod(m.getMethodName());
            Object result = method.invoke(classType.getInterfaces(),m.getParams());
            m.setResult(result);
            oOut.writeObject(m);
            oIn.close();
            oOut.close();
            socket.close();
        }
    }
}
