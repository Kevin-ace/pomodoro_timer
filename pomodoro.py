import time
import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
import pygame  # For playing alarm sounds

# Alarm sound file
ALARM_SOUND = "./mixkit-alarm-clock-beep-988.wav"  # Replace with the path to your alarm sound file


class PomodoroTimer:
    def __init__(self, root, work_duration, break_duration, cycles):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("300x400")
        self.root.resizable(False, False)

        self.is_running = False
        self.is_paused = False
        self.work_duration = work_duration
        self.break_duration = break_duration
        self.cycles = cycles
        self.current_cycle = 1
        self.time_left = self.work_duration
        self.mode = "Work"  # Modes: "Work" or "Break"

        # UI Setup
        self.label = tk.Label(root, text="Pomodoro Timer", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.timer_label = tk.Label(root, text=self.format_time(self.time_left), font=("Helvetica", 36))
        self.timer_label.pack(pady=10)

        self.status_label = tk.Label(root, text=f"Cycle {self.current_cycle}/{self.cycles} - {self.mode} Time", font=("Helvetica", 12))
        self.status_label.pack(pady=10)

        self.start_button = tk.Button(root, text="Pause", command=self.pause_timer, width=10)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_timer, width=10)
        self.stop_button.pack(pady=5)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer, width=10)
        self.reset_button.pack(pady=5)

        # Start the timer
        self.run_timer()

    def format_time(self, seconds):
        """Format time in MM:SS format."""
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02d}:{seconds:02d}"

    def update_timer(self):
        """Update the timer display."""
        self.timer_label.config(text=self.format_time(self.time_left))
        self.status_label.config(text=f"Cycle {self.current_cycle}/{self.cycles} - {self.mode} Time")

    def pause_timer(self):
        """Pause or continue the timer."""
        if not self.is_paused:
            self.is_paused = True
            self.start_button.config(text="Continue")
        else:
            self.is_paused = False
            self.start_button.config(text="Pause")

    def stop_timer(self):
        """Stop the timer."""
        self.is_running = False
        self.is_paused = False
        self.start_button.config(text="Pause")
        self.time_left = self.work_duration if self.mode == "Work" else self.break_duration
        self.update_timer()

    def reset_timer(self):
        """Reset the timer."""
        self.is_running = False
        self.is_paused = False
        self.current_cycle = 1
        self.mode = "Work"
        self.time_left = self.work_duration
        self.start_button.config(text="Pause")
        self.update_timer()

    def run_timer(self):
        """Run the timer in a separate thread."""
        def timer():
            self.is_running = True
            while self.current_cycle <= self.cycles and self.is_running:
                while self.time_left > 0 and self.is_running and not self.is_paused:
                    self.time_left -= 1
                    self.update_timer()
                    time.sleep(1)

                if self.is_running and not self.is_paused:
                    self.play_alarm()
                    if self.mode == "Work":
                        if self.current_cycle < self.cycles:
                            self.mode = "Break"
                            self.time_left = self.break_duration
                            messagebox.showinfo("Pomodoro", f"Cycle {self.current_cycle} complete! Time for a break.")
                        else:
                            messagebox.showinfo("Pomodoro", "All cycles complete! Great job!")
                            self.reset_timer()
                            break
                    else:
                        self.mode = "Work"
                        self.time_left = self.work_duration
                        self.current_cycle += 1
                        messagebox.showinfo("Pomodoro", "Break complete! Back to work.")

        threading.Thread(target=timer, daemon=True).start()

    def play_alarm(self):
        """Play an alarm sound."""
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(ALARM_SOUND)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Error playing alarm sound: {e}")


def get_user_inputs():
    """Get user inputs using pop-up dialogs."""
    work_duration = simpledialog.askinteger("Input", "Enter work duration (in minutes):", minvalue=1, initialvalue=25)
    break_duration = simpledialog.askinteger("Input", "Enter break duration (in minutes):", minvalue=1, initialvalue=5)
    cycles = simpledialog.askinteger("Input", "Enter number of cycles:", minvalue=1, initialvalue=1)
    return work_duration * 60, break_duration * 60, cycles


if __name__ == "__main__":
    try:
        root = tk.Tk()
        pygame.init()

        # Get user inputs
        work_time, break_time, total_cycles = get_user_inputs()

        # Initialize the app with user inputs
        app = PomodoroTimer(root, work_time, break_time, total_cycles)
        root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
