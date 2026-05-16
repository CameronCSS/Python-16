# Aliens Attack: Arcade Evolution 🚀

Day 10 of the Python course — a professional-grade, Object-Oriented arcade shooter featuring cinematic boss mechanics, deep statistics tracking, and high-fidelity spritesheet animations.

## About

**Aliens Attack!** is a high-performance arcade shooter built with **pygame-ce**. It features a modular class-based architecture, a comprehensive scoring system, and escalating "endurance-style" challenges that test your reflexes as you climb the leaderboard.

## How to Play

| Key | Action |
|-----|--------|
| Arrows | Move ship (Horizontal & Vertical) |
| Space | Shoot fireball |
| P | Pause / Resume |
| H | View Mission Intel & Rules (from menu) |
| R | Restart (on game over screen) |
| ESC | Quit |

## Features

- **Cinematic Boss Battles**:
    - **Regular Boss**: Spawns every 10,000 points (interval doubles at 250k and 500k). High endurance (20 HP) with dual-laser capabilities.
    - **Mega Boss**: Spawns every 50,000 points (interval doubles at 250k and 500k). Massive health pool (60 HP) for intense late-game standoffs.
    - **Mega Boss Finale**: A spectacular 2-second **Cinematic Slow-Motion** sequence triggers upon defeat, isolating the background music and the thunderous **Explosion 2** audio.
    - **Animated Destructions**: Custom chain-reaction explosions for both Regular and Mega Bosses (scaled up to 256x256).
- **Advanced Player Mechanics**:
    - **OVERSHIELD System**: Earned every 100,000 points. A tactical yellow health bar appears above the ship when active. It provides 2 layers of protection, shattering sequentially before any lives are lost.
    - **Directional Banking**: Ship tilts visually (using `leftship.png`/`rightship.png`) when moving horizontally for a fluid flight feel.
    - **Triple Shot**: Earned exponentially (10k, 20k, 40k...) or upon earning a life when at max health. Active for 30 seconds. Features a dedicated **Power-up Sound**.
    - **Exponential Extra Lives**: Bonus lives become progressively harder to earn as your score climbs, demanding higher point thresholds (5k, 10k, 20k...) to keep the end-game challenge intense.
- **High-Fidelity Animations**:
    - **Dynamic Enemy Explosions**: Every enemy variant features a unique 4-frame animated destruction sequence (using custom 2x2 spritesheets) that is perfectly synchronized to the ship's specific type.
    - **9-Frame Player Explosion**: Smoothly sequenced destruction animation using a custom 3x3 spritesheet.
- **Statistics Tracking & After Action Report**:
    - **Precision Engine**: Real-time tracking of Shots Fired vs. Shots Hit with accuracy percentage reporting.
    - **Defense Status**: Color-coded "Escaped" counter (**Green** for perfect defense, **Red** for breaches).
- **Enemy Variants**:
    - **Standard Ship**: Steady and common (100 pts).
    - **Elite Ship (Blue)**: Faster movement and high fire rate (200 pts).
    - **Ace Ship (Red)**: Lethal double-speed invaders (300 pts).
- **Difficulty & Defense**:
    - **Fleet Expansion**: Two additional enemies join the invasion for every 25,000 points earned, capped at a massive **50 simultaneous enemies** (reached at ~550,000 points).
    - **Elite Squadron Phasing**: Once the 50-enemy cap is hit, the game dynamically shifts spawn weights. Standard ships are slowly phased out, and by **1,000,000 points**, the entire invasion consists solely of Level 3 Ace Ships.
    - **Escape Penalty**: Failing to stop an invader costs Earth **1000 points**.

## Technical Details

- **Language**: Python 3.14+
- **Framework**: Pygame-ce
- **Architecture**:
    - `main.py`: Minimal entry point.
    - `game.py`: Central hub for state management, cinematic slow-motion, and collisions.
    - `player.py`: Weapon systems, OVERSHIELD HUD, and directional sprite banking.
    - `boss.py`: Boss AI, health management, and animated death sequences.
    - `enemy.py`: Weighted spawning, variant AI, and spritesheet animation handling.
    - `sound_manager.py`: Centralized audio asset management with cinematic SFX isolation.

## Future Ideas

- **Particle Effects**: Visual debris and ship fragments for explosions.
- **Screen Shake**: Impact feedback when taking damage or defeating bosses.
- **Leaderboard**: Local high-score tracking.
- **Multi-Phase Bosses**: Changing patterns and speeds as HP drops.
