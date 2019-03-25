package MyRMI;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;

public class ServiceStub implements InvocationHandler {
    private String serviceName ;
    private String host;
    private int port;
    public ServiceStub(){}
    public ServiceStub(String serviceName, String host, int port){
        this.serviceName = serviceName;
        this.host = host;
        this.port = port;
    }

    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        System.out.println("stub recv call");
        System.out.println("Service name:"+ this.serviceName);
        Message message = new Message(this.serviceName, method.getName(), method.getParameterTypes(), args);

        CM cm = new CM();
        System.out.println("message built");
        cm.connect(host, port);
        System.out.println("cm conneted");
        cm.send(message);
        System.out.println("stub message sent");
        Message result = cm.recv();
        System.out.println(result.getResult());
        cm.close();
        return true;

        //return message.getResult();

    }
}
