# dotfiles


# Overview

This tool automatically configures your machine to my liking using the tiling window manager `i3` with a set of predefined settings.


# Usage

To install all the tooling and apply the default config, execute the following commands.

```sh
git clone https://github.com/diegocarba99/dotfiles.git
cd dotfiles/
python3 ./autoricer.py
```

After executing the script, if no error appeared, restart your session.


# Default configuration

## Basic key bindings
- Mod key - `Windows Key` | `opt`
- Kill focused window - `mod + q`
- Rofi - `mod + d`

## Manage `i3`
- Reload config file - `mod + Shift + c`
- Restart `i3` in place - `mod + Shift + r`
- Exit `i3` - `mod + Shift + e`

## Window Management
- Split horizontally - `mod + h`
- Split vertically - `mod + v`
- Fullscreen - `mod + Shift + f`
- Floating modifider - `mod`
- Toggle floating/tiling - `mod + Shift + Space`
- Resize window - `mod + r`
    - Modify size with arrows
    - Exit resize mode using `Return` or `Escape`
- Modify window gaps - `mod + Shift + g`

## Workspaces
- Move to workspace N - `mod + N`
- Move window to workspace N - `mod + Shift + N`

## Moving around
- Focus left - `mod + Left`
- Focus right - `mod + Right`
- Focus up - `mod + up`
- Focus down - `mod + down`

## Applications
- Terminal - `mod + Return`
- Firefox - `mod + f`
- Nautilus - `mod + n`

## Screen management
By default this repo used `HDMI-1-0` as the default screen. If you want to change
the default screen, check the name using `xrandr` and modify the `i3` config
- Enable alt monitor as main - `mod + Shift + l`
- Disable monitor - `mod + Shift + o`

