# FloorProjectionGame

Interactive floor projection foundation using USB camera + projector.

## Features
- USB camera position tracking (OpenCV)
- Fullscreen projection window (Pygame)
- Simple calibration (homography)
- Modular game system
- Demo: stand on colored fields to score points + music

## Setup
```bash
pip install -r requirements.txt
python main.py
```

### Hardware
- USB webcam
- Projector (second display / fullscreen)
- Mount camera + projector close together, pointing down

### Controls
- `c` : Start calibration (click 4 corners of projection area in camera view)
- `d` : Toggle demo game
- `q` or ESC : Quit

Later games can be added in `games/` folder.
