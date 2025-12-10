#!/usr/bin/env python3
"""
SHAMIR - Gerador de Áudio com Frequências Divinas
Gera áudio ambiente com frequências sagradas 432Hz e 528Hz
"""

import numpy as np
from scipy.io import wavfile
import os

class DivineAudioGenerator:
    """Gera áudio com frequências de cura e espirituais"""
    
    def __init__(self):
        self.sample_rate = 44100  # CD quality
        self.output_dir = "static/audio"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_sacred_tone(self, frequency, duration=60, volume=0.15):
        """
        Gera um tom senoidal puro
        
        Args:
            frequency: Frequência em Hz (432 ou 528)
            duration: Duração em segundos
            volume: Volume (0.0 a 1.0)
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        wave = volume * np.sin(2 * np.pi * frequency * t)
        return wave
    
    def apply_envelope(self, wave, attack=2.0, release=3.0):
        """Aplica envelope ADSR suave para evitar clicks"""
        samples = len(wave)
        attack_samples = int(attack * self.sample_rate)
        release_samples = int(release * self.sample_rate)
        
        envelope = np.ones(samples)
        
        # Attack (fade in)
        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        
        # Release (fade out)
        if release_samples > 0:
            envelope[-release_samples:] = np.linspace(1, 0, release_samples)
        
        return wave * envelope
    
    def mix_frequencies(self, freq1, freq2, duration=60):
        """
        Mixa duas frequências com harmônicos sutis
        
        Args:
            freq1: Primeira frequência (ex: 432Hz)
            freq2: Segunda frequência (ex: 528Hz)
            duration: Duração em segundos
        """
        # Tom fundamental de cada frequência
        tone1 = self.generate_sacred_tone(freq1, duration, volume=0.10)
        tone2 = self.generate_sacred_tone(freq2, duration, volume=0.10)
        
        # Harmônicos sutis (oitavas)
        harmonic1_1 = self.generate_sacred_tone(freq1 / 2, duration, volume=0.03)
        harmonic2_1 = self.generate_sacred_tone(freq2 / 2, duration, volume=0.03)
        
        # Mix all layers
        mixed = tone1 + tone2 + harmonic1_1 + harmonic2_1
        
        # Normalizar
        mixed = mixed / np.max(np.abs(mixed)) * 0.5
        
        # Aplicar envelope
        mixed = self.apply_envelope(mixed, attack=3.0, release=4.0)
        
        return mixed
    
    def generate_432hz_ambient(self, duration=60):
        """
        432Hz - Frequência da Natureza e Harmonia Universal
        Conhecida como "Afinação de Verdi" ou "Tom Científico"
        """
        print("🎵 Gerando áudio 432Hz (Harmonia Universal)...")
        wave = self.mix_frequencies(432, 432/2, duration)
        
        filepath = os.path.join(self.output_dir, "ambient_432hz.wav")
        wavfile.write(filepath, self.sample_rate, (wave * 32767).astype(np.int16))
        print(f"✅ Salvo: {filepath}")
        return filepath
    
    def generate_528hz_healing(self, duration=60):
        """
        528Hz - Frequência do Amor e Cura DNA
        Conhecida como "MI" da escala Solfeggio
        """
        print("🎵 Gerando áudio 528Hz (Cura e Amor)...")
        wave = self.mix_frequencies(528, 528/2, duration)
        
        filepath = os.path.join(self.output_dir, "healing_528hz.wav")
        wavfile.write(filepath, self.sample_rate, (wave * 32767).astype(np.int16))
        print(f"✅ Salvo: {filepath}")
        return filepath
    
    def generate_divine_blend(self, duration=90):
        """
        Mix divino: 432Hz + 528Hz combinados
        Cria batidas binaurais sutis para meditação profunda
        """
        print("🎵 Gerando mix divino 432Hz + 528Hz...")
        wave = self.mix_frequencies(432, 528, duration)
        
        filepath = os.path.join(self.output_dir, "divine_blend.wav")
        wavfile.write(filepath, self.sample_rate, (wave * 32767).astype(np.int16))
        print(f"✅ Salvo: {filepath}")
        return filepath
    
    def generate_all(self):
        """Gera todos os áudios"""
        print("\n" + "="*50)
        print("🔮 SHAMIR - Gerador de Frequências Divinas")
        print("="*50 + "\n")
        
        self.generate_432hz_ambient(duration=90)
        self.generate_528hz_healing(duration=90)
        self.generate_divine_blend(duration=120)
        
        print("\n✨ Todos os áudios sagrados foram gerados!\n")


def main():
    generator = DivineAudioGenerator()
    generator.generate_all()


if __name__ == "__main__":
    main()
