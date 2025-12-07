#!/usr/bin/env ruby

largest_voltage = lambda do |chars|
  (0..(chars.size - 2)).map do |i|
    [chars[i].to_i, chars[(i + 1)..].max].join.to_i
  end.max
end

File.readlines(ARGV[0], chomp: true)
    .map { |line| line.chars.map(&:to_i) }
    .map(&largest_voltage)
    .sum
    .then(&method(:puts))
