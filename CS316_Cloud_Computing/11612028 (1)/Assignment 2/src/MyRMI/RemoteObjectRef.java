package MyRMI;
import main.java.RmiUtility.*;
import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Proxy;
import java.rmi.Remote;

public class RemoteObjectRef {
	String IP_adr;
	int Port;
	int Obj_Key;
	String Remote_Interface_Name;

	public RemoteObjectRef(String ip, int port, int obj_key, String riname) {
		IP_adr = ip;
		Port = port;
		Obj_Key = obj_key;
		Remote_Interface_Name = riname;
	}

	/**
	 *
	 * @param classType The remote service interface.class passed by the client.
	 * @return A stub (proxy) of the service.
	 */
	public Object localise(Class<?> classType) {
		Class c;
		try {
			InvocationHandler handler = new ServiceStub(this.Remote_Interface_Name, IP_adr, Port);
			Remote proxy = (Remote)Proxy.newProxyInstance(classType.getClassLoader(), new Class[] {classType}, handler);
			return proxy;
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		return null;
	}
}