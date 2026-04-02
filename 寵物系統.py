"""
2026.4.1 23:42
終於把它寫完，之前一直不懂的class，好像終於弄懂了。
好想睡覺 zzz 
edited by KC
"""
import random

class Dog:
    personalitys = {
        "貪吃": [40, 60],
        "好動": [60, 40],
        "乖巧": [50, 50],
        "調皮": [40, 40]
    }

    moods = {
        "開心": 1.2,
        "普通": 0.8,
        "憂鬱": 0.5
    }

    def __init__(self, name):
        self.name = name
        self.personality = random.choice(list(Dog.personalitys.keys()))
        self.energy = Dog.personalitys[self.personality][0]
        self.fullness = Dog.personalitys[self.personality][1]
        self.current_mood = self.get_mood()
        self.is_sick = False

    def limit_value(self):
        if self.energy < 0:
            self.energy = 0
        if self.fullness < 0:
            self.fullness = 0
        if self.energy > 100:
            self.energy = 100
        if self.fullness > 100:
            self.fullness = 100

    def get_mood(self):
        self.current_mood = random.choice(list(Dog.moods.keys()))
        return self.current_mood

    def train(self):
        value = Dog.moods[self.current_mood]
        energy_add = int(10 * value)
        fullness_add = int(10 * value)

        self.energy += energy_add
        self.fullness += fullness_add

        print("和{}一起訓練，活力值增加了{}，飽足值增加了{}" \
              .format(self.name, energy_add, fullness_add))

    def walk(self):
        value = Dog.moods[self.current_mood]
        energy_add = int(10 * value * random.randint(1, 3))
        fullness_add = int(10 * value)

        self.energy += energy_add
        self.fullness += fullness_add

        if self.current_mood == "開心":
            print("今天帶{}去散步，天氣很好，{}很開心，活力值增加了{}，飽足值增加了{}"\
                  .format(self.name, self.name, energy_add, fullness_add))
            
        elif self.current_mood == "普通":
            print("今天帶{}去散步，但什麼事都沒發生，活力值增加了{}，飽足值增加了{}"\
                  .format(self.name, energy_add, fullness_add))
            
        elif self.current_mood == "憂鬱":
            print("今天帶{}去散步，遇到了壞狗狗，活力值增加了{}，飽足值增加了{}"\
                  .format(self.name, energy_add, fullness_add))
        
        print("影響到了下一個月的心情")

    def feed(self):
        value = Dog.moods[self.current_mood]
        energy_add = int(10 * value)
        fullness_add = int(10 * random.randint(1, 3) * value)

        self.energy += energy_add
        self.fullness += fullness_add

        print("和{}一起吃飯，活力值增加了{}，飽足值增加了{}"\
            .format(self.name, energy_add, fullness_add))
    
    def maybe_get_sick(self):
        chance = random.random()
        if(chance < 0.3):
            self.is_sick = True
            self.energy -= 10
            self.fullness -= 10
            self.limit_value()
            print("突發狀況!!{}生病了，活力值和飽足值都各減10".format(dog.name))

    def sick_penalty(self):
        if self.is_sick:
            self.energy -= 5
            self.fullness -= 5
            self.limit_value()
            print("{}正在生病非常虛弱，活力值和飽足值再扣5".format(self.name))

    def doctor(self):
        if(self.is_sick == False):
            print("{}已經非常健康了喔")
        elif(self.is_sick == True):
            self.is_sick = False
            print("帶{}去看醫生，{}好多了".format(self.name, self.name))


print("你領養了一隻狗狗，要幫牠取什麼名字")
name = input("請輸入名字：")

dog = Dog(name) #記得記得記得!!!!!!!!! 一定要加 一直忘

month = 1

while(month <= 10):

    print("--------------------------------------")

    mood = dog.get_mood()
    print("第{}個月,{}心情很{}".format(month, dog.name, mood))
    if(month >= 3 and not dog.is_sick):
        dog.maybe_get_sick()

    while True:
        print("你要和牠一起做什麼事？")
        print("1.玩玩具訓練  2.散步  3.餵牠吃東西  4.帶牠去看醫生")
        option = input("輸入選擇的互動：")

        if option == '1':
            dog.train()
            break

        elif option == '2':
            dog.walk()
            break

        elif option == '3':
            dog.feed()
            break

        elif option == '4':
            dog.doctor()
            went_doctor = True
            break

        else:
            print("輸入錯誤，請再輸入一次！")


    print("--------------------------------------")
    print("{}已經休息，目前狀態：".format(dog.name))
    if dog.is_sick:
        dog.sick_penalty()

    dog.limit_value()
    print("活力值為{}，飽足值為{}".format(dog.energy, dog.fullness))

    if(dog.energy >= 100):
        print("{}成長為一個活潑的狗狗".format(dog.name))
        break
    if(dog.fullness >= 100):
        print("{}成長為一個健康的狗狗".format(dog.name))
        break
    if(dog.energy < 30 | dog.fullness < 30):
        print("{}覺得不快樂，離家出走了".format(dog.name))
        break

    if(month == 10 and dog.energy < 100 and dog.fullness < 100):
        print("{}成長為一個快樂平凡的狗狗".format(dog.name))
        break
    month += 1