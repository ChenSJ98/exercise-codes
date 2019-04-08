package MyRMI;

import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.net.ServerSocket;
import java.net.Socket;

public class ServiceSkeleton {
    public ServiceSkeleton(){}

    /**
     * Create a service skeleton that accepts RMI request, invoke corresponding method and return result.
     * @param port The port the service is running on.
     * @throws IOException
     * @throws ClassNotFoundException
     * @throws NoSuchMethodException
     * @throws InvocationTargetException
     * @throws IllegalAccessException
     * @throws InstantiationException
     */
    public void run(int port) throws IOException, ClassNotFoundException, NoSuchMethodException, InvocationTargetException, IllegalAccessException, InstantiationException {
        ServerSocket serverSocket = new ServerSocket(port);
        System.out.println("Server Skeleton is running");
        while(true) {
            Socket socket = serverSocket.accept();
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
        }
    }
}
