def get_search_table(goal):
    table = {}
    n = len(goal)
    for i in range(n - 1):
        table[goal[i]] = n - i - 1
    return table


def search_links(txt, depth):
    global visited_sites
    size = len(txt)
    goal = '<a href="/wiki/'
    goal_size = len(goal) - 1
    good_shit = []
    titles = []

    while goal_size < size:
        y = 0
        while txt[goal_size - y] == goal[-1 - y]:
            y += 1
            if y == len(goal) - 1:
                z = 0
                while txt[goal_size + z] != '"':
                    z += 1
                content = txt[goal_size - 5:goal_size + z]
                if ":" not in content:
                    if visited_sites.get(content, -1) == -1 or visited_sites[content] <= depth:
                        if depth != -1:
                            visited_sites[content] = depth
                        good_shit.append(content)
                        txt_end = z + 9
                        while txt[goal_size + txt_end] != '"':
                            txt_end += 1
                        titles.append(txt[goal_size + z + 9:goal_size + txt_end])
                break
        goal_size += search_table.get(txt[goal_size], len(goal))
    return good_shit, titles


def search(page, searched_page, path, depth):
    global total_sites

    total_sites += 1
    print('\rNumber of sites loaded = ' + str(total_sites) + ' ----------- ' + path, end='')

    links, titles = search_links(page.text, depth)
    if depth == -1:
        for i in range(len(links)):
            if 'https://en.wikipedia.org' + links[i] == searched_page:
                return path + ' / ' + titles[i]
        return

    for i in range(len(links)):
        if 'https://en.wikipedia.org' + links[i] == searched_page:
            return path + ' / ' + titles[i]
        test = search(requests.get('https://en.wikipedia.org' + links[i]), searched_page, path + ' / ' + titles[i],
                      depth - 1)
        if test is not None:
            return test


if __name__ == '__main__':
    import requests

    total_sites = 0
    visited_sites = {}
    search_table = get_search_table('<a href="/wiki/')
    starting_page = requests.get('https://en.wikipedia.org/wiki/Main_Page')
    ending_page = 'https://fr.wikipedia.org/wiki/420'

    print()
    print('===========================================================================================================')
    print()
    print()
    depth_search = -1
    x = search(starting_page, ending_page, 'Main Page', depth_search)
    while x is None:
        depth_search += 1
        x = search(starting_page, ending_page, 'Main Page', depth_search)

    print('\r' + str(x))
    print()
    print()
    print('===========================================================================================================')
    print('number of sites loaded : ', total_sites)
    print('number of sites checked : ', len(visited_sites))
