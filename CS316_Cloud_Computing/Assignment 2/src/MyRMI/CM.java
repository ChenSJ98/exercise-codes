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
        socket = new Socket(host, port);
        oOut = new ObjectOutputStream(socket.getOutputStream());
        oIn = new ObjectInputStream(socket.getInputStream());
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
