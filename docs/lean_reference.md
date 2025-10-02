# Lean 4 Quick Reference for Advent of Code

## File I/O and Main Function

```lean
-- Reading input file
def main : IO Unit := do
  let input ← IO.FS.readFile "input.txt"
  let lines := input.trim.splitOn "\n"
  IO.println s!"Part 1: {solvePart1 lines}"
  IO.println s!"Part 2: {solvePart2 lines}"
```

## String Operations

```lean
-- Parsing and manipulation
String.splitOn : String → String → List String
String.trim : String → String
String.toList : String → List Char
String.toInt? : String → Option Int
String.toNat? : String → Option Nat
String.contains : String → String → Bool
String.replace : String → String → String → String
String.length : String → Nat
String.get : String → Fin n → Char
String.data : String → List Char
```

## List Operations

```lean
-- Essential list functions
List.map : (α → β) → List α → List β
List.filter : (α → Bool) → List α → List α
List.foldl : (β → α → β) → β → List α → β
List.foldr : (α → β → β) → β → List α → β
List.zip : List α → List β → List (α × β)
List.zipWith : (α → β → γ) → List α → List β → List γ
List.take : Nat → List α → List α
List.drop : Nat → List α → List α
List.splitAt : Nat → List α → List α × List α
List.chunks : Nat → List α → List (List α)
List.sum : [Add α] [Zero α] → List α → α
List.product : [Mul α] [One α] → List α → α
List.maximum? : [Max α] → List α → Option α
List.minimum? : [Min α] → List α → Option α
List.reverse : List α → List α
List.sort : [Ord α] → List α → List α
List.dedup : [BEq α] → List α → List α
List.contains : [BEq α] → List α → α → Bool
List.count : [BEq α] → List α → α → Nat
List.indexOf? : [BEq α] → List α → α → Option Nat
List.findSome? : (α → Option β) → List α → Option β
List.all : (α → Bool) → List α → Bool
List.any : (α → Bool) → List α → Bool
```

## Array Operations

```lean
-- Arrays for performance
Array.mkEmpty : Nat → Array α
Array.push : Array α → α → Array α
Array.get : Array α → Fin n → α
Array.get! : [Inhabited α] → Array α → Nat → α
Array.get? : Array α → Nat → Option α
Array.set : Array α → Fin n → α → Array α
Array.modify : Array α → Fin n → (α → α) → Array α
Array.map : (α → β) → Array α → Array β
Array.foldl : (β → α → β) → β → Array α → β → β
Array.forM : [Monad m] → Array α → (α → m Unit) → m Unit
#[1, 2, 3] -- Array literal syntax
```

## HashMap/HashSet

```lean
-- For efficient lookups
HashMap.empty : HashMap α β
HashMap.insert : HashMap α β → α → β → HashMap α β
HashMap.find? : HashMap α β → α → Option β
HashMap.contains : HashMap α β → α → Bool
HashMap.toList : HashMap α β → List (α × β)
HashMap.ofList : List (α × β) → HashMap α β

HashSet.empty : HashSet α
HashSet.insert : HashSet α → α → HashSet α
HashSet.contains : HashSet α → α → Bool
HashSet.union : HashSet α → HashSet α → HashSet α
HashSet.inter : HashSet α → HashSet α → HashSet α
```

## Number Operations

```lean
-- Int and Nat operations
Int.natAbs : Int → Nat
Int.gcd : Int → Int → Nat
Int.lcm : Int → Int → Nat
Int.mod : Int → Int → Int
Int.div : Int → Int → Int
Nat.gcd : Nat → Nat → Nat
Nat.lcm : Nat → Nat → Nat
Nat.factors : Nat → List Nat  -- prime factorization
```

## Parsing Patterns

```lean
-- Common parsing patterns for AoC
def parseGrid (input : String) : Array (Array Char) :=
  input.trim.splitOn "\n"
    |>.map (·.data.toArray)
    |>.toArray

def parseNumbers (line : String) : List Int :=
  line.split (·.isWhitespace)
    |>.filterMap String.toInt?

def parseCommaSeparated (line : String) : List String :=
  line.split (· == ',') |>.map String.trim

-- Using Parsec for complex parsing
open Lean.Parsec in
def number : Parsec Nat := do
  let digits ← many1 digit
  return digits.foldl (fun acc d => acc * 10 + d.toNat - '0'.toNat) 0
```

