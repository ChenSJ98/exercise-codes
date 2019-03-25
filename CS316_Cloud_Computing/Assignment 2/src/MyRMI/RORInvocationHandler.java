package MyRMI;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.rmi.Remote;

public class RORInvocationHandler implements InvocationHandler {
    Object obj;
    public RORInvocationHandler(Remote o) {
        this.obj = o;
    }

    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        Object result;
        try {
            if(method.getName().indexOf("login") > -1) {
                System.out.println("... LOGIN Method Executing");
            } else if (method.getName().indexOf("register") > -1){
                System.out.println("... REGISTER Method Executing");
            }
            method.invoke(obj, args);
        } catch (InvocationTargetException e) {
            throw e;
        } catch (Exception e) {
            throw e;
        }
        return null;
    }

}
