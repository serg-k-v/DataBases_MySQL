import re

def read_data_(source) :
    with open(source, 'r') as content_file:
        return content_file.read()

# artists = read_data_artists('./resources/Artists.txt').splitlines()
# artists = [string.split(" ", 1)[1].split(', ') for string in artists]


# paintings = read_data_('./resources/Paintings.txt')
# artists_id = []
# paintings_on_id = []
# for m in re.finditer(r"(\d+) ?:(( +.+, \d+\n?)+)", paintings):
#     artists_id.append(int(m.group(1)))
#     paintings_on_id.append(m.group(2).split('\n '))
# paintings_on_id = [[s.strip().split(', ') for s in a] for a in paintings_on_id]
#
# print(paintings_on_id)

subtech = read_data_('./resources/Subtechnics.txt')
subtech_id = []
name = []
for m in re.finditer(r"(\d):(( +.+\n?)+)", subtech):
    subtech_id.append(int(m.group(1)))
    name.append(m.group(2).split('\n '))
name = [[s.strip().split(', ') for s in a] for a in name]
print(name)
print(subtech_id)




# paintings_on_id = [[s.strip().split(', ') for s in a] for a in paintings_on_id]
# print(paintings_on_id[0])

# data = read_data_artists('./resources/Techniques.txt')
# techniques = []
# for m in re.findall(r"\w+\n?", data):
#     techniques.append(m.strip())
#
# print(techniques)
# data = read_data_artists('./resources/Painting_styles.txt')
# styles = []
# for m in re.findall(r".+\n?", data):
#     styles.append(m.strip())
#
# print(styles)
