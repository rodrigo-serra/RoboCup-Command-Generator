import random
import re
import itertools
import warnings
from utils.utils import *

class CommandGenerator:

    def __init__(self, person_names, location_names, placement_location_names, room_names, object_names,
                 object_categories_plural, object_categories_singular):
        
        self.person_names = person_names
        self.location_names = location_names
        self.placement_location_names = placement_location_names
        self.room_names = room_names
        self.object_names = object_names
        self.object_categories_plural = object_categories_plural
        self.object_categories_singular = object_categories_singular

        # Load grammar data
        grammar_data_file_path = './params/grammar.yaml'
        grammar_data = read_yaml_file(file_path=grammar_data_file_path)

        self.verb_dict = grammar_data['verb_dict']
        self.prep_dict = grammar_data['prep_dict']
        self.connector_list = grammar_data['connector_list']
        self.gesture_person_list = grammar_data['gesture_person_list']
        self.pose_person_list = grammar_data['pose_person_list']
        self.gesture_person_plural_list = grammar_data['gesture_person_plural_list']
        self.pose_person_plural_list = grammar_data['pose_person_plural_list']
        self.person_info_list = grammar_data['person_info_list']
        self.object_comp_list = grammar_data['object_comp_list']
        self.talk_list = grammar_data['talk_list']
        self.question_list = grammar_data['question_list']
        self.color_list = grammar_data['color_list']
        self.clothe_list = grammar_data['clothe_list']
        self.clothes_list = grammar_data['clothes_list']

        # Initialize color clothing combinations
        self.color_clothe_list = [f"{a} {b}" for a, b in itertools.product(self.color_list, self.clothe_list)]
        self.color_clothes_list = [f"{a} {b}" for a, b in itertools.product(self.color_list, self.clothes_list)]

    def generate_command_start(self, cmd_category="", difficulty=0):
        # Load commands
        cmd_data_file_path = './params/commands.yaml'
        cmd_data = read_yaml_file(file_path=cmd_data_file_path)
        
        # HRI and people perception commands
        person_cmd_list = save_parameters(cmd_data, "person_cmd_list")

        # Object manipulation and perception commands
        object_cmd_list = save_parameters(cmd_data, "object_cmd_list")

         # Select command list
        cmd_list = {
            "people": person_cmd_list,
            "objects": object_cmd_list
        }.get(cmd_category, person_cmd_list if random.random() > 0.5 else object_cmd_list)

        command = random.choice(cmd_list)
        command_string = self.get_command_string(command, cmd_category, difficulty)

        if command_string == "WARNING":
            return command_string

        # Replace placeholders with values
        for ph in re.findall(r'(\{\w+\})', command_string, re.DOTALL):
            command_string = command_string.replace(ph, self.insert_placeholders(ph))

        # Adjust for articles (a/an)
        command_string = self.adjust_articles(command_string)

        # Eliminate double mentions of location
        command_string = self.eliminate_double_mentions(command_string)

        return command_string.replace('{', '').replace('}', '')

    def get_command_string(self, command, cmd_category, difficulty):
        # Define command patterns
        command_patterns = {
            "goToLoc": "{goVerb} {toLocPrep} the {loc_room} then " + self.generate_command_followup("atLoc", cmd_category, difficulty),
            "takeObjFromPlcmt": "{takeVerb} {art} {obj_singCat} {fromLocPrep} the {plcmtLoc} and " + self.generate_command_followup("hasObj", cmd_category, difficulty),
            "findPrsInRoom": "{findVerb} a {gestPers_posePers} {inLocPrep} the {room} and " + self.generate_command_followup("foundPers", cmd_category, difficulty),
            "findObjInRoom": "{findVerb} {art} {obj_singCat} {inLocPrep} the {room} then " + self.generate_command_followup("foundObj", cmd_category, difficulty),
            "meetPrsAtBeac": "{meetVerb} {name} {inLocPrep} the {room} and " + self.generate_command_followup("foundPers", cmd_category, difficulty),
            "countObjOnPlcmt": "{countVerb} {plurCat} there are {onLocPrep} the {plcmtLoc}",
            "countPrsInRoom": "{countVerb} {gestPersPlur_posePersPlur} are {inLocPrep} the {room}",
            "tellPrsInfoInLoc": "{tellVerb} me the {persInfo} of the person {inRoom_atLoc}",
            "tellObjPropOnPlcmt": "{tellVerb} me what is the {objComp} object {onLocPrep} the {plcmtLoc}",
            "talkInfoToGestPrsInRoom": "{talkVerb} {talk} {talkPrep} the {gestPers} {inLocPrep} the {room}",
            "answerToGestPrsInRoom": "{answerVerb} the {question} {ofPrsPrep} the {gestPers} {inLocPrep} the {room}",
            "followNameFromBeacToRoom": "{followVerb} {name} {fromLocPrep} the {loc} {toLocPrep} the {room}",
            "guideNameFromBeacToBeac": "{guideVerb} {name} {fromLocPrep} the {loc} {toLocPrep} the {loc_room}",
            "guidePrsFromBeacToBeac": "{guideVerb} the {gestPers_posePers} {fromLocPrep} the {loc} {toLocPrep} the {loc_room}",
            "guideClothPrsFromBeacToBeac": "{guideVerb} the person wearing a {colorClothe} {fromLocPrep} the {loc} {toLocPrep} the {loc_room}",
            "bringMeObjFromPlcmt": "{bringVerb} me {art} {obj} {fromLocPrep} the {plcmtLoc}",
            "tellCatPropOnPlcmt": "{tellVerb} me what is the {objComp} {singCat} {onLocPrep} the {plcmtLoc}",
            "greetClothDscInRm": "{greetVerb} the person wearing {art} {colorClothe} {inLocPrep} the {room} and " + self.generate_command_followup("foundPers", cmd_category, difficulty),
            "greetNameInRm": "{greetVerb} {name} {inLocPrep} the {room} and " + self.generate_command_followup("foundPers", cmd_category, difficulty),
            "meetNameAtLocThenFindInRm": "{meetVerb} {name} {atLocPrep} the {loc} then {findVerb} them {inLocPrep} the {room}",
            "countClothPrsInRoom": "{countVerb} people {inLocPrep} the {room} are wearing {colorClothes}",
            "tellPrsInfoAtLocToPrsAtLoc": "{tellVerb} the {persInfo} of the person {atLocPrep} the {loc} to the person {atLocPrep} the {loc2}",
            "followPrsAtLoc": "{followVerb} the {gestPers_posePers} {inRoom_atLoc}"
        }
        
        return command_patterns.get(command, "WARNING")

    def generate_command_followup(self, type, cmd_category="", difficulty=0):
        """Generates follow-up commands based on the type."""
        followup_commands = {
            "atLoc": {
                "people": ["findPrs", "meetName"],
                "objects": ["findObj"],
                "default": ["findPrs", "findObj"]
            },
            "hasObj": ["placeObjOnPlcmt", "deliverObjToMe", "deliverObjToPrsInRoom", "deliverObjToNameAtBeac"],
            "foundPers": ["talkInfo", "answerQuestion", "followPrs", "followPrsToRoom", "guidePrsToBeacon"],
            "foundObj": ["takeObj"]
        }

        # Determine command list based on type and category
        if type in followup_commands:
            if type == "atLoc":
                cmd_list = followup_commands[type].get(cmd_category, followup_commands[type]["default"])
            else:
                cmd_list = followup_commands[type]
        else:
            return "WARNING"

        command = random.choice(cmd_list)

        # Define follow-up command patterns
        followup_patterns = {
            "findObj": "{findVerb} {art} {obj_singCat} and {followup}",
            "findPrs": "{findVerb} {art} {gestPers_posePers} and {followup}",
            "meetName": "{meetVerb} {name} and {followup}",
            "placeObjOnPlcmt": "{placeVerb} it {onLocPrep} the {plcmtLoc2}",
            "deliverObjToMe": "{deliverVerb} it to me",
            "deliverObjToPrsInRoom": "{deliverVerb} it {deliverPrep} the {gestPers_posePers} {inLocPrep} the {room}",
            "deliverObjToNameAtBeac": "{deliverVerb} it {deliverPrep} {name} {inLocPrep} the {room}",
            "talkInfo": "{talkVerb} {talk}",
            "answerQuestion": "{answerVerb} a {question}",
            "followPrs": "{followVerb} them",
            "followPrsToRoom": "{followVerb} them {toLocPrep} the {loc2_room2}",
            "guidePrsToBeacon": "{guideVerb} them {toLocPrep} the {loc2_room2}",
            "takeObj": "{takeVerb} it and {followup}"
        }

        # Get the follow-up pattern for the command
        followup_command = followup_patterns.get(command, "WARNING")

        # Replace placeholders
        if "{followup}" in followup_command:
            # Mapping command to follow-up types
            followup_type_map = {
                "findObj": "foundObj",
                "takeObj": "hasObj"
            }

            # Determine the follow-up type based on the command
            followup_type = next(
                (ftype for cmd_key, ftype in followup_type_map.items() if cmd_key in command), 
                "foundPers"  # Default to "foundPers" if no match
            )

            # Generate follow-up command
            followup = self.generate_command_followup(followup_type)

            # Replace placeholder with the generated follow-up
            followup_command = followup_command.replace("{followup}", followup)


        return followup_command


    def insert_placeholders(self, ph):
        """Inserts the appropriate value for a given placeholder."""
        ph = ph.strip('{}')

        """Cases such as obj_singCat, loc2_room2, ..., it choose randomly loc2 or room2, in loc2_room2 example."""
        if len(ph.split('_')) > 1:
            ph = random.choice(ph.split('_'))

        placeholder_map = {
            # Verb mappings
            "goVerb": lambda: random.choice(self.verb_dict["go"]),
            "takeVerb": lambda: random.choice(self.verb_dict["take"]),
            "findVerb": lambda: random.choice(self.verb_dict["find"]),
            "meetVerb": lambda: random.choice(self.verb_dict["meet"]),
            "countVerb": lambda: random.choice(self.verb_dict["count"]),
            "tellVerb": lambda: random.choice(self.verb_dict["tell"]),
            "deliverVerb": lambda: random.choice(self.verb_dict["deliver"]),
            "talkVerb": lambda: random.choice(self.verb_dict["talk"]),
            "answerVerb": lambda: random.choice(self.verb_dict["answer"]),
            "followVerb": lambda: random.choice(self.verb_dict["follow"]),
            "placeVerb": lambda: random.choice(self.verb_dict["place"]),
            "guideVerb": lambda: random.choice(self.verb_dict["guide"]),
            "greetVerb": lambda: random.choice(self.verb_dict["greet"]),
            "bringVerb": lambda: random.choice(self.verb_dict["bring"]),
            # Preposition mappings
            "toLocPrep": lambda: random.choice(self.prep_dict["toLocPrep"]),
            "fromLocPrep": lambda: random.choice(self.prep_dict["fromLocPrep"]),
            "inLocPrep": lambda: random.choice(self.prep_dict["inLocPrep"]),
            "onLocPrep": lambda: random.choice(self.prep_dict["onLocPrep"]),
            "atLocPrep": lambda: random.choice(self.prep_dict["atLocPrep"]),
            "deliverPrep": lambda: random.choice(self.prep_dict["deliverPrep"]),
            "talkPrep": lambda: random.choice(self.prep_dict["talkPrep"]),
            "ofPrsPrep": lambda: random.choice(self.prep_dict["ofPrsPrep"]),
            # Placeholder mappings
            "connector": lambda: random.choice(self.connector_list),
            #
            "plcmtLoc": lambda: random.choice(self.placement_location_names),
            "loc": lambda: random.choice(self.location_names),
            "room": lambda: random.choice(self.room_names),
            "plcmtLoc2": lambda: "plcmtLoc2",
            "loc2": lambda: "loc2",
            "room2": lambda: "room2",
            "inRoom": lambda: random.choice(self.prep_dict["inLocPrep"]) + " the " + random.choice(self.room_names),
            "atLoc": lambda: random.choice(self.prep_dict["atLocPrep"]) + " the " + random.choice(self.location_names),
            #
            "gestPers": lambda: random.choice(self.gesture_person_list),
            "posePers": lambda: random.choice(self.pose_person_list),
            "name": lambda: random.choice(self.person_names),
            "gestPersPlur": lambda: random.choice(self.gesture_person_plural_list),
            "posePersPlur": lambda: random.choice(self.pose_person_plural_list),
            "persInfo": lambda: random.choice(self.person_info_list),
            #
            "obj": lambda: random.choice(self.object_names),
            "singCat": lambda: random.choice(self.object_categories_singular),
            "plurCat": lambda: random.choice(self.object_categories_plural),
            "objComp": lambda: random.choice(self.object_comp_list),
            #
            "talk": lambda: random.choice(self.talk_list),
            "question": lambda: random.choice(self.question_list),
            #
            "colorClothe": lambda: random.choice(self.color_clothe_list),
            "colorClothes": lambda: random.choice(self.color_clothes_list),
            #
            "art": lambda: "{art}",
        }

        # Return mapped choice or warning
        return placeholder_map.get(ph, lambda: warnings.warn(f"Placeholder not covered: {ph}"))()

    def adjust_articles(self, command_string):
        """Adjust articles (a/an) in the command string."""
        art_ph = re.findall(r'\{(art)\}\s*([A-Za-z])', command_string, re.DOTALL)
        if art_ph:
            command_string = command_string.replace("art", "an" if art_ph[0][1].lower() in ["a", "e", "i", "o", "u"] else "a")
        
        return command_string

    def eliminate_double_mentions(self, command_string):
        """Eliminate double mentions of locations."""
        for placeholder, choices in [("loc2", self.location_names), ("room2", self.room_names), ("plcmtLoc2", self.placement_location_names)]:
            if placeholder in command_string:
                command_string = command_string.replace(placeholder, random.choice([x for x in choices if x not in command_string]))
        return command_string
