import json
import random

from hashlib import md5
from datetime import datetime, timedelta


def load_json(path):
    with open(path) as f:
        return json.load(f)


npcs_info = load_json('utils/npcs_info.json')
items_time = load_json('utils/time_items.json')
items_energy = load_json('utils/energy_items.json')
social_items = load_json('utils/social_items.json')
protection_times = load_json('utils/protection_times.json')
silos_ressources = load_json('utils/silos_ressources.json')
crafting_rewards = load_json('utils/crafting_rewards.json')
alliance_powerups = load_json('utils/alliance_powerups.json')
use_action_reward = load_json('utils/use_action_reward.json')
default_player_items = load_json('utils/default_player_items.json')
minimum_level_attack = load_json('utils/minimum_level_attack.json')
missions_targets_size = load_json('utils/missions_targets_size.json')


default_colonies_items = {
    0: load_json('utils/colonies_default_items/blue_planet.json'),
    1: load_json('utils/colonies_default_items/green_planet.json'),
    2: load_json('utils/colonies_default_items/purple_planet.json'),
    3: load_json('utils/colonies_default_items/white_planet.json'),
    4: load_json('utils/colonies_default_items/red_planet.json'),
    5: load_json('utils/colonies_default_items/yellow_planet.json')
}


npc_bases = {
    'npc_A': {
        1: load_json('utils/npcs/universe_npc_A0.json')
    },
    'npc_B': {
        1: load_json('utils/npcs/universe_npc_B0.json'),
        2: load_json('utils/npcs/universe_npc_B1.json'),
        3: load_json('utils/npcs/universe_npc_B2.json'),
        4: load_json('utils/npcs/universe_npc_B3.json'),
        5: load_json('utils/npcs/universe_npc_B4.json'),
        6: load_json('utils/npcs/universe_npc_B5.json'),
        7: load_json('utils/npcs/universe_npc_B6.json'),
        8: load_json('utils/npcs/universe_npc_B7.json'),
        9: load_json('utils/npcs/universe_npc_B8.json'),
        10: load_json('utils/npcs/universe_npc_B9.json')
    },
    'npc_C': {
        1: load_json('utils/npcs/universe_npc_C0.json'),
        2: load_json('utils/npcs/universe_npc_C1.json'),
        3: load_json('utils/npcs/universe_npc_C2.json'),
        4: load_json('utils/npcs/universe_npc_C3.json'),
        5: load_json('utils/npcs/universe_npc_C4.json'),
        6: load_json('utils/npcs/universe_npc_C5.json'),
        7: load_json('utils/npcs/universe_npc_C6.json'),
        8: load_json('utils/npcs/universe_npc_C7.json'),
        9: load_json('utils/npcs/universe_npc_C8.json'),
        10: load_json('utils/npcs/universe_npc_C9.json')
    },
    'npc_D': {
        1: load_json('utils/npcs/universe_npc_D0.json'),
        2: load_json('utils/npcs/universe_npc_D1.json'),
        3: load_json('utils/npcs/universe_npc_D2.json'),
        4: load_json('utils/npcs/universe_npc_D3.json')
    }
}


def get_default_colony_items(galaxy_type):
    default_items = default_colonies_items.get(galaxy_type)

    if default_items is not None:
        return default_items

    else:
        return {}


def get_next_galaxy_coordinate(x, y):
    # Square expansion
    if x == y:
        return x + 1, 0

    elif x > y:
        if x - y == 1:
            return 0, y + 1

        else:
            return x, y + 1

    else:
        return x + 1, y


