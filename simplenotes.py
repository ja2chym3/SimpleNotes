import os
import pathlib
from anytree import Node, RenderTree
from sys import argv

def getFiles(path: str) -> list: # name, path
    files = []
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            files.append([(pathlib.Path(f).resolve().stem), os.path.join(path, f)])
    return files

# H1_a {h2_a {h3_a, h3_b...}, h2_b...},  H1_b...
def getHeadings(file: str):
    with open(file[1], "r", encoding="utf8") as f:
        border = "=" * (len(file[0])+8)
        root = Node(f"{border}\n=== {file[0].upper()} ===\n{border}\n")
        high, mid = None, None
        for line in f:
            if "#" == line[0]:
                if "###" == line[0:3]:
                    Node(line.rstrip()[3:], parent=mid)
                elif "##" == line[0:2]:
                    mid = Node(line.rstrip()[2:], parent=high)
                else:
                    high = Node(line.rstrip()[1:], parent=root)
    return root
file = getFiles("notes/")[2]


def makeIndex(filesLocation, outputLocation):
    files = getFiles(filesLocation)
    with open(outputLocation, "w", encoding="utf8") as outFile:
        for file in files:
            for pre, fill, node in RenderTree(getHeadings(file)):
                outFile.write("%s%s\n" % (pre, node.name))
            outFile.write("\n\n\n")

if __name__ == '__main__':
    HELPMESSAGE = """
This is a simple python script for generating an index of all your markdown notes.

python simplenotes.py <notes_dir> <output_file>

All the notes must be in the <notes_dir>, any nested structure will not be read for now.
The output file must be a text file, if existing, it will be overwritten.
"""
    if len(argv) == 3:
        try:
            makeIndex(str(argv[1]), str(argv[2]))
        except Exception as e:
            print(HELPMESSAGE)
            raise e
    else:
        print(HELPMESSAGE)