import gleam/int
import gleam/io
import gleam/list
import gleam/string
import utils

pub fn day2p1(path) -> Int {
  let input = utils.get_input_lines(path)
  let cnt = list.length(input)
  io.println("Day 2, Part 1 : " <> int.to_string(cnt))
  cnt
}

pub fn day2p2(path) -> Int {
  let input = utils.get_input_lines(path)
  let cnt = list.length(input)
  io.println("Day 2, Part 2 : " <> int.to_string(cnt))
  cnt
}
