import os
import requests
import pandas as pd
from PIL import Image
from settings import *
from prettytable import PrettyTable

def load_data():
    '''
    加载数据
    '''
    file_name = '/Users/Morris/Documents/Repositories/pokemon-stats/POKEMONS_STATS.csv'
    df = pd.read_csv(file_name)

    return df


def display_intro_table():
    '''
    用表格展示该程序如何使用
    '''
    x = PrettyTable()
    x.title = '欢迎来到 Pokemon 世界'
    x.field_names = ["I", 'II', "III", "IV"]
    x.add_row(['1.Name', '2.Hp', '3.Attack', '4.Defense'])
    x.add_row(['5.Special Atk', '6.Special Def', '7.Speed', '8.Total'])

    print(x)


def get_user_input(df):
    '''
    获取用户输入
    '''
    while True:
        # 显示简介表格
        display_intro_table()

        # 获取用户输入
        user_input = input(FIRST_INPUT)

        # 判断是否直接退出
        if user_input.lower() == EXIT or user_input == '':
            os._exit(0)

        # 判断用户输入是否正确
        condition_1 = user_input.title() not in list(df['english_name'])
        condition_2 = user_input.lower() not in TOP_STATS.keys()
        if condition_1 and condition_2:
            # 若不正确的话重新输入
            print('请按要求输入需查询的信息！')
            continue
        else:
            # 若正确则返回用户输入
            return user_input.title()


def select_pokemon(df, user_input):
    '''
    根据用户输入选择 Pokemon
    '''
    # 获取被选择的 Pokemon
    selected = df[df['english_name'] == user_input]
    flag = FLAG_DETAIL

    return selected, flag


def get_pokemon_rank(df, user_input):
    '''
    获取 Pokemon 的排名信息
    '''
    selected = df.sort_values(by=[TOP_STATS[user_input]], ascending=False)[:10]

    return selected


def get_pokemon_info(selected):
    '''
    获取被选中的Pokemon信息
    '''
    # 基础信息
    base_info = ["chinese_name", "english_name", "category",
                 "type_1", "type_2", "ability_1", "ability_2"]
    get_pokemon_stats(selected, base_info)

    # 种族值信息
    stat_info = ["total", "hp", "atk", "defense",
                 "spatk", "spdef", 'speed']
    get_pokemon_stats(selected, stat_info)

    # 其他信息
    other_info = ["height_m", "weight_kg", "catch_rate",
                  "hatch_time", "exp_100"]
    get_pokemon_stats(selected, other_info)

    # 属性相克1
    against_info_1 = ["against_bug", "against_dark", "against_dragon",
                      "against_electric", "against_fairy", "against_fight"]
    get_pokemon_stats(selected, against_info_1)

    # 属性相克2
    against_info_2 = ["against_fire", 'against_flying', "against_ghost",
                      "against_grass", "against_ground", "against_ice"]
    get_pokemon_stats(selected, against_info_2)

    # 属性相克3
    against_info_3 = ["against_normal", "against_poison", "against_psychic",
                      "against_rock", "against_steel", "against_water"]
    get_pokemon_stats(selected, against_info_3)


def get_top_ten_stat(selected_pokemon, user_input):
    '''
    获取种族值前10的Pokemon
    '''
    flag = FLAG_TOP_TEN
    x = PrettyTable()

    # 获取top10的Pokemon名字
    x.add_column('Rank',
                 [rank for rank in range(1, 11)])
    x.add_column('English Name',
                 [name for name in selected_pokemon.english_name.values])
    x.add_column('Chinese Name',
                 [name for name in selected_pokemon.chinese_name.values])
    x.add_column(STATS_DICT[TOP_STATS[user_input]],
                 [value for value in selected_pokemon[TOP_STATS[user_input]].values])
    x.add_column('Generation',
                 [GENERATION[value] for value in selected_pokemon.generation.values])

    return x, flag


def get_pokemon_stats(selected_pokemon, user_input):
    '''
    获取被选中的Pokemon信息
    '''
    # 以表格的形式输出
    x = PrettyTable()

    for i in range(len(user_input)):
        x.add_column(user_input[i],
                     selected_pokemon[user_input[i]].values)

    display_pokemon_info(x, user_input)


def is_display_image():
    '''
    判断用户是否像查看 Pokemon 图片
    '''
    user_input = input(DISPLAY_IMAGE_INPUT)

    return user_input.lower()


def download_image(url):
    '''
    根据 imgage_url 下载 Pokemon 图片

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

    display_image(file_path)


def display_image(file_path):
    '''
    展示 Pokemon 图片
    '''
    print('图片下载成功，以保存至 {}'.format(file_path))
    img = Image.open(file_path)
    img.show()


def display_pokemon_info(x, user_input, flag=None):
    '''
    展示获取的 Pokemon 信息
    '''
    if flag == FLAG_TOP_TEN:
        print(x.get_string(title='Top 10 {} Pokemons'.format(
            STATS_DICT[TOP_STATS[user_input]])))
    else:
        print(x)


def main():
    while True:
        # 加载 Pokemon 数据集
        df = load_data()

        # 获取用户输入
        user_input = get_user_input(df)

        # 查询单个 Pokemon 详细信息
        if user_input in list(df['english_name']):
            # 查找被选中的 Pokemon
            selected_pokemon, flag = select_pokemon(df, user_input)
            # 获取 Pokemon 各项信息
            get_pokemon_info(selected_pokemon)

        # 查询 Pokemon 的前十排名
        if user_input in TOP_STATS.keys():
            # 查找符合条件的 Pokemon
            selected_pokemon = get_pokemon_rank(df, user_input)
            # 展示符合条件的 Pokemon
            x, flag = get_top_ten_stat(selected_pokemon, user_input)
            display_pokemon_info(x, flag, user_input)
            # 查找排名前十的 Pokemon 的详细信息
            user_input = input(DISPLAY_DETAIL_INPUT)

            if type(user_input) == str:
                user_input = user_input.title()
                if user_input in list(df['english_name']):
                    # 查找被选中的 Pokemon
                    selected_pokemon, flag = select_pokemon(df, user_input)
                    # 获取 Pokemon 各项信息
                    get_pokemon_info(selected_pokemon)
                elif user_input.lower() == EXIT: # 输入 "q" 退出程序
                    break
                else: # 输入其他重新开始程序
                    main()

        if flag == FLAG_DETAIL:
            # 判断用户是否想查看当前 Pokemon 的图片
            if is_display_image() == 'img':  # 如果用户想要查看 image
                # 获取当前 Pokemon 的 image url
                print('请稍后，正在下载 {} ...'.format(user_input))
                img_url = df[df['english_name'] ==
                             user_input]['image_url'].values[0]
                download_image(img_url)
            else:  # 不查看 image 重新执行程序
                main()

        restart = input(EXIT_INPUT)
        if restart.lower() == EXIT:
            break


if __name__ == "__main__":
    main()
