# pylint: disable=wildcard-import, unused-wildcard-import, undefined-variable

from datetime import datetime

from command.game_command import *
from command.social_command import *
from command.message_command import *
from command.alliance_command import *


available_game_commands = {
    'updateMisc': UpdateMiscHandler,
    'updateItem': UpdateItemHandler,
    'updateShips': UpdateShipsHandler,
    'updateBattle': UpdateBattleHandler,
    'joinAccounts': JoinAccountsHandler,
    'updateAvatar': UpdateAvatarHandler,
    'updateTargets': UpdateTargetsHandler,
    'updateProfile': UpdateProfileHandler,
    'queryStarInfo': QueryStarInfoHandler,
    'queryVideoAds': QueryVideoAdsHandler,
    'obtainNpcList': ObtainNpcListHandler,
    'updateMissions': UpdateMissionsHandler,
    'obtainUniverse': ObtainUniverseHandler,
    'rejectPoolUnits': RejectPoolUnitsHandler,
    'updateAlliances': UpdateAlliancesHandler,
    'updateGameUnits': UpdateGameUnitsHandler,
    'updateSocialItem': UpdateSocialItemHandler,
    'obtainCustomizer': ObtainCustomizerHandler,
    'queryGalaxyWindow': QueryGalaxyWindowHandler,
    'obtainHangarsHelp': ObtainHangarsHelpHandler,
    'obtainSocialItems': ObtainSocialItemsHandler,
    'obtainAttackerLog': ObtainAttackerLogHandler,
    'obtainBattleReplay': ObtainBattleReplayHandler,
    'obtainAllianceHelps': ObtainAllianceHelpsHandler,
    'manageAllianceItems': ManageAllianceItemsHandler,
    'obtainRandomTargets': ObtainRandomTargetsHandler,
    'obtainNeighborsList': ObtainNeighborsListHandler,
    'queryStarsBookmarks': QueryStarsBookmarksHandler,
    'updateStarsBookmarks': UpdateStarsBookmarksHandler,
    'manageAllianceMembers': ManageAllianceMembersHandler,
    'deployPoolUnitsOnBunker': DeployPoolUnitsOnBunkerHandler,
    'queryPlanetAvailability': QueryPlanetAvailabilityHandler,
    'queryAllianceGiftUnitsOnPool': QueryAllianceGiftUnitsOnPoolHandler,
    'queryGetColonyConfirmPurchase': QueryGetColonyConfirmPurchaseHandler,
    'queryCheckAndLockAccountIfPossible': QueryCheckAndLockAccountIfPossibleHandler,
}

available_commands = {
    # Social command
    'send-gift': SendGiftHandler,
    'blacklist': BlacklistHandler,
    'ignore-gift': IgnoreGiftHandler,
    'accept-gift': AcceptGiftHandler,
    'add-neighbour': AddNeighbourHandler,
    'get-neighbours': GetNeighboursHandler,
    'accept-neighbour': AcceptNeighbourHandler,
    'ignore-neighbour': IgnoreNeighbourHandler,
    'remove-neighbour': RemoveNeighbourHandler,
    'get-incoming-gifts': GetIncomingGiftsHandler,

    # Message command
    'get-messages': GetMessagesHandler,
    'send-message': SendMessageHandler,
    'read-message': ReadMessageHandler,

    # Alliance command
    'getNews': GetNewsHandler,
    'tagPlanet': TagPlanetHandler,
    'askForHelp': AskForHelpHandler,
    'declareWar': DeclareWarHandler,
    'kickMember': KickMemberHandler,
    'grantMember': GrantMemberHandler,
    'getAlliance': GetAllianceHandler,
    'getAlliances': GetAlliancesHandler,
    'joinAlliance': JoinAllianceHandler,
    'getMyAlliance': GetMyAllianceHandler,
    'leaveAlliance': LeaveAllianceHandler,
    'addLoyaltyPoints': AddLoyaltyPointsHandler,
    'cancelAskForHelp': CancelAskForHelpHandler,
    'setMessageOfTheDay': SetMessageOfTheDayHandler,
    'getAllianceRequests': GetAllianceRequestHandler,
    'denyAllianceRequest': DenyAllianceRequestHandler,
    'acceptAllianceRequest': AcceptAllianceRequestHandler,
    'inviteAllianceRequest': InviteAllianceRequestHandler,
    'suggestAllianceRequest': SuggestAllianceRequestHandler,
    'inviteFriendsAllianceRequest': InviteFriendsAllianceRequestHandler,
    'suggestFriendsAllianceRequest': SuggestFriendsAllianceRequestHandler,
    'getShuffledSuggestedAlliances': GetShuffledSuggestedAlliancesHandler
}


def handle_game_command_list(command_list, answer_list, user):
    if user.is_online:
        for command in command_list:
            command_name = command['cmdName']
            command_data = command['cmdData']

            if command['cmdCount'] >= user.last_command_count + 1:
                if command_name in available_game_commands:
                    print('Game command {} handled , count: {} !'.format(
                        command_name, command['cmdCount']))

                    handler = available_game_commands[command_name]

                    add_command_answer(handler, command_name,
                                       command_data, answer_list, user)

                else:
                    print('Game command {} not handled !'.format(command_name))

                user.last_command_count = command['cmdCount']

            else:
                print('Command {} has already been processed'.format(
                    command['cmdCount']))

        user.last_command_time = datetime.utcnow()
        user.save()

    else:
        # Can happen since their online detection is the worst shit i've ever seen, in fact if you keep touching your
        # screen and moving on the base the game doesn't disconnect you for inactivity after more than 6 minutes even
        # if the game didn't sent any command so we gotta disconnect the client if we receive a command after more than 6 minutes

        answer_list.append({'cmdName': 'logOut', 'cmdData': {}})


def handle_command(command_name, command_data, answer_command, command_name_field, user):
    if command_name in available_commands:
        print('Command {} handled !'.format(command_name))

        handler = available_commands[command_name]
        command_handler = handler(user, command_data, answer_command)

        if command_handler.command_name is not None:
            answer_command[command_name_field] = command_handler.command_name

        else:
            answer_command[command_name_field] = command_name

        command_handler.process_command()

    else:
        print('Command {} not handled !'.format(command_name))


def add_command_answer(handler, answer_command_name, command_data, answer_list, user):
    answer_command = {}
    answer_command['cmdData'] = {}

    command_handler = handler(
        user, command_data, answer_command['cmdData'], answer_list)

    command_handler.process_command()

    if answer_command['cmdData']:
        answer_command['cmdName'] = answer_command_name
        answer_list.append(answer_command)
