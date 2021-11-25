from re import compile

timeline_start_container_cls = compile('^timeline__item timeline__item--start.*')
timeline_end_container_cls = compile('^timeline__item timeline__item--end.*')

timeline_start, timeline_end = 'start', 'end'
timeline_pattern = compile(f"^({timeline_start}|{timeline_end})")

time_container_cls = compile(f"^stime search-results__item-hour.*")
time_pattern = compile('(\d+:\d+)')

overall_info_container_cls = compile('^col-3 col-12--phone inline-center box.*')

number_pattern = compile('\d+')
website_date_pattern = compile(
    '(?P<date>(0[1-9]|[12][0-9]|3[01]|[1-9])[- \.](0[1-9]|[1-9]|1[012])[-\.](19|20\d\d))'
)