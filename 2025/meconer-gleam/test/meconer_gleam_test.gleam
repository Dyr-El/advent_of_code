import day1/day1
import day2/day2
import gleeunit

pub fn main() -> Nil {
  gleeunit.main()
}

// gleeunit test functions end in `_test`
pub fn day1p1_test() {
  let res = day1.day1p1("src/day1/sample.txt")
  assert res == 3
}

pub fn day1p2_test() {
  let res = day1.day1p2("src/day1/sample.txt")
  assert res == 6
}

pub fn day2p1_test() {
  let res = day2.day2p1("src/day2/sample.txt")
  assert res == 3
}
