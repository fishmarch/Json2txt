import json
import os
import glob
from tqdm import tqdm


def get_files(path, _ends=['*.json']):
    all_files = []
    for _end in _ends:
        files = glob.glob(os.path.join(path, _end))
        all_files.extend(files)
    file_num = len(all_files)
    return all_files, file_num


def get_text_mark(file_path):
    with open(file_path, 'r', encoding='utf-8') as fid:
        result_dict = json.load(fid)
        obj = result_dict['outputs']['object']
        names = file_path.split('\\')
        name = names[len(names)-1]
        file_name = name[:-5]
        all_text_mark = []
        all_text_mark.append(file_name+' ')
        all_text_mark.append(str(len(obj))+' ')
        for obj_item in obj:
            text = obj_item['name']
            try:
                coords = obj_item['polygon']
                try:
                    output_coord = [int(float(coords['x1'])), int(float(coords['y1'])), int(float(coords['x2']))
                        , int(float(coords['y2'])), int(float(coords['x3'])), int(float(coords['y3'])),
                                    int(float(coords['x4'])), int(float(coords['y4']))]
                except:
                    continue
            except:
                coords = obj_item['bndbox']
                try:
                    output_coord = [int(float(coords['xmin'])), int(float(coords['ymin'])),
                                    int(float(coords['xmax'])), int(float(coords['ymax']))]
                    print(output_coord)
                except:
                    continue
            output_text = text + ' 0.99 '
            for item in output_coord:
                output_text = output_text + str(item) + ' '
            all_text_mark.append(output_text)
        return all_text_mark


def write_to_txt(out_txt_path, one_file_all_mark):
    # windows
    with open(os.path.join(out_txt_path, file.split('\\')
                                         [-1].split('.')[0] + '.txt'), 'a+', encoding='utf-8') as fid:
        ##linux
        # with open(os.path.join(out_txt_path, file.split('/')
        #                                      [-1].split('.')[0] + '.txt'), 'a+', encoding='utf-8') as fid:
        for item in one_file_all_mark:
            fid.write(item)


if __name__ == "__main__":
    json_path = 'D:\\桌面\\outputs'
    out_txt_path = 'D:\\桌面\\outputs\\object.txt'
    files, files_len = get_files(json_path)
    bar = tqdm(total=files_len)
    with open(out_txt_path, 'a+', encoding='utf-8') as fid:
        for file in files:
            bar.update(1)
            print(file)
            try:
                one_file_all_mark = get_text_mark(file)
            except:
                print(file)
                continue
            for item in one_file_all_mark:
                fid.write(item)
            fid.write('\n')
    bar.close()
