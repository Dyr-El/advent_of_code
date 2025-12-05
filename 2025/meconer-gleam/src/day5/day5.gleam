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

pub fn is_fresh(ingr: Int, ranges: List(#(Int, Int))) -> Bool {
  list.any(ranges, fn(range) {
    let #(first, last) = range
    ingr >= first && ingr <= last
  })
}

pub fn parse_ranges(ranges_str) {
  string.split(ranges_str, "\n")
  |> list.map(fn(line) {
    string.split(line, on: "-")
    |> list.map(fn(s) { int.parse(s) |> result.unwrap(0) })
  })
  |> list.map(fn(rl) {
    case rl {
      [a, b] -> #(a, b)
      _ -> panic as "Err"
    }
  })
}

pub fn day5p1(path) -> Int {
  let #(ranges, ingredients) = get_input(path)
  let ranges = parse_ranges(ranges)
  let ingredients =
    string.split(ingredients, "\n")
    |> list.map(fn(s) { int.parse(s) |> result.unwrap(0) })
  let fresh_ingredients =
    list.filter(ingredients, fn(ing) { is_fresh(ing, ranges) })
  let res = list.length(fresh_ingredients)

  io.println("Day 5 part 1 : " <> int.to_string(res))
  res
}

pub fn combine_ranges(r1: #(Int, Int), r2: #(Int, Int)) -> List(#(Int, Int)) {
  let #(r1s, r1e) = r1
  let #(r2s, r2e) = r2

  case r1s < r2s {
    True ->
      case r1e < r2s {
        True -> [r1, r2]
        False -> [#(r1s, int.max(r1e, r2e))]
      }
    False ->
      case r1s == r2s {
        True -> [#(r1s, int.max(r1e, r2e))]
        False -> {
          // r2 starts before r1
          case r2e < r1s {
            True -> [r2, r1]
            False -> [#(r2s, int.max(r1e, r2e))]
          }
        }
      }
  }
}

pub fn overlaps(r1, r2) {
  let #(r1s, r1e) = r1
  let #(r2s, r2e) = r2
  case r1s < r2s {
    True -> r1e >= r2s
    False -> r2e >= r1s
  }
}

pub fn insert_fn(range_list: List(#(Int, Int))) -> List(#(Int, Int)) {
  list.fold(range_list, [], fn(acc, range) {
    case acc {
      [] -> [range]
      [a_range] -> {
        // Only 1 range accumulated
        let combined = combine_ranges(a_range, range)
        combined
      }
      acc -> {
        let #(overlapping, non_overlapping) =
          list.partition(acc, fn(rng) { overlaps(range, rng) })
        let new_range =
          list.fold(overlapping, range, fn(acc_range, rng) {
            let combined = combine_ranges(acc_range, rng)
            case combined {
              [cr] -> cr
              _ -> panic as "Err"
            }
          })
        [new_range, ..non_overlapping]
      }
    }
  })
}

pub fn day5p2(path) -> Int {
  let #(ranges, _ingredients) = get_input(path)
  let ranges = parse_ranges(ranges)
  let new_ranges = insert_fn(ranges)

  let res =
    list.fold(new_ranges, 0, fn(acc, range) {
      let #(rs, re) = range
      acc + re - rs + 1
    })
  io.println("Day 5 part 2 : " <> int.to_string(res))
  res
}
