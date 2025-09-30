import binaryen

module = binaryen.ModuleCreate()
params = binaryen.TypeCreate([binaryen.TypeInt32(), binaryen.TypeInt32()], 2)
results = binaryen.TypeInt32()
x = binaryen.LocalGet(module, 0, binaryen.TypeInt32())
y = binaryen.LocalGet(module, 1, binaryen.TypeInt32())
add = binaryen.Binary(module, binaryen.AddInt32(), x, y)
adder = binaryen.AddFunction(module, b"adder", params, results, binaryen.ffi.NULL, 0, add)
binaryen.ModulePrint(module)
binaryen.ModuleDispose(module)
