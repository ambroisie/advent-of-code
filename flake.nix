{
  description = "My Advent of Code solutions";

  inputs = {
    futils = {
      type = "github";
      owner = "numtide";
      repo = "flake-utils";
      ref = "main";
    };

    nixpkgs = {
      type = "github";
      owner = "NixOS";
      repo = "nixpkgs";
      ref = "nixpkgs-unstable";
    };

    pre-commit-hooks = {
      type = "github";
      owner = "cachix";
      repo = "pre-commit-hooks.nix";
      ref = "master";
      inputs = {
        nixpkgs.follows = "nixpkgs";
        nixpkgs-stable.follows = "nixpkgs";
      };
    };
  };

  outputs = { self, futils, nixpkgs, pre-commit-hooks }:
    futils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      {
        checks = {
          pre-commit = pre-commit-hooks.lib.${system}.run {
            src = self;

            hooks = {
              black = {
                enable = true;
              };

              isort = {
                enable = true;
              };

              nixpkgs-fmt = {
                enable = true;
              };
            };
          };
        };

        devShell = pkgs.mkShell {
          buildInputs = with pkgs; [
            (python3.withPackages (ps: with ps; [
              black
              isort
              mypy
              z3
            ]))
            pyright
          ];

          inherit (self.checks.${system}.pre-commit) shellHook;
        };
      });
}
