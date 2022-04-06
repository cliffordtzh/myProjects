import pandas as pd
import PySimpleGUI as Sg
import pyautogui as pg
from datetime import datetime

path = r'C:\Users\Clifford\Shortcuts\Clifford\Me\Coding\Me\Python\scanner'
scanner_path = path + '\scanner.csv'
pw_file_path = path + '\password.txt'
log_path = path + '\log.txt'
Sg.theme('SystemDefault')

main_name = 'Clifford\'s Scanner'

price_in = (297, 107)
prog_pos = (1209, 1052)
screen_size = pg.size()

col1 = [[Sg.Button('1', size=(12, 1))], [Sg.Button('4', size=(12, 1))], [Sg.Button('7', size=(12, 1))],
        [Sg.Button('.', size=(12, 1))]]
col2 = [[Sg.Button('2', size=(12, 1))], [Sg.Button('5', size=(12, 1))], [Sg.Button('8', size=(12, 1))],
        [Sg.Button('0', size=(12, 1))]]
col3 = [[Sg.Button('3', size=(12, 1))], [Sg.Button('6', size=(12, 1))], [Sg.Button('9', size=(12, 1))],
        [Sg.Button('<', size=(12, 1))], [Sg.Button('Enter', size=(12, 1), button_color='Green')]]

numpad = [Sg.Column(col1, element_justification='c', vertical_alignment='t', expand_x = True),
          Sg.Column(col2, element_justification='c', vertical_alignment='t', expand_x = True),
          Sg.Column(col3, element_justification='c', vertical_alignment='t', expand_x = True)]

main_layout = [
    [Sg.Text('Running', size=(12, 1))],
    [Sg.Text('', size=(40, 1), key='-result-')],
    [Sg.Text('Barcode: ', size=(12, 1)), Sg.InputText('', size=(30, 1), enable_events = True, key='-barcode-'),
     Sg.Button('Clear', size = (6, 1))],
    [Sg.Text('Price: ', size=(12, 1)), Sg.InputText('$', size=(30, 1), key='-price-')],
    [Sg.Text('', size=(40, 1))],
    numpad,
    [Sg.Text('', size=(40, 1))],
    [Sg.Text('Password', size=(12, 1)),
     Sg.InputText('', size=(20, 1), key='-Password-', password_char='*'),
     Sg.Text('', key='-WrongPW-', text_color='Red', size=(12, 1), auto_size_text=True)],
    [Sg.Button('Settings'), Sg.Button('Close')]
]


def update_log(function, result, c_value):
    f_description = {'add_price': 'Price add attempt',
                     'change_price': 'Price change attempt',
                     'find': 'Find attempt',
                     'remove': 'Remove attempt',
                     'change_pw': 'Password change attempted',
                     'output': 'Price output to main system',
                     'barcode_read': 'Barcode Read',
                     'settings_navi': 'Settings',
                     'Password': 'Open settings attempt',
                     'Main': 'Main'}

    attempted_event = f_description[function]
    log = open(log_path, 'a')
    time_now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    new_line = '\n'
    entry = f'[{time_now}] --- {attempted_event}: {result}, {c_value}{new_line}'
    log.write(entry)
    log.close()


def numpad_price(window, button, bar):
    if button in [str(x) for x in range(10)] or button == '.':
        new_line = bar['-price-'] + button

    else:
        new_line = bar['-price-'][:-1]

    window.FindElement('-price-').update(new_line)
    window.FindElement('-price-').SetFocus()


def add_price(sub, sub_value, from_main):
    mem = pd.read_csv(scanner_path)
    mem = mem
    code = sub_value['-barcode-']
    pre_price = sub_value['-price-']

    if code in mem['Barcode'].values and pre_price == mem[mem['Barcode'] == code]['Price'].values:
        sub.FindElement('-result-').update('Barcode already exists', text_color='Red')
        update_log('add_price', 'Barcode already exists', sub_value)

    elif code in mem['Barcode'].values and pre_price != mem[mem['Barcode'] == code]['Price'].values:
        sub.FindElement('-result-').update('Click Change Price to change price of this barcode',
                                           text_color='Red')
        update_log('add_price', 'Click Change Price to change price of this barcode', sub_value)

    elif code == '' or pre_price == '$':
        sub.FindElement('-result-').update('Scan a barcode and enter a price', text_color='Red')
        update_log('add_price', 'Scan a barcode and enter a price', sub_value)

    else:
        if '$' not in pre_price:
            price = f'${float(pre_price):.2f}'
        else:
            price = f'${float(pre_price[1:]):.2f}'

        entry = pd.DataFrame([[code, price]], columns=['Barcode', 'Price'])
        updated = mem.append(entry, ignore_index=True)
        updated = updated.astype('string')
        updated.to_csv(scanner_path, index=False)
        if not from_main:
            sub.FindElement('-table-').update(values=updated.values.tolist())
            sub.FindElement('-price-').update('')
            update_log('add_price', 'Price added', sub_value)
        else:
            update_log('add_price', 'Price added from main', sub_value)

    sub.FindElement('-barcode-').update('')
    sub.FindElement('-barcode-').SetFocus()
    sub.FindElement('-price-').update('$')


