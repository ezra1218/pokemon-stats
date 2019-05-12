# 输入语句
FIRST_INPUT = '请输入 Pokemon 的名字\n或输入对应的数字查看信息\n或输入"q"退出\n'
DISPLAY_IMAGE_INPUT = '输入"img"加回车下载并查看该 Pokemon 的图片\n或输入任意键加回车返回上一级菜单\n'
DISPLAY_DETAIL_INPUT = '输入 Pokemon 名字可查询该 Pokemon 的详细信息\n或输入任意键加回车返回上一层\n或输入"q"加回车退出\n'
EXIT_INPUT = '输入任意键加回车继续探索或输入"q"加回车退出\n'

DEFAULT_PATH = './pokemon-image/'

TOP_STATS = {'2': 'hp',
             '3': 'atk',
             '4': 'defense',
             '5': 'spatk',
             '6': 'spdef',
             '7': 'speed',
             '8': 'total'
             }

STATS_DICT = {'hp': 'Hp',
              'atk': 'Attack',
              'defense': 'Defense',
              'spatk': 'Special Attack',
              'spdef': 'Special Defense',
              'speed': 'Speed',
              'total': 'Total',
              'height_m': 'Height',
              'weight_kg': 'Weight'
              }

GENERATION = {'第一世代寶可夢': '1',
              '第二世代寶可夢': '2',
              '第三世代寶可夢': '3',
              '第四世代寶可夢': '4',
              '第五世代寶可夢': '5',
              '第六世代寶可夢': '6',
              '第七世代寶可夢': '7'
              }

# 退出程序标示
EXIT = 'q'
# POKEMON 详细信息
FLAG_DETAIL = 'DETAIL'
# POKEMON 前十
FLAG_TOP_TEN = 'TOP_TEN'