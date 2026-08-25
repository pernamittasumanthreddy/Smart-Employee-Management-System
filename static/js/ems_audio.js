/**
 * Smart Employee Management System (Smart EMS)
 * Enterprise Audio & Notification Chime Synthesizer Engine
 * 
 * Generates crystal-clear, studio-quality sound synthesized via Web Audio API.
 * Requires zero external audio files, operates offline with zero latency,
 * and includes user preferences persistence (localStorage).
 */

class EMSAudioEngine {
    constructor() {
        this.audioCtx = null;
        this.soundEnabled = localStorage.getItem('ems_sound_enabled') !== 'false'; // default true
        this.masterVolume = 0.35; // pleasant, non-intrusive default volume
    }

    getAudioContext() {
        if (!this.audioCtx) {
            const AudioContextClass = window.AudioContext || window.webkitAudioContext;
            if (AudioContextClass) {
                this.audioCtx = new AudioContextClass();
            }
        }
        if (this.audioCtx && this.audioCtx.state === 'suspended') {
            this.audioCtx.resume();
        }
        return this.audioCtx;
    }

    isSoundEnabled() {
        return this.soundEnabled;
    }

    toggleSound() {
        this.soundEnabled = !this.soundEnabled;
        localStorage.setItem('ems_sound_enabled', this.soundEnabled ? 'true' : 'false');
        if (this.soundEnabled) {
            this.playChime();
        }
        this.updateUI();
        return this.soundEnabled;
    }

    setSoundEnabled(enabled) {
        this.soundEnabled = Boolean(enabled);
        localStorage.setItem('ems_sound_enabled', this.soundEnabled ? 'true' : 'false');
        this.updateUI();
    }

    /**
     * Studio Modern Dual-Tone Notification Chime (F5 -> A5 with soft exponential decay)
     */
    playChime() {
        if (!this.soundEnabled) return;
        try {
            const ctx = this.getAudioContext();
            if (!ctx) return;

            const now = ctx.currentTime;
            const masterGain = ctx.createGain();
            masterGain.gain.setValueAtTime(this.masterVolume, now);
            masterGain.connect(ctx.destination);

            // Tone 1: 698.46 Hz (F5)
            const osc1 = ctx.createOscillator();
            const gain1 = ctx.createGain();
            osc1.type = 'sine';
            osc1.frequency.setValueAtTime(698.46, now);

            gain1.gain.setValueAtTime(0.01, now);
            gain1.gain.exponentialRampToValueAtTime(0.8, now + 0.02);
            gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.45);

            osc1.connect(gain1);
            gain1.connect(masterGain);
            osc1.start(now);
            osc1.stop(now + 0.46);

            // Tone 2: 880.00 Hz (A5)
            const osc2 = ctx.createOscillator();
            const gain2 = ctx.createGain();
            osc2.type = 'sine';
            osc2.frequency.setValueAtTime(880.00, now + 0.12);

            gain2.gain.setValueAtTime(0.01, now + 0.12);
            gain2.gain.exponentialRampToValueAtTime(0.9, now + 0.14);
            gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.75);

            // Subtle warm overtone (E6: 1318.51 Hz)
            const osc3 = ctx.createOscillator();
            const gain3 = ctx.createGain();
            osc3.type = 'triangle';
            osc3.frequency.setValueAtTime(1318.51, now + 0.12);
            gain3.gain.setValueAtTime(0.005, now + 0.12);
            gain3.gain.exponentialRampToValueAtTime(0.2, now + 0.14);
            gain3.gain.exponentialRampToValueAtTime(0.0001, now + 0.55);

            osc2.connect(gain2);
            gain2.connect(masterGain);
            osc2.start(now + 0.12);
            osc2.stop(now + 0.76);

