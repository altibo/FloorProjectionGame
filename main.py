import cv2
import pygame
import numpy as np
import sys
import os
from tracking import Tracker
from projection import Projector
from games.demo_game import DemoGame

class FloorGameApp:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.tracker = Tracker(camera_id=0)
        self.projector = Projector()
        self.demo = DemoGame(self.projector)
        
        self.calibrating = False
        self.calib_points = []
        self.running = True
        self.demo_active = True
        
        # Load simple beep sound (generate if needed)
        self.score_sound = self.create_beep()
        
    def create_beep(self):
        # Simple generated beep
        sample_rate = 44100
        duration = 0.2
        frequency = 800
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        wave = np.sin(2 * np.pi * frequency * t) * 0.3
        wave = (wave * 32767).astype(np.int16)
        stereo = np.column_stack((wave, wave))
        sound = pygame.sndarray.make_sound(stereo)
        return sound
    
    def run(self):
        print("Floor Projection Game Foundation")
        print("Press 'c' to calibrate, 'd' to toggle demo, ESC to quit")
        
        while self.running:
            frame, positions = self.tracker.get_frame_and_positions()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        self.calibrating = True
                        self.calib_points = []
                        print("Calibration: Click 4 corners of the projected area in the camera window")
                    elif event.key == pygame.K_d:
                        self.demo_active = not self.demo_active
                        print(f"Demo {'ON' if self.demo_active else 'OFF'}")
            
            # Calibration clicks
            if self.calibrating and frame is not None:
                cv2.imshow("Calibration - Click 4 corners", frame)
                if cv2.waitKey(1) & 0xFF == ord('c'):
                    pass  # already handled
                # Mouse click handling would need callback; simplified for demo
                # In real use: implement mouse callback for points
            
            # Update and draw
            if self.demo_active and positions:
                self.demo.update(positions)
                if self.demo.just_scored:
                    self.score_sound.play()
            
            self.projector.draw(self.demo if self.demo_active else None)
            
            # Show debug camera
            if frame is not None:
                debug = frame.copy()
                for pos in positions:
                    cv2.circle(debug, (int(pos[0]), int(pos[1])), 10, (0, 255, 0), -1)
                cv2.imshow("Camera Debug", debug)
            
            if cv2.waitKey(1) & 0xFF == 27:
                self.running = False
            
            pygame.display.flip()
            pygame.time.Clock().tick(30)
        
        self.tracker.release()
        pygame.quit()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = FloorGameApp()
    app.run()
