import argparse
import json 
import pprint
import random


def filter_genomes(jsonl_file) -> list:
    
    ''' parses a ncbi-datasets jsonl file to select accessions for 
        a diverse set of Wolbachia strains
        
        Arguments:  
            jsonl_file: str, path to jsonl file containing genome data
        
        Returns: 
            list of strain names and accession numbers  
        
    '''
    
    strain_count_dict = {}
    filtered_list = []
    accessions = set() 
    
    # parse jsonl file where each line is a json object 
    with open(jsonl_file, 'r') as f:
        for line in f:
            # load genome json object into genome_dict
            genome_dict = json.loads(line)
          
            # identify the strain name and accession number 
            accession_ID = genome_dict['accession']
            accession_num = genome_dict['accession'].split('_')[-1] # removing the GenBank or RefSeq prefix

            # check for strain
            strain = genome_dict['organism']['organismName']
            taxid = genome_dict['organism']['taxId']
            
            # add strains to filtered list 
            
            # no duplicate accession numbers  (one from RefSeq, one from GenBank)
            if accession_num not in accessions:
                accessions.add(accession_num)
                # check total count for strain and add to output list if under 2
                if strain in strain_count_dict:
                    if strain_count_dict[strain] < 2:
                        filtered_list.append((strain, accession_ID, taxid))
                    strain_count_dict[strain] += 1
                else:
                    filtered_list.append((strain, accession_ID, taxid))
                    strain_count_dict[strain] = 1
                
    return filtered_list

def save_genomes(filtered_list, number_genomes, output_path):
    
    # Save the first number of genomes in the filtered list to a tsv file at output path
    with open(output_path, 'w') as f:   
        for i in range(number_genomes):
            strain, accession_ID, taxid = filtered_list[i]
            f.write(f"{accession_ID}\t{taxid}\t{strain}\n")

def main():
    
    '''Script to parse jsonl file to select accessions for a diverse set of Wolbachia strains
    
        Input: jsonl file from ncbi-datasets query 
        
        Output: list of accesion number and taxids for a diverse set of Wolbachia strains
        
        
    '''
    parser = argparse.ArgumentParser(description='Process JSON file.')
    parser.add_argument('-f', '--file', type=str, help='Path to the JSON file')
    parser.add_argument('-n', '--number_genomes', type=int, help='Number of genomes to select')
    parser.add_argument('-o', '--output', type=str, help='Path to the output file')
    args = parser.parse_args()

    filtered_list = filter_genomes(args.file)  
    random.shuffle(filtered_list) 
    
    save_genomes(filtered_list, args.number_genomes, args.output)
   
if __name__ == '__main__':
    main()
