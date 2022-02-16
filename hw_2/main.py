import os.path
import subprocess

from hw1tree.tree import Tree


def length(x):
    if not x:
        return 0
    else:
        return 1 + length(x[:-1])


def line(content):
    if not content[1:]:
        return str(content[0]) + " \\\ \n"
    else:
        return str(content[0]) + " & " + line(content[1:])


def begin_of_table(size):
    return "\\begin{tabular}{ " + ("| c " * size) + "| }\n"


def body(content):
    if not content:
        return "\\hline\n"
    else:
        return "\\hline\n" + line(content[0]) + body(content[1:])


def end_of_table():
    return "\end{tabular}\n"


def tex(content):
    if not content:
        return "\documentclass{article}\n" + \
               "\\usepackage[utf8]{inputenc}\n" + \
               "\\begin{document}\n" \
               "\\end{document}"
    else:
        return "\documentclass{article}\n" \
               "\\usepackage[utf8]{inputenc}\n" \
               "\\usepackage{graphicx}" \
               "\\graphicspath{ {./} }" \
               "\\begin{document}\n" + \
               begin_of_table(length(content[0])) + \
               body(content) + \
               end_of_table() + "\n" + \
               "\includegraphics{image.png}" \
               "\\end{document}"


if __name__ == "__main__":
    my_file = open(os.path.join("artifacts", "file.tex"), "w+")
    my_file.write(tex([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]))
    my_file.close()

    t = Tree()
    t.run("image.png")

    subprocess.run('pdflatex ' + os.path.join("artifacts", "file.tex"))

    os.replace("file.pdf", os.path.join("artifacts", "file.pdf"))

    os.remove("file.aux")
    os.remove("file.log")
    os.remove("image.png")
    os.remove(os.path.join("artifacts", "file.tex"))
