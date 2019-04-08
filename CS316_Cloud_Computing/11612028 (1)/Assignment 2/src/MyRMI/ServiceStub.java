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


        Message message = new Message(this.serviceName, method.getName(), method.getParameterTypes(), args);
        CM cm = new CM();
        cm.connect(host, port);
        cm.send(message);
        Message result = cm.recv();
        System.out.println(result.getResult());
        cm.close();
        return result.getResult();

        //return message.getResult();

    }
}
