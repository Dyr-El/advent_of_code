import gleam/int
import gleam/io
import gleam/list
import gleam/result
import gleam/string
import utils

pub fn get_input(path) {
  utils.get_input_lines(path)
  |> list.map(string.trim)
  |> list.map(fn(s) { string.replace(s, "  ", " ") })
  |> list.map(fn(s) { string.replace(s, "  ", " ") })
  |> list.map(fn(s) { string.replace(s, "  ", " ") })
  |> list.map(fn(s) { string.replace(s, "  ", " ") })
  |> list.map(fn(s) { string.replace(s, "  ", " ") })
  |> list.map(fn(s) { string.split(s, " ") })
}

pub fn calc_cols(
  lines: List(List(Int)),
  operators: List(String),
  acc: List(Int),
) -> List(Int) {
  case list.is_empty(list.first(lines) |> result.unwrap([])) {
    True -> acc
    False -> {
      let cols =
        list.fold(lines, [], fn(firsts, lst) {
          [list.first(lst) |> result.unwrap(-1), ..firsts]
        })
      let new_lines = list.map(lines, fn(line) { list.drop(line, 1) })
      let operator = list.first(operators) |> result.unwrap("")
      let new_operators = list.drop(operators, 1)
      let value = case operator {
        "+" -> list.fold(cols, 0, fn(a, n) { a + n })
        "*" -> list.fold(cols, 1, fn(a, n) { a * n })
        _ -> panic as "Err operator"
      }
      calc_cols(new_lines, new_operators, [value, ..acc])
    }
  }
}

pub fn day6p1(path) -> Int {
  let lines = get_input(path)
  let operators = list.last(lines) |> result.unwrap([])
  let lines =
    list.take(lines, list.length(lines) - 1)
    |> list.map(fn(l) {
      list.map(l, fn(s) { int.parse(s) |> result.unwrap(-1) })
    })
  let cols = calc_cols(lines, operators, [])
  let res = list.fold(cols, 0, fn(acc, n) { acc + n })

  io.println("Day 6 part 1 : " <> int.to_string(res))
  res
}

fn find_first(s: String, ch: String) {
  let #(white_sp, _rest) = string.split_once(s, ch) |> result.unwrap(#("", ""))
  string.length(white_sp)
}

pub fn find_idx_of_second_op(operators: String) -> Int {
  let op2 = string.drop_start(operators, 1)
  let idx_plus = find_first(op2, "+")
  let idx_times = find_first(op2, "*")
  int.min(idx_plus, idx_times)
}

pub fn get_ceph_numbers(cols: List(String)) -> List(Int) {
  let first = case list.first(cols) {
    Ok(f) -> f
    Error(_) -> panic as ""
  }
  let len = string.length(first)
  let last_cols =
    list.map(cols, fn(col) { string.slice(col, len - 1, 1) }) |> echo

  []
}

pub fn calc_cols2(
  lines: List(String),
  operators: String,
  acc: List(Int),
) -> List(Int) {
  let operator = string.first(operators) |> result.unwrap("")
  let idx = find_idx_of_second_op(operators)
  let new_operators = string.drop_start(operators, idx + 1)
  let new_lines = list.map(lines, fn(line) { string.drop_start(line, idx + 1) })
  let cols = list.map(lines, fn(line) { string.slice(line, 0, idx) })
  let numbers = get_ceph_numbers(cols)
  acc
}

pub fn day6p2(path) -> Int {
  let lines = utils.get_input_lines(path)
  let operators = list.last(lines) |> result.unwrap("")
  let lines = list.take(lines, list.length(lines) - 1)
  let res = calc_cols2(lines, operators, [])
  let res = 0
  io.println("Day 6 part 2 : " <> int.to_string(res))
  res
}