def find(sub, sub_value):
    mem = pd.read_csv(scanner_path)
    mem = mem.astype('string')
    # If no row selected, use search bar
    if len(sub_value['-table-']) == 0 and len(sub_value['-barcode-']) > 0:
        indexed_row = mem.index[mem['Barcode'] == str(sub_value['-barcode-'])].tolist()
    # Else, use table
    elif len(sub_value['-table-']) > 0:
        indexed_row = sub_value['-table-']
    # If no row selected and search bar empty, return a message and indexed_row = None
    else:
        sub.FindElement('-result-').update('Select a row, or scan a barcode', text_color='Red')
        indexed_row = None
        update_log('find', 'Select a row, or scan a barcode', sub_value)

    try:
        if len(indexed_row) == 0:
            sub.FindElement('-result-').update('Barcode not found', text_color='Red')
            sub.FindElement('-price-').update('$')
            update_log('find', 'Barcode not found', sub_value)
            return_row = []
        else:
            return_row = indexed_row
            price = mem[mem['Barcode'] == sub_value['-barcode-']]['Price']
            if len(price) == 1:
                sub.FindElement('-price-').update(price.values[0])
                sub.FindElement('-result-').update('')
                update_log('find', 'Barcode found', sub_value)
            else:
                sub.FindElement('-result-').update('Barcode not found', text_color='Red')
                sub.FindElement('-price-').update('$')
                update_log('find', 'Barcode not found', sub_value)
                return_row = []
    except TypeError or ValueError:
        return_row = []

    sub.FindElement('-barcode-').update('')
    sub.FindElement('-table-').update(select_rows=tuple(return_row))


def remove(sub, sub_value):
    mem = pd.read_csv(scanner_path)
    mem = mem.astype('string')
    # If no row selected, use search bar
    if len(sub_value['-table-']) == 0 and len(sub_value['-barcode-']) > 0:
        indexed_row = mem.index[mem['Barcode'] == str(sub_value['-barcode-'])].tolist()
    # Else, use table
    elif len(sub_value['-table-']) > 0:
        indexed_row = sub_value['-table-']
    # If no row selected and search bar empty, return a message and indexed_row = None
    else:
        sub.FindElement('-result-').update('Select a row to remove, or scan a barcode', text_color='Red')
        indexed_row = None

    # Catches the error when no row selected and search bar is empty
    try:
        if len(indexed_row) == 0:
            sub.FindElement('-result-').update('Barcode not found', text_color='Red')
            update_log('remove', 'Barcode not found', sub_value)
            updated = mem
        else:
            updated = mem.drop(indexed_row)
            update_log('remove', 'Barcode found', sub_value)
    except TypeError or ValueError:
        updated = mem

    updated = updated.astype('string')
    updated.to_csv(scanner_path, index=False)
    sub.FindElement('-barcode-').update('')
    sub.FindElement('-table-').update(values=updated.values.tolist())


def change_pw(sub, sub_value):
    q = open(pw_file_path, 'r+')
    content = q.readline()
    q.seek(0)
    password = content[content.find('<') + 1: content.find('>')]
    old_password = sub_value['-old-']
    new_password = sub_value['-new-']
    new_line = f'password=<{new_password}>'
    if new_password == 'password':
        sub.FindElement('-result-').update('Password cannot be \'password\'', text_color='Red')
        update_log('change_pw', 'Password cannot be \'password\'', sub_value)

    elif old_password == password:
        q.write(new_line)
        q.truncate()
        sub.FindElement('-result-').update('Password reset!', text_color='Green')
        update_log('change_pw', 'Password reset!', sub_value)

    elif old_password != password:
        sub.FindElement('-result-').update('Wrong password', text_color='Red')
        update_log('change_pw', 'Wrong password', sub_value)

    sub.FindElement('-old-').update('')
    sub.FindElement('-old-').SetFocus()
    sub.FindElement('-new-').update('')


