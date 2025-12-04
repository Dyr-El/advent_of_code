import gleam/int
import gleam/io
import gleam/list
import utils

pub fn day5p1(path) -> Int {
  let res = utils.get_input_lines(path) |> list.length

  io.println("Day 5 part 1 : " <> int.to_string(res))
  res
}

pub fn day5p2(path) -> Int {
  let res = utils.get_input_lines(path) |> list.length

  io.println("Day 5 part 2 : " <> int.to_string(res))
  res
}
