import random
import qrcode
from PIL import Image, ImageDraw, ImageFont
from gpsr_commands import CommandGenerator
from egpsr_commands import EgpsrCommandGenerator
from utils.utils import *



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
    test = True
    # Generate x random commands
    cmds_number = 50

    if test:
        for _ in range(cmds_number):  
            generator = CommandGenerator(names, location_names, placement_location_names, room_names, object_names,
                                        object_categories_plural, object_categories_singular)
            command = generator.generate_command_start(cmd_category="")
            command = command[0].upper() + command[1:]
            print(command)
    else:
        user_prompt = "'1': Any command,\n" \
                    "'2': Command without manipulation,\n" \
                    "'3': Command with manipulation,\n" \
                    "'4': Batch of three commands,\n" \
                    "'5': Generate EGPSR setup,\n" \
                    "'0': Generate QR code,\n" \
                    "'q': Quit"
        
        print(user_prompt)
        command = ""
       
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=30,
            border=4,
        )
        
        last_input = '?'
        
        try:
            while True:
                # Read user input
                user_input = input()

                # Check user input
                if user_input == '1':
                    command = generator.generate_command_start(cmd_category="")
                    last_input = "1"
                elif user_input == '2':
                    command = generator.generate_command_start(cmd_category="people")
                    last_input = "2"
                elif user_input == '3':
                    command = generator.generate_command_start(cmd_category="objects")
                    last_input = "3"
                elif user_input == '4':
                    command_one = generator.generate_command_start(cmd_category="people")
                    command_two = generator.generate_command_start(cmd_category="objects")
                    command_three = generator.generate_command_start(cmd_category="")
                    command_list = [command_one[0].upper() + command_one[1:], command_two[0].upper() + command_two[1:],
                                    command_three[0].upper() + command_three[1:]]
                    random.shuffle(command_list)
                    command = command_list[0] + "\n" + command_list[1] + "\n" + command_list[2]
                    last_input = "4"
                elif user_input == "5":
                    command = egpsr_generator.generate_setup()
                    last_input = "5"
                elif user_input == 'q':
                    break
                elif user_input == '0':
                    if last_input == '4':
                        commands = command_list
                    else:
                        commands = [command]
                    for c in commands:
                        qr.clear()
                        qr.add_data(c)
                        qr.make(fit=True)

                        img = qr.make_image(fill_color="black", back_color="white")
                        # Create a drawing object
                        draw = ImageDraw.Draw(img)

                        # Load a font
                        font = ImageFont.truetype("Arial.ttf", 30)

                        # Calculate text size and position
                        text_size = draw.textsize(c, font)
                        if text_size[0] > img.size[0]:
                            font = ImageFont.truetype("Arial.ttf", 15)
                            text_size = draw.textsize(c, font)
                        text_position = ((img.size[0] - text_size[0]) // 2, img.size[1] - text_size[1] - 10)

                        # Draw text on the image
                        draw.text(text_position, c, font=font, fill="black")
                        img.show()
                else:
                    print(user_prompt)
                    continue
                command = command[0].upper() + command[1:]
                print(command)

        except KeyboardInterrupt:
            print("KeyboardInterrupt. Exiting the loop.")

