package MyRMI;

import java.util.*;
import java.util.Map.Entry;

// This is simple. ROR needs a new object key for each remote object (or its skeleton). 
// This can be done easily, for example by using a counter.
// We also assume a remote object implements only one interface, which is a remote interface.

public class RORtbl {
	// I omit all instance variables. you can use hash table, for example.
	// The table would have a key by ROR.
	static Hashtable<RemoteObjectRef, Object> table = new Hashtable<RemoteObjectRef, Object>();
    int   counter;
	// make a new table.
	public RORtbl() {
//		table   = new Hashtable<MyRMI.RemoteObjectRef, Object>();
		counter = 0;
	}

	// add a remote object to the table.
	// Given an object, you can get its class, hence its remote interface.
	// Using it, you can construct a ROR.
	// The host and port are not used unless it is exported outside.
	// In any way, it is better to have it for uniformity.
	public void addObj(RemoteObjectRef ror, Object o) {
		
		table.put(ror, o);
		counter ++;
	}

	// given ror, find the corresponding object.
	public Object findObj(RemoteObjectRef ror) {
		// if you use a hash table this is easy.
		if (table.containsKey(ror)){
			return table.get(ror);			
		}
		return null;
	}
	
	public Object findObjByname(String name){
		Iterator<Map.Entry<RemoteObjectRef, Object>> it = RORtbl.table.entrySet().iterator();
		Entry<RemoteObjectRef, Object> entry;
		while(it.hasNext()){
			entry = it.next();
			if (entry.getKey().Remote_Interface_Name.equals(name)){
				return entry.getValue();
				
			}
		}
		return null;
	}
}
