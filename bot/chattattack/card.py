import os
import math

from decimal import Decimal, ROUND_HALF_UP

from PIL import Image

os.chdir(os.path.abspath(os.path.dirname(__file__)))

AMONG_BG = "among.jpg"
FOREST_BG = "forest.jpg"
COSMIC_BG = "cosmic.jpg"
COSMOS_BG = "cosmos.jpg"
CITY_BG = "city.jpg"

TEMPLATE_CARD = "template_card.png"

CAT_1 = "catt.jpg"
CAT_2 = "ccat.jpg"
CAT_3 = "caat.jpg"
CAT_4 = "cat.png"
CAT_5 = "cat.jpg"

NAME_CARD = "name_container.png"

image = Image.open(TEMPLATE_CARD)
name_card = Image.open(NAME_CARD)
cat = Image.open(CAT_3)

global_width = image.width
global_height = image.height


def round_half_up(x):
    return int(Decimal(x).to_integral_value(rounding=ROUND_HALF_UP))


###################################################################################
# * Add a margin around the card

margin_width = 2 / 100
margin_height = 2 / 100

main_container_margin_width = round_half_up(global_width * margin_width)
main_container_margin_height = round_half_up(global_height * margin_height)

main_container_width = round_half_up(global_width - (main_container_margin_width * 2))
main_container_height = round_half_up(global_height - (main_container_margin_height * 2))

###################################################################################
# * Set the spaces between two boxes in the main container

main_container_sep_boxes = 5 / 100
main_container_sep_width = round_half_up(main_container_width * main_container_sep_boxes)
main_container_sep_height = round_half_up(main_container_height * main_container_sep_boxes)

###################################################################################
# * Split the card in two part, left and right

main_container_middle_width = round_half_up(main_container_width / 2)
main_container_sep_middle_width = round_half_up(main_container_sep_width / 2)

main_container_left_width = main_container_width - main_container_middle_width - main_container_sep_middle_width
main_container_left_height = main_container_height

main_container_right_width = main_container_width - main_container_left_width - main_container_sep_width
main_container_right_height = main_container_height

###################################################################################
# * Left part - Name box

name_box_height = 15 / 100
name_box_container_width = main_container_left_width
name_box_container_height = round_half_up(main_container_left_height * name_box_height)

abs_name_box_container_coord_up = main_container_margin_height
abs_name_box_container_coord_left = main_container_margin_width

name_card_placement_height = 2 / 3
_name_card_height = round_half_up(name_box_container_height * name_card_placement_height)
name_card.thumbnail((name_box_container_width, _name_card_height))
name_card_width = name_card.width
name_card_height = name_card.height

name_card_paste_up = round_half_up( (name_box_container_height - name_card_height) / 2)
name_card_paste_left = round_half_up( (name_box_container_width - name_card_width) / 2)

# ! Draw text

###################################################################################
# * Left part - Stat box

stat_box_height = 30 / 100
stat_box_container_width = main_container_left_width
stat_box_container_height = round_half_up(main_container_left_height * stat_box_height)

abs_stat_box_container_coord_up = abs_name_box_container_coord_up + name_box_container_height + main_container_sep_height + 1
abs_stat_box_container_coord_left = main_container_margin_width

up_stat_box_container = 1 / 3
up_stat_box_container_height = round_half_up(stat_box_container_height * up_stat_box_container)
up_stat_box_container_width = stat_box_container_width

# ! Draw line last pixel of up_stat_box_container_height
# ! Draw text & emoji at the middle of up_stat_box_container_height

down_stat_box_height = stat_box_container_height - up_stat_box_container_height
down_left_stat_box = 2 / 3
down_left_stat_box_width = round_half_up(stat_box_container_width * down_left_stat_box)
down_right_stat_box_width = stat_box_container_width - down_left_stat_box_width

# ! Draw text

###################################################################################
# * Left part - Nature box

nature_box_height = 25 / 100
nature_box_container_width = main_container_left_width
nature_box_container_height = round_half_up(main_container_left_height * nature_box_height)

abs_nature_box_container_coord_up = abs_stat_box_container_coord_up + stat_box_container_height + main_container_sep_height + 1
abs_nature_box_container_coord_left = main_container_margin_width

up_nature_box_container = 1 / 3
up_nature_box_container_height = round_half_up(nature_box_container_height * up_nature_box_container)
up_nature_box_container_width = nature_box_container_width

# ! Draw line last pixel of up_nature_box_container_height
# ! Draw text & emoji at the middle of up_nature_box_container_height

down_nature_box_height = nature_box_container_height - up_nature_box_container_height

# ! Draw text (mono to center with width?)

###################################################################################
# * Left part - Rank & id box

rank_box_height = 15 / 100
margin_rank_box = 10 / 100

_rank_box_container_height = round_half_up(main_container_left_height * rank_box_height)
margin_rank_box_container_height = _rank_box_container_height * margin_rank_box

rank_box_container_height = round_half_up(_rank_box_container_height - (margin_rank_box_container_height * 2))
rank_box_container_width = main_container_left_width

abs_rank_box_container_coord_up = abs_nature_box_container_coord_up + nature_box_container_height + main_container_sep_height + 1
abs_rank_box_container_coord_left = main_container_margin_width

left_rank_box_container = 2 / 3
left_rank_box_container_width = round_half_up(rank_box_container_width * left_rank_box_container)
right_rank_box_container_width = rank_box_container_width - left_rank_box_container_width

# ! Draw text

###################################################################################
# * Right part - Main cat info

