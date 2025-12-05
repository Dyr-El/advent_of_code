import gleam/int
import gleam/io
import gleam/list
import gleam/result
import gleam/string
import utils

pub fn get_input(path) {
  let input = utils.read_input(path) |> string.split("\n\n")
  case input {
    [a, b] -> {
      #(a, b)
    }

    _ -> {
      #("", "")
    }
  }
}

pub fn day6p1(path) -> Int {
  let res = 0

  io.println("Day 6 part 1 : " <> int.to_string(res))
  res
}

pub fn day6p2(path) -> Int {
  let res = 0
  io.println("Day 6 part 2 : " <> int.to_string(res))
  res
}
