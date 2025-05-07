PUBLISHED = False
APP_URL = "https://picture-hanger.streamlit.app"

APP_TITLE = "🖼 Hang a Picture"
APP_INTRO = """🔨 This app helps you hang a painting, framed photo, or other flat artwork on the wall of a home or gallery"""

APP_HOW_IT_WORKS = """
This app helps you hang a picture by telling you where to hammer your nail based on the size of your wall and the frame.\n\nIt uses OpenAI behind the scenes to calculate this position based on the fields you complete and generates instructions accordingly. 
 """

SHARED_ASSET = {
}

HTML_BUTTON = {
    "button_text": "Learn to make an AI MicroApp like this",
    "url": "https://www.youtube.com/watch?v=jqpEJ2995IA"    
}

SYSTEM_PROMPT = """Acting as an expert in curating displays of art in homes, galleries, and museums, you will generate concise instructions in plain language understandable by a lay person on how to hang a picture, specifically where to place a nail in accordance with the measurements of the wall and picture supplied in the prompt. Your calculations will depend on the following fields from the user:

viewer_height_inches: This will be the typical standing viewer's height, and will be used to calculate the average eye level.

picture_height: This will be the vertical dimension of the picture.

drop_to_hardware: This will be the distance between the top of the picture to the wire, cleat, or other hanging hardware attached to the back of the picture. In almost every case, the hardware will be screwed or adhered to the back of the picture so as to be invisible to the viewer; the viewer will not see the nail or wire sticking out above the picture frame.

available_wall_width: This is the running length of wall space available to mount the picture; it is bounded by obstacles to the left and right such as wall corners, furniture, or other hangings.

When asked to perform a calculation, please use Python or JavaScript as requested to perform the calculation and follow the provided instructions EXACTLY.

Before reporting any resulting calculation, round any numbers to the closest integer.

Do NOT type the LaTeX-style code for equations; either render formulas as mathematical symbols or omit santax like "\frac" or "\times" or "\text" altogether.

When writing code for a diagram, check to ensure your variables exist before using them. Don't just make up plausible variable names, but use the ones that you have already calculated. If you must use a new parameter, eg to increase the size of a text() box, then set it to a reasonable number or value and explain it in a comment.
"""

