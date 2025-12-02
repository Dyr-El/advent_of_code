

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class Day1a {

    public static void main(String[] args) throws IOException {
        System.out.println("Day 1");
        int i = 0;
        List<String> lines = Files.readAllLines(Path.of("src/input1.txt"));
        int pass = 50;
        for (String line : lines) {
            String r = line.substring(0,1);
            int p = Integer.parseInt(line.substring(1,line.length()));

            p = p%100;
            System.out.println("yyy " + p);
           if (r.equals("L")) {
              pass =  pass  - p;
              if (pass < 0) {
                  pass = 100 + pass;
              }
            } else if (r.equals("R")) {
               pass =  pass  + p;
               if (pass >= 100) {
                   pass =  pass  -100;
               }
            }
            System.out.println("a"+pass);

           if (pass==0) {
               i++;
           }
        }

        System.out.println("Final Password: " + i);



    }
}
