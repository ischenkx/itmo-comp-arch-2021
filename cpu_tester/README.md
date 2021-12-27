Генерирует рандомные тесты -> запускает их внутри себя -> запускает в верилоге -> сравнивает снэпшоты памяти.

Для начала потребуются: готовый проц, python (+numpy), icarus verilog (iverilog, vvp должны быть в PATH).

Запуск:
1. Скопировать все файлы из этой папки
2. В <SOURCE\_DIR (default=cpu)> положить файлы своего процессора (+ cpu_test.v из папки cpu)
3. Если не хотите использовать дефолтные значения - надо написать конфиг файл (json)
4. Запустить tester.py: python tester.py [CONFIG_PATH]
5. Если у вас будет что-то неправильно (с точки зрения тестера конечно же :)), вам выдастся сообщение об ошибке, и программа, неправильно отработавшая, будет записана в <FAILS\_FOLDER> в файлы <TAG>\_asm и <TAG>\_bin. (сайт, где можно запустить ассемблер - http://www.csbio.unc.edu/mcmillan/miniMIPS.html)

Конфиг:
json
{
    'cpu_test_path': './cpu/cpu_test.v',
    'cpu_folder': './cpu',
    'max_instructions': 200,
    'instructions_file': 'instructions.dat',
    'tests': 10000,
    'memory_cells': 10,
    'iverilog_flags': '-g2012',
    'test_build_folder': 'test_build_folder',
    'registers_range': (1, 10),
    'fails_folder': './fails'
}
'register_range' - диапазон разрешенных регистров (регистры 0, 29, 30, 31 запрещено включать)
