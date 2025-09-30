{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-25.05";
  };

  outputs =
    inputs:
    let
      forSystem = inputs.nixpkgs.lib.genAttrs [
        "x86_64-linux"
        "aarch64-linux"
      ];
      pkgsFor = forSystem (system: import inputs.nixpkgs { inherit system; });
    in
    {

      devShells = forSystem (
        system:
        let
          pkgs = pkgsFor."${system}";
        in
        {
          default = pkgs.mkShell {
            venvDir = ".venv";
            UV_PRERELEASE = "allow";
            BINARYEN_HEADER_PATH = "${pkgs.binaryen}/include/binaryen-c.h";
            LD_LIBRARY_PATH="${pkgs.binaryen}/lib";
            packages = [
              pkgs.clang
              pkgs.git-subrepo
              pkgs.just
              pkgs.uv
              pkgs.python313
              pkgs.python313Packages.venvShellHook
              pkgs.binaryen
            ];
            # shellHook = ''
            #     export LD_LIBRARY_PATH="${pkgs.binaryen}/lib:$LD_LIBRARY_PATH"
            #   '';
          };
        }
      );

    };
}
