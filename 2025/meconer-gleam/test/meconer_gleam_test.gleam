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
  assert res == 1_227_775_554
}

pub fn is_valid_p2_inner_test() {
  assert day2.is_valid_p2_inner("1", "1111", 1) == False
  assert day2.is_valid_p2_inner("11", "1111", 2) == False
  assert day2.is_valid_p2_inner("11", "1121", 2) == True
  assert day2.is_valid_p2_inner("12", "1121", 2) == True
  assert day2.is_valid_p2_inner("12", "1212", 2) == False
  assert day2.is_valid_p2_inner("12", "121212", 2) == False
}

pub fn is_valid_p2_test() {
  assert day2.is_valid_p2(112_233) == True
  assert day2.is_valid_p2(123_444) == True
  assert day2.is_valid_p2(111_122) == True
  assert day2.is_valid_p2(121_212) == False
}

pub fn day2p2_test() {
  let res = day2.day2p2("src/day2/sample.txt")
  assert res == 4_174_379_265
}
