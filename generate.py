from sa import cit

if __name__ == '__main__':
    covering_arrays = cit("input.txt", t=3)
    print(f'Start to generate {len(covering_arrays)} configs')
    with open(f'./django/tests/test_sqlite.py', 'r') as f:
        sqlite = f.readlines()
    for i, ca in enumerate(covering_arrays):
        with open(f'./django/tests/cit_configs/config_{i}.py', 'w') as f:
            f.write(f"print('CONFIG {i} IN COVERING ARRAY IS STARTED TO BE TESTED')\n")
            f.writelines(sqlite)
            for param, value in ca:
                f.write(f'{param} = {value}\n')
                if param == 'DEBUG' and value:
                    f.write("ALLOWED_HOSTS = ['127.0.0.1', 'localhost']\n")
            print(f'Saved config #{i}')
    print('All configs are successfully saved in ./django/tests/cit_configs')
