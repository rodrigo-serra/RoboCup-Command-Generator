import tkinter as tk
from gpsr_commands_opt import CommandGenerator
from egpsr_commands import EgpsrCommandGenerator
from utils.utils import *
from gui import CommandGeneratorGUI



if __name__ == "__main__":
    
    ######################################################################
    # LOAD TASK PARAMETERS
    # (objects, rooms, person names)
    ######################################################################
    task_params_file_path = './params/params.yaml'
    task_params = read_yaml_file(file_path=task_params_file_path)  
    
    names = save_parameters(task_params, "names")
    
    rooms_data = save_parameters(task_params, "room_names")
    room_names, location_names, placement_location_names = parse_room_data(rooms_data)
    
    object_data = save_parameters(task_params, "objects")
    object_categories_plural, object_categories_singular, object_names = parse_objects(object_data)
    
    
    ######################################################################
    # CREATE COMMAND GENERATOR
    # ()
    ######################################################################

    generator = CommandGenerator(names, location_names, placement_location_names, room_names, object_names,
                                 object_categories_plural, object_categories_singular)
    
    egpsr_generator = EgpsrCommandGenerator(generator)
    
    
    ######################################################################
    # GENERATE COMMAND ACCORDING TO USER INPUT
    # ()
    ######################################################################
    # In case the user wants to test command generate without user interface
    test = False
    # Generate x random commands
    cmds_number = 500

    if test:
        for _ in range(cmds_number):  
            generator = CommandGenerator(names, location_names, placement_location_names, room_names, object_names,
                                        object_categories_plural, object_categories_singular)
            command = generator.generate_command_start(cmd_category="")
            command = command[0].upper() + command[1:]
            print(command)
    else:    
        root = tk.Tk()
        app = CommandGeneratorGUI(root, generator, egpsr_generator)
        root.mainloop()
        
