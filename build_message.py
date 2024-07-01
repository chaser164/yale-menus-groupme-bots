from datetime import datetime

colleges = ['BK', 'BR', 'SB', 'DP', 'ES', 'MO', 'BF', 'PM', 'GH', 'JE', 'PS', 'SM', 'TD', 'TB']


def build_message_string(pref):
    header = f'-------------------------------\n{datetime.now().month}/{datetime.now().day} results for "{pref['term']}"\n\n'
    footer = '\n-------------------------------'

    results_if_matches = ''

    any_hits = False

    # BREAKFAST
    count = 0
    included_colleges = ''
    # Accumulate colleges
    for col in colleges:
        if col in pref['breakfast']:
            count += 1
            included_colleges += col + ', '
    # Append
    if count > 0:
        any_hits = True
        results_if_matches += 'breakfast:\n'
        if count == 14:
           results_if_matches += 'all colleges\n\n'
        else:
            results_if_matches += included_colleges[:-2] + '\n\n'

    # BRUNCH / LUNCH
    count = 0
    included_colleges = ''
    # Accumulate colleges
    for col in colleges:
        if col in pref['brunch_lunch']:
            count += 1
            included_colleges += col + ', '
    # Append
    if count > 0:
        any_hits = True
        results_if_matches += 'brunch / lunch:\n'
        if count == 14:
           results_if_matches += 'all colleges\n\n'
        else:
            results_if_matches += included_colleges[:-2] + '\n\n'

    # DINNER
    count = 0
    included_colleges = ''
    # Accumulate colleges
    for col in colleges:
        if col in pref['dinner']:
            count += 1
            included_colleges += col + ', '
    # Append
    if count > 0:
        any_hits = True
        results_if_matches += 'dinner:\n'
        if count == 14:
           results_if_matches += 'all colleges'
        else:
            results_if_matches += included_colleges[:-2]

    if any_hits:
        return header + results_if_matches + footer
    else:
        return 'NO_HITS'