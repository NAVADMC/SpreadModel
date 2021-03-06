"""URLs is entirely procedural based on the contents of models.py. This has the advantage that urls automatically update as the models change or are renamed."""


"""NEVER MODIFY THIS FILE
Instead, modify the 'makeresultsurls' management command."""

from django.conf.urls import patterns, url

urlpatterns = patterns('', url('^$', 'Results.views.results_home'),
         url('^RunSimulation/$', 'Results.views.run_simulation'),
         url('^Population\.png$', 'Results.graphing.population_png'),
         url('^population_d3_map/$', 'Results.interactive_graphing.population_d3_map'),
         url('^population_thumbnail\.png$', 'Results.interactive_graphing.population_thumbnail_png'),
         url('^population_zoom\.png$', 'Results.interactive_graphing.population_zoom_png'),
         url('^(?P<model_name>\w+)/(?P<field_name>\w+)/(?P<iteration>\d*)/?$', 'Results.views.graph_field'),
         url('^(?P<model_name>\w+)/(?P<field_name>\w+)/(?P<iteration>\d*)/?(?P<zone>[^/]*)/?Graph\.png$', 'Results.graphing.graph_field_png'),
         url('^Inputs/$', 'Results.views.back_to_inputs'),
         url('^simulation_status.json$', 'Results.views.simulation_status'),
         url('^abort_simulation$', 'Results.utils.abort_simulation'),
         url('^SummaryCSV/$', 'Results.views.summary_csv'),
         url('^CombineOutputs/$', 'Results.views.combine_outputs'),
         url('^OutputBaseModel/$',                          'Results.views.model_list'),
         url('^OutputBaseModel/prefix/(?P<prefix>\w{1,4})/$',  'Results.views.filtered_list'),
         url('^DailyByProductionType/$',                          'Results.views.model_list'),
         url('^DailyByProductionType/prefix/(?P<prefix>\w{1,4})/$',  'Results.views.filtered_list'),
         url('^DailyByZoneAndProductionType/$',                          'Results.views.model_list'),
         url('^DailyByZoneAndProductionType/prefix/(?P<prefix>\w{1,4})/$',  'Results.views.filtered_list'),
         url('^DailyByZone/$',                          'Results.views.model_list'),
         url('^DailyByZone/prefix/(?P<prefix>\w{1,4})/$',  'Results.views.filtered_list'),
         url('^DailyControls/$',                          'Results.views.model_list'),
         url('^DailyControls/prefix/(?P<prefix>\w{1,4})/$',  'Results.views.filtered_list'),
         url('^UnitStats/$',                          'Results.views.model_list'),
         url('^UnitStats/prefix/(?P<prefix>\w{1,4})/$',  'Results.views.filtered_list'),
         url('^ResultsVersion/$',                          'Results.views.model_list'),
         url('^ResultsVersion/prefix/(?P<prefix>\w{1,4})/$',  'Results.views.filtered_list'))