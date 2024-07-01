from scraper import scrape
from send_message import post_to_groupme

def main():
    # Get bots info
    bots_path = '/Users/chasereynders/Developer/personal-projects/yale-menus-projects/yale-menus-groupme-bots/bots.json'
    bot_dicts = scrape(bots_path)
    # Send groupme messages
    for bot_dict in bot_dicts:
        post_to_groupme(bot_dict)


if __name__ == "__main__":
    main()


# bot_dicts = [{'term': 'pancakes', 'bot_id': 'e1aa9e3fd2633cdf562b349283', 'breakfast': '', 'brunch_lunch':'', 'dinner': ''}]