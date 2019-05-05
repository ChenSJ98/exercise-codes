package dao;



import Resources.BCrypt;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class UserDao {
    public UserDao(){}
    private static final String URL = "jdbc:mysql://155.138.128.229:3306/cs316?useSSL=true";
    private static final String USER_NAME = "user1";
    private static final String PASSWORD = "12345@Cs";

    /**
     * This method checks if the credential provided by the user is valid.
     * @param username
     * @param password
     * @return Return true if the operation is successful.
     */
    public int login_authenticate(String username, String password) {
        Connection connection = null;
        try {
            //get connection to database
            connection = DriverManager.getConnection(URL, USER_NAME, PASSWORD);
            //execute mysql query
            String sql = "SELECT id, username, password FROM users where username = \""
                    + username + "\"";
            PreparedStatement prst = connection.prepareStatement(sql);
            ResultSet rs = prst.executeQuery();
            int id = 0;
            if(rs.next()) {
                if (BCrypt.checkpw(password, rs.getString("password"))) {
                    id = rs.getInt("id");
                    rs.close();
                    prst.close();
                    return id;
                } else {
                    rs.close();
                    prst.close();
                    return 0;
                }
            }
            rs.close();
            prst.close();
        } catch (Exception e) {
            e.printStackTrace();
        }finally {
            closeConnection(connection);
        }
        return 0;
    }

    /**
     * This method try to write the credential of a user in to the database.
     * @param username
     * @param password
     * @return Return true if the operation is successful.
     */
    public boolean register_user(String username, String password){
        Connection connection = null;
        Statement stmt;
        try {
            System.out.println("call register");
            //get connection to database
            connection = DriverManager.getConnection(URL, USER_NAME, PASSWORD);
            stmt = connection.createStatement();
            //insert user info to database
            String hashed = BCrypt.hashpw(password, BCrypt.gensalt());
            String sql = "insert into users (username, password)values" +
                    "(\""+username+"\",\""+hashed+"\")";
            stmt.execute(sql);
        } catch (SQLException se) {
            closeConnection(connection);
            return false;
        } catch (Exception e) {
            e.printStackTrace();
        }finally {
            closeConnection(connection);
        }
        return true;
    }

    public boolean subscribeTopic(int userId, String topic) {
        Connection connection = null;
        Statement stmt;
        try {
            System.out.println("call subscribe");
            //get connection to database
            connection = DriverManager.getConnection(URL, USER_NAME, PASSWORD);
            stmt = connection.createStatement();
            //insert user info to database

            String sql = "insert into user_topic (id, topic)values" +
                    "(\""+userId+"\",\""+topic+"\")";
            stmt.execute(sql);
        } catch (SQLException se) {
            closeConnection(connection);
            return false;
        } catch (Exception e) {
            e.printStackTrace();
        }finally {
            closeConnection(connection);
        }
        return true;
    }
    public List<String> getSubscribedTopics(int userId) {
        List<String> topics = new ArrayList<>();
        Connection connection = null;
        try {
            //get connection to database
            connection = DriverManager.getConnection(URL, USER_NAME, PASSWORD);
            //execute mysql query
            String sql = "SELECT topic FROM user_topic where id = \""
                    + userId + "\"";
            PreparedStatement prst = connection.prepareStatement(sql);
            ResultSet rs = prst.executeQuery();

            while(rs.next()) {
                String topic = rs.getString("topic");
                topics.add(topic);
            }
            rs.close();
            prst.close();
        } catch (Exception e) {
            e.printStackTrace();
        }finally {
            closeConnection(connection);
        }
        return topics;
    }
    private void closeConnection(Connection connection) {
        if (connection != null) {
            try {
                connection.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }

    public int getIdByUsername(String username) {
        Connection connection = null;
        int id = 0;
        try {
            //get connection to database
            connection = DriverManager.getConnection(URL, USER_NAME, PASSWORD);
            //execute mysql query
            String sql = "SELECT id FROM users where username = \""
                    + username + "\"";
            PreparedStatement prst = connection.prepareStatement(sql);
            ResultSet rs = prst.executeQuery();
            if(rs.next()) {
                id = rs.getInt("id");
            }
            rs.close();
            prst.close();
        } catch (Exception e) {
            e.printStackTrace();
        }finally {
            closeConnection(connection);
        }
        return id;

    }
}