def change_price(sub, sub_value):
    code = sub_value['-barcode-']
    pre_price = sub_value['-price-']

    mem = pd.read_csv(scanner_path)
    mem = mem.astype('string')

    if pre_price == '':
        price = ' '

    elif '$' not in pre_price:
        price = f'${float(pre_price):.2f}'
    else:
        price = f'${float(pre_price[1:]):.2f}'

    system_price = mem.loc[mem.index[mem['Barcode'] == code].tolist(), 'Price'].values

    if code in mem['Barcode'].values and price not in system_price and price != ' ':
        mem[mem['Barcode'] == code] = [code, price]

        updated = mem
        updated = updated.astype('string')
        updated.to_csv(scanner_path, index=False)
        sub.FindElement('-table-').update(values=updated.values.tolist())
        sub.FindElement('-result-').update('')
        sub.FindElement('-price-').update('')
        update_log('change_price', 'Price changed', sub_value)

    elif code in mem['Barcode'].values and price in system_price:
        sub.FindElement('-result-').update('The new price and old price is the same', text_color='Red')
        update_log('change_price', 'The new price and old price is the same', sub_value)

    elif code not in mem['Barcode'].values:
        sub.FindElement('-result-').update('Barcode does not exist', text_color='Red')
        update_log('change_price', 'Barcode does not exist', sub_value)

    else:
        sub.FindElement('-result-').update('Scan a barcode and enter a price', text_color='Red')
        update_log('change_price', 'Scan a barcode and enter a price', sub_value)

    sub.FindElement('-barcode-').update('')
    sub.FindElement('-barcode-').SetFocus()


def subpad(sub, sub_event, sub_value):
    if sub_event in [str(x) for x in range(10)] or sub_event == '.':
        line = sub_value['-price-']
        new_line = f'{line}{sub_event}'
    else:
        new_line = sub_value['-price-'][:-1]

    sub.FindElement('-price-').update(new_line)
    sub.FindElement('-price-').SetFocus()


def output(price_out):
    pg.moveTo(price_in)
    pg.click()
    pg.write(price_out)
    pg.press('enter')
    pg.moveTo(prog_pos)
    pg.click()
    update_log('output', 'Price output completed', price_out)


