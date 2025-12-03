import gleam/int
import gleam/io
import gleam/list
import gleam/result
import gleam/string
import utils

fn rec_largest(lst, acc, size) {
  case size {
    0 -> acc
    _ -> {
      let with_last_removed = list.take(lst, list.length(lst) - size + 1)
      let largest =
        list.max(with_last_removed, int.compare) |> result.unwrap(-1)
      let lst_after_largest =
        list.drop_while(lst, fn(el) { el != largest }) |> list.drop(1)
      rec_largest(lst_after_largest, acc * 10 + largest, size - 1)
    }
  }
}

pub fn largest_twelve(lst: List(Int)) -> Int {
  rec_largest(lst, 0, 12)
}

pub fn largest_two(lst: List(Int)) -> Int {
  rec_largest(lst, 0, 2)
}

pub fn day3p1(path) -> Int {
  let input =
    utils.get_input_lines(path)
    |> list.map(fn(line) {
      string.to_graphemes(line)
      |> list.map(fn(c) { utils.safe_int_parse(c) })
    })
  let largests = list.map(input, largest_two)
  let res = list.fold(largests, 0, fn(acc, el) { acc + el })
  io.println("Day 3 part 1 : " <> int.to_string(res))
  res
}

pub fn day3p2(path) -> Int {
  let input =
    utils.get_input_lines(path)
    |> list.map(fn(line) {
      string.to_graphemes(line)
      |> list.map(fn(c) { utils.safe_int_parse(c) })
    })
  let largests = list.map(input, largest_twelve)
  let res = list.fold(largests, 0, fn(acc, el) { acc + el })
  io.println("Day 3 part 1 : " <> int.to_string(res))
  res
}