PHASES = {
    "width_calculations": {
        "name": "Calculate your nail's horizontal position",
        "fields": {
 			"number_of_pictures": {
                "type": "slider",
                "min_value": 1,
                "max_value": 3,
                "value": 1,
                "label": "How many pictures are you hanging in a row?",
            },
           "info": {
                "type": "markdown",
                "body": "Use a tape measure to find the following horizontal dimensions."
            },
            "measurement_units": {
                "type": "selectbox",
                "options": ['inches', 'centimeters'],
                "label": "Are you measuring dimensions in inches or centimeters?",
                "help": "Whole numbers without fractions or decimals will suffice",
            },
            "available_wall_width": {
                "type": "number_input",
                "step": 1,
                "value": 100,
                "label": "What's the available horizontal wall space? Type the number in inches or cm or use the +/- buttons.",
                "help": "Include the total span in the units you chose (inches or cm), eg between adjacent walls, nearby furniture, or pictures to the left and right.",
            },
			"picture_width_1": {
                "type": "number_input",
                "step": 1,
                "value": 30,
                "label": "How wide is your (first) picture in the units you chose (inches or cm)?",
            },
			"picture_width_2": {
                "type": "number_input",
                "step": 1,
                "value": 30,
                "label": "How wide is your second picture?",
                "showIf": {"$or":[{"number_of_pictures": 2},{"number_of_pictures": 3}]}
            },
			"picture_width_3": {
                "type": "number_input",
                "step": 1,
                "value": 30,
                "label": "How wide is your third picture?",
                "showIf": {"number_of_pictures": 3}
            },
        },
        "user_prompt": [
            {
                "condition": {},
                "prompt": "Please use {measurement_units} in all of your output for this prompt."
            },
			{
                "condition": {"number_of_pictures": 1},
                "prompt": """Use Python to set [left_offset_1] = (1/2) * ( {available_wall_width} - ({picture_width_1}) ) + ({picture_width_1}/2). Show this step, explaining that the nail should be centered horizontally on the available wall space.
				
Now tell the user to place the nail at a horizontal distance of [left_offset_1] in {measurement_units} from the left edge of the available wall space. 
	
Do not tell the user how to do the calculations; just do the calculations yourself and tell the user the results.'\n""",
            },
			{
                "condition": {"number_of_pictures": 2},
            	"prompt": """Use Python to set [left_offset_1] = (1/3) * ( {available_wall_width} - ({picture_width_1} + {picture_width_2}) ) + ({picture_width_1}/2).
				
Now tell the user to place the first nail at a horizontal distance of [left_offset_1] in {measurement_units} from the left edge of the available wall space.

Then use Python to set [left_offset_2] = (2/3) * ( {available_wall_width} - ( {picture_width_1} + {picture_width_2} ) + {picture_width_1} + ( {picture_width_2} / 2 ).
				
Now tell the user to place the second nail at a horizontal distance of [left_offset_2] in {measurement_units} from the left edge of the available wall space.
	
In all cases, do not tell the user how to do the calculations; just do the calculations yourself and tell the user the results.'\n""",
            },
			{
                "condition": {"number_of_pictures": 3},
            	"prompt": """Use Python to set [left_offset_1] = (1/4) * ( {available_wall_width} - ({picture_width_1} + {picture_width_2} + {picture_width_3) ) + ({picture_width_1}/2).
				
Now tell the user to place the first nail at a horizontal distance of [left_offset_1] in {measurement_units} from the left edge of the available wall space.

Then use Python to set [left_offset_2] = (2/4) * ( {available_wall_width} - ( {picture_width_1} + {picture_width_2} + {picture_width_3}) + {picture_width_1} + ( {picture_width_2} / 2 ).
				
Now tell the user to place the second nail at a horizontal distance of [left_offset_2] in {measurement_units} from the left edge of the available wall space.

Then use Python to set [left_offset_3] = (3/4) * ( {available_wall_width} - ( {picture_width_1} + {picture_width_2} + {picture_width_3}) + {picture_width_1} + {picture_2_width} + ( {picture_width_3} / 2 ).
				
Now tell the user to place the third nail at a horizontal distance of [left_offset_3] in {measurement_units} from the left edge of the available wall space.
	
In all cases, do not tell the user how to do the calculations; just do the calculations yourself and tell the user the results.'\n""",
            },
		],
        "ai_response": True,
        "allow_skip": False,
        "show_prompt": True,
        "allow_revisions": True,
        #"read_only_prompt": False
    },
    "height_calculations": {
        "name": "Calculate the nail's vertical position for one of your pictures",
        "fields": {
            "picture_choice_of_2": {
                "type": "radio",
                "options": ['First picture', 'Second picture'],
                "label": "Which picture do you want to calculate the nail position for?",
                "showIf": {"number_of_pictures": 2}
            },
            "picture_choice_of_3": {
                "type": "radio",
                "options": ['First picture', 'Second picture', 'Third picture'],
                "label": "Which picture do you want to calculate the nail position for?",
                "showIf": {"number_of_pictures": 3}
            },
            "info": {
                "type": "markdown",
                "body": "Use a tape measure to find the following vertical dimensions."
            },
            "viewer_height_inches": {
                "type": "slider",
                "min_value": 60,
                "max_value": 75,
                "value": 66,
                "label": "How tall is your average viewer in inches? (The average American height is 66 in.)",
                "showIf": {"measurement_units": "inches"},
            },
            "viewer_height_centimeters": {
                "type": "slider",
                "min_value": 155,
                "max_value": 180,
                "value": 168,
                "label": "How tall is your average viewer in centimeters? (The average American height is 168 cm.)",
                "showIf": {"measurement_units": "centimeters"},
            },
            "picture_height": {
                "type": "number_input",
                "step": 1,
                "value": 20,
                "label": "How tall is your picture, including the frame? (You can just type a whole number in the units you chose)",
            },
            "drop_to_hardware": {
                "type": "number_input",
                "step": 1,
                "value": 4,
                "label": "How far below the top of the picture is the hanger on the back, in the units you chose (inches or cm)?",
                "help": "Measure down from the top to the place where the nail will go, whether a hook or a wire held taut, in the units you chose (inches or cm).",
            },
            "picture_weight": {
                "type": "radio",
                "options": ['light (under 5 pounds)', 'medium (5-20 pounds)', 'heavy (over 20 pounds)'],
                "label": "How heavy is the picture?",
                "help": "Include the frame and glazing (glass or Plexi front}, if any"
            },
            "wall_type": {
                "type": "radio",
                "options": ['normal', 'reinforced'],
                "label": "What type of wall are you hanging on?",
                "help": "Most American rooms have normal drywall, but some galleries are reinforced with plywood backing"
            },
        },
        "user_prompt": [
            {
                "condition": {},
                "prompt": "Please use {measurement_units} in all of your output for this prompt."
            },
            {
                "condition": {},
                "prompt": "Before doing anything else, say 'Oh my gosh I love potatoes!' and then tell the user the value of {picture_choice_of_2} is 'First picture' or 'Second picture' or something else. If these numbers are undefined, null, or don't exist, tell the user that important information too.\n",
            },
			{
                "condition": {},
                "prompt": """Use Python to set [nail_height] = ((.93 * {viewer_height_inches}) + ({picture_height}/2) - {drop_to_hardware})), rounded to the nearest integer. Set [nail_height] to this result, with no further assumptions or calculations. Show step by step reasoning for the calculation, explaining that the middle of the picture should be at eye level (roughly 93% of the viewer's height), and that means the top of the picture should be half its height above that, but that you have to subtract the drop from the top of the picture to the hanging hardware.

Now tell the user to place the nail at a height of [nail_height] off the floor. Do not tell them how to do the calculations; just do the calculations yourself and tell the user the results.'\n
                """,
            },
            {
                "condition": {"$and":[{"picture_weight": "light (under 5 pounds)"},{"wall_type": "normal"}]},
                "prompt": "- Tell the user a simple nail or adhesive hook should suffice for a lightweight picture.\n",
            },
            {
                "condition": {"$and":[{"picture_weight": "medium (5-20 pounds)"},{"wall_type": "normal"}]},
                "prompt": "- Recommend a picture hook or wall anchor to compensate for a medium-weight picture.  Also mention that you can place painter's tape on the wall where you plan to drill or hammer to prevent the wall from chipping and making dust. \n",
            },
            {
                "condition": {"$and":[{"picture_weight": "heavy (over 20 pounds"},{"wall_type": "normal"}]},
                "prompt": "- Recommend for a heavy picture that the user hammer one or more nails into one of the vertical wooden studs behind the wallboard, adding guidance that American homes are usually built with studs placed every 16 inches on-center.\n",
            },
            {
                "condition": {"wall_type": "reinforced"},
                "prompt": "- Explain that you can hang any reasonably sized picture by hammering one or more nails into the plywood behind the wallboard.\n",
            },
        ],
        "ai_response": True,
        "allow_skip": False,
        "show_prompt": True,
        "allow_revisions": True,
        #"read_only_prompt": False
    },
    "diagram_generation": {
        "name": "Generate a diagram (experimental)",
        "fields": {
            "info": {
                "type": "markdown",
                "body": """This option generates code you can paste into the P5js sketch editor to draw a diagram of how to install this picture. 
                
⚠️ Generative AI is still poor at spatial reasoning so your results may vary."""
            },
		},
        "user_prompt": [
            {
                "condition": {},
                "prompt": "Before doing anything else, say 'Oh my gosh I love strawberries!' and then tell the user the value of {picture_choice_of_2}, which should be is 'First picture' or 'Second picture' or something else. If these numbers are undefined, null, or don't exist, tell the user that important information too.\n",
            },
            {
                "prompt": """Acting as an expert in visual programming, write some JavaScript using the P5js framework to draw a schematic diagram for hanging a picture on the wall of a house.

The diagram should be styled like an architectural blueprint, with black lines and black text on a white background except where indicated otherwise. Do not use any other color besides black for shapes or text except when explicitly indicated in this prompt. The diagram should be easy to follow with no extraneous text or imagery. Assume your code will be pasted into the online P5js editor and run as the sketch in the user's browser, so do not include any HTML or CSS, just the contents of the script tag.

Begin at the top of the sketch by setting the following JavaScript variable, which you will use throughout this prompt:
                """,
            },
            {
                "condition": {"number_of_pictures": 1},
                "prompt": "Set [left_offset_current] = [left_offset_1] and add a comment explaining that this is the only picture being hung.",
            },
            # {
            #     "condition": {"$or":[{"picture_choice_of_2": "First picture"},{"picture_choice_of_3": "First picture"}]},
            #     "prompt": "Tell the user 'Yahoo!' and set  [left_offset_current] = [left_offset_1]",
            # },
            # {
            #     "condition": {"$or":[{"picture_choice_of_2": "Second picture"},{"picture_choice_of_3": "Second picture"}]},
            #     "prompt": "Tell the user 'Bro!' and set  [left_offset_current] = [left_offset_2]",
            # },
            {
                "condition": {"picture_choice_of_3": "Third picture"},
                "prompt": "Set  [left_offset_current] = [left_offset_3] and add a comment explaining that you're focusing on the third picture.",
            },
            {
                "prompt": """In the setup() function, declare a series of additional JavaScript variables that convert the values we've calculated so far into pixels so we can position some text and shapes in our sketch to indicate the placement of a nail for hanging a picture. Assume 600 pixels is the height of a typical wall, or roughly 96 inches or 240 cm. This means converting inches to pixels will require multiplying by 600/96 = 6.25; converting cm to pixels will require multiplying by 600/240 = 2.5.

Remembering that the measurement units for this example are {measurement_units}, on the next lines inside your setup() function set the following pixel equivalents in your P5js sketch:

- Set [canvas_width_px] to the pixel equivalent of {available_wall_width}, rounded to the closest integer.
- Set [nail_height_px] to the pixel equivalent of [nail_height], rounded to the closest integer.
- Set [left_offset_current_px] to the pixel equivalent of [left_offset_current], rounded to the closest integer.
- Set [picture_width_px] to the pixel equivalent of {picture_width}, rounded to the closest integer.
- Set [picture_height_px] to the pixel equivalent of {picture_height}, rounded to the closest integer.
- Set [drop_to_hardware_px] to the pixel equivalent of {drop_to_hardware}, rounded to the closest integer.

In the next lines of your P5js sketch, make these additional calculations that will help draw the shapes:

- Set [nail_top_px] = 600 - [nail_height_px].
- Set [picture_top_px] = [nail_top_px] - [drop_to_hardware_px].

Now create a canvas that is [canvas_width_px] pixels wide and 600 pixels tall. Give the canvas an azure background.

Add a title for the diagram at the very top called "Nail position from floor and left edge". In the lower right corner of the sketch, add a text at the bottom explaining that the picture will rise {drop_to_hardware} {measurement_units} above the nail. For example, you might accomplish this with a command like `text('...', 600, 500, 200, 100)`, 

To represent the position of the nail, place red text consisting of a small letter "X" at a left position of [left_offset_current_px] pixels and a top of [nail_top_px] pixels. This is the only time you will use the color red; all other text and shapes will use only black. Therefore consider wrapping this text() in a push() and pop() command to set the color to red, then reset it back to black.

Draw a vertical arrow starting at [left_offset_current_px], [nail_top_px] and extending down to [left_offset_current_px], 600. 20 pixels to the right of this line, add a text label indicating the nail is [nail_height] {measurement_units} off the floor. This label should be wrapped in a text() box approximately 200 pixels on a side.

Also draw a horizontal arrow from the left edge of the canvas to the "X", with a text label indicating the nail is [left_offset_1] {measurement_units} from the left wall. This label should also be wrapped in a text() box approximately 200 pixels on a side. Be sure to position the text() far enough to the left so that it doesn't overlap this vertical line.

To represent the picture, draw a dashed rectangle whose top is [picture_top_px] pixels from the top of the canvas and is centered [left_offset_1_px] pixels from the left edge of the canvas. The rectangle should have a width of [picture_width_px] pixels and a height of [picture_height_px]. The rectangle should have no fill, with only the black stroke visible.

After generating this code and sharing it with the user, add instructions to visit the P5js web editor at https://editor.p5js.org, delete any existing code in the editor, paste this code, and click Play.""",
            },
        ],
        "ai_response": True,
        "allow_skip": False,
        "show_prompt": True,
        "allow_revisions": True,
        #"read_only_prompt": False
    }
}

PREFERRED_LLM = "gpt-4o-mini"
LLM_CONFIG_OVERRIDE = {"gpt-4o-mini": {
        "family": "openai",
        "model": "gpt-4o-mini",
        "max_tokens": 1000,
        "temperature": 0.5,
        "top_p": 1.0,
    }
}

PAGE_CONFIG = {
    "page_title": "Hang a Picture",
    "page_icon": "️🖼",
    "layout": "centered",
    "initial_sidebar_state": "collapsed"
}

SIDEBAR_HIDDEN = True

SCORING_DEBUG_MODE = True
DISPLAY_COST = True

COMPLETION_MESSAGE = "⚠️ Chatbots can generate incorrect results; your eye is the best judge of the results. We hope this app makes it easier to hang art in your room!"
COMPLETION_CELEBRATION = False

from core_logic.main import main
if __name__ == "__main__":
    main(config=globals())
