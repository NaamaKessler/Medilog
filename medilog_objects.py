from dataclasses import dataclass, field
import os
import numpy as np
import pandas as pd
import calendar
import xlsxwriter as xlw


class Roster:
    month_dict_abbr = {month: index for index, month in enumerate(calendar.month_abbr) if month}
    month_dict = {month: index for index, month in enumerate(calendar.month_name) if month}
    days_list = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ש']

    # days_list = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']

    def __init__(self, medilog):
        self.medilog = medilog

        self.month = None
        self.month_full = None
        self.year = None

        self.seniors = None
        self.residents = None
        self.assignments = None
        self.shifts = None

        self.assign_table = None
        self.request_table = None
        self.quota_table = None

        self.path = None

        self.first_day_of_month = None
        self.num_of_days = None
        self.num_of_physicians = None
        self.num_of_shifts = None

    def load_roster(self, month, year):
        self.month = month
        self.month_full = calendar.month_name[list(calendar.month_abbr).index(self.month)]
        self.year = year
        self.validate_input()

        self.path = os.getcwd() + '\\' + self.month + self.year  # fix to account for changing the roster
        os.chdir(self.path)

        fail_flag = False
        try:
            self.load_physicians()
            self.load_assignments()
            self.load_requests()
            self.load_quotas()
            self.load_shifts()
        except IOError:
            self.medilog.app_gui.popup_message(msg_title='Warning',
                                               msg_str='Close all Excel files.',
                                               msg_symbol='warning')
            fail_flag = True
            return fail_flag

        self.first_day_of_month, self.num_of_days = calendar.monthrange(year=int(year),
                                                                        month=self.month_dict_abbr[self.month])
        self.num_of_physicians = len(self.seniors) + len(self.residents)
        self.num_of_shifts = len(self.shifts)

        return fail_flag

    def load_physicians(self):
        self.seniors = []
        self.residents = []

        for senior in pd.read_csv('seniors.csv').values.tolist():
            self.seniors.append(Senior(first=senior[0], last=senior[1]))

        for resident in pd.read_csv('residents.csv').values.tolist():
            self.residents.append(Resident(first=resident[0], last=resident[1]))

    def load_assignments(self):
        assignments = pd.read_csv('assignments.csv')
        self.assign_table = AssignTable(assignments)

    def load_requests(self):
        # read files
        seniors_path = 'Requests - ' + 'Seniors - ' + self.month_full + str(self.year) + '.xlsx'
        residents_path = 'Requests - ' + 'Residents - ' + self.month_full + str(self.year) + '.xlsx'
        seniors_requests_pd = pd.read_excel(seniors_path,
                                            skiprows=[0, 1, 2],
                                            convert_float=True)
        residents_requests_pd = pd.read_excel(residents_path,
                                              skiprows=[0, 1, 2],
                                              convert_float=True)

        # validate list of physicians' names
        seniors_list = seniors_requests_pd.iloc[:, 0].to_list()
        residents_list = residents_requests_pd.iloc[:, 0].to_list()
        if seniors_list != [senior.last for senior in self.seniors]:
            msg_str = 'Seniors requests table is incompatible with list of seniors.'
            self.medilog.app_gui.popup_message(msg_title='Warning', msg_str=msg_str, msg_symbol='warning')
        if residents_list != [resident.last for resident in self.residents]:
            msg_str = 'Residents requests table is incompatible with list of residents.'
            self.medilog.app_gui.popup_message(msg_title='Warning', msg_str=msg_str, msg_symbol='warning')

        # extract actual tabular data
        seniors_requests_data = seniors_requests_pd.iloc[:, 1:].fillna('').values.tolist()
        residents_requests_data = residents_requests_pd.iloc[:, 1:].fillna('').values.tolist()
        self.request_table = RequestTable(seniors_requests_data, residents_requests_data)

    def load_quotas(self):
        # read file
        quotas_pd = pd.read_excel('quotas.xlsx')

        # validate list of physicians' names
        physicians_list = quotas_pd.iloc[:, 0].to_list()
        existing_list = [senior.last for senior in self.seniors] + \
                        [np.nan] + [resident.last for resident in self.residents]
        if physicians_list != existing_list:
            msg_str = 'Quotas table is incompatible with list of seniors or residents.'
            self.medilog.app_gui.popup_message(msg_title='Warning', msg_str=msg_str, msg_symbol='warning')

        # extract actual tabular data
        quotas_data = (quotas_pd.iloc[:, 1:]).values.tolist()
        self.quota_table = QuotaTable(quotas_data)

    def load_shifts(self):
        self.shifts = []
        shift_pd = pd.read_excel('shifts.xlsx')
        for i in range(len(shift_pd.index)):
            curr_attr = shift_pd.iloc[i, :].to_dict()
            self.shifts.append(Shift(i, **curr_attr))

    def validate_input(self):
        if self.month not in self.month_dict_abbr and self.month not in self.month_dict:
            raise Exception('Invalid month input.')
        if str(self.year)[0] != str(2) or str(self.year)[1] != str(0) or len(str(self.year)) > 4:
            raise Exception('Invalid year input.')

    def save_tables(self):

        # Quota table
        phys_list = [senior.last for senior in self.seniors] + \
                         [np.nan] + \
                         [resident.last for resident in self.residents]
        for i, name in enumerate(phys_list):
            if pd.isnull(name):
                phys_list[i] = ''

        data = [[phys_list[i]] + self.quota_table.quotas_data[i][:] for i in range(len(phys_list))]
        columns = ['name'] + [shift.name for shift in self.shifts]
        quota_df = pd.DataFrame(data, columns=columns)
        quota_df.to_excel('quotas.xlsx', index=False)


