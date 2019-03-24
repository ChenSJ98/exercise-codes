import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.rmi.Remote;

public class RORInvocationHandler implements InvocationHandler {
    public RORInvocationHandler(Remote o) {
    }

    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        return null;
    }

}
