package MyRMI;

import java.io.Serializable;

public class Message implements Serializable {
    private String serviceName;
    private String methodName;
    private Class<?>[] argTypes;
    private Object[] params;
    private Object result;
    public Message(){}
    public Message(String serviceName, String methodName, Class<?>[] argTypes, Object[] params) {
        this.serviceName = serviceName;
        this.methodName = methodName;
        this.argTypes = argTypes;
        this.params = params;
    }

    public String getServiceName() {
        return serviceName;
    }

    public String getMethodName() {
        return methodName;
    }

    public Object[] getParams() {
        return params;
    }

    public Object getResult() {
        return result;
    }

    public Class<?>[] getArgTypes() {
        return argTypes;
    }
    public void setResult(Object result) {
        this.result = result;
    }
}
