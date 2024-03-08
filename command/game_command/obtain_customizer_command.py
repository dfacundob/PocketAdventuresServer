from command.base_command import BaseCommand


class ObtainCustomizerHandler(BaseCommand):

    def answer(self):
        self.answer_command_data['customizer'] = []

        # Not possible to make it work on PA, ubi devs probably coded it but never
        # used it so they couldn't see it wasn't working. To make it work you gotta put button
        # info in the content field, else there's only one button on the popup and it cannot be closed
        # Content is supposed to be an object ({}), but it is parsed like an array. So if you set an object the
        # game fail at parsing it and crash, and if you set an array the game simply don't parse the field

        # customizer = {}

        # customizer['type'] = 1

        # customizer['title'] = 'Test Popup Title'
        # customizer['text'] = 'Testtext'
        # customizer['img'] = ''

        # customizer['content'] = [9,85,4]

        # self.answer_command_data['customizer'].append(customizer)

        # customizer_content = {}
        # customizer_content['label'] = 'ButLa'

        # # In PA different action are: followLink, goToShop, goToInventory, goToFriends
        # customizer_content['action'] = 'close_popup'
        # customizer_content['actionButton'] = {}

        # action_button = {}
        # action_button['params'] = None

        # customizer_content['actionButton'][1] = action_button

        # action_button = {}

        # action_button['params'] = {}
        # action_button['params']['url'] = 'https://google.com'

        # # Different parameters: goToInventory: tab
        # #                       goToFriends: tab
        # #                       goToShop: tab, item

        # customizer_content['actionButton'].append(action_button)

        # customizer['content'][1] = customizer_content

        # self.answer_command_data['customizer'].append(customizer)
