import re
import shutil
from pathlib import Path

def sorting_files(*path_from_bot):
    def translate(name):
        return_name = ""
        for i in name:
            return_name += i.translate(TRANS)
        return return_name

    def iter_dir(path):
        for i in path.iterdir():
            if i.is_dir():
                if Path(i).stem in file_type and Path(i).parents[0] == G_path:
                    pass
                else:
                    iter_dir(i)
                    try:
                        i.rmdir()
                    except OSError:
                        norm_name_file = normalize(str(i.stem))
                        i.rename(Path(i.parents[0], norm_name_file))
            else:
                norm_name = normalize(i.stem)
                norm_name = Path(norm_name + i.suffix)
                sort_file(i, norm_name)


    def sort_file(src_file, name_file):
        suff_file = str(name_file.suffix)
        new_dir = "unknown"
        for key, my_vol in file_type.items():
            if suff_file in my_vol:
                new_dir = key
                break
        if new_dir == "archives":
            unpack_file(src_file, name_file, new_dir)
        elif new_dir == "unknown":
            pass
        else:
            move_file(src_file, name_file, new_dir)
        set_of_list_file_by_type[new_dir].append(name_file)
        set_suffix[new_dir].add((name_file.suffix)[1:])

    def unpack_file(src_file, name_file, new_dir):
        shutil.unpack_archive(src_file, Path(G_path,new_dir,name_file.stem))
        src_file.unlink()

    def move_file(src_file, name_file, new_dir):
        to_file = Path(str(G_path), new_dir, str(name_file))
        iter_post = 1
        while True:
            if Path.is_file(to_file):
                to_file = Path(str(G_path), new_dir, name_file.stem + str(iter_post) + str(name_file.suffix))
                iter_post += 1
            else:
                src_file.rename(to_file)
                break

    def normalize(name):
        trans_name = translate(name)
        norm_name = re.sub(r"\W", "_", trans_name)
        return(norm_name)

    file_type = {'images':['.jpeg', '.png', '.jpg', '.svg', '.bmp'],
                'documents':['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
                'video':['.avi', '.mp4', '.mov', '.mkv'],
                'audio':['.mp3', '.ogg', '.wav', '.amr'],
                'archives':['.zip', '.gz', '.tar']}

    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

    G_path = Path(path_from_bot[1][0].lower())
    print(G_path)
    if not G_path.is_dir():
        return f"Path not found"
    for new_dir in file_type:
        path_new_dir = Path(path_from_bot[1][0],new_dir)
        try:
            Path.mkdir(path_new_dir)
        except FileExistsError:
            pass
    set_of_list_file_by_type = {'images':[],
                                'documents':[],
                                'video':[],
                                'audio':[],
                                'archives':[],
                                'unknown':[]}


    set_suffix = {'images':set(),
                    'documents':set(),
                    'video':set(),
                    'audio':set(),
                    'archives':set(),
                    'unknown':set()}

    iter_dir(G_path)

    return_ = ""
    for kay, value in set_of_list_file_by_type.items():
        return_ += f"list of {kay} files: {', '.join(p.stem for p in value)}\n"
    
    for kay, value in set_suffix.items():
        return_ += f"set {kay} suffix: {', ' .join(p for p in value)}\n"
    return return_

if __name__ == '__main__':
    pass    