dic = dict()

lis = ['one', 'two', 'three', 'four']

count = 1
for item in lis:
    dic[item] = count
    count += 1

def card_gen():
    for item in dic:
        yield item, dic[item]   

card_gen = card_gen()

for item in card_gen:
    print(next(card_gen))
