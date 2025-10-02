import Lean
import Batteries.Data.HashMap
import Batteries.Data.List.Basic
import Batteries.Data.Array.Basic

open Lean Meta Elab Command

-- Extract signature as a string
def getSignature (name : Name) : MetaM String := do
  try
    let info ← getConstInfo name
    let type ← ppExpr info.type
    return s!"{name} : {type}"
  catch _ =>
    return s!"{name} : <not found>"

-- Command to extract all AoC-relevant signatures
elab "#extract_aoc_reference" : command => do
  logInfo "# Lean 4 Quick Reference for Advent of Code\n"
  logInfo "## Automatically Generated Function Signatures\n"
  
  -- File I/O
  logInfo "### File I/O and Main Function\n```lean"
  let ioFunctions := [
    `IO.FS.readFile,
    `IO.FS.writeFile,
    `IO.FS.lines,
    `IO.println,
    `IO.print
  ]
  for name in ioFunctions do
    try
      let sig ← liftTermElabM <| MetaM.run' <| getSignature name
      logInfo sig
    catch _ => pure ()
  logInfo "```\n"
  
  -- String Operations
  logInfo "### String Operations\n```lean"
  let stringFunctions := [
    `String.splitOn,
    `String.trim,
    `String.toList,
    `String.toInt?,
    `String.toNat?,
    `String.contains,
    `String.replace,
    `String.length,
    `String.get,
    `String.data,
    `String.isEmpty,
    `String.append,
    `String.drop,
    `String.take,
    `String.startsWith,
    `String.endsWith,
    `String.toCharArray,
    `String.mk,
    `String.join,
    `String.intercalate
  ]
  for name in stringFunctions do
    try
      let sig ← liftTermElabM <| MetaM.run' <| getSignature name
      logInfo sig
    catch _ => pure ()
  logInfo "```\n"
  
  -- List Operations  
  logInfo "### List Operations\n```lean"
  let listFunctions := [
    `List.map,
    `List.filter,
    `List.filterMap,
    `List.foldl,
    `List.foldr,
    `List.zip,
    `List.zipWith,
    `List.take,
    `List.drop,
    `List.splitAt,
    `List.reverse,
    `List.append,
    `List.join,
    `List.sum,
    `List.prod,
    `List.maximum?,
    `List.minimum?,
    `List.sort,
    `List.dedup,
    `List.contains,
    `List.elem,
    `List.count,
    `List.indexOf?,
    `List.findSome?,
    `List.find?,
    `List.all,
    `List.any,
    `List.range,
    `List.range',
    `List.iota,
    `List.length,
    `List.isEmpty,
    `List.head?,
    `List.tail?,
    `List.head!,
    `List.tail!,
    `List.getLast?,
    `List.partition,
    `List.span,
    `List.groupBy,
    `List.lookup,
    `List.enumFrom,
    `List.enum,
    `List.intersperse,
    `List.intercalate,
    `List.transpose,
    `List.permutations,
    `List.sublists,
    `List.combinations
  ]
  for name in listFunctions do
    try
      let sig ← liftTermElabM <| MetaM.run' <| getSignature name
      logInfo sig
    catch _ => pure ()
  logInfo "```\n"
  
  -- Array Operations
  logInfo "### Array Operations\n```lean"
  let arrayFunctions := [
    `Array.empty,
    `Array.mkEmpty,
    `Array.push,
    `Array.append,
    `Array.get,
    `Array.get!,
    `Array.get?,
    `Array.getD,
    `Array.set,
    `Array.set!,
    `Array.setD,
    `Array.modify,
    `Array.modifyM,
    `Array.map,
    `Array.mapM,
    `Array.filter,
    `Array.filterMap,
    `Array.foldl,
    `Array.foldr,
    `Array.forM,
    `Array.forRevM,
    `Array.size,
    `Array.isEmpty,
    `Array.toList,
    `Array.data,
    `Array.zip,
    `Array.zipWith,
    `Array.unzip,
    `Array.swap,
    `Array.reverse,
    `Array.sort,
    `Array.qsort,
    `Array.insertionSort,
    `Array.binSearch,
    `Array.contains,
    `Array.elem,
    `Array.find?,
    `Array.findSome?,
    `Array.indexOf?,
    `Array.any,
    `Array.all,
    `Array.partition,
    `Array.range,
    `Array.extract,
    `Array.take,
    `Array.drop
  ]
  for name in arrayFunctions do
    try
      let sig ← liftTermElabM <| MetaM.run' <| getSignature name
      logInfo sig
    catch _ => pure ()
  logInfo "```\n"
  
  -- HashMap Operations
  logInfo "### HashMap Operations\n```lean"
  let hashMapFunctions := [
    `Std.HashMap.empty,
    `Std.HashMap.insert,
    `Std.HashMap.insertIfNew,
    `Std.HashMap.find?,
    `Std.HashMap.findD,
    `Std.HashMap.find!,
    `Std.HashMap.contains,
    `Std.HashMap.remove,
    `Std.HashMap.size,
    `Std.HashMap.isEmpty,
    `Std.HashMap.toList,
    `Std.HashMap.toArray,
    `Std.HashMap.keys,
    `Std.HashMap.values,
    `Std.HashMap.fold,
    `Std.HashMap.forM,
    `Std.HashMap.map,
    `Std.HashMap.filter,
    `Std.HashMap.merge,
    `Std.HashMap.ofList
  ]
  for name in hashMapFunctions do
    try
      let sig ← liftTermElabM <| MetaM.run' <| getSignature name
      logInfo sig
    catch _ => pure ()
  logInfo "```\n"
  
  -- HashSet Operations  
  logInfo "### HashSet Operations\n```lean"
  let hashSetFunctions := [
    `Std.HashSet.empty,
    `Std.HashSet.insert,
    `Std.HashSet.contains,
    `Std.HashSet.remove,
    `Std.HashSet.size,
    `Std.HashSet.isEmpty,
    `Std.HashSet.toList,
    `Std.HashSet.toArray,
    `Std.HashSet.union,
    `Std.HashSet.intersect,
    `Std.HashSet.diff,
    `Std.HashSet.fold,
    `Std.HashSet.forM,
    `Std.HashSet.filter,
    `Std.HashSet.all,
    `Std.HashSet.any,
    `Std.HashSet.ofList
  ]
  for name in hashSetFunctions do
    try
      let sig ← liftTermElabM <| MetaM.run' <| getSignature name
      logInfo sig
    catch _ => pure ()
  logInfo "```\n"
  
  -- Int/Nat Operations
  logInfo "### Number Operations\n```lean"
  let numberFunctions := [
    `Int.natAbs,
    `Int.gcd,
    `Int.lcm,
    `Int.mod,
    `Int.div,
    `Int.ediv,
    `Int.emod,
    `Int.toNat,
    `Int.ofNat,
    `Int.neg,
    `Int.abs,
    `Int.sign,
    `Int.min,
    `Int.max,
    `Int.pow,
    `Nat.gcd,
    `Nat.lcm,
    `Nat.factors,
    `Nat.Prime,
    `Nat.mod,
    `Nat.div,
    `Nat.pred,
    `Nat.succ,
    `Nat.min,
    `Nat.max,
    `Nat.pow,
    `Nat.sqrt,
    `Nat.log2,
    `Nat.factorial,
    `Nat.choose,
    `Nat.digits,
    `Nat.toDigits,
    `Nat.ofDigits
  ]
  for name in numberFunctions do
    try
      let sig ← liftTermElabM <| MetaM.run' <| getSignature name
      logInfo sig
    catch _ => pure ()
  logInfo "```\n"
  
  -- Option Operations
  logInfo "### Option Handling\n```lean"
  let optionFunctions := [
    `Option.getD,
    `Option.get!,
    `Option.map,
    `Option.bind,
    `Option.filter,
    `Option.orElse,
    `Option.isSome,
    `Option.isNone,
    `Option.toList,
    `Option.toArray,
    `Option.all,
    `Option.any,
    `Option.zip,
    `Option.zipWith,
    `Option.unzip
  ]
  for name in optionFunctions do
    try
      let sig ← liftTermElabM <| MetaM.run' <| getSignature name
      logInfo sig
    catch _ => pure ()
  logInfo "```\n"
  
  -- Char Operations
  logInfo "### Char Operations\n```lean"
  let charFunctions := [
    `Char.toNat,
    `Char.ofNat,
    `Char.toLower,
    `Char.toUpper,
    `Char.isAlpha,
    `Char.isDigit,
    `Char.isAlphanum,
    `Char.isWhitespace,
    `Char.isLower,
    `Char.isUpper
  ]
  for name in charFunctions do
    try
      let sig ← liftTermElabM <| MetaM.run' <| getSignature name
      logInfo sig
    catch _ => pure ()
  logInfo "```\n"
  
  -- Result/Except Operations
  logInfo "### Result/Except Handling\n```lean"
  let exceptFunctions := [
    `Except.map,
    `Except.mapError,
    `Except.bind,
    `Except.toBool,
    `Except.toOption,
    `Except.tryCatch,
    `Except.orElseLazy,
    `Except.isOk,
    `Except.isError
  ]
  for name in exceptFunctions do
    try
      let sig ← liftTermElabM <| MetaM.run' <| getSignature name
      logInfo sig
    catch _ => pure ()
  logInfo "```\n"
  
  -- StateM Operations (for memoization)
  logInfo "### State Monad (for memoization)\n```lean"
  let stateFunctions := [
    `StateM,
    `StateM.run,
    `StateM.run',
    `get,
    `set,
    `modify,
    `modifyGet,
    `StateT.run,
    `StateT.run'
  ]
  for name in stateFunctions do
    try
      let sig ← liftTermElabM <| MetaM.run' <| getSignature name
      logInfo sig
    catch _ => pure ()
  logInfo "```\n"
  
  -- Additional commonly needed functions
  logInfo "### Utility Functions\n```lean"
  let utilFunctions := [
    `id,
    `Function.comp,
    `Function.const,
    `flip,
    `curry,
    `uncurry,
    `Prod.fst,
    `Prod.snd,
    `Prod.swap,
    `Prod.map,
    `Sum.isLeft,
    `Sum.isRight,
    `Sum.getLeft?,
    `Sum.getRight?,
    `toString,
    `repr,
    `dbg_trace,
    `dbgTrace,
    --`panic!,
    --`assert!,
    --`unreachable!,
    --`sorry,
    `Decidable.decide,
    `Inhabited.default
  ]
  for name in utilFunctions do
    try
      let sig ← liftTermElabM <| MetaM.run' <| getSignature name
      logInfo sig
    catch _ => pure ()
  logInfo "```"

#extract_aoc_reference