## Common Patterns

```lean
-- BFS/DFS
structure State where
  pos : Nat × Nat
  steps : Nat
  deriving BEq, Hashable

def bfs (start : State) (isGoal : State → Bool) (getNeighbors : State → List State) : Option Nat :=
  let rec go (queue : List State) (visited : HashSet State) : Option Nat :=
    match queue with
    | [] => none
    | s :: rest =>
      if isGoal s then some s.steps
      else if visited.contains s then go rest visited
      else
        let neighbors := getNeighbors s |>.filter (!visited.contains ·)
        go (rest ++ neighbors) (visited.insert s)
  go [start] HashSet.empty

-- Memoization using HashMap
def memoize {α β : Type} [BEq α] [Hashable α] (f : α → β) : α → StateM (HashMap α β) β :=
  fun x => do
    let cache ← get
    match cache.find? x with
    | some y => return y
    | none =>
      let y := f x
      modify (·.insert x y)
      return y

-- Grid navigation
def neighbors4 (pos : Nat × Nat) (width height : Nat) : List (Nat × Nat) :=
  [(pos.1-1, pos.2), (pos.1+1, pos.2), (pos.1, pos.2-1), (pos.1, pos.2+1)]
    |>.filter (fun (x, y) => x < width && y < height)

def neighbors8 (pos : Nat × Nat) (width height : Nat) : List (Nat × Nat) :=
  let deltas := [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
  deltas.filterMap fun (dx, dy) =>
    let x := pos.1 + dx
    let y := pos.2 + dy
    if x < width && y < height then some (x, y) else none
```

## Range and Iteration

```lean
-- Ranges for loops
List.range : Nat → List Nat  -- [0, 1, ..., n-1]
List.range' : Nat → Nat → List Nat  -- [start, start+1, ..., start+n-1]
List.iota : Nat → List Nat  -- [1, 2, ..., n]

-- For loops
for x in [1, 2, 3] do
  IO.println x

for i in [:10] do  -- 0 to 9
  IO.println i

-- Monadic iteration
list.forM : [Monad m] → List α → (α → m Unit) → m Unit
```

## Option/Result Handling

```lean
-- Option utilities
Option.getD : Option α → α → α  -- with default
Option.map : (α → β) → Option α → Option β
Option.bind : Option α → (α → Option β) → Option β
Option.filter : (α → Bool) → Option α → Option α
Option.orElse : Option α → (Unit → Option α) → Option α

-- Pattern matching
match someValue? with
| some x => x * 2
| none => 0
```

## Useful Syntax

```lean
-- String interpolation
s!"The answer is {answer}"

-- List comprehension-like syntax (using map/filter)
[x * 2 | x ← list, x > 5]  -- Not built-in, but achievable with:
list.filter (· > 5) |>.map (· * 2)

-- Lambda syntax
fun x => x + 1
(· + 1)  -- shorthand

-- Pipe operators
list |> List.reverse |> List.take 5
list |>.reverse |>.take 5  -- auto-parenthesizing version

-- Pattern matching in let
let (a, b) := pair
let [x, y, z] := list  -- careful: partial!

-- Guards in match
match x with
| n if n > 0 => "positive"
| 0 => "zero"
| _ => "negative"
```

## Debugging

```lean
-- Printing for debugging
IO.println : ToString α => α → IO Unit
dbg_trace : ToString α => α → β → β
dbgTrace "{x}" fun _ => continuation

-- Assertions
assert! condition
```

## Type Classes for AoC

```lean
-- Common derivations
structure Point where
  x : Int
  y : Int
  deriving BEq, Hashable, Repr, ToString

-- Making custom types work with HashMap
instance : Hashable Point where
  hash p := mixHash p.x.hash p.y.hash
```
