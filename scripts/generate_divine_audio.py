#!/usr/bin/env python3
"""Experimental sine-tone generator for SHAMIR.

This utility generates simple 432 Hz and 528 Hz tones for interface or audio
experiments. It makes no medical, therapeutic, biological, or scientific
claims about those frequencies.
"""

import math
import os
import struct
import wave


class AudioToneGenerator:
    """Generate simple WAV tones using only the Python standard library."""

    def __init__(self):
        self.sample_rate = 44100
        self.output_dir = "static/audio"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_tone(self, frequency, duration=60, volume=0.15):
        """Generate a mono sine tone with a short fade in/out."""
        num_samples = int(self.sample_rate * duration)
        wave_data = []

        for index in range(num_samples):
            time_value = index / self.sample_rate
            sample = volume * math.sin(2 * math.pi * frequency * time_value)

            fade_samples = self.sample_rate * 2
            if index < fade_samples:
                sample *= index / fade_samples
            elif index > num_samples - fade_samples:
                sample *= (num_samples - index) / fade_samples

            wave_data.append(struct.pack("h", int(sample * 32767)))

        return b"".join(wave_data)

    def _write_wav(self, filename, audio_data):
        filepath = os.path.join(self.output_dir, filename)
        with wave.open(filepath, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(audio_data)
        return filepath

    def generate_432hz(self, duration=90):
        return self._write_wav("ambient_432hz.wav", self.generate_tone(432, duration, 0.15))

    def generate_528hz(self, duration=90):
        return self._write_wav("ambient_528hz.wav", self.generate_tone(528, duration, 0.15))

    def generate_blend(self, duration=120):
        num_samples = int(self.sample_rate * duration)
        wave_data = []
        fade_samples = self.sample_rate * 3

        for index in range(num_samples):
            time_value = index / self.sample_rate
            sample = (
                0.10 * math.sin(2 * math.pi * 432 * time_value)
                + 0.10 * math.sin(2 * math.pi * 528 * time_value)
            )

            if index < fade_samples:
                sample *= index / fade_samples
            elif index > num_samples - fade_samples:
                sample *= (num_samples - index) / fade_samples

            wave_data.append(struct.pack("h", int(sample * 32767)))

        return self._write_wav("tone_blend_432_528.wav", b"".join(wave_data))

    def generate_all(self):
        paths = [self.generate_432hz(), self.generate_528hz(), self.generate_blend()]
        for path in paths:
            print(f"Generated: {path}")
        return paths


def main():
    AudioToneGenerator().generate_all()


if __name__ == "__main__":
    main()
