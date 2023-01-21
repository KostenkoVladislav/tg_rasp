import json
import pprint


text0 = [1, 1,
         1, 1, ]
text1 = [1, 1,
         1, 1, ]
for i in range(4):
    text0[i] = [f'{i}'] * 7  # type: ignore #   пустой массив 4х7
    text1[i] = [f'{i}'] * 7  # type: ignore

#   pprint.pprint(text)
# Чтение расписания из файлов и заполнение массива
fls = [11, 12, 21, 22]
i = 0
for i in range(4):
    for j in range(7):
        f = open(f'data/{fls[i]}/{j + 1}.txt', 'r', encoding="utf-8")
        text0[i][j] = f.read()  # type: ignore
        #   print(f'i={i} j={j} file={text0[i][j]}')
        f.close()
        f = open(f'data/{fls[i]}/{j + 1}1.txt', 'r', encoding="utf-8")
        text1[i][j] = f.read()  # type: ignore
        #   print(f'i={i} j={j} file={text1[i][j]}')
        f.close()

pprint.pprint(text0)
pprint.pprint(text1)

data = {
    -1:'0-ИС1 1-ИС2',
    0: {
        0:{ 
            0:  {0:text0[0][0], 1:text0[0][1], 2:text0[0][2],
                 3:text0[0][3], 4:text0[0][4], 5:text0[0][5],
                 6:text0[0][6], },
            1:  {0:text0[0][0], 1:text0[0][1], 2:text0[0][2],
                 3:text0[0][3], 4:text0[0][4], 5:text0[0][5],
                 6:text0[0][6], }
            },
        1: {
            0: {0: text1[1][0], 1: text1[1][1], 2: text1[1][2],
                3: text1[1][3], 4: text1[1][4], 5: text1[1][5],
                6: text1[1][6], },
            1: {0: text1[1][0], 1: text1[1][1], 2: text1[1][2],
                3: text1[1][3], 4: text1[1][4], 5: text1[1][5],
                6: text1[1][6], }
        }
        ,
    1: {
        0:{ 
            0:  {0:text0[1][0], 1:text0[1][1], 2:text0[1][2],
                 3:text0[1][3], 4:text0[1][4], 5:text0[1][5],
                 6:text0[1][6], },
            1:  {0:text0[1][0], 1:text0[1][1], 2:text0[1][2],
                 3:text0[1][3], 4:text0[1][4], 5:text0[1][5],
                 6:text0[1][6], }
            },
        1: {
            0: {0: text1[0][0], 1: text1[0][1], 2: text1[0][2],
                3: text1[0][3], 4: text1[0][4], 5: text1[0][5],
                6: text1[0][6], },
            1: {0: text1[0][0], 1: text1[0][1], 2: text1[0][2],
                3: text1[0][3], 4: text1[0][4], 5: text1[0][5],
                6: text1[0][6],
                }
            }
        }
        }
}

with open("../data_file.json", "w") as write_file:
   json.dump(data, write_file)

