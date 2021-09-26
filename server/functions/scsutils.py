import math
import csv
import copy



def CalculatePopulationMigration(Rmax): 
    population_data=[]
    zlplot=''
    population=''
    max_plot_population = 0
    total_population = 0
    #Read population by zlplot data
    with open('./public/data/population.csv') as population_file:
        population_reader = csv.reader(population_file, delimiter=',')
        line_count=0
        for row in population_reader:
            if line_count == 0:
                line_count +=1
            else:
                zlplot = row[0]
                population=float(row[10])
                if population > max_plot_population:
                    max_plot_population = population
                total_population += population
                thiszlplot=[]
                thiszlplot.append(zlplot)
                thiszlplot.append(population)
                population_data.append(thiszlplot)
        #Read ImpactZone Data and calculate total population of  primary zone and secondary zones n1 and n2
    population_data_after_migration=copy.deepcopy(population_data)
        
    K=max_plot_population * 6
    P=total_population
    with open('./public/data/ImpactZones.csv') as ImpactZone_file:
        ImpactZone_reader = csv.reader(ImpactZone_file, delimiter=',')
        DC_Number=''
        PZ1=''
        PZ2=''
        PZ3=''
        PZ4=''
        PZ5=''
        PZ6=''
        SZ1=''
        SZ2=''
        SZ3=''
        SZ4=''
        SZ5=''
        SZ6=''
        line_count = 0
        for row in ImpactZone_reader:
            if line_count == 0:
                line_count += 1
            else:
                DC_Number = row[0]
                PZ1 = row[1]
                PZ2 = row[2]
                PZ3 = row[3]
                PZ4 = row[4]
                PZ5 = row[5]
                PZ6 = row[6]
                SZ1 = row[7]
                SZ2 = row[8]
                SZ3 = row[9]
                SZ4 = row[10]
                SZ5 = row[11]
                SZ6 = row[12]
                PZ1_pop=get_population(PZ1, population_data)
                PZ2_pop=get_population(PZ2, population_data)
                PZ3_pop=get_population(PZ3, population_data)
                PZ4_pop=get_population(PZ4, population_data)
                PZ5_pop=get_population(PZ5, population_data)
                PZ6_pop=get_population(PZ6, population_data)
                SZ1_pop=get_population(SZ1, population_data)
                SZ2_pop=get_population(SZ2, population_data)
                SZ3_pop=get_population(SZ3, population_data)
                SZ4_pop=get_population(SZ4, population_data)
                SZ5_pop=get_population(SZ5, population_data)
                SZ6_pop=get_population(SZ6, population_data)
                
                n1 = PZ1_pop + PZ2_pop + PZ3_pop + PZ4_pop + PZ5_pop + PZ6_pop
                n2 = SZ1_pop + SZ2_pop + SZ3_pop + SZ4_pop + SZ5_pop + SZ6_pop
                N = n1 + n2
                R = Rmax * ((K - n1)/K)
                Xnum = n1 * (R/100)
                Ynum = Xnum / 3
                Tnum = Xnum + Ynum
                Xinc = Xnum / 6
                Yinc = Ynum / 6
                m = (Tnum / (P - N)) * 100
                j = 0
                while j < len(population_data):
                    zlplot = population_data[j][0]
                    pop = get_population(zlplot, population_data)
                    if ((zlplot == PZ1) | (zlplot == PZ2) | (zlplot == PZ3) | (zlplot == PZ4) | (zlplot == PZ5) | (zlplot == PZ6)):
                        pop_new = pop + Xinc
                    elif ((zlplot == SZ1) | (zlplot == SZ2) | (zlplot == SZ3) | (zlplot == SZ4) | (zlplot == SZ5) | (zlplot == SZ6)):
                        pop_new = pop + Yinc
                    else:
                        pop_new = pop - (pop * m / 100) 
                    population_data_after_migration=set_population(zlplot,population_data_after_migration,pop_new)
                    j +=1
                line_count += 1
   
    with open('./public/data/population_after_migration.csv', mode='w', newline='') as popam_file:
        popam_csv_writer = csv.writer(popam_file)
        popam_csv_writer.writerow(['ZeroLevelPlot', 'current population', 'population after migration'])
        i = 0
        while i < len(population_data):
            popam_csv_writer.writerow([population_data[i][0], population_data[i][1], population_data_after_migration[i][1]])
            i +=1
    
    return


def get_population(zlplot, population_data): 
    i = 0
    while i < len(population_data):
        if zlplot == '':
            return  0
        if population_data[i][0] == zlplot:
            return population_data[i][1]
        i += 1
def set_population(zlplot, population_data_after_migration, new_population): 
    i = 0
    if zlplot == '':
        return population_data_after_migration
    while i < len(population_data_after_migration):
        if population_data_after_migration[i][0] == zlplot:
            population_data_after_migration[i][1] = new_population
            return population_data_after_migration
        i += 1
