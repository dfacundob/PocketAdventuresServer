from command.base_command import BaseCommand
from utils.utils import npcs_info


class ObtainNpcListHandler(BaseCommand):

    def answer(self):
        # Levels are stored as key "exp" instead of score in xml npc definitions

        self.answer_command_data['npcList'] = []

        for npc_sku in ['npc_A', 'npc_B', 'npc_C', 'npc_D']:
            npc_progress = str(self.user.profile.npcs.get_npc_progress(npc_sku))
            npc_info = npcs_info[npc_sku][npc_progress]

            npc = {}
            npc['sku'] = npc_sku
            npc['HQLevel'] = npc_info['HQLevel']
            npc['xp'] = npc_info['xp']

            self.answer_command_data['npcList'].append(npc)