class AssignTable:

    def __init__(self, assignments):
        self.assignments = assignments


class RequestTable:

    def __init__(self, senior_requests_data, residents_requests_data):

        self.requests_data = senior_requests_data + \
                             [['' for _ in range(len(senior_requests_data[0]))]] + \
                             residents_requests_data


class QuotaTable:

    def __init__(self, quotas_data):
        self.quotas_data = quotas_data


@dataclass
class Physician:
    first: str
    last: str
    assignments: list[tuple] = field(default_factory=list)

    def is_available(self, roster, day, shift):
        """
        Determine whether the physician is available for a specific shift for a given day.
        :param roster: The current roster object.
        :param day: The queried day.
        :param shift: The queried shift.
        :return: True is available, False if not.
        """
        if self.assignment_collision(roster, day, shift):
            return False
        elif self.request_collision(roster, day, shift):
            return False
        elif self.quotas_collision(roster, day, shift) == 0:
            return False
        else:
            return True

    def assignment_collision(self, roster, day, shift):
        current_day = roster.assign_table.assignments.iloc[day].tolist()
        current_day.pop(shift.index)
        if self in current_day:
            return True

        return False

    def request_collision(self, roster, day, shift):
        return False

    def quotas_collision(self, roster, day, shift):
        num_of_quotas = 1
        return num_of_quotas


class Senior(Physician):
    pass


class Resident(Physician):
    pass


class Shift:

    def __init__(self, index, **kwargs):
        self.attributes_dict = kwargs
        self.index = index
        for attr in self.attributes_dict:
            setattr(self, attr.lower(), self.attributes_dict[attr])


""" Auxiliary functions"""


def get_available(medilog, day, shift):
    available_list = ['']
    if shift.senior:
        for senior in medilog.roster.seniors:
            if senior.is_available(medilog.roster, day, shift):
                available_list.append(
                    senior.last)  ### change from .last to the actual object and handle consequences! ###

    if shift.resident:
        for resident in medilog.roster.residents:
            if resident.is_available(medilog.roster, day, shift):
                available_list.append(
                    resident.last)  ### change from .last to the actual object and handle consequences! ###

    return available_list


def update_assignment_table(medilog, day, shift_id, physician_name):
    # inefficient, change mechanism to pass actual physician and not only name

    if physician_name == '':
        previous_physician = medilog.roster.assign_table.assignments.iloc[day, shift_id]
        previous_physician.assignments.remove((day, shift_id))
        medilog.roster.assign_table.assignments.iloc[day, shift_id] = np.NaN

    else:
        physician = physician_by_name(medilog, physician_name)
        if physician is None:
            raise Exception('Physician not found.')
        else:
            medilog.roster.assign_table.assignments.iloc[day, shift_id] = physician
            physician.assignments.append((day, shift_id))

    # print(medilog.roster.assign_table.assignments.iloc[0])


def physician_by_name(medilog, name):
    physician = None
    for senior in medilog.roster.seniors:
        if name == senior.last:
            return senior

    for resident in medilog.roster.residents:
        if name == resident.last:
            return resident

    return physician


def weekday_lister(roster):
    weekday_list = []
    for k in range(roster.num_of_days):
        weekday_list.append(str(roster.days_list[(roster.first_day_of_month + k) % 7]))

    return weekday_list


""" Excel interface """


