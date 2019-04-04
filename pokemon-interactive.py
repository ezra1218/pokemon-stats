import pandas as pd
from prettytable import PrettyTable

def load_data():
    '''
    加载数据
    '''
    file_name = '/Users/Morris/Desktop/Udacity/data_analysis/my_project/01-pokemon/pokemon.csv'
    df = pd.read_csv(file_name)

    return clean_data(df)

def clean_data(df):
    '''
    清理数据
    '''
    # 删除 classfication 后面的 Pokemon 字符
    df.classfication = df.classfication.map(lambda x:x[:-8])

    return df

def get_user_input():
    '''
    获取用户输入
    '''
    part1 = '欢迎来到神奇宝贝数据世界，请输入要查询的神奇宝贝'
    part2 = '或输入hp、atk、def、spatk、spdef、spd查看排名前十的Pokemon：\n'
    user_input = input('{}，{}'.format(part1, part2)).title()

    return  user_input

def select_pokemon(df, user_input):
    '''
    根据用户输入选择Pokemon
    '''
    selected = df[df['name'] == user_input]
    return selected

def get_pokemon_info(selected):
    '''
    获取被选中的Pokemon信息
    '''

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

def main():
    while True:
        # 获取用户输入
        user_input = get_user_input()

        # 加载Pokemon数据集
        df = load_data()

        # 获取被选中的Pokemon
        selected = select_pokemon(df, user_input)

        # 获取Pokemon各项信息
        get_pokemon_info(selected)

        restart = input('\n输入‘y’键继续探索或按输入任意键退出\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
