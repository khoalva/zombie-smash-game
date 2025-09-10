"""
Sound and music management system
"""
import pygame
import os
import config
from typing import Dict, List, Optional

class SoundManager:
    def __init__(self):
        self.sound_enabled = False
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.music_volume = config.DEFAULT_MUSIC_VOLUME
        self.sound_volume = config.DEFAULT_SOUND_VOLUME
        self.background_music_loaded = False
        
        self.init_sounds()
    
    def init_sounds(self) -> None:
        """Initialize sound system and load sound effects"""
        try:
            if not pygame.mixer.get_init():
                print("Audio mixer not initialized - running without sound")
                return
            
            self.sound_enabled = True
            self._load_sound_effects()
            self._load_background_music()
            
        except Exception as e:
            print(f"Could not initialize sound effects: {e}")
            self.sound_enabled = False
    
    def _load_sound_effects(self) -> None:
        """Load sound effect files"""
        sound_files = {
            config.SoundType.CLICK.value: ['click.wav', 'button.wav', 'menu_select.wav'],
            config.SoundType.HIT.value: ['hit.wav', 'punch.wav', 'whack.wav'],
            config.SoundType.MISS.value: ['miss.wav', 'swing.wav']
        }
        
        for sound_name, possible_files in sound_files.items():
            self._try_load_sound_files(sound_name, possible_files)
    
    def _try_load_sound_files(self, sound_name: str, possible_files: List[str]) -> None:
        """Try to load sound files from a list of possibilities"""
        for sound_file in possible_files:
            try:
                sound_path = os.path.join(config.SOUND_DIR, sound_file)
                if os.path.exists(sound_path):
                    sound = pygame.mixer.Sound(sound_path)
                    sound.set_volume(self.sound_volume)
                    self.sounds[sound_name] = sound
                    print(f"Loaded sound effect: {sound_file} as {sound_name}")
                    return
            except Exception as e:
                print(f"Could not load {sound_file}: {e}")
                continue
        
        # If no sound file found, skip (no fallback sound)
        print(f"No sound effect available for {sound_name}")
    
    def _load_background_music(self) -> None:
        """Load background music"""
        music_files = [
            "music.wav", "background_music.mp3", "background_music.wav", 
            "background_music.ogg", "music.mp3", "sound_1.wav"
        ]
        
        for music_file in music_files:
            try:
                music_path = os.path.join(config.SOUND_DIR, music_file)
                if os.path.exists(music_path):
                    pygame.mixer.music.load(music_path)
                    self.background_music_loaded = True
                    pygame.mixer.music.set_volume(self.music_volume)
                    print(f"Loaded background music: {music_file}")
                    return
            except Exception as e:
                print(f"Could not load {music_file}: {e}")
                continue
        
        print("No background music found in assets/sounds/")
    
    def play_sound(self, sound_name: str) -> None:
        """Play a sound effect"""
        if self.sound_enabled and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"Error playing sound {sound_name}: {e}")
    
    def start_background_music(self) -> None:
        """Start playing background music"""
        if self.sound_enabled and self.background_music_loaded:
            try:
                pygame.mixer.music.play(-1)  # Loop indefinitely
                print("Background music started")
            except Exception as e:
                print(f"Could not start background music: {e}")
    
    def stop_background_music(self) -> None:
        """Stop background music"""
        if self.sound_enabled:
            try:
                pygame.mixer.music.stop()
            except:
                pass
    
    def set_sound_volume(self, volume: float) -> None:
        """Set volume for all sound effects"""
        self.sound_volume = max(config.MIN_VOLUME, min(config.MAX_VOLUME, volume))
        if self.sound_enabled:
            for sound in self.sounds.values():
                sound.set_volume(self.sound_volume)
    
    def set_music_volume(self, volume: float) -> None:
        """Set music volume"""
        self.music_volume = max(config.MIN_VOLUME, min(config.MAX_VOLUME, volume))
        if self.sound_enabled and self.background_music_loaded:
            try:
                pygame.mixer.music.set_volume(self.music_volume)
            except:
                pass
    
    def get_sound_volume(self) -> float:
        """Get current sound effects volume"""
        return self.sound_volume
    
    def get_music_volume(self) -> float:
        """Get current music volume"""
        return self.music_volume
    
    def cleanup(self) -> None:
        """Clean up sound resources"""
        self.stop_background_music()
        if self.sound_enabled:
            try:
                pygame.mixer.quit()
            except:
                pass