catinfo_box_height = 80 / 100
catinfo_box_container_height = round_half_up(main_container_right_height * catinfo_box_height)
catinfo_box_container_width = main_container_right_width

abs_catinfo_box_container_coord_up = main_container_margin_height
abs_catinfo_box_container_coord_left = round_half_up(global_width - main_container_margin_width - catinfo_box_container_width)

catinfo_part_separation = 1 / 3

###################################################################################
# * Right part - Main cat info / Image

catinfo_image_container_height = round_half_up(catinfo_box_container_height * catinfo_part_separation)
catinfo_image_container_width = catinfo_box_container_width

catinfo_border = 5 / 100
catinfo_image_border_width = round_half_up(catinfo_image_container_width * catinfo_border)
catinfo_image_border_height = round_half_up(catinfo_image_container_height * catinfo_border)

_catinfo_image_box_width = round_half_up(catinfo_image_container_width - (catinfo_image_border_width * 2))
_catinfo_image_box_height = round_half_up(catinfo_image_container_height - (catinfo_image_border_height * 2))
cat.thumbnail((_catinfo_image_box_width, _catinfo_image_box_height))

catinfo_image_width = cat.width
catinfo_image_height = cat.height

catinfo_image_placement_up = round_half_up((catinfo_image_container_height - catinfo_image_height) / 2)
catinfo_image_placement_left = round_half_up((catinfo_image_container_width - catinfo_image_width) / 2)

catinfo_image_level_box_width = 30 / 100
catinfo_image_level_box_height = 20 / 100
catinfo_image_level_container_width = round_half_up(catinfo_image_width * catinfo_image_level_box_width)
catinfo_image_level_container_height = round_half_up(catinfo_image_height * catinfo_image_level_box_height)

catinfo_image_level_placement_up = catinfo_image_placement_up + catinfo_image_height - catinfo_image_level_container_height
catinfo_image_level_placement_left = catinfo_image_placement_left

# ! Draw text
# ! Draw lines around the image
# ?  [(catinfo_image_placement_left, catinfo_image_placement_up - catinfo_image_border_height), (catinfo_image_placement_left + catinfo_image_width, catinfo_image_placement_up)]
# ?  [(catinfo_image_placement_left + catinfo_image_width + catinfo_image_border_width, catinfo_image_placement_up - catinfo_image_border_height), (catinfo_image_placement_left + catinfo_image_width, catinfo_image_placement_up + catinfo_image_height)]
# ?  [(catinfo_image_placement_left + catinfo_image_width + catinfo_image_border_width, catinfo_image_placement_up + catinfo_image_height + catinfo_image_border_height), (catinfo_image_placement_left, catinfo_image_placement_up + catinfo_image_height)]
# ?  (catinfo_image_placement_left - catinfo_image_border_width, catinfo_image_placement_up + catinfo_image_height + catinfo_image_border_height), (catinfo_image_placement_left, catinfo_image_placement_up - catinfo_image_border_height)

###################################################################################
# * Right part - Main cat info / Life & Weapon

catinfo_maininfo_container_height = round_half_up(catinfo_box_container_height * catinfo_part_separation)
catinfo_maininfo_container_width = catinfo_box_container_width

catinfo_maininfo_up = 1 / 2
catinfo_maininfo_up_height = round_half_up(catinfo_maininfo_up * catinfo_maininfo_container_height)
catinfo_maininfo_top_up_height = round_half_up(catinfo_maininfo_up_height / 2)
catinfo_maininfo_up_left = 1 / 3
catinfo_maininfo_up_left_width = round_half_up(catinfo_maininfo_container_width * catinfo_maininfo_up_left)

# ! Draw text
# ? Draw rectangle 2 / 3 width, 5px 
# ? Place in the middle
# ! Draw text

# ! Same

# ! Draw text in the middle

catinfo_maininfo_down_height = catinfo_maininfo_container_height - catinfo_maininfo_up_height
catinfo_main_info_down_box_container = 1 / 2
catinfo_main_info_down_box_container_height = round_half_up(catinfo_maininfo_down_height * catinfo_main_info_down_box_container)
catinfo_maininfo_down_box_container_pos = 25 / 100
catinfo_maininfo_down_box_container_pos_height = round_half_up(catinfo_maininfo_down_box_container_pos * catinfo_maininfo_down_height)
catinfo_maininfo_down_box_container_middle = 1 / 2
catinfo_maininfo_down_box_container_middle_width = round_half_up(catinfo_maininfo_container_width * catinfo_maininfo_down_box_container_middle)

# ! Draw text left and right

###################################################################################
# * Right part - Main cat info / Status

catinfo_subinfo_container_height = round_half_up(catinfo_box_container_height * catinfo_part_separation)
catinfo_subinfo_container_width = catinfo_box_container_width

catinfo_subinfo_container_left = 20 / 100
catinfo_subinfo_container_right = 20 / 100
catinfo_subinfo_container = 1 / 6
catinfo_subinfo_container_height = round_half_up(catinfo_subinfo_container * catinfo_subinfo_container_height)
catinfo_subinfo_container_left_width = round_half_up(catinfo_subinfo_container_left * catinfo_subinfo_container_width)
catinfo_subinfo_container_right_width = round_half_up(catinfo_subinfo_container_right * catinfo_subinfo_container_width)

# ? Draw rectangle width - container_right - container_left, 5px 
# ? Place in the middle

# ! Draw text & emoji

###################################################################################
# * Right part - Main cat info / Badges
# TODO