def create_request_file(medilog):
    if medilog.roster is None:
        medilog.app_gui.popup_message(msg_title='Warning',
                                      msg_str='No month was chosen.',
                                      msg_symbol='warning')
        return

    month = medilog.roster.month_full
    year = medilog.roster.year
    first_day_of_month = (medilog.roster.first_day_of_month + 1) % 7

    color_palette = medilog.app_gui.color_palette
    hex_bg_colors = [color_palette.rgb2hex(color_palette.color_list[i]) for i in range(len(color_palette.color_list))]
    hex_label_color = color_palette.rgb2hex(color_palette.label_color)

    try:
        for i, physicians in enumerate(['Seniors', 'Residents']):
            wb = xlw.Workbook('Requests - ' + physicians + ' - ' + month + str(year)
                              + '.xlsx', {'use_future_functions': True})
            ws = wb.add_worksheet(name='Requests')

            # create header format
            header_format = wb.add_format()
            header_format.set_align('center')
            header_format.set_bold()
            header_format.set_bg_color(hex_bg_colors[0])
            header_format.set_font_color(hex_label_color)

            # create headers
            ws.write('A3', month, header_format)
            ws.write('A4', int(medilog.roster.year), header_format)
            ws.freeze_panes(row=4, col=1)
            ws.set_column(0, 0, width=14)

            # names format
            names_format = wb.add_format()
            names_format.set_bg_color(hex_bg_colors[3])
            names_format.set_border()

            # add names
            if i == 0:
                last_names = [senior.last for senior in medilog.roster.seniors]
            else:
                last_names = [senior.last for senior in medilog.roster.residents]

            for j, name in enumerate(last_names):
                ws.write('A' + str(5 + j), name, names_format)

            # date and day format
            date_format = wb.add_format()
            date_format.set_bg_color(hex_bg_colors[3])
            date_format.set_border()
            date_format.set_align('center')
            date_format.set_bold()

            day_format = wb.add_format()
            day_format.set_bg_color(hex_bg_colors[2])
            day_format.set_border()
            day_format.set_align('center')
            day_format.set_bold()

            extra_format = wb.add_format()
            extra_format.set_border()
            extra_format.set_font_size(9)
            extra_format.set_locked(False)
            extra_format.set_align('center')

            counter_format = wb.add_format()
            counter_format.set_bg_color('white')
            counter_format.set_font_color('white')
            counter_format.set_align('center')

            error_format = wb.add_format()
            error_format.set_align('center')
            error_format.set_bg_color('#f54242')
            error_format.set_font_color('#f54242')

            error_indication_format = wb.add_format()
            error_indication_format.set_align('center')
            error_indication_format.set_bg_color('#f54242')
            error_indication_format.set_font_color('white')
            error_indication_format.set_bold()

            # add dates and days
            ws.set_column(1, medilog.roster.num_of_days, width=5)
            weekday_list = weekday_lister(medilog.roster)
            for k in range(medilog.roster.num_of_days):
                # add restriction for seniors requests only
                if i == 0:
                    current_column = column_string(2 + k)
                    start_cell = current_column + '5'
                    end_cell = current_column + str(4 + len(last_names))
                    range_str = start_cell + ':' + end_cell
                    formula = '=IFS(COUNTIF({}, 3) > 1, 3,' \
                              'COUNTIF({}, 4) > 2, 4,' \
                              'COUNTIF({}, 5) > 2, 5, TRUE, 0)'.format(range_str, range_str, range_str)
                    ws.write_formula(row=0, col=1 + k, formula=formula, cell_format=counter_format)

                    # add conditional formatting
                    error_cell = current_column + '1'
                    ws.conditional_format(error_cell, {'type': 'cell',
                                                       'criteria': '>',
                                                       'value': 0,
                                                       'format': error_format})

                # add extra cell for special dates
                ws.write(1, 1 + k, '', extra_format)

                # add day of week
                curr_day = weekday_list[k]
                ws.write(2, 1 + k, curr_day, day_format)

                # add day of month
                ws.write(3, 1 + k, k + 1, date_format)

            # error indication cell
            errors_range = column_string(2) + '1' + ':' + column_string(1 + medilog.roster.num_of_days) + '1'
            ws.write_formula('A2', '=IFS(COUNTIF({}, 3)>0, "Too many \'3\'s", '
                                   'COUNTIF({}, 4)>0, "Too many \'4\'s", '
                                   'COUNTIF({}, 5)>0, "Too many \'5\'s", '
                                   'TRUE, 0)'.format(errors_range, errors_range, errors_range),
                             cell_format=counter_format)
            ws.conditional_format('A2', {'type': 'cell',
                                         'criteria': 'not equal to',
                                         'value': 0,
                                         'format': error_indication_format})

            """ Main table """
            even_format = wb.add_format()
            even_format.set_bg_color('#ffffff')

            odd_format = wb.add_format()
            odd_format.set_bg_color(hex_bg_colors[3])

            fri_format = wb.add_format()
            fri_format.set_bg_color(hex_bg_colors[1])
            fri_format.set_font_color('#ffffff')

            sat_format = wb.add_format()
            sat_format.set_bg_color(hex_bg_colors[0])
            sat_format.set_font_color('#ffffff')

            day_formats = [even_format, odd_format, fri_format, sat_format]
            for day_format in day_formats:
                day_format.set_border()
                day_format.set_align('center')
                day_format.set_locked(False)

            for j in range(medilog.roster.num_of_days):
                for k in range(len(last_names)):
                    curr_day = (first_day_of_month + j) % 7

                    # choose format for the day
                    if curr_day == 5:
                        curr_format = fri_format
                    elif curr_day == 6:
                        curr_format = sat_format
                    elif k % 2 == 0:
                        curr_format = even_format
                    else:
                        curr_format = odd_format

                    ws.write(4 + k, 1 + j, '', curr_format)

                # data validation
                validation_list = [1, 2, 3, 4, 5] if i == 0 else [1, 3]
                ws.data_validation(first_col=1, first_row=4, last_col=medilog.roster.num_of_days,
                                   last_row=3 + len(last_names), options={'validate': 'list',
                                                                          'source': validation_list})
                # hide grid lines
                ws.hide_gridlines(2)
                ws.hide_row_col_headers()

            # add tooltip
            options_1 = {'width': 140,
                         'height': 22,
                         'align': {'text': 'right'},
                         'fill': {'color': hex_bg_colors[0]},
                         'font': {'color': 'white', 'bold': True}}
            options_2 = {'width': 140,
                         'height': 22,
                         'align': {'text': 'right'},
                         'x_offset': -10,
                         'fill': {'color': hex_bg_colors[1]},
                         'font': {'color': 'white', 'bold': True}}
            options_3 = {'width': 140,
                         'height': 22,
                         'align': {'text': 'right'},
                         'y_offset': 2,
                         'fill': {'color': hex_bg_colors[1]},
                         'font': {'color': 'white', 'bold': True}}
            options_4 = {'width': 140,
                         'height': 22,
                         'align': {'text': 'right'},
                         'y_offset': 2,
                         'x_offset': -10,
                         'fill': {'color': hex_bg_colors[0]},
                         'font': {'color': 'white', 'bold': True}}
            options_5 = {'width': 140,
                         'height': 22,
                         'align': {'text': 'right'},
                         'y_offset': 4,
                         'fill': {'color': hex_bg_colors[0]},
                         'font': {'color': 'white', 'bold': True}}
            options_6 = {'width': 140,
                         'height': 22,
                         'align': {'text': 'right'},
                         'y_offset': 4,
                         'x_offset': -10,
                         'fill': {'color': hex_bg_colors[1]},
                         'font': {'color': 'white', 'bold': True}}

            if i == 0:
                text_1 = ' לא פעיל - 1'
                text_2 = ' לא בכלל - 2'
                text_3 = ' כן תורנות - 3'
                text_4 = ' כן כוננות פעילה - 4'
                text_5 = ' כן חצי תורנות - 5'
                text_6 = ''

                ws.insert_textbox(0, 36, text_1, options_1)
                ws.insert_textbox(0, 34, text_2, options_2)
                ws.insert_textbox(1, 36, text_3, options_3)
                ws.insert_textbox(1, 34, text_4, options_4)
                ws.insert_textbox(2, 36, text_5, options_5)
                ws.insert_textbox(2, 34, text_6, options_6)

            else:
                text_1 = ' לא תורנות - 1'
                text_3 = ' כן תורנות - 3'

                ws.insert_textbox(0, 34, text_1, options_1)
                ws.insert_textbox(1, 34, text_3, options_3)

            # lock worksheet
            ws.protect(options={'select_locked_cells': False})

            wb.close()

    except xlw.exceptions.FileCreateError:
        medilog.app_gui.popup_message(msg_title='Warning', msg_str='Close requests files.', msg_symbol='warning')
        return

    medilog.app_gui.popup_message(msg_title='Success',
                                  msg_str='Requests files created successfully.',
                                  msg_symbol='information')


def column_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string

