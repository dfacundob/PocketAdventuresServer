from sqlalchemy import and_
from command.base_command import BaseCommand
from database.models.galaxy.galaxy import Galaxy
from database.models.user.star_bookmark import StarsBookmarks


class UpdateStarsBookmarksHandler(BaseCommand):

    def process(self):
        action = self.command_data['action']

        if action == 'addBookmark':
            galaxy = Galaxy.query.get(self.command_data['starId'])

            if galaxy is not None:
                self.user.profile.stars_bookmarks.append(StarsBookmarks(
                    x=galaxy.x,
                    y=galaxy.y,
                    type=galaxy.type,
                    star_id=galaxy.id,
                    star_name=galaxy.name,
                    edited_name=self.command_data['starNameUserGenerated']))

            else:
                print('An user tried to add an unknown galaxy to his bookmarks: {}-{}'.format(self.command_data['coordX'], self.command_data['coordY']))

        elif action == 'removeBookmark':
            bookmark = self.user.profile.stars_bookmarks.filter(and_(StarsBookmarks.x == self.command_data['coordX'],
                                                                     StarsBookmarks.y == self.command_data['coordY'])).first()

            if bookmark is not None:
                bookmark.delete()

            else:
                print('An user tried to delete an unknown bookmark: {}-{}'.format(self.command_data['coordX'], self.command_data['coordY']))

        self.user.profile.save()
