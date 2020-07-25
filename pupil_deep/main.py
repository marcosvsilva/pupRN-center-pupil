import os
from multiprocessing import Process
from execution import Execution


class Main:
    def __init__(self):
        # Directoris
        self._projects_path = '/media/marcos/Dados/Projects'

        self._path_dataset = '{}/Datasets/Exams'.format(self._projects_path)
        self._path_information = '{}/Datasets/Exams/Information_Exams'.format(self._projects_path)

        self._path_out = '{}/Results/Qualificacao/CenterPupilTec2/Frames'.format(self._projects_path)
        self._path_label = '{}/Results/Qualificacao/CenterPupilTec2/Labels'.format(self._projects_path)

        # self._path_out = '{}/Results/PupilDeep/Frames'.format(self._projects_path)
        # self._path_label = '{}/Results/PupilDeep/Labels'.format(self._projects_path)

        # Exams to execute
        self._list_available = ['07080107_08_2019_08_04_39.mp4']

    def _make_path(self, path):
        try:
            os.mkdir(path)
        except FileExistsError:
            pass

    def run(self):
        number_of_process = int(os.cpu_count()/2)

        print(self._path_out)
        print(os.listdir(self._path_out))

        exams_exists = ['{}.mp4'.format(x) for x in os.listdir(self._path_out)]
        if len(self._list_available) > 0:
            list_exams = [x for x in self._list_available if ('.mp4' in x) and (x not in exams_exists)]
        else:
            list_exams = [x for x in os.listdir(self._path_dataset) if ('.mp4' in x) and (x not in exams_exists)]

        list_exams = ['benchmark_final.avi']

        process = []
        while len(list_exams) > 0:
            end_list = number_of_process if len(list_exams) > number_of_process else len(list_exams)
            list_process = list_exams[0:end_list]
            list_exams = list_exams[end_list:len(list_exams)]

            for exam in list_process:
                title = exam.replace('.avi', '')

                paths = {'path_exam': '{}/{}'.format(self._path_dataset, exam),
                         'path_information':  '{}/{}.log'.format(self._path_information, title),
                         'path_out': '{}/{}'.format(self._path_out, title),
                         'path_label': '{}/{}_label.csv'.format(self._path_label, title)}

                self._make_path(paths['path_out'])

                execution = Execution()
                thread = Process(target=execution.pupil_process, args=(paths, ))
                process.append(thread)
                thread.start()

            for thread in process:
                thread.join()



main = Main()
if __name__ == '__main__':
    main.run()
