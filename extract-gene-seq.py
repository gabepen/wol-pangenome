from Bio import SeqIO
from collections import defaultdict
from glob import glob 
import argparse
import os
import subprocess
from tqdm import tqdm

def extract_gene_sequence(fasta_file, gff_file, gene_name):
  '''
  Extracts the sequence of a gene from a fasta file based on its ID in a gff3 file.

  Args:
    fasta_file: Path to the fasta file containing the genomic sequences.
    gff_file: Path to the gff3 file with gene annotations.
    gene_id: The ID of the gene to extract the sequence for.

  Returns:
    The sequence of the gene, or None if not found.
  '''
  
  # Load fasta sequences
  fasta_sequences = SeqIO.to_dict(SeqIO.parse(fasta_file, "fasta"))

  # Parse GFF3 file and store gene locations
  gene_locations = defaultdict(list)
  with open(gff_file) as gff:
    for line in gff:
      if line.startswith("#"):
        continue
      fields = line.strip().split("\t")
      print(fields[8].split(";")[1].split("=")[1])
      input()
      if fields[2] == "gene" and gene_name in fields[8].split(";")[1].split("=")[1]:
        print('here')
        input()
        start, end = int(fields[3]), int(fields[4])
        gene_locations[fields[0]].append((start, end))

  # Extract sequence based on gene location
  for chrom, locations in gene_locations.items():
    print(chrom, locations)
    input()
    if chrom not in fasta_sequences:
      continue
    for start, end in locations:
      return fasta_sequences[chrom].seq[start-1:end]  # Adjust for 0-based indexing

  # Gene not found
  return None

def predict_rrna_seq(fasta_file, output_path):
  
  '''
  Predicts the sequence of ribsomoal RNA from a fasta file using barrap

  Args:
    fasta_file: Path to the fasta file containing the genomic sequences.
   
  Returns:
    Nothing, creates output files in the output path 
  '''
  subprocess.call(['barrnap', '-k', 'bac', '--threads', '20', '-o', output_path + '/output_rrna.fna'], 
                  stdin=open(fasta_file, 'r'), stdout=open(output_path + '/output_rrna.gff', 'w'), stderr=open('/dev/null', 'w'))
  
def merge_result_files(output_dir, acc_list):
  
  '''
  Merge extracted sequences into a single file adding genome accession to fasta header
  
  Args:
    output_dir: Path to the directory containing the extracted sequence files 
    acc_list: List of genome accessions to merge
    
  Returns:
    Nothing, creates output file in the output directory
  '''
  
  # collect acc_list from file
  with open(acc_list) as f:
    acc_list = [l.strip().split()[0] for l in f.readlines()]
  
  with open(output_dir + '/all_16S.fasta', 'w') as out_f:
    for acc_num in acc_list:
      genome_folder = os.path.join(output_dir, acc_num)
      rrna_file = glob(genome_folder + '/*.fna')
      with open(rrna_file[0]) as in_f:
        for line in in_f:
          if line.startswith('>16S'):
            out_f.write('>' + acc_num + '\n')
            out_f.write(next(in_f))
            break 

def main():
    
    '''Script to extract orthologs from a set of genomes
    
        Input: 
            gff3 directory, an unzipped ncbi-datasets where each folder is an accession of a genome 
            genomic fna directory, an unzipped ncbi-datasets where each folder is an accession of a genome
            
        Output: 
            multiple sequence fasta of extracted gene sequences for each genome
        
        
    '''
    
    parser = argparse.ArgumentParser(description='Extract orthologs from a set of genomes')
    parser.add_argument('-g', '--genomes', type=str, help='Path to the genome directory')
    parser.add_argument('-f', '--gffs', type=str, help='Path to the gffs directory')
    parser.add_argument('-i', '--gene_id', type=str, help='Gene ID to extract')
    parser.add_argument('-l', '--acc_list', type=str, help='List of genome accessions to extract')
    args = parser.parse_args() 
    
    # create output directory
    output_dir = '../16S_seqs'
    if not os.path.exists(output_dir):
      os.mkdir(output_dir)
      
    # extract gene sequences for each genome using gene name 
    '''
    for genome in os.listdir(args.genomes):
      genome_folder = os.path.join(args.genomes, genome)
      fasta_file_path = glob(genome_folder + '/*')
      gff_folder_id = 'GCF_' + genome.split('_')[1]
      gff_path = os.path.join(args.gffs, gff_folder_id + '/genomic.gff')
      gene_sequence = extract_gene_sequence(fasta_file_path[0], gff_path, args.gene_id)
      print(gene_sequence)
      input()
     '''
    
    # extract 16S sequences using barrap
    for genome in tqdm([g for g in os.listdir(args.genomes) if os.path.isdir(os.path.join(args.genomes, g))]):
      
      # get genome accession and file paths 
      genome_folder = os.path.join(args.genomes, genome)
      fasta_file_path = glob(genome_folder + '/*')
      output_path = output_dir + '/' + genome
      if not os.path.exists(output_path):
        os.mkdir(output_path)
      else:
        if len(glob(output_path + '/*')) == 2:
          continue

  
      # predict 16S rRNA sequence with barrap
      try:
        predict_rrna_seq(fasta_file_path[0], output_path)
      except IndexError:
        print('Error predicting 16S rRNA sequence for genome: ', genome)
        input()
        continue
      
    # merge all 16S rRNA sequences into a single file
    merge_result_files(output_dir, args.acc_list)
    
if __name__ == '__main__':
    main()
