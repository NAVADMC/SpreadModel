"""URLs is entirely procedural based on the contents of models.py. This has the advantage that urls automatically update as the models change or are renamed."""


"""NEVER MODIFY THIS FILE
Instead, modify the 'makescenariocreatorurls' management command."""

from django.conf.urls import patterns, url

urlpatterns = patterns('', url('^AssignSpreads/$', 'ScenarioCreator.views.assign_disease_spread'),
         url('^AssignProtocols/$', 'ScenarioCreator.views.assign_protocols'),
         url('^AssignProgressions/$', 'ScenarioCreator.views.assign_progressions'),
         url('^AssignZoneEffects/$', 'ScenarioCreator.views.zone_effects'),
         url('^Protocols.json/$', 'ScenarioCreator.views.protocols_json'),
         url('^ControlProtocol/$', 'ScenarioCreator.views.control_protocol_list'),
         url('^ControlProtocol/(?P<primary_key>\d+)/(?P<field>use_\w+)/', 'ScenarioCreator.views.update_protocol_enabled'),
         url('^Populations/$', 'ScenarioCreator.views.population'),
         url('^Population/new/$', 'ScenarioCreator.views.population'),
         url('^UploadPopulation/$', 'ScenarioCreator.views.upload_population'),
         url('^OpenPopulation/(?P<target>.+)$', 'ScenarioCreator.views.open_population'),
         url('^PopulationPanel/$', 'ScenarioCreator.views.population_panel_only'),
         url('^ValidateScenario/$', 'ScenarioCreator.views.validate_scenario'),
         url('^ProductionTypeList.json/$', 'ScenarioCreator.views.production_type_list_json'),
         url('^PopulationPanelStatus.json/$', 'ScenarioCreator.views.population_panel_status_json'),
         url('^DisableAllControls.json/$', 'ScenarioCreator.views.disable_all_controls_json'),
         url('^VaccinationGlobal/$', 'ScenarioCreator.views.vaccination_global'),
         url('^DestructionGlobal/$', 'ScenarioCreator.views.destruction_global'),
         url('^ProbabilityDensityFunction/(?P<primary_key>\d+)/graph.png$', 'ScenarioCreator.function_graphs.probability_graph'),
         url('^RelationalFunction/(?P<primary_key>\d+)/graph.png$', 'ScenarioCreator.function_graphs.relational_graph'),
         url('^ProbabilityDensityFunction/new/graph.png$', 'ScenarioCreator.function_graphs.empty_graph'),
         url('^RelationalFunction/new/graph.png$', 'ScenarioCreator.function_graphs.empty_graph'),
         url('^SpreadOptions.json/$', 'ScenarioCreator.views.spread_options_json'),
         url('^SpreadInputs.json/$', 'ScenarioCreator.views.spread_inputs_json'),
         url('^DiseaseSpreadAssignments.json/$', 'ScenarioCreator.views.disease_spread_assignments_json'),
         url('^ModifySpreadAssignments/$', 'ScenarioCreator.views.modify_spread_assignments'),
         url('^ExportPopulation/(?P<format>.+)$', 'ScenarioCreator.views.export_population'),
         url('^ExportFunctions/(?P<block>.+)$', 'ScenarioCreator.views.export_functions'),
         url('^ImportFunctions/(?P<block>.+)$', 'ScenarioCreator.views.import_functions'),
         url('^ExportRelGraph/$', 'ScenarioCreator.views.export_graph'),
         url('^BaseModel/$',                      'ScenarioCreator.views.model_list'),
         url('^BaseModel/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^BaseModel/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^BaseModel/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^BaseModel/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^InputSingleton/$',                      'ScenarioCreator.views.model_list'),
         url('^InputSingleton/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^InputSingleton/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^InputSingleton/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^InputSingleton/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^FloatField/$',                      'ScenarioCreator.views.model_list'),
         url('^FloatField/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^FloatField/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^FloatField/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^FloatField/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^Population/$',                      'ScenarioCreator.views.model_list'),
         url('^Population/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^Population/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^Population/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^Population/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^Unit/$',                      'ScenarioCreator.views.model_list'),
         url('^Unit/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^Unit/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^Unit/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^Unit/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^Function/$',                      'ScenarioCreator.views.model_list'),
         url('^Function/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^Function/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^Function/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^Function/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^ProbabilityDensityFunction/$',                      'ScenarioCreator.views.model_list'),
         url('^ProbabilityDensityFunction/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^ProbabilityDensityFunction/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^ProbabilityDensityFunction/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^ProbabilityDensityFunction/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^RelationalFunction/$',                      'ScenarioCreator.views.model_list'),
         url('^RelationalFunction/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^RelationalFunction/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^RelationalFunction/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^RelationalFunction/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^RelationalPoint/$',                      'ScenarioCreator.views.model_list'),
         url('^RelationalPoint/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^RelationalPoint/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^RelationalPoint/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^RelationalPoint/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^VaccinationGlobal/$',                      'ScenarioCreator.views.model_list'),
         url('^VaccinationGlobal/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^VaccinationGlobal/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^VaccinationGlobal/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^VaccinationGlobal/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^ControlMasterPlan/$',                      'ScenarioCreator.views.model_list'),
         url('^ControlMasterPlan/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^ControlMasterPlan/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^ControlMasterPlan/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^ControlMasterPlan/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^DestructionGlobal/$',                      'ScenarioCreator.views.model_list'),
         url('^DestructionGlobal/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^DestructionGlobal/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^DestructionGlobal/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^DestructionGlobal/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^ControlProtocol/$',                      'ScenarioCreator.views.model_list'),
         url('^ControlProtocol/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^ControlProtocol/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^ControlProtocol/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^ControlProtocol/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^ProtocolAssignment/$',                      'ScenarioCreator.views.model_list'),
         url('^ProtocolAssignment/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^ProtocolAssignment/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^ProtocolAssignment/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^ProtocolAssignment/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^Disease/$',                      'ScenarioCreator.views.model_list'),
         url('^Disease/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^Disease/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^Disease/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^Disease/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^DiseaseProgression/$',                      'ScenarioCreator.views.model_list'),
         url('^DiseaseProgression/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^DiseaseProgression/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^DiseaseProgression/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^DiseaseProgression/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^DiseaseProgressionAssignment/$',                      'ScenarioCreator.views.model_list'),
         url('^DiseaseProgressionAssignment/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^DiseaseProgressionAssignment/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^DiseaseProgressionAssignment/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^DiseaseProgressionAssignment/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^DiseaseSpread/$',                      'ScenarioCreator.views.model_list'),
         url('^DiseaseSpread/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^DiseaseSpread/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^DiseaseSpread/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^DiseaseSpread/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^AbstractSpread/$',                      'ScenarioCreator.views.model_list'),
         url('^AbstractSpread/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^AbstractSpread/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^AbstractSpread/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^AbstractSpread/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^IndirectSpread/$',                      'ScenarioCreator.views.model_list'),
         url('^IndirectSpread/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^IndirectSpread/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^IndirectSpread/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^IndirectSpread/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^DirectSpread/$',                      'ScenarioCreator.views.model_list'),
         url('^DirectSpread/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^DirectSpread/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^DirectSpread/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^DirectSpread/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^AirborneSpread/$',                      'ScenarioCreator.views.model_list'),
         url('^AirborneSpread/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^AirborneSpread/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^AirborneSpread/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^AirborneSpread/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^Scenario/$',                      'ScenarioCreator.views.model_list'),
         url('^Scenario/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^Scenario/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^Scenario/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^Scenario/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^OutputSettings/$',                      'ScenarioCreator.views.model_list'),
         url('^OutputSettings/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^OutputSettings/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^OutputSettings/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^OutputSettings/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^ProductionType/$',                      'ScenarioCreator.views.model_list'),
         url('^ProductionType/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^ProductionType/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^ProductionType/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^ProductionType/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^DiseaseSpreadAssignment/$',                      'ScenarioCreator.views.model_list'),
         url('^DiseaseSpreadAssignment/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^DiseaseSpreadAssignment/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^DiseaseSpreadAssignment/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^DiseaseSpreadAssignment/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^Zone/$',                      'ScenarioCreator.views.model_list'),
         url('^Zone/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^Zone/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^Zone/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^Zone/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^ZoneEffect/$',                      'ScenarioCreator.views.model_list'),
         url('^ZoneEffect/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^ZoneEffect/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^ZoneEffect/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^ZoneEffect/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^ZoneEffectAssignmentManager/$',                      'ScenarioCreator.views.model_list'),
         url('^ZoneEffectAssignmentManager/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^ZoneEffectAssignmentManager/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^ZoneEffectAssignmentManager/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^ZoneEffectAssignmentManager/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^ZoneEffectAssignment/$',                      'ScenarioCreator.views.model_list'),
         url('^ZoneEffectAssignment/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^ZoneEffectAssignment/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^ZoneEffectAssignment/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^ZoneEffectAssignment/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^ProductionGroup/$',                      'ScenarioCreator.views.model_list'),
         url('^ProductionGroup/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^ProductionGroup/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^ProductionGroup/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^ProductionGroup/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^VaccinationTrigger/$',                      'ScenarioCreator.views.model_list'),
         url('^VaccinationTrigger/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^VaccinationTrigger/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^VaccinationTrigger/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^VaccinationTrigger/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^FilteredVaccinationTrigger/$',                      'ScenarioCreator.views.model_list'),
         url('^FilteredVaccinationTrigger/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^FilteredVaccinationTrigger/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^FilteredVaccinationTrigger/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^FilteredVaccinationTrigger/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^DiseaseDetection/$',                      'ScenarioCreator.views.model_list'),
         url('^DiseaseDetection/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^DiseaseDetection/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^DiseaseDetection/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^DiseaseDetection/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^RateOfNewDetections/$',                      'ScenarioCreator.views.model_list'),
         url('^RateOfNewDetections/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^RateOfNewDetections/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^RateOfNewDetections/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^RateOfNewDetections/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^DisseminationRate/$',                      'ScenarioCreator.views.model_list'),
         url('^DisseminationRate/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^DisseminationRate/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^DisseminationRate/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^DisseminationRate/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^TimeFromFirstDetection/$',                      'ScenarioCreator.views.model_list'),
         url('^TimeFromFirstDetection/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^TimeFromFirstDetection/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^TimeFromFirstDetection/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^TimeFromFirstDetection/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^DestructionWaitTime/$',                      'ScenarioCreator.views.model_list'),
         url('^DestructionWaitTime/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^DestructionWaitTime/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^DestructionWaitTime/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^DestructionWaitTime/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^SpreadBetweenGroups/$',                      'ScenarioCreator.views.model_list'),
         url('^SpreadBetweenGroups/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^SpreadBetweenGroups/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^SpreadBetweenGroups/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^SpreadBetweenGroups/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^StopVaccination/$',                      'ScenarioCreator.views.model_list'),
         url('^StopVaccination/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^StopVaccination/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^StopVaccination/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^StopVaccination/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'),
         url('^VaccinationRingRule/$',                      'ScenarioCreator.views.model_list'),
         url('^VaccinationRingRule/new/$',                  'ScenarioCreator.views.new_entry'),
         url('^VaccinationRingRule/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
         url('^VaccinationRingRule/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry'),
         url('^VaccinationRingRule/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry'))