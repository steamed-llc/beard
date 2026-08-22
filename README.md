# Local Rendering

[Gemfile](Gemfile) is needed for local rendering, but not needed if you rely on GitHub to render the website remotely.

## Linux Mint

- `sudo apt install ruby-dev build-essential` to enable compilation of some Ruby gems locally.
- add `export GEM_HOME=~/.gem` and `export PATH=$GEM_HOME/bin:$PATH` to `~/.bashrc` so that `gem install` puts all gems in `~/.gem` instead of a system folder.
- `gem install bundler` to install bundler, a gem to manage dependencies of other gems, into `~/.gem`
- run `bundle install` in this folder to install gems declared in [Gemfile](Gemfile) and their dependencies
- run `bundle exec jekyll serve --incremental --livereload` to start a local server at <http://127.0.0.1:4000>

## Docker

- run Docker Desktop
- run `docker compose up` in this folder. If it doesn't work, delete `Gemfile.lock` and try again

# To-do's

- [x] allow 1 background and 1 calibration source run file upload on https://bolder.streamlit.app
