# VerificationWorstUI

## Run

```sh
source venv/bin/activate && python main.py
```

## Setup

- **Python 3.9.25** via pyenv, venv at `venv/`
- Only dependency: **pygame 2.6.1** (`pip install pygame`)
- No requirements.txt, pyproject.toml, or any build/test/lint config
- `pygame.init()` must run before importing `Ball` (font init order — `Ball._font` is lazy, but some font tools need init first)

## Structure

```
main.py       — Entrypoint: game loop, constants, event handling
src/
  ball.py       — Ball sprite, bounces off walls
  flashlight.py — Rotatable beam from bottom center
  lock.py       — 6-digit sequential verification code lock
  timer.py      — Countdown timer (60s default)
```

No tests, no linters, no type checkers, no CI.

## Constructor signatures (post-refactor)

- `Ball(number, x, y, screen_width=1200, screen_height=700, radius=25)` — pass screen dims, not module constants
- `Flashlight(screen_width, screen_height, beam_width=100, handle_length=60, darkness=200)` — no `radius` param
- `Lock(x=1050, y=80)` — class constants `BOX_SIZE=60`, `BOX_GAP=15`
- `Timer(interval=60000)` — calls `pygame.time.get_ticks()` in `__init__` (requires pygame init)

## Gameplay quirks

- **`ball_group` is a plain list, not `pygame.sprite.Group`** — and balls are never removed (grows unboundedly)
- **Debug shortcut**: press **W** to fill first 5 lock slots (`lock.skip(5)`)
- `COLLECT_TIME = 5000` (hold beam on ball 5s), `BEAM_HALF_ANGLE = 15` degrees, `BEAM_MAX_DIST = 700`, `BALL_MAX = 20`
- Screen: 1200×700
- Beam angle formula: `math.degrees(math.atan2(dy, dx)) + 90` — 0 = straight up, positive = clockwise
