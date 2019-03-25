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

	// this method is important, since it is a stub creator.
	//
	public Object localise() {
		// Implement this as you like: essentially you should
		// create a new stub object and returns it.
		// Assume the stub class has the name e.g.
		//
		// Remote_Interface_Name + "_stub".
		//
		// Then you can create a new stub as follows:
		//
		// Class c = Class.forName(Remote_Interface_Name + "_stub");
		// Object o = c.newinstance()
		//
		// For this to work, your stub should have a constructor without
		// arguments.
		// You know what it does when it is called: it gives communication
		// module
		// all what it got (use CM's static methods), including its method name,
		// arguments etc., in a marshalled form, and CM (yourRMI) sends it out
		// to
		// another place.
		// Here let it return null.
		Class c;
		try {
			//System.out.println("ROR looking for class:"+Remote_Interface_Name+"Impl");
			//c = Class.forName("main.java.RmiUtility."+Remote_Interface_Name+"Impl");
			//Object o = c.newInstance();
			//RORtbl.table.put(this, o);
			Object o = new Object();//(new RORtbl()).findObjByname(this.Remote_Interface_Name);
			//ServiceStub h = new ServiceStub();
			Class<?> classType =ServerAction.class;
			InvocationHandler handler = new ServiceStub(this.Remote_Interface_Name, IP_adr, Port);
			//InvocationHandler handler = new RORInvocationHandler((Remote) o);
			Remote proxy = (Remote)Proxy.newProxyInstance(classType.getClassLoader(), new Class[] {ServerAction.class}, handler);
			return proxy;
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		return null;
	}
}