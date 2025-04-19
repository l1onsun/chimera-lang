[working-directory: 'tree-sitter-walktime']
build:
    tree-sitter generate --abi 14

[working-directory: 'tree-sitter-walktime']
parse file_path:
    tree-sitter parse ../{{file_path}}

rebuild: build
    rm ~/.config/helix/runtime/grammars/walktime.so
    hx -g build
