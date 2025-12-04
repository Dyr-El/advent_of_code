import gleam/dict
import gleam/int
import gleam/io
import gleam/list
import gleam/result
import gleam/string
import utils

pub fn get_grid(path) {
  let input = utils.get_input_lines(path)
  let height = list.length(input)
  let first_line = list.first(input) |> result.unwrap("")
  let width = string.length(first_line)
  let #(_, grid) =
    list.fold(input, #(#(0, 0), dict.new()), fn(acc, str) {
      let cols = string.to_graphemes(str)
      let #(_, col_dict) =
        list.fold(cols, acc, fn(inn_acc, el) {
          let #(#(row, col), mtx_dict) = inn_acc
          #(#(row, col + 1), dict.insert(mtx_dict, #(row, col), el))
        })
      let #(#(row, _col), mtx_dict) = acc
      #(#(row + 1, 0), dict.merge(mtx_dict, col_dict))
    })
  #(height, width, grid)
}

pub fn get_el(grid, coord) {
  dict.get(grid, coord) |> result.unwrap(".")
}

pub fn day4p1(path) -> Int {
  let #(height, width, grid) = get_grid(path)

  let res =
    list.fold(list.range(0, height - 1), 0, fn(cnt, row) {
      list.fold(list.range(0, width - 1), cnt, fn(cnt, col) {
        let neighbour_coords = [
          #(row - 1, col - 1),
          #(row - 1, col),
          #(row - 1, col + 1),
          #(row, col - 1),
          #(row, col + 1),
          #(row + 1, col - 1),
          #(row + 1, col),
          #(row + 1, col + 1),
        ]
        let neighbours =
          list.map(neighbour_coords, fn(coord) { get_el(grid, coord) })
        let cnt_rolls =
          list.fold(neighbours, 0, fn(cnt, el) {
            case el == "@" {
              True -> cnt + 1
              False -> cnt
            }
          })
        case cnt_rolls < 4 {
          True -> {
            // Less than 4 neighbour rolls. Count only if there is a roll here
            case get_el(grid, #(row, col)) == "@" {
              True -> cnt + 1
              False -> cnt
            }
          }
          False -> cnt
        }
      })
    })

  io.println("Day 4 part 1 : " <> int.to_string(res))
  res
}

pub fn day4p2(path) -> Int {
  let input = utils.get_input_lines(path)
  let res = list.length(input)
  io.println("Day 4 part 2 : " <> int.to_string(res))
  res
}
