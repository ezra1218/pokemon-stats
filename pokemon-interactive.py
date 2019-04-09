import pandas as pd
from prettytable import PrettyTable
from PIL import Image
import os
import requests

DEFAULT_PATH = './pokemon-image/'

TOP_STATS = {'total': 'base_total',
             'hp': 'hp',
             'atk': 'attack',
             'def': 'defense',
             'spatk': 'sp_attack',
             'spdef': 'sp_defense',
             'spd': 'speed'}

def load_data():
    '''
    加载数据
    '''
    file_name = '/Users/Morris/Desktop/Udacity/data_analysis/my_project/01-pokemon/pokemon3.csv'
    df = pd.read_csv(file_name)

    return clean_data(df)

def clean_data(df):
    '''
    清理数据
    '''
    # 删除 classfication 后面的 Pokemon 字符
    df.classfication = df.classfication.map(lambda x:x[:-8])

    return df

def get_user_input(df):
    '''
    获取用户输入
    '''
    while True:
        part0 = '欢迎来到 Pokemon 的世界'
        part1 = '若要查询Pokemon，请输入Pokemon名称'
        part2 = '或输入total、hp、atk、def、spatk、spdef、spd查看排名前十的Pokemon'
        part3 = '或输入"q"退出'
        print('{}\n{}\n{}\n{}'.format(part0, part1, part2, part3))

        user_input = input('请输入要查询的内容：\n')

        # 判断是否直接退出
        if user_input.lower() == 'q':
            break

        # 判断用户输入是否正确
        condition_1 = user_input.title() not in list(df['name'])
        condition_2 = user_input.lower() not in TOP_STATS.keys()
        if condition_1 and condition_2:
            # 若不正确的话重新输入
            continue
        else:
            # 若正确则返回用户输入
            return user_input.title()

def select_pokemon(df, user_input):
    '''
    根据用户输入选择Pokemon
    '''
    # 判断用户输入
    if user_input.lower() in TOP_STATS.keys():
        flag = user_input.lower()
        selected = df.sort_values(by=[TOP_STATS[flag]],
                                  ascending=False)[:10]
    else:
        flag = 'pokemon'
        selected = df[df['name'] == user_input]

    return selected, flag

def get_pokemon_info(selected, flag):
    '''
    获取被选中的Pokemon信息
    '''
    if flag == 'pokemon':
        # 基础信息
        base_info = ["name", "classfication", "type1", "type2", "abilities"]
        output_pokemon_stats(selected, base_info)

        # 种族值信息
        stat_info = ["base_total", "hp", "attack", "defense",
                     "sp_attack", "sp_defense", 'speed']
        output_pokemon_stats(selected, stat_info)

        # 其他信息
        other_info = ["height_m", "weight_kg", "base_happiness",
                      "capture_rate", "base_egg_steps", "experience_growth"]
        output_pokemon_stats(selected, other_info)

        # 属性相克1
        against_info_1 = ["against_bug", "against_dark", "against_dragon",
                         "against_electric", "against_fairy", "against_fight"]
        output_pokemon_stats(selected, against_info_1)

        # 属性相克2
        against_info_2 = ["against_fire", 'against_flying', "against_ghost",
                         "against_grass", "against_ground", "against_ice"]
        output_pokemon_stats(selected, against_info_2)

        # 属性相克3
        against_info_3 = ["against_normal", "against_poison", "against_psychic",
                         "against_rock", "against_steel", "against_water"]
        output_pokemon_stats(selected, against_info_3)
    else:
        get_top_ten_stat(selected, flag)

def get_top_ten_stat(selected_pokemon, stat):
    '''
    获取种族值前10的Pokemon
    '''
    x = PrettyTable()

    # 获取top10的Pokemon名字
    x.add_column(TOP_STATS[stat],
                 [name for name in selected_pokemon.name.values])
    x.add_column('stat_value',
                 [value for value in selected_pokemon[TOP_STATS[stat]].values])

    print(x)

def output_pokemon_stats(selected_pokemon, pokemon_stats):
    '''
    输出被选中的Pokemon信息
    '''
    # 以表格的形式输出
    x = PrettyTable()

    for i in range(len(pokemon_stats)):
        x.add_column(pokemon_stats[i],
                     selected_pokemon[pokemon_stats[i]].values)

    print(x)

def wanna_show():
    '''
    判断用户是否像查看 Pokemon 图片
    '''
    part1 = '输入"img"加回车下载并查看该 Pokemon 的图片'
    part2 = '输入任意键加回车返回上一级菜单'
    user_input = input('{}\n{}:\n'.format(part1, part2))

    return user_input.lower()

def download_img(url):
    '''
    根据 img_link 下载 Pokemon 图片

    params:
        url: 需下载的图片链接
    '''
    r = requests.get(url, stream=True)

    # 保存的文件名
    file_name = url.split('/')[-1]

    # 创建文件保存路径
    if not os.path.exists(DEFAULT_PATH):
        os.makedirs(DEFAULT_PATH)

    # 文件路径
    file_path = DEFAULT_PATH+file_name

    # 需指定文件名，否则会出现 [Errno 21] Is a directory 错误
    with open(file_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=32):
            f.write(chunk)

    show_img(file_path)

def show_img(file_path):
    '''
    展示 Pokemon 图片
    '''
    print('图片下载成功，以保存至 {}'.format(file_path))
    img = Image.open(file_path)
    img.show()


def main():
    while True:
        # 加载Pokemon数据集
        df = load_data()

        # 获取用户输入
        user_input = get_user_input(df)

        if user_input:
            # 获取被选中的Pokemon
            selected, flag = select_pokemon(df, user_input)

            # 获取Pokemon各项信息
            get_pokemon_info(selected, flag)
        else:
            break

        # 判断用户是否想查看当前 Pokemon 的图片
        if wanna_show() == 'img':
            # 获取当前 Pokemon 的 image url
            print('请稍后，程序正在下载 {} ...'.format(user_input))
            img_url = df[df['name'] == user_input]['img_url'].values[0]
            download_img(img_url)

        restart = input('\n输入任意键加回车继续探索或输入"q"加回车退出\n')
        if restart.lower() == 'q':
            break


if __name__ == "__main__":
	main()
