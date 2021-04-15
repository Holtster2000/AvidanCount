from PIL import Image
from sty import fg, bg, ef, rs, RgbBg, Style
import pandas as pd


# Change these variables:
imagePath = "C:\\Users\\bp\OneDrive - Michigan State University\_IBIO 150\AvidaResearch\Images\\"
n_configs = 3       # number of configurations (Put in folders named "ConfigA-B" where A is config # and B is trial #)
n_trials = 5        # number of trials
n_updates = 300     # number of updates (name pictures "50.png", "100.png", etc. for every 50 updates)

pos = (232, 226)    # center pixel of top left cell
width = 31          # pixel width of each cell
gap = 1             # pixel gap between each cell
cells = (21, 15)    # size of dish (e.g. 21 x 15 cells)

# Ancestor RGB color values:
ancestors = [[0, 109, 219], [255, 109, 182], [220, 190, 0],
             [0, 93, 93], [182, 219, 255], [93, 20, 166],
             [254, 182, 219], [156, 82, 10], [182, 109, 255]]
# Don't modify past here!

# Colors for print_colored_cells function... comment out if you don't have sty installed
bg.a1 = Style(RgbBg(ancestors[0][0], ancestors[0][1], ancestors[0][2]))
bg.a2 = Style(RgbBg(ancestors[1][0], ancestors[1][1], ancestors[1][2]))
bg.a3 = Style(RgbBg(ancestors[2][0], ancestors[2][1], ancestors[2][2]))
bg.a4 = Style(RgbBg(ancestors[3][0], ancestors[3][1], ancestors[3][2]))
bg.a5 = Style(RgbBg(ancestors[4][0], ancestors[4][1], ancestors[4][2]))
bg.a6 = Style(RgbBg(ancestors[5][0], ancestors[5][1], ancestors[5][2]))
bg.a7 = Style(RgbBg(ancestors[6][0], ancestors[6][1], ancestors[6][2]))
bg.a8 = Style(RgbBg(ancestors[7][0], ancestors[7][1], ancestors[7][2]))
bg.a9 = Style(RgbBg(ancestors[8][0], ancestors[8][1], ancestors[8][2]))

colors = [bg.a1, bg.a2, bg.a3, bg.a4, bg.a5, bg.a6, bg.a7, bg.a8, bg.a9]


# checks if pixel matches any ancestors and return the number. returns 0 if not matched
def check_pixel(pixel):
    p = [pixel[x] for x in range(3)]
    for a in range(len(ancestors)):
        if p == ancestors[a]:
            return a+1
    return 0


# converts cell coordinates to pixel coordinates (e.g. 4,3 is cell in 5th col 4th row)
def get_coordinates(x, y):
    return pos[0]+(x*(width+gap)), pos[1]+(y*(width+gap))


# print cell colors to console. (need sty installed)
def print_colored_cells(results):
    for r in results:
        for c in r:
            if c == 0:
                print(" ", end="")
            else:
                print(colors[c-1] + " " + bg.rs, end="")
        print("")


# print avidian counts to console.
def print_counts(counts):
    for a in range(len(counts)):
        print(f"Ancestor{a+1}: {counts[a]}")


# create empty dict that mirrors the spreadsheet setup
data = {
    "Configuration": [],
    "Trial": [],
    "Ancestor Avidian": [],
    "50": [],
    "100": [],
    "150": [],
    "200": [],
    "250": [],
    "300": []
}

# actual image processing:
for config in range(1, n_configs+1):
    # seed data in the configuration column
    data["Configuration"].append(config)
    for _ in range(len(ancestors)*n_trials-1):
        data["Configuration"].append(None)

    # trials:
    for trial in range(1, n_trials+1):
        # seed data in the trial column and ancestor avidian column
        for i in range(len(ancestors)):
            if i == 0:
                data["Trial"].append(trial)
            else:
                data["Trial"].append(None)
            data["Ancestor Avidian"].append(i + 1)

        # start at 50.png and go through all pictures in trial folder
        for update in range(50, n_updates+1, 50):
            # load image using PIL library
            with Image.open(imagePath+f"Config{config}-{trial}\\{update}.png") as im:
                px = im.load()

            # initialize result and count lists (results only used for colored output fn)
            results = [[0 for _ in range(cells[0])] for _ in range(cells[1])]
            counts = [0 for _ in range(len(ancestors))]

            # check all cell center pixels and check for matching avidian
            for i in range(cells[0]):
                for j in range(cells[1]):
                    ancestor = check_pixel(px[get_coordinates(i, j)])
                    results[j][i] = ancestor

                    # increment count if a match was found
                    if ancestor != 0:
                        counts[ancestor-1] += 1

            # add counts to data dict
            for av in range(len(ancestors)):
                data[f"{update}"].append(counts[av])

# convert data to a pandas dataframe for output and converting to csv
df = pd.DataFrame(data)
print(df)
df.to_csv("out.csv", index=False)

# print_counts(counts)
# print_colored_cells(results)
