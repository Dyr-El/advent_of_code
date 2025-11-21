package com.lennell;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public class Day1 {

    public static void main(String[] args) throws IOException {
        System.out.println("Day 1");

        List<Integer> leftNumbers = new ArrayList<>();
        List<Integer> rightNumbers = new ArrayList<>();


        List<String> lines = Files.readAllLines(Path.of("src/com/lennell/input1.txt"));
        for (String line : lines) {
            String[] parts = line.trim().split("\\s+");
            if (parts.length == 2) {
                leftNumbers.add(Integer.parseInt(parts[0]));
                rightNumbers.add(Integer.parseInt(parts[1]));
            }
        }


        List<Integer> sortedLeft = leftNumbers.stream().sorted().toList();
        List<Integer> sortedRight = rightNumbers.stream().sorted().toList();
        if (sortedLeft.size() != sortedRight.size()) {
            System.out.println("Lists are of different sizes");
            return;
        }

        int sum = 0;
        for (int i = 0; i < sortedLeft.size(); i++) {
            sum += Math.abs(sortedLeft.get(i) - sortedRight.get(i));

        }
        System.out.println("Sum of paired elements: " + sum);

        int sum2 = 0;

        for (int l: leftNumbers){
            sum2 += l * (int) rightNumbers.stream().filter( r -> r==l).count();
        }

        System.out.println("Sum part 2 of paired elements: " + sum2);


    }
}
