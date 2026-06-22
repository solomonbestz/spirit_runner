# Ghost Runner 👻

Ghost Runner is a small game built with Python and Pygame Community Edition.

The project is primarily a learning playground to understand how game engines work internally before implementing a proper Entity Component System (ECS).

Instead of jumping directly into ECS, the game is built incrementally to understand:

- game loops
- delta time (dt)
- animations
- sprite sheets
- collisions
- mask collisions
- AI movement
- game state management
- data-oriented thinking

---

## Story

You are a small spirit trapped inside a dark arena.

Magical orbs appear throughout the map.

Each orb grants energy points, but a ghost relentlessly chases you.

Collect as many orbs as possible before the ghost catches you.

Survive for as long as you can.

---

## Features

### Player

- 4-frame idle animation
- 4-frame run animation
- left and right movement support
- sprite flipping for left movement
- boundary clamping

### Collectibles

- Green orb = 10 points
- Yellow orb = 20 points
- Purple orb = 30 points
- Red orb = 40 points

### Ghost

- Spawns randomly
- Chases the player
- Uses pixel-perfect collision

### Collision Debugging

Visual debugging tools were added to understand collisions:

- Red rectangle = player Rect
- Green rectangle = ghost Rect
- Blue overlay = pixel mask

---

## Controls

| Key | Action |
|-----|--------|
| W | Move up |
| A | Move left |
| S | Move down |
| D | Move right |
| ← | Move left |
| → | Move right |
| ↑ | Move up |
| ↓ | Move down |
| R | Restart after Game Over |

---

## Concepts Learned

### Delta Time

Movement is frame-independent.

```python
position += velocity * dt
```

This ensures movement speed remains consistent across different computers.

---

### Sprite Sheets

The player character is animated by slicing frames from a sprite sheet.

Each frame is extracted and scaled before rendering.

---

### Rect Collision

```python
rect1.colliderect(rect2)
```

Detects overlap between bounding rectangles.

---

### Mask Collision

```python
mask.overlap(other_mask, offset)
```

Detects collisions only between visible pixels and ignores transparent areas.

---

### Data-Oriented Thinking

Instead of creating a large Player class, data is separated into small structures.

Examples:

```python
Transform
Orb
Collectible
Animation
Ghost
```

This is the first step toward learning Entity Component System (ECS).

---

## Technologies

- Python 3
- Pygame Community Edition
- uv

---

## Running the Game

Install dependencies:

```bash
uv sync
```

Run:

```bash
uv run python main.py
```

---

## Next Steps

- Introduce proper ECS architecture
- Separate systems from data
- Add health
- Add ghost states
- Add orb effects
- Add increasing difficulty
- Add multiple enemies
- Add menus
- Add sound effects
- Add particles
- Add timers