            osc3.connect(gain3);
            gain3.connect(masterGain);
            osc3.start(now + 0.12);
            osc3.stop(now + 0.56);

        } catch (e) {
            console.warn("EMS Audio playback prevented or unsupported:", e);
        }
    }

    /**
     * Success Fanfare Chime (C5 -> E5 -> G5)
     */
    playSuccess() {
        if (!this.soundEnabled) return;
        try {
            const ctx = this.getAudioContext();
            if (!ctx) return;

            const now = ctx.currentTime;
            const freqs = [523.25, 659.25, 783.99]; // C5, E5, G5
            
            freqs.forEach((freq, idx) => {
                const startTime = now + (idx * 0.09);
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                
                osc.type = 'sine';
                osc.frequency.setValueAtTime(freq, startTime);
                
                gain.gain.setValueAtTime(0.01, startTime);
                gain.gain.exponentialRampToValueAtTime(this.masterVolume * 0.7, startTime + 0.02);
                gain.gain.exponentialRampToValueAtTime(0.001, startTime + (idx === 2 ? 0.6 : 0.25));

                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(startTime);
                osc.stop(startTime + (idx === 2 ? 0.62 : 0.26));
            });
        } catch (e) {
            console.warn("EMS Audio playback error:", e);
        }
    }

    /**
     * Alert / Attention Ping (High double ping)
     */
    playAlert() {
        if (!this.soundEnabled) return;
        try {
            const ctx = this.getAudioContext();
            if (!ctx) return;

            const now = ctx.currentTime;
            [880.0, 1046.5].forEach((freq, idx) => {
                const startTime = now + (idx * 0.1);
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(freq, startTime);
                
                gain.gain.setValueAtTime(0.01, startTime);
                gain.gain.exponentialRampToValueAtTime(this.masterVolume * 0.8, startTime + 0.02);
                gain.gain.exponentialRampToValueAtTime(0.001, startTime + 0.2);

                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(startTime);
                osc.stop(startTime + 0.22);
            });
        } catch (e) {
            console.warn("EMS Audio playback error:", e);
        }
    }

    /**
     * Modern UI Pop / Button Click Feedback
     */
    playPop() {
        if (!this.soundEnabled) return;
        try {
            const ctx = this.getAudioContext();
            if (!ctx) return;

            const now = ctx.currentTime;
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            
            osc.type = 'sine';
            osc.frequency.setValueAtTime(400, now);
            osc.frequency.exponentialRampToValueAtTime(800, now + 0.05);
            
            gain.gain.setValueAtTime(this.masterVolume * 0.4, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.06);

            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(now);
            osc.stop(now + 0.07);
        } catch (e) {
            console.warn("EMS Audio playback error:", e);
        }
    }

    updateUI() {
        const soundToggles = document.querySelectorAll('.ems-sound-toggle-btn');
        soundToggles.forEach(btn => {
            if (this.soundEnabled) {
                btn.innerHTML = '<i class="bi bi-volume-up-fill text-primary me-1"></i><span class="d-none d-md-inline small fw-semibold">Sound On</span>';
                btn.classList.remove('btn-outline-secondary');
                btn.classList.add('btn-outline-primary');
                btn.setAttribute('title', 'Notification Sound: Active (Click to Mute)');
            } else {
                btn.innerHTML = '<i class="bi bi-volume-mute-fill text-danger me-1"></i><span class="d-none d-md-inline small fw-semibold">Muted</span>';
                btn.classList.remove('btn-outline-primary');
                btn.classList.add('btn-outline-secondary');
                btn.setAttribute('title', 'Notification Sound: Muted (Click to Enable)');
            }
        });
    }
}

// Global Singleton Instance
window.emsAudio = new EMSAudioEngine();

// Auto-bind sound controls on DOM load
document.addEventListener('DOMContentLoaded', () => {
    window.emsAudio.updateUI();

    // Attach click listener to sound toggle buttons
    document.querySelectorAll('.ems-sound-toggle-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            window.emsAudio.toggleSound();
        });
    });

    // Attach click listener to sound test buttons
    document.querySelectorAll('.ems-test-sound-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const soundType = btn.getAttribute('data-sound-type') || 'chime';
            if (soundType === 'success') window.emsAudio.playSuccess();
            else if (soundType === 'alert') window.emsAudio.playAlert();
            else if (soundType === 'pop') window.emsAudio.playPop();
            else window.emsAudio.playChime();
        });
    });

    // Automatically play notification chime if page loaded with messages
    const flashAlerts = document.querySelectorAll('.alert');
    if (flashAlerts.length > 0) {
        // Play gentle chime after small delay to ensure user audio context unlocks
        setTimeout(() => {
            window.emsAudio.playChime();
        }, 300);
    }
});
