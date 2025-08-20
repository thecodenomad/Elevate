# Elevate

Elevate is a desktop meditation app for inducing mental states (e.g., Sleep, Focus) through audio (binaural beats) and visual stimuli.

# Keybindings

`s` - Show Sidebar
`f` - Enable full screen
`esc` - Escape full screen (when full screen)
`space` - Play the binaural

## Manually Building

You can manually build this by opening the repo in GNOME Builder.

Using flatpak:

```
flatpak-builder --force-clean --user --install builddir io.github.thecodenomad.elevate.json
```

Alternatively, you can use foundry to build:

```
foundry build
```

To create a Flatpak package:

```
foundry export
```

## License

This project is licensed under the GPLv3.0 License - see the COPYING file for details.
