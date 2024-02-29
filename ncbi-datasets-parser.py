import argparse
import json 

def filter_genomes(jsonl_file):
    
    ''' parses a ncbi-datasets jsonl file to select accessions for 
        a diverse set of Wolbachia strains
    '''
    
    # parse jsonl file where each line is a json object 
    with open(jsonl_file, 'r') as f:
        for line in f:
            #TODO: json loading and parsing
            # load genome json object into genome_dict
            
            # identify the strain name and accession number 
            accesion_num = genome_dict['accession']
            # this is the portion of the dictionary you need to check for strain: ( "attributes":[{"name":"strain","value":"wMel"})
            
            # print out the strain and accession number for each genome
    
    pass 

def main():
    parser = argparse.ArgumentParser(description='Process JSON file.')
    parser.add_argument('-f', '--file', type=str, help='Path to the JSON file')
    args = parser.parse_args()

    filter_genomes(args.file)   

if __name__ == '__main__':
    main()
