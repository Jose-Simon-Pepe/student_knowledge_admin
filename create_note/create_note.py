import os
import shutil
import sys
import datetime

# Función para crear una nota siguiendo el estándar zettelk
def crear_nota(args):
    run_editor:str = "nvim"
    separator = "---"+"\n"
    title_words = [word for word in args if not word.startswith("-")]
    tags = [word.replace("-", "#") for word in args if word.startswith("-")]
    title = '_'.join(map(str, title_words))
    target = "/home/peace/notes/study/"+title+".md"
    
    if len(sys.argv[1:]) == 0:
        target = os.getcwd() + "/nonamednote.md"

    new_first_line = "# "+" ".join(map(str, title_words))
    tags_end_line = " ".join(map(str, [tag for tag in tags]))

    with open(target, "a") as file:
        first_line = separator
        second_line = "ID: "+str(hash(' '.join(map(str, title_words)))) + "\n"  # id
        third_line = "Date: "+str(datetime.datetime.now()) + "\n"
        fourth_line = separator
        fifth_line = new_first_line + "\n"
        sixth_line = tags_end_line
        file.writelines([first_line,
                         second_line,
                         third_line,
                         fourth_line,
                         fifth_line,
                         sixth_line])

    os.system(run_editor+" "+target)

def main():
    args = sys.argv[1:]
    crear_nota(args)

if __name__ == "__main__":
    main()
