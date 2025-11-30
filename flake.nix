{
  description = "rembgclipboard";
  
  inputs.nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      python-with-packages = pkgs.python3.withPackages (ps: [ 
        ps.pillow 
        ps.rembg 
      ]);
    in
    {
      packages.${system}.default = pkgs.writeShellApplication {
        name = "rembgclipboard";
        runtimeInputs = [ 
          python-with-packages
          pkgs.wl-clipboard
          pkgs.libnotify
        ];
        text = ''
          python ${self}/src/rembgclipboard/app.py "$@"
        '';
      };
    };
}