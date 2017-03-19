Look at the config-example to see how I've used this script. I use i3-input for the renaming and renumbering of the workspace and the specific workspace number commands. This is not inside of the script; it's used within the config to send to the script. I had issues with escaping when using the i3-input program inside of the config, so I made some script files to wrap those commands.

# Features
* Standardized workspace names: '#: Name'
* Easily Rename and Renumber current workspace
* Go and Move within 1-10 workspace 'blocks'
* Go and Move to next/previous workspace 'block'
* Go and Move directly to specific workspace number

# Usage
You should add keybindings to your i3 config to fit the workflow you want, as I haven't covered all of the usage of this program with the example keybindings.

I swapped the standard 1-10 workspace go and move keybindings to use this script instead. Without the '--exact' argument, this will go and move to the 1-10 workspaces of the current block of 10, e.g. 3 will be 33 if you're in the 31-40 block.

I added two new keybindings to use the directional up and down versions to go and move between the blocks of 10. There's also two for going and moving to a specifically numbered workspace.

Two more rename and renumber the current workspace, and I usually name every workspace and sometimes push them to other blocks.

```
usage: i3-workspacer.py [-h] [--version] {go,move,rename} ...

simplifying large amounts of i3 workspaces

positional arguments:
  {go,move,rename}  check help for each command for required arguments
    go              like the 'workspace number' command
    move            like the 'move container to workspace number' command
    rename          like the 'rename workspace to' command

optional arguments:
  -h, --help        show this help message and exit
  --version         show program's version number and exit
```
## Go command
```
usage: i3-workspacer.py go [-h] [--exact] (-d {up,down,next,prev} | -n NUMBER)

optional arguments:
  -h, --help            show this help message and exit
  --exact               number arguments will be the actual workspace number
                        instead of the index in the current block
  -d {up,down,next,prev}, --direction {up,down,next,prev}
                        operate relative to the current workspace; up/down =
                        +/- 10
  -n NUMBER, --number NUMBER
                        specify workspace number
```
## Move command
```
usage: i3-workspacer.py move [-h] [--exact]
                             (-d {up,down,next,prev} | -n NUMBER)

optional arguments:
  -h, --help            show this help message and exit
  --exact               number arguments will be the actual workspace number
                        instead of the index in the current block
  -d {up,down,next,prev}, --direction {up,down,next,prev}
                        operate relative to the current workspace; up/down =
                        +/- 10
  -n NUMBER, --number NUMBER
                        specify workspace number
```
## Rename command
```
usage: i3-workspacer.py rename [-h] [-na NAME] [-nu NUMBER]

optional arguments:
  -h, --help            show this help message and exit
  -na NAME, --name NAME
                        change the name of the current workspace
  -nu NUMBER, --number NUMBER
                        change the number of the current workspace
```