from requests_html import HTMLSession
import numpy as np

num_recent_lot_draws = 40
rate = 0.4
url = "https://match.lottery.sina.com.cn/lotto/pc_zst/index?lottoType=ssq&actionType=chzs"

session = HTMLSession()
r = session.get(url)
tbody = r.html.find('#chartsTable.zst_table tbody#cpdata', first=True)
trs = tbody.find('tr')

# <id, {record}>
# record = {
#     date,
#     draws,
#     red_draws,
#     blue_draws,
# }

records_map = {}

for lot_list_id, tr in enumerate(trs):
    # print("lot_list_id: {}".format(lot_list_id))

    records_map[lot_list_id] = {}

    # get dates
    date = tr.find('td', first=True)

    records_map[lot_list_id]['date'] = date.text

    records_map[lot_list_id]['draws'] = []
    records_map[lot_list_id]['red_draws'] = []
    records_map[lot_list_id]['blue_draws'] = []

    # chartballs
    lot_draws = tr.find('.chartball01, .chartball20, .chartball02')
    for lot_draw_id, lot_draw in enumerate(lot_draws):
        lot_draw_int = int(lot_draw.text)
        records_map[lot_list_id]['draws'].append(lot_draw_int)
        if lot_draw_id < 6:         
            records_map[lot_list_id]['red_draws'].append(lot_draw_int)
        else:
            records_map[lot_list_id]['blue_draws'].append(lot_draw_int)

# print(records_map)

# reversely sort keys
sorted_keys = sorted(records_map.keys(), reverse=True)

# 33 red lot draws
red_freq_list = [0 for i in range(33 + 1)]
    
# 16 blue lot draws
blue_freq_list = [0 for i in range(16 + 1)]


for i in range(num_recent_lot_draws):
    record = records_map[sorted_keys[i]]
    for lot_draw in record['red_draws']:
        red_freq_list[lot_draw] += 1
    for lot_draw in record['blue_draws']:
        blue_freq_list[lot_draw] += 1

red_freq_list = [i / sum(red_freq_list) for i in red_freq_list]
blue_freq_list = [i / sum(blue_freq_list) for i in blue_freq_list]

red_freq_dict = {i: red_freq_list[i] for i in range(len(red_freq_list))}
blue_freq_dict = {i: blue_freq_list[i] for i in range(len(blue_freq_list))}


print("------------------------------------")
print("最近{}期双色球开奖数据".format(num_recent_lot_draws))
print("------------------------------------")
print("红球频率表")
for (key, value) in red_freq_dict.items():
    print("红球{}: {:.2%}".format(key, value))
print("------------------------------------")
print("蓝球频率表")
for (key, value) in blue_freq_dict.items():
    print("蓝球{}: {:.2%}".format(key, value))
print("------------------------------------")

# choose top 12 from red_freq_dict, choose top 3 from blue_freq_dict
top_red = sorted(red_freq_dict.items(), key=lambda x: x[1], reverse=True)[:12]
top_blue = sorted(blue_freq_dict.items(), key=lambda x: x[1], reverse=True)[:3]

# print("top_red", top_red)
# print("top_blue", top_blue)

red_lot_draw_predict = []
blue_lot_draw_predict = []

for i in range(6):
    while True:
        # red_rand_num = np.random.choice(np.arange(0,33 + 1), p=red_freq_list)
        # randomly pick a number from top_red
        red_rand_num = np.random.choice([x[0] for x in top_red])
        if red_rand_num not in red_lot_draw_predict:
            red_lot_draw_predict.append(int(red_rand_num))
            break

for i in range(1):
    while True:
        # blue_rand_num = np.random.choice(np.arange(0,16 + 1),
        # p=blue_freq_list)
        # randomly pick a number from top_blue
        blue_rand_num = np.random.choice([x[0] for x in top_blue])
        if blue_rand_num not in blue_lot_draw_predict:
            blue_lot_draw_predict.append(int(blue_rand_num))
            break

red_lot_draw_predict = sorted(red_lot_draw_predict)
blue_lot_draw_predict = sorted(blue_lot_draw_predict)

# print("red_freq_list", red_freq_list)
# print("blue_freq_list", blue_freq_list)

print("红球预测：", red_lot_draw_predict)
print("蓝球预测：", blue_lot_draw_predict)