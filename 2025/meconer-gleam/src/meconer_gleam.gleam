import day1/day1
import day2/day2

pub fn main() -> Nil {
  let path = "src/day1/input.txt"
  day1.day1p1(path)
  day1.day1p2(path)
  let path = "src/day2/input.txt"
  day2.day2p1(path)
  day2.day2p2(path)
  Nil
}
