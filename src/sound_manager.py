import pygame
import os
import config

class SoundManager:
    def __init__(self):
        self.sound_enabled = False
        self.sounds = {}
        self.music_volume = config.DEFAULT_MUSIC_VOLUME
        self.sound_volume = config.DEFAULT_SOUND_VOLUME
        
        self.init_sounds()
    
    def init_sounds(self):
        """Initialize sound system and load sound effects"""
        try:
            if not pygame.mixer.get_init():
                print("Audio mixer not initialized - running without sound")
                return
            
            self.sound_enabled = True
            
            # Try to load sound effects (if available)
            sound_files = {
                'click': ['click.wav', 'button.wav', 'menu_select.wav'],
                'hit': ['hit.wav', 'punch.wav', 'whack.wav'],
                'miss': ['miss.wav', 'swing.wav']
            }
            
            for sound_name, possible_files in sound_files.items():
                for sound_file in possible_files:
                    try:
                        sound_path = os.path.join(config.SOUND_DIR, sound_file)
                        if os.path.exists(sound_path):
                            sound = pygame.mixer.Sound(sound_path)
                            sound.set_volume(self.sound_volume)
                            self.sounds[sound_name] = sound
                            print(f"Loaded sound effect: {sound_file} as {sound_name}")
                            break
                    except Exception as e:
                        print(f"Could not load {sound_file}: {e}")
                        continue
                
                # If no sound file found, create a simple beep
                if sound_name not in self.sounds:
                    self.create_simple_sound(sound_name)
            
        except Exception as e:
            print(f"Could not initialize sound effects: {e}")
            self.sound_enabled = False
    
    def create_simple_sound(self, sound_name):
        """Create a simple programmatic sound"""
        # Skip creating sounds for now - just print a message
        print(f"No sound effect available for {sound_name}")
    
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if self.sound_enabled and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"Error playing sound {sound_name}: {e}")
    
    def set_sound_volume(self, volume):
        """Set volume for all sound effects"""
        self.sound_volume = max(0.0, min(1.0, volume))
        if self.sound_enabled:
            for sound in self.sounds.values():
                sound.set_volume(self.sound_volume)
    
    def set_music_volume(self, volume):
        """Set music volume"""
        self.music_volume = max(0.0, min(1.0, volume))
        if self.sound_enabled:
            try:
                pygame.mixer.music.set_volume(self.music_volume)
            except:
                pass
    
    def get_sound_volume(self):
        """Get current sound effects volume"""
        return self.sound_volume
    
    def get_music_volume(self):
        """Get current music volume"""
        return self.music_volume