def generate_random_galaxy_name():
    nm1 = ['b', 'c', 'ch', 'd', 'g', 'h', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'th', 'v', 'x', 'y', 'z', '', '', '', '', '']
    nm2 = ['a', 'e', 'i', 'o', 'u']
    nm3 = ['b', 'bb', 'br', 'c', 'cc', 'ch', 'cr', 'd', 'dr', 'g', 'gn', 'gr', 'l', 'll', 'lr', 'lm', 'ln',
           'lv', 'm', 'n', 'nd', 'ng', 'nk', 'nn', 'nr', 'nv', 'nz', 'ph', 's', 'str', 'th', 'tr', 'v', 'z']
    nm3b = ['b', 'br', 'c', 'ch', 'cr', 'd', 'dr', 'g', 'gn', 'gr', 'l', 'll', 'm', 'n', 'ph', 's', 'str', 'th', 'tr', 'v', 'z']
    nm4 = ['a', 'e', 'i', 'o', 'u', 'a', 'e', 'i', 'o', 'u', 'a', 'e', 'i', 'o', 'u', 'ae', 'ai', 'ao', 'au',
           'a', 'ea', 'ei', 'eo', 'eu', 'e', 'ua', 'ue', 'ui', 'u', 'ia', 'ie', 'iu', 'io', 'oa', 'ou', 'oi', 'o']
    nm5 = ['turn', 'ter', 'nus', 'rus', 'tania', 'hiri', 'hines', 'gawa', 'nides', 'carro', 'rilia', 'stea', 'lia', 'lea', 'ria', 'nov', 'phus', 'mia', 'nerth',
           'wei', 'ruta', 'tov', 'zuno', 'vis', 'lara', 'nia', 'liv', 'tera', 'gantu', 'yama', 'tune', 'ter', 'nus', 'cury', 'bos', 'pra', 'thea', 'nope', 'tis', 'clite']
    nm6 = ['una', 'ion', 'iea', 'iri', 'illes', 'ides', 'agua', 'olla', 'inda', 'eshan', 'oria', 'ilia', 'erth', 'arth', 'orth', 'oth', 'illon', 'ichi', 'ov', 'arvis',
           'ara', 'ars', 'yke', 'yria', 'onoe', 'ippe', 'osie', 'one', 'ore', 'ade', 'adus', 'urn', 'ypso', 'ora', 'iuq', 'orix', 'apus', 'ion', 'eon', 'eron', 'ao', 'omia']
    nm7 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1',
           '2', '3', '4', '5', '6', '7', '8', '9', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '', '', '', '', '', '', '', '', '', '', '', '', '', '']

    out_name = []

    use_number = random.randint(0, 10) > 7

    if use_number:
        name_type = random.randint(0, 3)

        if name_type < 2:
            rnd = random.choice(nm1)
            rnd2 = random.choice(nm2)
            rnd3 = random.choice(nm3)

            while rnd == rnd3:
                rnd3 = random.choice(nm3)

            if name_type == 0:
                out_name.append(''.join([rnd, rnd2, rnd3, random.choice(nm4), random.choice(nm5)]))

            else:
                out_name.append(''.join([rnd, rnd2, rnd3, random.choice(nm4)]))

        elif name_type == 2:
            rnd = random.choice(nm1)
            rnd4 = random.choice(nm4)
            rnd5 = random.choice(nm5)

            out_name.append(''.join([rnd, rnd4, rnd5]))

        else:
            rnd = random.choice(nm1)
            rnd2 = random.choice(nm2)
            rnd3 = random.choice(nm3b)

            while rnd == rnd3:
                rnd3 = random.choice(nm3b)

            rnd4 = random.choice(nm2)
            rnd5 = random.choice(nm5)

            out_name.append(''.join([rnd3, rnd2, rnd, rnd4, rnd5]))

        rnd3 = random.choice(nm7)
        rnd4 = random.choice(nm7)
        rnd5 = random.choice(nm7)
        rnd6 = random.choice(nm7)

        out_name.append(''.join([rnd3, rnd4, rnd5, rnd6]))

    else:
        for _ in range(2):
            name_type = random.randint(0, 3)

            if name_type < 2:
                rnd = random.choice(nm1)
                rnd2 = random.choice(nm2)
                rnd3 = random.choice(nm3)

                while rnd == rnd3:
                    rnd3 = random.choice(nm3)

                if name_type == 0:
                    out_name.append(''.join([rnd, rnd2, rnd3, random.choice(nm4), random.choice(nm5)]))

                else:
                    out_name.append(''.join([rnd, rnd2, rnd3, random.choice(nm6)]))

            elif name_type == 2:
                rnd = random.choice(nm1)
                rnd4 = random.choice(nm4)
                rnd5 = random.choice(nm5)

                out_name.append(''.join([rnd, rnd4, rnd5]))

            else:
                rnd = random.choice(nm1)
                rnd2 = random.choice(nm2)
                rnd3 = random.choice(nm3b)

                while rnd == rnd3:
                    rnd3 = random.choice(nm3b)

                rnd4 = random.choice(nm2)
                rnd5 = random.choice(nm5)

                out_name.append(''.join([rnd3, rnd2, rnd, rnd4, rnd5]))

    return ' '.join(out_name)


def get_initial_gifts_timestamps():
    initial_timestamp = (datetime.utcnow() - timedelta(days=1)).timestamp()

    return '{0}:{0}:{0}'.format(initial_timestamp)


def get_signature(form, user_token, sig_key):
    out = []

    for key in form:
        if key != 'sig':
            out.append('{}={}'.format(key, form[key]))

    final = ('&'.join(out) + user_token + sig_key).encode('utf-8')

    return md5(final).hexdigest()
