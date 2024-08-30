## GLOBAL VARIABLES

## INPUT 1: A tab delimited file that matches samples with population
## INPUT 2: A vcf file with variants for statistic analysis
POP_INFO_FILE   = '1KGP.sample.pop.tab'
VCF_FILE        = 'VCF_SAMPLE.vcf'
OUTPUT_FILENAME = 'result'
POPULATION_LIST = []

ZEROZERO = "0/0" 
ZEROONE  = "0/1"
ONEONE   = "1/1"


# function to parse population file and store info into a dictionary
# Dictionary keys are sample names and values are a list with population name and a number,
# that will be used as a counter. This number will keep the number of insertions in this sample
# In POPULATION_LIST, we store a list of all populations, for future use
def parse_population_file():
    print(f'Parsing Population file')
    global POPULATION_LIST
    result  = {}
    with open(POP_INFO_FILE, "r") as file:
        for line in file:
            tokens = line.split("\n")[0].split("\t")
            sample_id     = tokens[0]
            population_id = tokens[1]

            result[sample_id] = [population_id, 0]

            if population_id not in POPULATION_LIST:
                POPULATION_LIST.append(population_id)

    POPULATION_LIST.sort()
    return result


# two functions to get and change the dictionary holding population info
# a function that accepts a sample name and returns the population name
def get_population_from_sample(dictionary_, key_):
    if key_ in dictionary_:
        return dictionary_[key_][0]
    return 0

# and a function that increases the counter number for a specific sample
def increase_sample_counter(dictionary_, key_):
    dictionary_[key_][1] += 1


# Function that reads the vcf file and creates a dictionary for each row
# As value we keep a list that includes counters for the amount of 0/0, 0/1 and 1/1
# a list of all samples that have info regards to this row and
# a list of populations that have this row/insertion
# 
# This method uses and modifies the dictionary holding population data
# It uses increase_sample_counter, whenever a sample is characterized with 0/1 or 1/1
def parse_vcf_file(pop_data):
    print(f'Parsing VCF file')
    result = {}
    file_header = ''
    with open(VCF_FILE, "r") as file:
        for line in file:
            if '##' in line:
                continue
            if '#' in line:
                file_header = line.split('\n')[0].split('\t')
            else:
                tokens = line.split('\n')[0].split('\t')
                chr_number    = tokens[0]
                pos_number    = tokens[1]
                insertion_id  = chr_number + '_' + pos_number
                
                ins_count_00    = 0
                ins_count_01    = 0
                ins_count_11    = 0
                ins_sample_data = []

                ins_pop_list_01_11 = []

                pos_GT = 0
                for i, token in enumerate(tokens):
                    if 'GT' in token:
                        format = token.split(":")
                        pos_GT = format.index('GT')
                        continue

                    if i < len(file_header):
                        sample_name = file_header[i]
                        sample_population = get_population_from_sample(pop_data, sample_name)
                        values = token.split(':')
                    
                        if ZEROZERO in values[pos_GT]:
                            ins_count_00 += 1
                        elif ZEROONE in values[pos_GT]:
                            ins_count_01 += 1
                        elif ONEONE in values[pos_GT]:
                            ins_count_11 += 1
                        else:
                            pass

                        ins_sample_data.append((sample_name, values[pos_GT], sample_population))
                        if ZEROONE in values[pos_GT] or ONEONE in values[pos_GT]:
                            increase_sample_counter(pop_data, sample_name)
                            if sample_population not in ins_pop_list_01_11:
                                ins_pop_list_01_11.append(sample_population)
                ins_pop_list_01_11.sort()
                result[insertion_id] = (ins_count_00, ins_count_01, ins_count_11, ins_sample_data, ins_pop_list_01_11)
    return result


# The function that uses the dictionary created from parse_vcf_file
# and creates 2 files with some statistics
# The first output file will contain information about each line on the vcf file.
#   Number of 0/0, 0/1 and 1/1 in total and per population
# The second outout file will contain insights on how many and which populations
#   have insertions of each row on vcf file
def analysis_1(vcf_data):
    print(f'Starting Analysis 1')
    outputfile  = OUTPUT_FILENAME + ".1.tab"
    outputfile2 = OUTPUT_FILENAME + ".2.tab"
    with open(outputfile, "w") as file, open(outputfile2, "w") as file2:
        # header of the files
        file.write(f'insertion\tno_00\tno_01\tno_11')
        for population in POPULATION_LIST:
            file.write(f"\t{population}.00")
        for population in POPULATION_LIST:
            file.write(f"\t{population}.01")
        for population in POPULATION_LIST:
            file.write(f"\t{population}.11")
        file.write(f'\n')
        file2.write(f'insertion\tno_of_populations\tpopulations\n')

        # main data
        for key, value in vcf_data.items():
            (ins_count_00, ins_count_01, ins_count_11, ins_sample_data, ins_pop_list_01_11) =  value
            file.write(f'{key}\t{ins_count_00}\t{ins_count_01}\t{ins_count_11}')

            list_of_populations     = "\t".join(ins_pop_list_01_11)
            len_list_of_populations = len(ins_pop_list_01_11)
            file2.write(f'{key}\t{len_list_of_populations}\t{list_of_populations}\n')

            per_population_counter00 = ''
            per_population_counter01 = ''
            per_population_counter11 = ''
            for population in POPULATION_LIST:
                all00 = len(list(filter(lambda data: data[2] == population and data[1] == ZEROZERO, ins_sample_data)))
                all01 = len(list(filter(lambda data: data[2] == population and data[1] == ZEROONE, ins_sample_data)))
                all11 = len(list(filter(lambda data: data[2] == population and data[1] == ONEONE, ins_sample_data)))
                per_population_counter00 += f'\t{all00}'
                per_population_counter01 += f'\t{all01}'
                per_population_counter11 += f'\t{all11}'
            
            file.write(f'{per_population_counter00}{per_population_counter01}{per_population_counter11}\n')


# The function that uses the dictionary created from parse_population_file
# and creates a file that contains insertions/SNPs per sample.
def analysis_2(pop_data):
    print(f'Starting Analysis 2')
    outputfile = OUTPUT_FILENAME + ".3.tab"
    with open(outputfile, "w") as file:
        # header of the file
        file.write(f"sample_name\tnumber_of_insertions\tpopulation\n")
        # main data
        for item in pop_data:
            insertions_per_sample = pop_data[item][1]
            sample_population     = pop_data[item][0]
            file.write(f"{item}\t{insertions_per_sample}\t{sample_population}\n")



if __name__ == "__main__":
    print(f'Psarema: Started')

    # Lets parse the population file
    pop_data = parse_population_file()

    # Lets parse VCF file
    vcfDB = parse_vcf_file(pop_data)

    # first analysis
    analysis_1(vcfDB)

    # second analysis
    analysis_2(pop_data)
    
    print(f'Psarema: Completed')