{ pkgs, lib, ... }:
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
    docker
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

  # Add tasks section
  tasks = {
    "app:launch" = {
      exec = ''
        ${lib.getExe pkgs.tmux} new-session -d -s dcss
        ${lib.getExe pkgs.tmux} split-window -h -p 20
        ${lib.getExe pkgs.tmux} send-keys -t 1 'python main.py' Enter
        ${lib.getExe pkgs.tmux} attach-session
      '';
    };
    "app:postgres" = {
      exec = ''
        if [ ! -d "./data/postgres" ]; then
          mkdir -p ./data/postgres
        fi
        ${lib.getExe pkgs.docker} run \
          -e POSTGRES_PASSWORD=postgres \
          -p 54320:5432 -d \
          -v ./data/postgres:/var/lib/postgresql/data \
          --name dcss-postgres \
          pgvector/pgvector:pg17
      '';
    };
  };
}
