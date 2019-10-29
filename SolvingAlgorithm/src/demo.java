import lib.Search;

import java.io.*;
import java.util.HashMap;
import java.util.Scanner;

public class demo {

    public static String simpleSolve(String scrambledCube) {
        return new Search().solution(scrambledCube, 21, 100000000, 0, 0);
    }

    public static String getInitalState(String[] input) {
        String[] faceNames = {"Top Face", "Right Face", "Front Face", "Bottom Face", "Left Face", "Back Face"};
        StringBuilder output = new StringBuilder();
        output.append("=== INITIAL STATE ===\n");
        for (int i = 0; i < 6; i++) {
            output.append(faceNames[i]).append(":\n");
            for (int j = 0; j < 3; j++) {
                output.append(input[i].charAt(j)).append(" ").append(input[i].charAt(j + 1)).append(" ").append(input[i].charAt(j + 2)).append("\n");
            }
        }
        output.append("======\n");
        return output.toString();
    }

    public static String parseInput(String[] input) {
        // Possible Colours: W R O Y B G
        /*
        Enter this way
        1 2 3
        4 5 6
        7 8 9
         */
        String front = input[0];
        String left = input[1];
        String right = input[2];
        String top = input[3];
        String bottom = input[4];
        String back = input[5];

        HashMap<Character, Character> mapping = new HashMap<>();
        mapping.put('W', 'D');
        mapping.put('R', 'F');
        mapping.put('G', 'R');
        mapping.put('B', 'L');
        mapping.put('Y', 'U');
        mapping.put('O', 'B');

        StringBuilder scrambled = new StringBuilder();
        for (int i = 0; i < 9; i++) {
            if (!mapping.containsKey(top.charAt(i))) {
                System.out.println("Error - Invalid colour " + top.charAt(i) + " in top face.");
                return null;
            }
            scrambled.append(mapping.get(top.charAt(i)));
        }
        for (int i = 0; i < 9; i++) {
            if (!mapping.containsKey(right.charAt(i))) {
                System.out.println("Error - Invalid colour " + right.charAt(i) + " in right face.");
                return null;
            }
            scrambled.append(mapping.get(right.charAt(i)));
        }
        for (int i = 0; i < 9; i++) {
            if (!mapping.containsKey(front.charAt(i))) {
                System.out.println("Error - Invalid colour " + front.charAt(i) + " in front face.");
                return null;
            }
            scrambled.append(mapping.get(front.charAt(i)));
        }
        for (int i = 0; i < 9; i++) {
            if (!mapping.containsKey(bottom.charAt(i))) {
                System.out.println("Error - Invalid colour " + bottom.charAt(i) + " in bottom face.");
                return null;
            }
            scrambled.append(mapping.get(bottom.charAt(i)));
        }
        for (int i = 0; i < 9; i++) {
            if (!mapping.containsKey(left.charAt(i))) {
                System.out.println("Error - Invalid colour " + left.charAt(i) + " in left face.");
                return null;
            }
            scrambled.append(mapping.get(left.charAt(i)));
        }
        for (int i = 0; i < 9; i++) {
            if (!mapping.containsKey(back.charAt(i))) {
                System.out.println("Error - Invalid colour in " + back.charAt(i) + " back face.");
                return null;
            }
            scrambled.append(mapping.get(back.charAt(i)));
        }
        return scrambled.toString();
    }

    public static void main(String[] args) throws FileNotFoundException {

        try {
            ProcessBuilder processBuilder = new ProcessBuilder();
            processBuilder.command("python", "../../../\"Color Detection\"/colour_sensing.py");
            Process process = processBuilder.start();

            String line;
            BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
            while ((line = errorReader.readLine()) != null) {
                System.err.println(line);
            }

            BufferedReader outReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
            while ((line = outReader.readLine()) != null) {
                System.out.println(line);
            }

            int exitCode = process.waitFor();
            System.out.println("\nExited with error code : " + exitCode);
        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        Scanner in = new Scanner(new FileReader("./test.txt"));
        in.nextLine();
        String[] input = new String[6];
        for (int i = 0; i < 6; i++) {
            input[i] = in.nextLine().trim();
        }
        String parsedInput = parseInput(input);
        String initialState = getInitalState(input);

        System.out.println(initialState);
        if (parsedInput == null) {
            return;
        }
        Search.init();
        String result = simpleSolve(parsedInput);
        System.out.println("Solution: " + result);
    }
}