def settings_navi():
    while True:
        settings = Sg.Window('Settings', [
            [Sg.Text('Menu', font=(Sg.DEFAULT_FONT, 20))],
            [Sg.Button('Add Prices'), Sg.Button('Check Memory')],
            [Sg.Button('Change Password'), Sg.CloseButton('Close')]
        ])
        s_event, s_value = settings.read()

        if s_event == 'Close' or s_event == Sg.WINDOW_CLOSED:
            settings.close()
            main.un_hide()
            update_log('settings_navi', 'Closed', s_value)
            break

        # Windows for each of menu options
        if s_event == 'Add Prices':
            settings.close()
            update_log('settings_navi', 'Add Price', s_value)
            mem = pd.read_csv(scanner_path)
            values = mem.values.tolist()
            headers = mem.columns.tolist()
            sub = Sg.Window('Add Prices', [
                [Sg.Button('Back'), Sg.Text('', key='-result-', size=(30, 1))],
                [Sg.Text('Scan Barcode: ', size=(12, 1)), Sg.InputText('', size=(20, 1), key='-barcode-')],
                [Sg.Text('Input Price: ', size=(12, 1)), Sg.InputText('$', size=(20, 1), key='-price-')],
                [Sg.Column([[Sg.Table(values=values, headings=headers,
                                      auto_size_columns=False,
                                      col_widths=list(map(lambda x: len(x) + 1, headers)), key='-table-')],
                            [Sg.Button('Add'), Sg.Button('Change Price', size=(11, 1))]]),
                 Sg.Column([[Sg.Button('1', size=(6, 1))], [Sg.Button('4', size=(6, 1))],
                            [Sg.Button('7', size=(6, 1))], [Sg.Button('.', size=(6, 1))]],
                           element_justification='c', vertical_alignment='t'),
                 Sg.Column([[Sg.Button('2', size=(6, 1))], [Sg.Button('5', size=(6, 1))],
                            [Sg.Button('8', size=(6, 1))], [Sg.Button('0', size=(6, 1))]],
                           element_justification='c', vertical_alignment='t'),
                 Sg.Column([[Sg.Button('3', size=(6, 1))], [Sg.Button('6', size=(6, 1))],
                            [Sg.Button('9', size=(6, 1))], [Sg.Button('<', size=(6, 1))]],
                           element_justification='c', vertical_alignment='t')
                 ]
            ])
        elif s_event == 'Check Memory':
            settings.close()
            update_log('settings_navi', 'Check Memory', s_value)
            mem = pd.read_csv(scanner_path)
            values = mem.values.tolist()
            headers = mem.columns.tolist()

            table = [[Sg.Table(values=values, headings=headers,
                               auto_size_columns=False,
                               col_widths=list(map(lambda x: len(x) + 1, headers)), key='-table-')],
                     [Sg.Button('Remove', size=(12, 1))]]

            sub = Sg.Window('Check Memory', [
                [Sg.Button('Back'), Sg.Text('', size=(30, 1), key='-result-')],
                [Sg.Text('Scan Barcode: ', size=(12, 1)), Sg.InputText('', key='-barcode-', size=(16, 1)),
                 Sg.Button('Find', size=(8, 1))],
                [Sg.Text('Price: ', size=(12, 1)), Sg.InputText('$', key='-price-', size=(16, 1))],
                [Sg.Column(table, justification='l'),
                 Sg.Column([[Sg.Button('1', size=(6, 1))], [Sg.Button('4', size=(6, 1))],
                            [Sg.Button('7', size=(6, 1))], [Sg.Button('.', size=(6, 1))]],
                           element_justification='c', vertical_alignment='t'),
                 Sg.Column([[Sg.Button('2', size=(6, 1))], [Sg.Button('5', size=(6, 1))],
                            [Sg.Button('8', size=(6, 1))], [Sg.Button('0', size=(6, 1))]],
                           element_justification='c', vertical_alignment='t'),
                 Sg.Column([[Sg.Button('3', size=(6, 1))], [Sg.Button('6', size=(6, 1))],
                            [Sg.Button('9', size=(6, 1))], [Sg.Button('<', size=(6, 1))]],
                           element_justification='c', vertical_alignment='t')
                 ]
            ])

        else:
            settings.close()
            update_log('settings_navi', 'Change Password', s_value)
            sub = Sg.Window('Change Password', [
                [Sg.Button('Back'), Sg.Text('', size=(40, 1), key='-result-')],
                [Sg.Text('Old Password:', size=(12, 1)), Sg.InputText('', key='-old-', password_char='*')],
                [Sg.Text('New Password:', size=(12, 1)), Sg.InputText('', key='-new-', password_char='*')],
                [Sg.Button('Change')]
            ])

        # Events happening in sub window
        while True:
            sub_event, sub_value = sub.read()
            if sub_event == 'Back' or sub_event == Sg.WINDOW_CLOSED:
                sub.close()
                update_log('settings_navi', 'Settings closed', sub_value)
                break

            char = [str(x) for x in range(10)]
            char.extend(['.', '<'])
            if sub_event in char:
                subpad(sub, sub_event, sub_value)

            elif sub_event == 'Add':
                add_price(sub, sub_value, from_main=False)

            elif sub_event == 'Change Price':
                change_price(sub, sub_value)

            elif sub_event == 'Find':
                find(sub, sub_value)

            elif sub_event == 'Remove':
                remove(sub, sub_value)

            elif sub_event == 'Change':
                change_pw(sub, sub_value)


main = Sg.Window(main_name, main_layout)
while True:
    event, value = main.read()
    update_log('Main', 'Main opened', value)
    numpad_chars = [str(x) for x in range(10)]
    numpad_chars.extend(['.', '<'])

    if event == 'Close' or event == Sg.WINDOW_CLOSED:
        update_log('Main', 'Main closed', value)
        break

    elif event == 'Settings':
        p = open(pw_file_path, 'rt')
        contents = p.read()
        passwords = contents[contents.find('<') + 1: contents.find('>')]
        if value['-Password-'] == passwords:
            p.close()
            main.FindElement('-WrongPW-').update('')
            main.FindElement('-Password-').update('')
            update_log('Password', 'Correct password', value)
            main.hide()
            settings_navi()
        else:
            main.FindElement('-WrongPW-').update('Wrong Password')
            main.FindElement('-barcode-').SetFocus()
            update_log('Password', 'Incorrect password', value)

    elif event in numpad_chars:
        numpad_price(main, event, value)

    elif event == 'Enter':
        memory = pd.read_csv(scanner_path)
        if value['-barcode-'] not in memory['Barcode']:
            add_price(main, value, from_main=True)
            output(value)

    elif event == 'Clear':
        main.FindElement('-barcode-').update('')

    else:
        while True:
            memory = pd.read_csv(scanner_path)
            current_code = value['-barcode-']
            search = memory[memory['Barcode'].str.find(current_code) == 0]
            if len(search.index.tolist()) == 1 and len(current_code) == len(search.Barcode.values[0]):
                memory_price = memory[memory['Barcode'] == value['-barcode-']]['Price'].values
                if len(memory_price) == 1:
                    formatted_price = memory_price[0]
                    output(formatted_price)
                    main.FindElement('-barcode-').update('')
                    main.FindElement('-result-').update('')
                    update_log('barcode_read', 'Successful', value)
                    break
            else:
                break

    main.refresh()
