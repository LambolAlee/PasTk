import PySimpleGUI as sg
from .abstract_window import Window
from .helpers.helper import copier, get_resource

background_color = sg.theme_background_color()

prompt = '$> 请向文本框中添加内容...'
Image_B = lambda key, filename: sg.Button('', image_subsample=20, pad=(0,3), mouseover_colors=background_color, k=key, image_filename=get_resource(filename), button_color=background_color, enable_events=True)


class DetailWindow(Window):

    @classmethod
    def build(cls):
        cls.layout = [[sg.Frame('', [
            [sg.Column([[sg.Listbox([], pad=(0,0), select_mode='LISTBOX_SELECT_MODE_SINGLE', 
            enable_events=True, k='-DETAIL_LIST-', no_scrollbar=True, size=(12, 15), font=('', 16))],
            [Image_B('-D_ADD-', 'square-plus-colored.png'),
            Image_B('-D_REMOVE-', 'square-minus-colored.png'),
            Image_B('-D_LEAVE-', 'square-caret-right-colored.png')
            ]], expand_y=True),

            sg.Column([
                [sg.Multiline(background_color='#B2D5C0', pad=(0,0), default_text='Hello World', font=('', 16), k='-TXT-', size=(40, 16), no_scrollbar=True, enable_events=True)],
                [sg.T('Enter to a newline', text_color='#E6E6FA', font=('', 12)), sg.T(' '), 
                sg.T('Ctrl-Enter to submit the text', text_color='#E6E6FA', font=('', 12)), 
                sg.T(' ', size=(4,1)), sg.B('', image_filename=get_resource('squarecheck.png'), button_color=background_color, mouseover_colors=background_color, pad=(0,0), k='-SUBMIT-', enable_events=True)],
            ], expand_y=True)]])
        ]]
        return cls.layout

    @classmethod
    def init(cls):
        cls.window = sg.Window('库存详情', layout=cls.build(), enable_close_attempted_event=True, finalize=True)
        cls.window['-TXT-'].Widget.bind('<Control Return>', cls.update_list)
        cls.window['-TXT-'].bind('<Key-BackSpace>', '*BACK*')
        cls.window['-TXT-'].set_focus(True)
        cls.window['-D_ADD-'].Widget.configure(takefocus=0)
        cls.window['-D_REMOVE-'].Widget.configure(takefocus=0)
        cls.window['-D_LEAVE-'].Widget.configure(takefocus=0)

    @classmethod
    def update_list(cls, event):
        window = cls.window

        txt = window['-TXT-'].get()
        item = window['-DETAIL_LIST-'].get()[0]
        try:
            i = copier.index(item)
        except ValueError:
            i = 0
            copier.append(txt[:-1])
        else:
            copier.remove(item)
            copier.insert(i, txt[:-1])
        window['-DETAIL_LIST-'].update(copier, set_to_index=i)
        window.write_event_value('-DETAIL_LIST-', [copier[i]])

    @classmethod
    def set_source(cls):
        if copier:
            cls.window['-DETAIL_LIST-'].update(copier, set_to_index=0)
        else:
            cls.window['-DETAIL_LIST-'].update(['No data here...'], set_to_index=0)

    @classmethod
    def run_loop(cls):
        super().run_loop()

        window = cls.window
        cls.set_source()

        while True:
            e, v = window.read()

            if e in [sg.WINDOW_CLOSE_ATTEMPTED_EVENT, '-D_LEAVE-']:
                try:
                    copier.remove(prompt)
                finally:
                    window.hide()
                    break

            if e == '-DETAIL_LIST-':
                if copier == [] or v[e][0] == prompt:
                    value = ''
                else:
                    value = v[e][0]
                window['-TXT-'].update(value)

            elif e == '-D_ADD-':
                if not prompt in copier:
                    copier.append(prompt)
                window['-DETAIL_LIST-'].update(copier, set_to_index=len(copier)-1)
                window.write_event_value('-DETAIL_LIST-', [prompt])

            elif e == '-D_REMOVE-':
                try:
                    copier.remove(window['-DETAIL_LIST-'].get()[0])
                except (IndexError, ValueError):
                    continue
                window['-DETAIL_LIST-'].update(copier)
                if len(copier) != 0:
                    window['-DETAIL_LIST-'].update(set_to_index=0)
                    window.write_event_value('-DETAIL_LIST-', [copier[0]])
                else:
                    window['-TXT-'].update('')
                
            elif e == '-SUBMIT-':
                cls.update_list((e, v))

            elif e.startswith('-TXT-') and v['-TXT-'].rstrip('\n'):
                value = v['-TXT-'].rstrip('\n')
                if e.endswith('*BACK*') and value[-1] == ' ':
                    count_of_space_ending = len(value) - len(value.rstrip(' '))
                    space_to_delete = count_of_space_ending % 4
                    if space_to_delete == 0:
                        continue
                    else:
                        window['-TXT-'].update(value[:(-space_to_delete)])
                elif value[-1] == '\t':
                    window['-TXT-'].update(value[:-1] + '  ' *4)
