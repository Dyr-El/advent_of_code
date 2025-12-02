import gleam/int
import gleam/io
import gleam/list
import gleam/string
import utils

pub fn day2p1(path) -> Int {
  let input =
    utils.read_input(path)
    |> string.split(on: ",")
    |> list.map(fn(line) {
      string.split(line, on: "-")
      |> list.map(utils.safe_int_parse)
    })
    |> list.map(fn(list) {
      case list {
        [a, b] -> #(a, b)
        _ -> panic as "Err"
      }
    })
  let invalids =
    input
    |> list.fold([], fn(acc, tup) { list.append(acc, list.range(tup.0, tup.1)) })
  list.each(invalids, fn(el) { echo el })
  let cnt = 4
  io.println("Day 2, Part 1 : " <> int.to_string(cnt))
  cnt
}

pub fn day2p2(path) -> Int {
  let input = utils.get_input_lines(path)
  let cnt = list.length(input)
  io.println("Day 2, Part 2 : " <> int.to_string(cnt))
  cnt
}
