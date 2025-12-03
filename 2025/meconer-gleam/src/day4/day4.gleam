import gleam/int
import gleam/io
import gleam/list
import gleam/string
import utils

fn get_input(path) {
  utils.get_input_lines(path)
  |> list.map(fn(line) {
    string.to_graphemes(line)
    |> list.map(fn(c) { utils.safe_int_parse(c) })
  })
}

pub fn day4p1(path) -> Int {
  let input = get_input(path)
  let res = list.length(input)
  io.println("Day 4 part 1 : " <> int.to_string(res))
  res
}

pub fn day4p2(path) -> Int {
  let input = get_input(path)
  let res = list.length(input)
  io.println("Day 4 part 2 : " <> int.to_string(res))
  res
}
