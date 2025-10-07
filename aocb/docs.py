DOCS = """
# Lean 4 Quick Reference for Advent of Code
## Automatically Generated Function Signatures
### File I/O and Main Function
```lean
IO.FS.readFile (fname : System.FilePath) (a._@._internal._hyg.0 : IO.RealWorld) : EStateM.Result IO.Error IO.RealWorld String
IO.FS.writeFile (fname : System.FilePath) (content : String) (a._@._internal._hyg.0 : IO.RealWorld) : EStateM.Result IO.Error IO.RealWorld Unit
IO.FS.lines (fname : System.FilePath) (a._@._internal._hyg.0 : IO.RealWorld) : EStateM.Result IO.Error IO.RealWorld (Array String)
IO.println (α : Type u_1) (s : α) (a._@._internal._hyg.0 : IO.RealWorld) : EStateM.Result IO.Error IO.RealWorld Unit
IO.print (α : Type u_1) (s : α) (a._@._internal._hyg.0 : IO.RealWorld) : EStateM.Result IO.Error IO.RealWorld Unit
```
### String Operations
```lean
String.splitOn (s : String) (sep : optParam String " ") : List String
String.trim (s : String) : String
String.toList (s : String) : List Char
String.toInt? (s : String) : Option Int
String.toNat? (s : String) : Option Nat
String.contains (s : String) (c : Char) : Bool
String.replace (s : String) (pattern : String) (replacement : String) : String
String.length (a._@._internal._hyg.0 : String) : Nat
String.get (s : String) (p : String.Pos) : Char
String.data (self : String) : List Char
String.isEmpty (s : String) : Bool
String.append (a._@._internal._hyg.0 : String) (a._@._internal._hyg.0 : String) : String
String.drop (s : String) (n : Nat) : String
String.take (s : String) (n : Nat) : String
String.startsWith (s : String) (pre : String) : Bool
String.endsWith (s : String) (post : String) : Bool
String.mk (data : List Char) : String
String.join (l : List String) : String
String.intercalate (s : String) (a._@._internal._hyg.0 : List String) : String
```
### List Operations
```lean
List.map (α : Type u) (β : Type v) (f : α → β) (l : List α) : List β
List.filter (α : Type u) (p : α → Bool) (l : List α) : List α
List.filterMap (α : Type u) (β : Type v) (f : α → Option β) (a._@._internal._hyg.0 : List α) : List β
List.foldl (α : Type u) (β : Type v) (f : α → β → α) (init : α) (a._@._internal._hyg.0 : List β) : α
List.foldr (α : Type u) (β : Type v) (f : α → β → β) (init : β) (l : List α) : β
List.zip (α : Type u) (β : Type v) (a._@._internal._hyg.0 : List α) (a._@._internal._hyg.0 : List β) : List (α × β)
List.zipWith (α : Type u) (β : Type v) (γ : Type w) (f : α → β → γ) (xs : List α) (ys : List β) : List γ
List.take (α : Type u) (n : Nat) (xs : List α) : List α
List.drop (α : Type u) (n : Nat) (xs : List α) : List α
List.splitAt (α : Type u) (n : Nat) (l : List α) : List α × List α
List.reverse (α : Type u) (as : List α) : List α
List.append (α : Type u) (xs : List α) (ys : List α) : List α
List.sum (α : Type u_1) (a._@._internal._hyg.0 : List α) : α
List.mergeSort (α : Type u_1) (xs : List α) (le : autoParam (α → α → Bool) _auto✝) : List α
List.contains (α : Type u) (as : List α) (a : α) : Bool
List.elem (α : Type u) (a : α) (l : List α) : Bool
List.count (α : Type u) (a : α) (a._@._internal._hyg.0 : List α) : Nat
List.findSome? (α : Type u) (β : Type v) (f : α → Option β) (a._@._internal._hyg.0 : List α) : Option β
List.find? (α : Type u) (p : α → Bool) (a._@._internal._hyg.0 : List α) : Option α
List.all (α : Type u) (a._@._internal._hyg.0 : List α) (a._@._internal._hyg.0 : α → Bool) : Bool
List.any (α : Type u) (l : List α) (p : α → Bool) : Bool
List.range (n : Nat) : List Nat
List.range' (start : Nat) (len : Nat) (step : optParam Nat 1) : List Nat
List.length (α : Type u_1) (a._@._internal._hyg.0 : List α) : Nat
List.isEmpty (α : Type u) (a._@._internal._hyg.0 : List α) : Bool
List.head? (α : Type u) (a._@._internal._hyg.0 : List α) : Option α
List.tail? (α : Type u) (a._@._internal._hyg.0 : List α) : Option (List α)
List.head! (α : Type u_1) (a._@._internal._hyg.0 : List α) : α
List.tail! (α : Type u_1) (a._@._internal._hyg.0 : List α) : List α
List.getLast? (α : Type u) (a._@._internal._hyg.0 : List α) : Option α
List.partition (α : Type u) (p : α → Bool) (as : List α) : List α × List α
List.span (α : Type u) (p : α → Bool) (as : List α) : List α × List α
List.lookup (α : Type u) (β : Type v) (a._@._internal._hyg.0 : α) (a._@._internal._hyg.0 : List (α × β)) : Option β
List.intersperse (α : Type u) (sep : α) (l : List α) : List α
List.intercalate (α : Type u) (sep : List α) (xs : List (List α)) : List α
List.transpose (α : Type u_1) (l : List (List α)) : List (List α)
List.sublists (α : Type u_1) (l : List α) : List (List α)
```
### Array Operations
```lean
Array.empty (α : Type u) : Array α
Array.mkEmpty (α : Type u) (c : Nat) : Array α
Array.push (α : Type u) (a : Array α) (v : α) : Array α
Array.append (α : Type u) (as : Array α) (bs : Array α) : Array α
Array.get (α : Type u) (xs : Array α) (i : Nat) (h : i < xs.size) : α
Array.get! (α : Type u) (xs : Array α) (i : Nat) : α
Array.get? (α : Type u) (xs : Array α) (i : Nat) : Option α
Array.getD (α : Type u_1) (a : Array α) (i : Nat) (v₀ : α) : α
Array.set (α : Type u_1) (xs : Array α) (i : Nat) (v : α) (h : autoParam (i < xs.size) _auto✝) : Array α
Array.set! (α : Type u_1) (xs : Array α) (i : Nat) (v : α) : Array α
Array.modify (α : Type u) (xs : Array α) (i : Nat) (f : α → α) : Array α
Array.modifyM (α : Type u) (m : Type u → Type u_1) (xs : Array α) (i : Nat) (f : α → m α) : m (Array α)
Array.map (α : Type u) (β : Type v) (f : α → β) (as : Array α) : Array β
Array.mapM (α : Type u) (β : Type v) (m : Type v → Type w) (f : α → m β) (as : Array α) : m (Array β)
Array.filter (α : Type u) (p : α → Bool) (as : Array α) (start : optParam Nat 0) (stop : optParam Nat as.size) : Array α
Array.filterMap (α : Type u) (β : Type u_1) (f : α → Option β) (as : Array α) (start : optParam Nat 0) (stop : optParam Nat as.size) : Array β
Array.foldl (α : Type u) (β : Type v) (f : β → α → β) (init : β) (as : Array α) (start : optParam Nat 0) (stop : optParam Nat as.size) : β
Array.foldr (α : Type u) (β : Type v) (f : α → β → β) (init : β) (as : Array α) (start : optParam Nat as.size) (stop : optParam Nat 0) : β
Array.forM (α : Type u) (m : Type v → Type w) (f : α → m PUnit) (as : Array α) (start : optParam Nat 0) (stop : optParam Nat as.size) : m PUnit
Array.forRevM (α : Type u) (m : Type v → Type w) (f : α → m PUnit) (as : Array α) (start : optParam Nat as.size) (stop : optParam Nat 0) : m PUnit
Array.size (α : Type u) (a : Array α) : Nat
Array.isEmpty (α : Type u) (xs : Array α) : Bool
Array.toList (α : Type u) (self : Array α) : List α
Array.zip (α : Type u) (β : Type u_1) (as : Array α) (bs : Array β) : Array (α × β)
Array.zipWith (α : Type u) (β : Type u_1) (γ : Type u_2) (f : α → β → γ) (as : Array α) (bs : Array β) : Array γ
Array.unzip (α : Type u) (β : Type u_1) (as : Array (α × β)) : Array α × Array β
Array.swap (α : Type u) (xs : Array α) (i : Nat) (j : Nat) (hi : autoParam (i < xs.size) _auto✝) (hj : autoParam (j < xs.size) _auto✝) : Array α
Array.reverse (α : Type u) (as : Array α) : Array α
Array.qsort (α : Type u_1) (as : Array α) (lt : autoParam (α → α → Bool) _auto✝) (lo : optParam Nat 0) (hi : optParam Nat (as.size - 1)) : Array α
Array.insertionSort (α : Type u_1) (xs : Array α) (lt : autoParam (α → α → Bool) _auto✝) : Array α
Array.binSearch (α : Type) (as : Array α) (k : α) (lt : α → α → Bool) (lo : optParam Nat 0) (hi : optParam Nat (as.size - 1)) : Option α
Array.contains (α : Type u) (as : Array α) (a : α) : Bool
Array.elem (α : Type u) (a : α) (as : Array α) : Bool
Array.find? (α : Type u) (p : α → Bool) (as : Array α) : Option α
Array.findSome? (α : Type u) (β : Type v) (f : α → Option β) (as : Array α) : Option β
Array.any (α : Type u) (as : Array α) (p : α → Bool) (start : optParam Nat 0) (stop : optParam Nat as.size) : Bool
Array.all (α : Type u) (as : Array α) (p : α → Bool) (start : optParam Nat 0) (stop : optParam Nat as.size) : Bool
Array.partition (α : Type u) (p : α → Bool) (as : Array α) : Array α × Array α
Array.range (n : Nat) : Array Nat
Array.extract (α : Type u_1) (as : Array α) (start : optParam Nat 0) (stop : optParam Nat as.size) : Array α
Array.take (α : Type u) (xs : Array α) (i : Nat) : Array α
Array.drop (α : Type u) (xs : Array α) (i : Nat) : Array α
```
### HashMap Operations
```lean
Std.HashMap.empty (α : Type u_1) (β : Type u_2) (capacity : optParam Nat 8) : Std.HashMap α β
Std.HashMap.insert (α : Type u) (β : Type v) (m : Std.HashMap α β) (a : α) (b : β) : Std.HashMap α β
Std.HashMap.insertIfNew (α : Type u) (β : Type v) (m : Std.HashMap α β) (a : α) (b : β) : Std.HashMap α β
Std.HashMap.contains (α : Type u) (β : Type v) (m : Std.HashMap α β) (a : α) : Bool
Std.HashMap.size (α : Type u) (β : Type v) (m : Std.HashMap α β) : Nat
Std.HashMap.isEmpty (α : Type u) (β : Type v) (m : Std.HashMap α β) : Bool
Std.HashMap.toList (α : Type u) (β : Type v) (m : Std.HashMap α β) : List (α × β)
Std.HashMap.toArray (α : Type u) (β : Type v) (m : Std.HashMap α β) : Array (α × β)
Std.HashMap.keys (α : Type u) (β : Type v) (m : Std.HashMap α β) : List α
Std.HashMap.values (α : Type u) (β : Type v) (m : Std.HashMap α β) : List β
Std.HashMap.fold (α : Type u) (β : Type v) (γ : Type w) (f : γ → α → β → γ) (init : γ) (b : Std.HashMap α β) : γ
Std.HashMap.forM (α : Type u) (β : Type v) (m : Type w → Type w') (f : α → β → m PUnit) (b : Std.HashMap α β) : m PUnit
Std.HashMap.map (α : Type u) (β : Type v) (γ : Type w) (f : α → β → γ) (m : Std.HashMap α β) : Std.HashMap α γ
Std.HashMap.filter (α : Type u) (β : Type v) (f : α → β → Bool) (m : Std.HashMap α β) : Std.HashMap α β
Std.HashMap.ofList (α : Type u) (β : Type v) (l : List (α × β)) : Std.HashMap α β
```
### HashSet Operations
```lean
Std.HashSet.empty (α : Type u_1) (capacity : optParam Nat 8) : Std.HashSet α
Std.HashSet.insert (α : Type u) (m : Std.HashSet α) (a : α) : Std.HashSet α
Std.HashSet.contains (α : Type u) (m : Std.HashSet α) (a : α) : Bool
Std.HashSet.size (α : Type u) (m : Std.HashSet α) : Nat
Std.HashSet.isEmpty (α : Type u) (m : Std.HashSet α) : Bool
Std.HashSet.toList (α : Type u) (m : Std.HashSet α) : List α
Std.HashSet.toArray (α : Type u) (m : Std.HashSet α) : Array α
Std.HashSet.union (α : Type u) (m₁ : Std.HashSet α) (m₂ : Std.HashSet α) : Std.HashSet α
Std.HashSet.fold (α : Type u) (β : Type v) (f : β → α → β) (init : β) (m : Std.HashSet α) : β
Std.HashSet.forM (α : Type u) (m : Type v → Type w) (f : α → m PUnit) (b : Std.HashSet α) : m PUnit
Std.HashSet.filter (α : Type u) (f : α → Bool) (m : Std.HashSet α) : Std.HashSet α
Std.HashSet.all (α : Type u) (m : Std.HashSet α) (p : α → Bool) : Bool
Std.HashSet.any (α : Type u) (m : Std.HashSet α) (p : α → Bool) : Bool
Std.HashSet.ofList (α : Type u) (l : List α) : Std.HashSet α
```
### Number Operations
```lean
Int.natAbs (m : Int) : Nat
Int.gcd (m : Int) (n : Int) : Nat
Int.lcm (m : Int) (n : Int) : Nat
Int.ediv (a._@._internal._hyg.0 : Int) (a._@._internal._hyg.0 : Int) : Int
Int.emod (a._@._internal._hyg.0 : Int) (a._@._internal._hyg.0 : Int) : Int
Int.toNat (a._@._internal._hyg.0 : Int) : Nat
Int.ofNat (a._@._internal._hyg.0 : Nat) : Int
Int.neg (n : Int) : Int
Int.sign (a._@._internal._hyg.0 : Int) : Int
Int.pow (m : Int) (a._@._internal._hyg.0 : Nat) : Int
Nat.gcd (m : Nat) (n : Nat) : Nat
Nat.lcm (m : Nat) (n : Nat) : Nat
Nat.mod (a._@._internal._hyg.0 : Nat) (a._@._internal._hyg.0 : Nat) : Nat
Nat.div (x : Nat) (y : Nat) : Nat
Nat.pred (a._@._internal._hyg.0 : Nat) : Nat
Nat.succ (n : Nat) : Nat
Nat.min (n : Nat) (m : Nat) : Nat
Nat.max (n : Nat) (m : Nat) : Nat
Nat.pow (m : Nat) (a._@._internal._hyg.0 : Nat) : Nat
Nat.log2 (n : Nat) : Nat
Nat.toDigits (base : Nat) (n : Nat) : List Char
```
### Option Handling
```lean
Option.getD (α : Type u_1) (opt : Option α) (dflt : α) : α
Option.get! (α : Type u) (a._@._internal._hyg.0 : Option α) : α
Option.map (α : Type u_1) (β : Type u_2) (f : α → β) (a._@._internal._hyg.0 : Option α) : Option β
Option.bind (α : Type u_1) (β : Type u_2) (a._@._internal._hyg.0 : Option α) (a._@._internal._hyg.0 : α → Option β) : Option β
Option.filter (α : Type u_1) (p : α → Bool) (a._@._internal._hyg.0 : Option α) : Option α
Option.orElse (α : Type u_1) (a._@._internal._hyg.0 : Option α) (a._@._internal._hyg.0 : Unit → Option α) : Option α
Option.isSome (α : Type u_1) (a._@._internal._hyg.0 : Option α) : Bool
Option.isNone (α : Type u_1) (a._@._internal._hyg.0 : Option α) : Bool
Option.toList (α : Type u_1) (a._@._internal._hyg.0 : Option α) : List α
Option.toArray (α : Type u_1) (a._@._internal._hyg.0 : Option α) : Array α
Option.all (α : Type u_1) (p : α → Bool) (a._@._internal._hyg.0 : Option α) : Bool
Option.any (α : Type u_1) (p : α → Bool) (a._@._internal._hyg.0 : Option α) : Bool
```
### Char Operations
```lean
Char.toNat (c : Char) : Nat
Char.ofNat (n : Nat) : Char
Char.toLower (c : Char) : Char
Char.toUpper (c : Char) : Char
Char.isAlpha (c : Char) : Bool
Char.isDigit (c : Char) : Bool
Char.isAlphanum (c : Char) : Bool
Char.isWhitespace (c : Char) : Bool
Char.isLower (c : Char) : Bool
Char.isUpper (c : Char) : Bool
```
### Result/Except Handling
```lean
Except.map (ε : Type u) (α : Type u_1) (β : Type u_2) (f : α → β) (a._@._internal._hyg.0 : Except ε α) : Except ε β
Except.mapError (ε : Type u) (ε' : Type u_1) (α : Type u_2) (f : ε → ε') (a._@._internal._hyg.0 : Except ε α) : Except ε' α
Except.bind (ε : Type u) (α : Type u_1) (β : Type u_2) (ma : Except ε α) (f : α → Except ε β) : Except ε β
Except.toBool (ε : Type u) (α : Type u_1) (a._@._internal._hyg.0 : Except ε α) : Bool
Except.toOption (ε : Type u) (α : Type u_1) (a._@._internal._hyg.0 : Except ε α) : Option α
Except.tryCatch (ε : Type u) (α : Type u_1) (ma : Except ε α) (handle : ε → Except ε α) : Except ε α
Except.orElseLazy (ε : Type u) (α : Type u_1) (x : Except ε α) (y : Unit → Except ε α) : Except ε α
Except.isOk (ε : Type u) (α : Type u_1) (a._@._internal._hyg.0 : Except ε α) : Bool
```
### State Monad (for memoization)
```lean
StateM (σ : Type u) (α : Type u) : Type u
modify (σ : Type u) (m : Type u → Type v) (f : σ → σ) : m PUnit
StateT.run (σ : Type u) (m : Type u → Type v) (α : Type u) (x : StateT σ m α) (s : σ) : m (α × σ)
StateT.run' (σ : Type u) (m : Type u → Type v) (α : Type u) (x : StateT σ m α) (s : σ) : m α
```
### Utility Functions
```lean
id (α : Sort u) (a : α) : α
Function.comp (α : Sort u) (β : Sort v) (δ : Sort w) (f : β → δ) (g : α → β) (a._@._internal._hyg.0 : α) : δ
Function.const (α : Sort u) (β : Sort v) (a : α) (a._@._internal._hyg.0 : β) : α
flip (α : Sort u) (β : Sort v) (φ : Sort w) (f : α → β → φ) (a._@._internal._hyg.0 : β) (a._@._internal._hyg.0 : α) : φ
Prod.fst (α : Type u) (β : Type v) (self : α × β) : α
Prod.snd (α : Type u) (β : Type v) (self : α × β) : β
Prod.swap (α : Type u_1) (β : Type u_2) (a._@._internal._hyg.0 : α × β) : β × α
Prod.map (α₁ : Type u₁) (α₂ : Type u₂) (β₁ : Type v₁) (β₂ : Type v₂) (f : α₁ → α₂) (g : β₁ → β₂) (a._@._internal._hyg.0 : α₁ × β₁) : α₂ × β₂
Sum.isLeft (α : Type u_1) (β : Type u_2) (a._@._internal._hyg.0 : α ⊕ β) : Bool
Sum.isRight (α : Type u_1) (β : Type u_2) (a._@._internal._hyg.0 : α ⊕ β) : Bool
Sum.getLeft? (α : Type u_1) (β : Type u_2) (a._@._internal._hyg.0 : α ⊕ β) : Option α
Sum.getRight? (α : Type u_1) (β : Type u_2) (a._@._internal._hyg.0 : α ⊕ β) : Option β
repr (α : Type u_1) (a : α) : Format
Decidable.decide (p : Prop) : Bool
Inhabited.default (α : Sort u) : α


Note: if you decide to use any operation that isn't in this list, it is likely that your solution
will fail to compile.
```
"""
