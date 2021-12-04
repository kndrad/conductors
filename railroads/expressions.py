from re import compile

start_container_selector_regex = compile('^timeline__item timeline__item--start.*')
end_container_selector_regex = compile('^timeline__item timeline__item--end.*')

timeline_start, timeline_end = 'start', 'end'
timeline_regex = compile(f"^({timeline_start}|{timeline_end})")

time_container_selector_regex = compile(f"^stime search-results__item-hour.*")
hour_regex = compile('(\d+:\d+)')

overall_info_container_selector_regex = compile('^col-3 col-12--phone inline-center box.*')

number_regex = compile('\d+')
search_engine_date_regex = compile(
    '(?P<date>(0[1-9]|[12][0-9]|3[01]|[1-9])[- \.](0[1-9]|[1-9]|1[012])[-\.](19|20\d\d))'
)
