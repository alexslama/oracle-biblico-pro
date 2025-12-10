#!/usr/bin/env python3
"""
SHAMIR - Gerador de Áudio com Frequências Divinas
Gera áudio ambiente com frequências sagradas 432Hz e 528Hz
USA APENAS BIBLIOTECAS NATIVAS DO PYTHON (sem numpy/scipy)
"""

import wave
import struct
import math
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
        num_samples = int(self.sample_rate * duration)
        wave_data = []
        
        for i in range(num_samples):
            # Gera onda senoidal
            t = i / self.sample_rate
            sample = volume * math.sin(2 * math.pi * frequency * t)
            
            # Aplica envelope suave (fade in/out)
            if i < self.sample_rate * 2:  # 2s fade in
                sample *= i / (self.sample_rate * 2)
            elif i > num_samples - self.sample_rate * 2:  # 2s fade out
                sample *= (num_samples - i) / (self.sample_rate * 2)
            
            # Converte para 16-bit signed integer
            wave_data.append(struct.pack('h', int(sample * 32767)))
        
        return b''.join(wave_data)
    
    def generate_432hz_ambient(self, duration=90):
        """Gera tom 432Hz (Frequência Natural da Terra)"""
        print("🎵 Gerando tom 432Hz (Frequência Natural)...")
        audio_data = self.generate_sacred_tone(432, duration, 0.15)
        
        filepath = os.path.join(self.output_dir, "ambient_432hz.wav")
        with wave.open(filepath, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(audio_data)
        
        print(f"   ✅ Salvo: {filepath}")
        return filepath
    
    def generate_528hz_healing(self, duration=90):
        """Gera tom 528Hz (Frequência de Cura do DNA)"""
        print("🎵 Gerando tom 528Hz (Frequência de Cura)...")
        audio_data = self.generate_sacred_tone(528, duration, 0.15)
        
        filepath = os.path.join(self.output_dir, "healing_528hz.wav")
        with wave.open(filepath, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(audio_data)
        
        print(f"   ✅ Salvo: {filepath}")
        return filepath
    
    def generate_divine_blend(self, duration=120):
        """Mistura 432Hz + 528Hz para frequência divina"""
        print("🎵 Gerando mistura divina (432Hz + 528Hz)...")
        
        num_samples = int(self.sample_rate * duration)
        wave_data = []
        
        for i in range(num_samples):
            t = i / self.sample_rate
            
            # Mistura as duas frequências
            sample_432 = 0.10 * math.sin(2 * math.pi * 432 * t)
            sample_528 = 0.10 * math.sin(2 * math.pi * 528 * t)
            sample = sample_432 + sample_528
            
            # Envelope
            if i < self.sample_rate * 3:  # 3s fade in
                sample *= i / (self.sample_rate * 3)
            elif i > num_samples - self.sample_rate * 3:  # 3s fade out
                sample *= (num_samples - i) / (self.sample_rate * 3)
            
            wave_data.append(struct.pack('h', int(sample * 32767)))
        
        audio_data = b''.join(wave_data)
        
        filepath = os.path.join(self.output_dir, "divine_blend.wav")
        with wave.open(filepath, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(audio_data)
        
        print(f"   ✅ Salvo: {filepath}")
        return filepath
    
    def generate_all(self):
        """Gera todos os arquivos de áudio"""
        print("\n" + "="*60)
        print("🔮 SHAMIR - Gerador de Frequências Divinas")
        print("="*60 + "\n")
        
        self.generate_432hz_ambient()
        self.generate_528hz_healing()
        self.generate_divine_blend()
        
        print("\n" + "="*60)
        print("✅ Todos os arquivos de áudio foram gerados com sucesso!")
        print("="*60 + "\n")

def main():
    generator = DivineAudioGenerator()
    generator.generate_all()

if __name__ == "__main__":
    main()
