from command.base_command import BaseCommand


class QueryStarsBookmarksHandler(BaseCommand):

    def answer(self):
        self.answer_command_data['Bookmarks'] = []

        for bookmark in self.user.profile.stars_bookmarks:
            bookmark_info = {}
            bookmark_info['sku'] = bookmark.sku
            bookmark_info['starId'] = bookmark.star_id
            bookmark_info['starType'] = bookmark.type
            bookmark_info['starName'] = bookmark.star_name
            bookmark_info['starNameUserEdited'] = bookmark.edited_name

            self.answer_command_data['Bookmarks'].append(bookmark_info)
