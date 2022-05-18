from fhirpy import SyncFHIRClient
from gui import *

HAPI_BASE_URL = "http://localhost:8080/baseR4/"

import datetime as dt

import matplotlib.pyplot as plt
plt.style.use('dark_background')
from matplotlib.figure import Figure


class Patient:
    def __init__(self, patient):
        self.name = patient["name"][0].given[0]
        self.surname = patient["name"][0].family
        self.gender = patient["gender"]
        self.birth_date = patient["birthDate"]
        self.identifier = patient["identifier"][0].value
        self.id = patient["id"]

        self.observations = []
        self.medications = []
        self.observations_values_names = []

    def medicationsLoader(self):
        if len(self.medications) == 0:
            client = SyncFHIRClient(HAPI_BASE_URL)
            resources = client.resources('MedicationRequest')
            resources = resources.search(subject=self.id).limit(10000)
            medication_requests = resources.fetch()

            for medication_request in medication_requests:
                medication_dict = {
                    "name": medication_request["medicationCodeableConcept"].coding[0].display,
                    "date": medication_request["authoredOn"],
                    "type": 'medication',  #aby sprawdzac typ podczas przechodzenia po zmieszanej liscie
                    "id": medication_request["id"]
                }
                self.medications.append(medication_dict)

    def history_rangeLoader(self, start_date, end_date):

        history = []

        start_date = dt.datetime.strptime(start_date,"%Y-%m-%d")
        end_date = dt.datetime.strptime(end_date,"%Y-%m-%d")

        counter = 0
        for obs in self.observations:

            obs_date =  dt.datetime.strptime(obs['date'][:16], "%Y-%m-%dT%H:%M")
            if(obs_date<start_date):
                continue
            elif(obs_date>end_date):
                break

            while counter<len(self.medications) and dt.datetime.strptime(self.medications[counter]['date'][:16],"%Y-%m-%dT%H:%M")< obs_date:
                if dt.datetime.strptime(self.medications[counter]['date'][:16],"%Y-%m-%dT%H:%M")<start_date:
                    counter+=1
                    continue
                elif dt.datetime.strptime(self.medications[counter]['date'][:16],"%Y-%m-%dT%H:%M")>end_date:
                    break
                else:
                    history.append(self.medications[counter])
                counter += 1

            history.append(obs)

        for i in range(counter,len(self.medications)):
            med_date = dt.datetime.strptime(self.medications[i]['date'][:16],"%Y-%m-%dT%H:%M")
            if(med_date<start_date):
                continue
            elif(med_date>end_date):
                break
            else:
                history.append(self.medications[i])

        print("(get_history) found ",len(history)," notes between ",start_date," and ",end_date)

        return  history

    def observations_values_namesLoader(self):
        for obs in self.observations:
            if (obs['type'] == 'values' or obs['type'] == 'value' )and obs['name'] not in self.observations_values_names:
                self.observations_values_names.append(obs['name'])
        return self.observations_values_names


    def observationsLoader(self):

        if len(self.observations) == 0:
            client = SyncFHIRClient(HAPI_BASE_URL)
            resources = client.resources('Observation')
            resources = resources.search(subject=self.id).limit(10000).sort('date')
            observations = resources.fetch()

            for observation in observations:
                observation_dict = {
                    "category": observation["category"][0].coding[0].display,
                    "name": observation["code"].coding[0].display,
                    "date": observation["effectiveDateTime"],
                    "id": observation["id"]
                }
                if "component" in observation.keys():
                    values = []
                    units = []
                    specific_names = []
                    for x in observation["component"]:
                        specific_names.append(x.code.coding[0].display)
                        values.append(x.valueQuantity.value)
                        units.append(x.valueQuantity.unit)
                    observation_dict["value"] = values
                    observation_dict["unit"] = units
                    observation_dict["specific_name"] = specific_names
                    observation_dict["type"] = 'values'  # more than one value
                elif "valueQuantity" in observation.keys():
                    observation_dict["value"] = observation["valueQuantity"].value
                    observation_dict["unit"] = observation["valueQuantity"].unit
                    observation_dict["type"] = 'value'  # one value
                else:
                    observation_dict["type"] = 'text'  # no value

                self.observations.append(observation_dict)


class Plot:
    def __init__(self):
        self.fig = Figure(figsize=(7, 4), dpi=100)

    def create_plot(self, patient, observation_name, start_date, days):
        print("CREATE PLOT:", observation_name)
        unit = ''
        x = []
        y = []
        y2 = []
        unit2 = ''

        specific_names = ['', '']

        if not self.fig is None:
            self.fig.clear()

        start_date = dt.datetime.strptime(start_date, "%Y-%m-%d")

        for obs in patient.observations:
            obs_date = dt.datetime.strptime(obs['date'][:10], "%Y-%m-%d")
            if obs['name'] == observation_name and obs_date >= start_date and obs_date <= start_date + dt.timedelta(
                    days):
                if obs['type'] == 'value':
                    unit = obs['unit']
                    x.append(obs['date'][:10] + '\n' + obs['date'][11:16])
                    y.append(obs['value'])
                elif obs['type'] == 'values':
                    unit = obs['unit'][0]
                    unit2 = obs['unit'][1]
                    specific_names[0] = obs['specific_name'][0]
                    specific_names[1] = obs['specific_name'][1]
                    x.append(obs['date'][:10] + '\n' + obs['date'][11:16])
                    y.append(obs['value'][0])
                    y2.append(obs['value'][1])

        if unit2 == '':
            self.fig.add_subplot(111)
            ax = self.fig.gca()
            ax.plot(x, y, 'o--')
            ax.set(title=observation_name)
            ax.set_ylabel(unit)

            ax.grid()
            plt.xticks(rotation=0)
            # plt.show()

        else:
            ax1 = self.fig.add_subplot(2, 1, 1)
            ax2 = self.fig.add_subplot(2, 1, 2)

            ax1.plot(x, y, 'o--')
            ax1.set(title=specific_names[0])
            ax1.set_ylabel(unit)

            ax2.plot(x, y2, 'o--')
            ax2.set(title=specific_names[1])
            ax2.set_ylabel(unit2)

            # plt.ylabel(unit, rotation=0)
            self.fig.tight_layout()
            ax1.grid()
            ax2.grid()
            plt.yticks(rotation=0)
            plt.xticks(rotation=0)

            # plt.show()
        return self.fig



class PatientsDataLoader:
    def __init__(self, patients):
        self.patients = patients

    def getPatient(self, id):
        for patient in self.patients:
            if patient.identifier == id:
                patient.observationsLoader()
                patient.medicationsLoader()
                patient.observations_values_namesLoader()
                return patient
        return None

    def get_all_patients(self):
        return self.patients

    def getPatients_filtered(self, surname):
        patients_filtered = []
        for patient in self.patients:
            if surname in patient.surname:
                patients_filtered.append(patient)
        return patients_filtered


def main():
    client = SyncFHIRClient(HAPI_BASE_URL)

    resources = client.resources('Patient')
    resources = resources.search().limit(10000)
    patients_resource = resources.fetch()
    list_of_patient = []

    for patient in patients_resource:
        list_of_patient.append(Patient(patient))

    print("(main) loaded", len(list_of_patient), "patients")

    patients_data = PatientsDataLoader(list_of_patient)

    gui = GUI("Karta pacjenta", 800, 500, False, patients_data)


if __name__ == "__main__":
    main()
