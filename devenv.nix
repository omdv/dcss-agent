{ pkgs, ... }:
let
  pname = "dcss";
  version = "0.32.1";
  dcssAppImage = pkgs.fetchurl {
    url = "https://github.com/crawl/crawl/releases/download/0.32.1/dcss-0.32.1-linux-console.x86_64.AppImage";
    sha256 = "sha256-nLc8oepthMszyRRAiU5rrI5yDKw8MILSEc5CBMBJUpI=";
    name = "${pname}-${version}.AppImage";
  };
in
{
  packages = with pkgs; [
    (writeShellScriptBin "dcss" ''
      #!${stdenv.shell}
      ${lib.getExe pkgs.appimage-run} ${dcssAppImage} "$@"
    '')
  ];

  languages.python = {
    enable = true;
    package = pkgs.python313;
    venv.enable = true;
    uv = {
      enable = true;
      sync.enable = true;
    };
  };
}
