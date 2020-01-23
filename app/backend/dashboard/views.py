import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def dashboard_index_view(request):
    data = request.user.profile.practice_graph_data()
    sidebar_items = [
        ('dashboard__li-practice', 'graduation-cap', 'Practice'),
        ('dashboard__li-stats', 'golf-ball', 'Statistics')
    ]

    stats = request.user.profile.get_practice_stats()
    if stats:
        stats_table_items = [
            ('Total Practice Time', f'{stats.total_practice_time}m'),
            ('Average Practice Time', f'{round(stats.avg_practice_time, 2)}m'),
            ('Median Practice Time', f'{round(stats.median_practice_time, 2)}m'),
            ('Maximum Practice Time', f'{round(stats.max_practice_time, 2)}m'),
            ('Minimum Practice Time', f'{round(stats.min_practice_time, 2)}m'),
            ('', ''),
            ('Number of Exercises', stats.num_exercises),
            ('Average Number of Exercises', round(stats.avg_num_exercises, 2)),
            ('Median Number of Exercises', round(stats.median_num_exercises, 2)),
            ('Average Exercise Length', f'{round(stats.avg_exercise_length, 2)}m'),
            ('Median Exercise Length', f'{round(stats.median_exercise_length, 2)}m'),
            ('', ''),
            ('Most Practiced Instrument', stats.most_practiced_instrument.title()),
            ('Least Practice Instrument', stats.least_practiced_instrument.title())
        ]

        args = dict(title='Dashboard',
                    stats=stats,
                    datasets=data.sets,
                    datasets_json=json.dumps(data.sets),
                    dates=data.dates,
                    dates_json=json.dumps(data.dates),
                    sidebar_items=sidebar_items,
                    stats_table_items=stats_table_items)
    else:
        stats_table_items = [
            ('Total Practice Time', 'm'),
            ('Average Practice Time', '0m'),
            ('Median Practice Time', '0m'),
            ('Maximum Practice Time', '0m'),
            ('Minimum Practice Time', '0m'),
            ('', ''),
            ('Number of Exercises', 0),
            ('Average Number of Exercises', 0),
            ('Median Number of Exercises', 0),
            ('Average Exercise Length', '0m'),
            ('Median Exercise Length', '0m'),
            ('', ''),
            ('Most Practiced Instrument', 0),
            ('Least Practice Instrument', 0)
        ]

        args = dict(title='Dashboard',  stats=stats, stats_table_items=stats_table_items, sidebar_items=sidebar_items)

    return render(request, 'dashboard/dashboard.html', args)
