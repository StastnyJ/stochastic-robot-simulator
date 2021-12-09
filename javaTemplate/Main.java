package javaTemplate;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Arrays;

import javaTemplate.Model.Environment;
import javaTemplate.Model.SensorData;

public class Main {

    private static boolean GPS = false; // Change this to true if you want to solve GPS variant

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
                        Solution.Result res;
                        if (GPS) {
                            Integer[] xy = Arrays.stream(line.substring(6).replace("(", "").replace(")", "").split(","))
                                    .map(x -> Integer.parseInt(x)).toArray(Integer[]::new);
                            res = solution.getInstructionGPS(xy[0], xy[1]);
                        } else {
                            res = solution.getInstruction(SensorData.parseSensorData(line.substring(6)));
                        }
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
