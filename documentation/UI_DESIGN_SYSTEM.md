# UI/UX Design System & Web Audio Engine

## 1. Design Tokens & Visual Architecture
Smart EMS features a glassmorphic user interface crafted with Vanilla CSS and Bootstrap 5:
- **Glassmorphism Backdrop Filters**: Dynamic frosted-glass effects with CSS `backdrop-filter: blur(16px)` and translucent surfaces.
- **HSL-Tailored Color Palette**: Cohesive semantic gradients (Primary Cyan `#0ea5e9`, Violet `#8b5cf6`, Emerald `#10b981`, Amber `#f59e0b`).
- **Typography & Hierarchy**: Clean typography using Google Inter and Outfit font pairings for executive readability.
- **Adaptive Dark / Light Themes**: Seamless theme toggles with CSS variables stored in `localStorage`.

## 2. Web Audio Notification Synthesizer
Smart EMS incorporates a zero-dependency Web Audio API synthesizer for acoustic user feedback:
- **Audio Chimes**: Synthesized sine/triangle wave harmonics for success actions, warnings, punch-ins, and errors.
- **Dynamic Gain Envelope**: Smooth attack-decay envelope curves preventing audio clipping.
- **Mute / Preference Persistence**: User volume and mute settings saved locally per browser profile.
