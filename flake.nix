{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs =
    inputs:
    let
      forSystem = inputs.nixpkgs.lib.genAttrs [
        "x86_64-linux"
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
            packages = [
            # buildInputs = [
              pkgs.just
              pkgs.uv
              pkgs.python313
              pkgs.python313Packages.venvShellHook
            ];
          };
        }
      );

    };
}
