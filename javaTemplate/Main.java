package javaTemplate;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

import javaTemplate.Model.Environment;

public class Main {
    public static void main(String[] args) throws Exception {
        final ServerSocket srv = new ServerSocket(8080);
        Solution solution = null;
        try {
            while (true) {
                Socket clientSocket = srv.accept();
                BufferedReader reader = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);
                String line;
                do {
                    line = reader.readLine();
                    if (line != null && line.equals("END")) {
                        srv.close();
                        return;
                    }
                    if (line != null && line.startsWith("INIT: ")) {
                        solution = new Solution(Environment.parseEnvironment(line.substring(6)));
                        out.println("DONE");
                        out.flush();
                    }
                    if (line != null && line.startsWith("STEP")) {
                        Solution.Result res = solution.getInstruction();
                        out.println(res.toString());
                        out.flush();
                    }
                } while (line != null && !line.isEmpty());
            }
        } finally {
            if (!srv.isClosed())
                srv.close();
        }
    }
}
