import os
import shutil
import zipfile
import psutil

from django.shortcuts import redirect

from ADSMSettings.models import SimulationProcessRecord, SmSession
from ADSMSettings.utils import workspace_path, supplemental_folder_has_contents, scenario_filename


def is_simulation_running():
    """Returns True if the simulation is currently active.  Also sets the simulation_has_started for historical context."""
    if len(get_simulation_controllers()) > 0:
        SmSession.objects.all().update(simulation_has_started=True)
        return True
    return False

def is_simulation_stopped():
    """ :return: True if the Simulation has started and either completed or been aborted 
    """
    return not is_simulation_running() and SmSession.objects.get().simulation_has_started  # This order is important   


def get_simulation_controllers():
    results = []
    records = SimulationProcessRecord.objects.all()  # really shouldn't be longer than 1
    for record in records:
        for process in psutil.process_iter():
            if process.pid == record.pid:
                try:
                    if 'python' not in process.name().lower() and 'adsm' not in process.name().lower():
                        record.delete()  # stale process record where the pid was reused
                    else:  # process call python
                        results.append(process)
                except psutil.AccessDenied as e:
                    continue
    return results


def delete_supplemental_folder():
    scenario_folder = scenario_filename()
    if scenario_folder != '':
        try:
            shutil.rmtree(workspace_path(scenario_folder + "/" + scenario_folder))
        except:
            pass  # because the folder doesn't exist (which is fine)

        from django.db import connections
        connections['scenario_db'].cursor().execute('VACUUM')
        

def map_zip_file():
    """This is a file named after the scenario in the folder that's also named after the scenario."""
    return workspace_path(scenario_filename() + '/' + "Supplemental Output Files" + '/' + scenario_filename() + " Map Output.zip")


def zip_map_directory_if_it_exists():
    dir_to_zip = workspace_path(scenario_filename() + "/" + "Supplemental Output Files" + "/Map")
    if os.path.exists(dir_to_zip) and supplemental_folder_has_contents(subfolder='/Map'):
        zipname = map_zip_file()
        dir_to_zip_len = len(dir_to_zip.rstrip(os.sep)) + 1
        with zipfile.ZipFile(zipname, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
            for dirname, subdirs, files in os.walk(dir_to_zip):
                for filename in files:
                    path = os.path.join(dirname, filename)
                    entry = path[dir_to_zip_len:]
                    zf.write(path, entry)
    else:
        print("Folder is empty: ", dir_to_zip)


def abort_simulation(request=None):
    # Import these things locally since several other modules import this utils
    from django.db import close_old_connections
    from ADSMSettings.views import save_scenario
    from Results.interactive_graphing import population_zoom_png

    # Kill each of the open processes
    for process in get_simulation_controllers():
        print("Aborting Simulation Thread")
        process.kill()

    if request is not None:
        return redirect('/results/')


def delete_all_outputs():
    from Results.models import DailyControls, DailyByZone, DailyByProductionType, DailyByZoneAndProductionType, UnitStats, ResultsVersion
    abort_simulation()
    if DailyControls.objects.count() > 0:
        print("DELETING ALL OUTPUTS")
    for model in [DailyControls, DailyByZone, DailyByProductionType, DailyByZoneAndProductionType, UnitStats, ResultsVersion]:
        model.objects.all().delete()
    SmSession.objects.all().update(iteration_text = '', simulation_has_started=False)  # This is also reset from open_scenario
    if os.path.isdir(workspace_path(scenario_filename() + "/" + "Supplemental Output Files")):
        shutil.rmtree(workspace_path(scenario_filename() + "/" + "Supplemental Output Files"), ignore_errors=True)
