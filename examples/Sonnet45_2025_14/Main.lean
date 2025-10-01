import Sonnet45202514.Input

structure Reindeer where
  name : String
  speed : Nat
  flyTime : Nat
  restTime : Nat
deriving Repr

def parseReindeer (line : String) : Option Reindeer := do
  let words := line.splitOn " "
  if words.length < 15 then none
  else
    let name := words[0]?
    let speed := words[3]?.bind String.toNat?
    let flyTime := words[6]?.bind String.toNat?
    let restTime := words[13]?.bind String.toNat?
    match name, speed, flyTime, restTime with
    | some n, some s, some f, some r => some { name := n, speed := s, flyTime := f, restTime := r }
    | _, _, _, _ => none

def distanceAt (r : Reindeer) (time : Nat) : Nat :=
  let cycleTime := r.flyTime + r.restTime
  let fullCycles := time / cycleTime
  let remainder := time % cycleTime
  let flyInRemainder := min remainder r.flyTime
  fullCycles * r.speed * r.flyTime + flyInRemainder * r.speed

def part1 (input : String) : String :=
  let lines := input.splitOn "\n" |>.filter (fun s => s.trim != "")
  let reindeer := lines.filterMap parseReindeer
  let distances := reindeer.map (fun r => distanceAt r 2503)
  let maxDist := distances.foldl max 0
  toString maxDist

def part2 (input : String) : String :=
  let lines := input.splitOn "\n" |>.filter (fun s => s.trim != "")
  let reindeer := lines.filterMap parseReindeer
  let n := reindeer.length
  
  let rec simulate (timeRemaining : Nat) (points : List Nat) : List Nat :=
    match timeRemaining with
    | 0 => points
    | remaining + 1 =>
      let currentTime := 2503 - remaining
      let distances := reindeer.map (fun r => distanceAt r currentTime)
      let maxDist := distances.foldl max 0
      let newPoints := List.zipWith (fun p d => if d == maxDist then p + 1 else p) points distances
      simulate remaining newPoints
  
  let initialPoints := List.replicate n 0
  let finalPoints := simulate 2503 initialPoints
  let maxPoints := finalPoints.foldl max 0
  toString maxPoints

def main : IO Unit := do
  IO.println (part1 Sonnet45202514.Input.input)
  IO.println (part2 Sonnet45202514.Input.input)
