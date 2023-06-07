# Create an instance of Tkinter frame
from tkinter import Tk
from new_gui.settings.env_gui import get_env_settings, get_parameter_settings, get_game_settings, get_test_settings

main = Tk()

# Set the geometry of Tkinter frame
main.title("Brick Breaker")
main.geometry("600x450")

# Get frames and widgets
env_frame, parameter_button = get_env_settings(main)
parameter_frame = get_parameter_settings(main)
other_frame = get_game_settings(main)
test_frame, widget_vars, button_list = get_test_settings(main)

# Load frame and run
# env_frame.pack(fill='both', expand=1)
# parameter_frame.pack(fill='both', expand=1)
# other_frame.pack(fill='both', expand=1)
test_frame.pack(fill='both', expand=1)
main.mainloop()
