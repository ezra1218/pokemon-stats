import pandas as pd
from prettytable import PrettyTable
from PIL import Image
import os
import requests

DEFAULT_PATH = './pokemon-image/'

TOP_STATS = {'2': 'hp',
             '3': 'attack',
             '4': 'defense',
             '5': 'sp_attack',
             '6': 'sp_defense',
             '7': 'speed',
             '8': 'base_total',
             '9': 'height_m',
             '10': 'weight_kg',
             '11': 'base_happiness',
             '12': 'is_legendary'
}

STATS_DICT = {'hp': 'Hp',
              'attack': 'Attack',
              'defense': 'Defense',
              'sp_attack': 'Special Attack',
              'sp_defense': 'Special Defense',
              'speed': 'Speed',
              'base_total': 'Total',
              'height_m': 'Height',
              'weight_kg': 'Weight',
              'base_happiness': 'Base Happiness',
              'is_legendary': 'Legendary'
}

def load_data():
    '''
    加载数据
    '''
    file_name = '/Users/Morris/Documents/Repositories/pokemon-stats/POKEMONS_STATS.csv'
    df = pd.read_csv(file_name)

    return clean_data(df)

# def clean_data(df):
    '''
    清理数据
    '''
    # 删除 classfication 后面的 Pokemon 字符
    df.classfication = df.classfication.map(lambda x:x[:-8])

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
    x.add_row(['9.Tallest', '10.Heaviest', '11.Base Happiness', '12.Legendary'])

    print(x)

def get_user_input(df):
    '''
    获取用户输入
    '''
    while True:
        # 显示简介表格
        display_intro_table()

        # 获取用户输入
        user_input = input('请输入Pokemon的名字或输入对应的数字查看信息或输入"q"退出：\n')

        # 判断是否直接退出
        if user_input.lower() == 'q' or user_input == '':
            os._exit(0)

        # 判断用户输入是否正确
        condition_1 = user_input.title() not in list(df['name'])
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
    根据用户输入选择Pokemon
    '''
    # 获取被选择的 Pokemon
    selected = df[df['name'] == user_input]
    flag = 'detail'

    return selected, flag

def get_pokemon_rank(df, user_input):
    '''
    获取 Pokemon 的排名信息
    '''
    if user_input != '12':
        selected = df.sort_values(by=[TOP_STATS[user_input]], ascending=False)[:10]
    else:
        selected = df.query('is_legendary == 1')
    flag = 'rank'

    return selected, flag

def get_pokemon_info(selected):
    '''
    获取被选中的Pokemon信息
    '''
    # 基础信息
    base_info = ["name", "classfication", "type1", "type2", "abilities"]
    display_pokemon_stats(selected, base_info)

    # 种族值信息
    stat_info = ["base_total", "hp", "attack", "defense",
                 "sp_attack", "sp_defense", 'speed']
    display_pokemon_stats(selected, stat_info)

    # 其他信息
    other_info = ["height_m", "weight_kg", "base_happiness",
                  "capture_rate", "base_egg_steps", "experience_growth"]
    display_pokemon_stats(selected, other_info)

    # 属性相克1
    against_info_1 = ["against_bug", "against_dark", "against_dragon",
                     "against_electric", "against_fairy", "against_fight"]
    display_pokemon_stats(selected, against_info_1)

    # 属性相克2
    against_info_2 = ["against_fire", 'against_flying', "against_ghost",
                     "against_grass", "against_ground", "against_ice"]
    display_pokemon_stats(selected, against_info_2)

    # 属性相克3
    against_info_3 = ["against_normal", "against_poison", "against_psychic",
                     "against_rock", "against_steel", "against_water"]
    display_pokemon_stats(selected, against_info_3)

def display_top_ten_stat(selected_pokemon, pokemon_stat):
    '''
    获取种族值前10的Pokemon
    '''
    x = PrettyTable()

    # 获取top10的Pokemon名字
    if pokemon_stat != '12':
        x.add_column(TOP_STATS[pokemon_stat],
                     [name for name in selected_pokemon.name.values])
        x.add_column('stat_value',
                     [value for value in selected_pokemon[TOP_STATS[pokemon_stat]].values])
        print(x.get_string(title='Top 10 {} Pokemons'.format(STATS_DICT[TOP_STATS[pokemon_stat]])))
    else:
        x.add_column('ALL LEGENDARY POKEMONS',
                     [name for name in selected_pokemon.name.values])
        print(x)

def display_pokemon_stats(selected_pokemon, pokemon_stats):
    '''
    输出被选中的Pokemon信息
    '''
    # 以表格的形式输出
    x = PrettyTable()

    for i in range(len(pokemon_stats)):
        x.add_column(pokemon_stats[i],
                     selected_pokemon[pokemon_stats[i]].values)

    print(x)

def is_display_image():
    '''
    判断用户是否像查看 Pokemon 图片
    '''
    part1 = '输入"img"加回车下载并查看该 Pokemon 的图片'
    part2 = '输入任意键加回车返回上一级菜单'
    user_input = input('{}\n{}:\n'.format(part1, part2))

    return user_input.lower()

def download_image(url):
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

    display_image(file_path)

def display_image(file_path):
    '''
    展示 Pokemon 图片
    '''
    print('图片下载成功，以保存至 {}'.format(file_path))
    img = Image.open(file_path)
    img.show()

def main():
    while True:
        # 加载 Pokemon 数据集
        df = load_data()

        # 获取用户输入
        user_input = get_user_input(df)

        # 查询单个 Pokemon 详细信息
        if user_input in list(df['name']):
            # 查找被选中的 Pokemon
            selected, flag = select_pokemon(df, user_input)
            # 获取 Pokemon 各项信息
            get_pokemon_info(selected)

        # 查询 Pokemon 的排名
        if user_input in TOP_STATS.keys():
            # 查找符合条件的 Pokemon
            selected, flag = get_pokemon_rank(df, user_input)
            # 展示符合条件的 Pokemon
            display_top_ten_stat(selected, user_input)

        if flag == 'detail':
            # 判断用户是否想查看当前 Pokemon 的图片
            if is_display_image() == 'img': # 如果用户想要查看 image
                # 获取当前 Pokemon 的 image url
                print('请稍后，程序正在下载 {} ...'.format(user_input))
                img_url = df[df['name'] == user_input]['img_url'].values[0]
                download_image(img_url)
            else: # 不查看 image 重新执行程序
                main()

        restart = input('\n输入任意键加回车继续探索或输入"q"加回车退出\n')
        if restart.lower() == 'q':
            break

if __name__ == "__main__":
	main()
