# [working-directory: 'tree-sitter-walktime']
# build:
#     tree-sitter generate --abi 14

# [working-directory: 'tree-sitter-walktime']
# parse file_path:
#     tree-sitter parse ../{{file_path}}

# rebuild: build
#     rm ~/.config/helix/runtime/grammars/walktime.so
#     hx -g build
highlights_symlink:
    ln -s $PWD/queries/highlights.scm  ~/.config/helix/runtime/queries/chimera/

helix_log:
    tail --follow ~/.cache/helix/helix.log

pygls_log:
    tail --follow ./pygls.log

echo:
    echo $PWD/queries/highlights.scm
