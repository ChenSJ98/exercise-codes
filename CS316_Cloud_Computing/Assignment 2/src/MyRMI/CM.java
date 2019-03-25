package MyRMI;

import java.io.*;
import java.net.Socket;
import java.net.UnknownHostException;

public class CM {
    private Socket socket;
    private ObjectInputStream oIn;
    private ObjectOutputStream oOut;

    public CM() {}

    public void connect(String host, int port) throws UnknownHostException, IOException {
        System.out.println("CM tries to connect to "+host+":" + port);
        System.out.println("1");
        socket = new Socket(host, port);
        System.out.println("1");
        oOut = new ObjectOutputStream(socket.getOutputStream());
        System.out.println("1");
        oIn = new ObjectInputStream(socket.getInputStream());

        System.out.println("CM get connection");
    }
    public void close() throws IOException {
        socket.close();
        oIn.close();
        oOut.close();
    }
    public  void send(Message m) throws IOException {
        oOut.writeObject(m);
    }
    public Message recv() throws IOException, ClassNotFoundException {
        return (Message) oIn.readObject();
    }
}
