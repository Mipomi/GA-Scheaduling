import random
import csv
import os
from tabulate import tabulate

# fungsi membaca data set
def read_csv(filename):
    path = os.path.join('dataset', filename)
    with open(path, 'r') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

# load semua data set
classes = read_csv('classes.csv')
subjects = read_csv('subjects.csv')
teachers = read_csv('teachers.csv')
rooms = read_csv('rooms.csv')
timeslots = read_csv('timeslots.csv')
days = read_csv('days.csv')

# inisialisasi populasi awal
def initialize_population(size=10):
    population = []
    for _ in range(size):
        schedule = []
        used_subjects = {cls['class']: set() for cls in classes}
        for cls in classes:
            for day in days:
                for timeslot in timeslots:
                    available_subject = [
                        subj['subject'] for subj in subjects
                        if subj['subject'] not in used_subjects[cls['class']]
                    ]
                    if available_subject:
                        subject = random.choice(available_subject)
                        used_subjects[cls['class']].add(subject)
                        entry ={
                            'day': day['day'],
                            'class': cls['class'],
                            'subject': subject,
                            'teacher': random.choice(teachers)['name'],
                            'room': random.choice(rooms)['room'],
                            'timeslot': timeslot['time_range'],
                        }
                        schedule.append(entry)
        population.append(schedule)
    return population

# menghitung fitnes
def calculate_fitness(schedule):
    conflicts = 0
    for i in range(len(schedule)):
        for j in range(i + 1, len(schedule)):
            if (schedule[i]['day'] == schedule[j]['day'] and schedule[i]['timeslot'] == schedule[j]['timeslot']):
                if (schedule[i]['teacher'] == schedule[j]['teacher'] or schedule[i]['class'] == schedule[j]['class'] or schedule[i]['room'] == schedule[j]['room']):
                    conflicts += 1
    return -conflicts

# seleksi individu terbaik
def selectiion(population):
    return sorted(population, key=calculate_fitness, reverse=True)[:2]

# crossover individu
def crossover(parent1, parent2):
    point = len(parent1) // 2
    child = parent1[:point] + parent2[point:]
    return child

# mutasi
def mutate(schdule):
    if schdule:
        index = random.randint(0, len(schdule) - 1)
        schdule[index]['teacher'] = random.choice(teachers)['name']

# algoritma genetik
def genetic_algorithm(generations=100):
    population = initialize_population()
    best_solution = None
    for _ in range(generations):
        parents = selectiion(population)
        child = crossover(parents[0], parents[1])
        mutate(child)
        population.append(child)

        # solusi terbaik
        best_solution = selectiion(population)[0]
    return best_solution

# tempilkan jadwal
def display_schedule_per_class(schedule, title="jadwal terbaik"):
    schedule.sort(key=lambda x: (x['class'], x['day'], x['timeslot'])) #sesuai kelas, hari dan jam
    current_class = None
    table = []
    for entry in schedule:
        if entry['class'] != current_class:
            if table:
                print(f"\n{title} untuk kelas {current_class}:\n")
                print(tabulate(table, headers="keys", tablefmt="grid"))
                table = []
            current_class = entry['class']
        table.append({
            "hari": entry['day'],
            "Mata Pelajaran": entry['subject'],
            "Guru": entry['teacher'],
            "Ruangan": entry['room'],
            "Jam": entry['timeslot']
        })
    # cetak jadwal terakhir
    if table:
        print(f"\n{title} untuk kelas {current_class}:\n")
        print(tabulate(table, headers="keys", tablefmt="grid"))
        
# jalankan algoritma genetika
best_schadule = genetic_algorithm()

display_schedule_per_class(best_schadule, title="Hasil tebaik jadwal")