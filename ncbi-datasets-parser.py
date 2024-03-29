import argparse
import json 
import pprint


def filter_genomes(jsonl_file) -> list:
    
    ''' parses a ncbi-datasets jsonl file to select accessions for 
        a diverse set of Wolbachia strains
        
        Arguments:  jsonl_file: str, path to jsonl file containing genome data
        
        Returns: list of strain names and accession numbers  
        
    '''
    
    strain_count_dict = {}
    filtered_list = []
    
    # parse jsonl file where each line is a json object 
    with open(jsonl_file, 'r') as f:
        for line in f:
            #TODO: json loading and parsing
            # load genome json object into genome_dict
            genome_dict = json.loads(line)
            '''
            # debug
            pprint.pprint(genome_dict, indent=5)
            input()
            '''
            # identify the strain name and accession number 
            accesion_num = genome_dict['accession']
            
            # check for strain
            strain = genome_dict['organism']['organismName']
            taxid = genome_dict['organism']['taxId']
            
            # check total count for strain and add to output list if under 2
            if strain in strain_count_dict:
                if strain_count_dict[strain] < 2:
                    filtered_list.append((strain, accesion_num, taxid))
                strain_count_dict[strain] += 1
            else:
                filtered_list.append((strain, accesion_num, taxid))
                strain_count_dict[strain] = 1
                
    return filtered_list

def main():
    
    '''Script to parse jsonl file to select accessions for a diverse set of Wolbachia strains
    
        Input: jsonl file from ncbi-datasets query 
        
        Output: list of accesion number and taxids for a diverse set of Wolbachia strains
        
        
    '''
    parser = argparse.ArgumentParser(description='Process JSON file.')
    parser.add_argument('-f', '--file', type=str, help='Path to the JSON file')
    args = parser.parse_args()

    filtered_list = filter_genomes(args.file)   
    for l in filtered_list:
        print(l[1], l[2], l[0])

if __name__ == '__main__':
    main()
