{
  description = "Reproducible Playbooks development environment";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs =
    { nixpkgs, ... }:
    let
      supportedSystems = [
        "aarch64-darwin"
        "aarch64-linux"
        "x86_64-darwin"
        "x86_64-linux"
      ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
    in
    {
      devShells = forAllSystems (
        system:
        let
          pkgs = import nixpkgs { inherit system; };
        in
        {
          default = pkgs.mkShell {
            packages = with pkgs; [
              git
              just
              nixfmt-rfc-style
              python312
              shellcheck
              uv
            ];

            env = {
              UV_PYTHON = "${pkgs.python312}/bin/python";
              UV_PYTHON_DOWNLOADS = "never";
            };

            shellHook = ''
              echo "Playbooks development shell"
              echo "Run 'just bootstrap' once, then 'just check'."
            '';
          };
        }
      );

      formatter = forAllSystems (
        system:
        let
          pkgs = import nixpkgs { inherit system; };
        in
        pkgs.nixfmt-rfc-style
      );
    };
}
