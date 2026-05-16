# Space Invaders 🚀

Day 10 of the Python course — apparently I'm a real Python developer now.
That's what they tell you at this point anyway. Good enough for me.

## About

A Space Invaders clone built with pygame-ce (pygame doesn't support Python 3.14 yet).
Shoot down enemy ships, dodge their lasers, and survive as long as you can.

## How to Play

| Key | Action |
|-----|--------|
| ← → | Move left / right |
| Space | Shoot fireball |
| R | Restart (on game over screen) |
| ESC | Quit |

## Features

- 5 enemy ships that bounce and descend
- Enemies randomly fire lasers
- 3 lives with visual indicator (red X when lost)
- Score tracking
- Explosions and sound effects
- Background music
- Game over screen with final score

## Future Ideas

### Gameplay
- Score multiplier — consecutive hits without dying increase points per kill
- Enemies gradually speed up as score increases
- Multiple enemy types with different speeds and point values
- Power-ups dropped by killed enemies — shield, rapid fire, triple shot
- Boss enemy every 20,000 points that takes multiple hits
- Level system — clear all enemies to advance, each level gets harder

### Polish
- Animated explosions cycling through multiple frames
- Particle effects on enemy death
- Screen shake when player is hit
- Start screen before the game begins
- Pause menu with P key
- Sound effect when enemies reach the bottom of the screen
