import argparse
from glob import glob
from tqdm import tqdm

def generate_cactus_input(accession_file, newick_file, genome_dir, output_file='cactus_input.txt'):
    
    '''generate cactus input from a list of accession numbers and a newick file
    
       Arguments:
           accession_file: str, path to the file containing genomic accession numbers
           newick_file: str, path to the newick file
           output_file: str, path to the output file
           
       Returns:
           None
    '''
    
    # read in accession numbers
    with open(accession_file) as f:
        acc_list = [l.strip().split()[0] for l in f.readlines()]
    
    # read in newick file
    with open(newick_file) as f:
        newick = f.readline().strip() + '\n'
        
    # create cactus input file
    with open(output_file, 'w') as f:
        f.write(newick)
        for acc in tqdm(acc_list):
            try:
                fasta_path = glob(f'{genome_dir}/{acc}/*.fna')[0]
            except IndexError:
                print(f'Genome not found: {acc}')
                input()
            f.write(f'{acc}\t{fasta_path}\n')
    

def main():
    parser = argparse.ArgumentParser(description='Generate Cactus input')
    parser.add_argument('-a', '--accession_file', help='Path to the file containing genomic accession numbers')
    parser.add_argument('-n', '--newick_file', help='Path to the newick file')
    parser.add_argument('-g', '--genome_dir', help='Path to the directory containing the genomes')
    parser.add_argument('-o', '--output_file', help='Path to the output file')
    args = parser.parse_args()

    generate_cactus_input(args.accession_file, args.newick_file, args.genome_dir, args.output_file)
    
if __name__ == '__main__':
    main()