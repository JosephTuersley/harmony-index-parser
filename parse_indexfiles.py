#!/usr/bin/env python3
"""
Script to parse indexfiles directory structure and extract plate barcodes 
and measurement signatures from indexfile.txt files.
"""

import os
import csv
import re
import argparse
from pathlib import Path


def extract_measurement_signature(url):
    """
    Extract measurement signature from URL.
    
    Args:
        url (str): URL containing the measurement signature
        
    Returns:
        str: Measurement signature or None if not found
    """
    # Pattern to match UUID in the URL path
    pattern = r'/([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/'
    match = re.search(pattern, url)
    return match.group(1) if match else None


def extract_plate_barcode(folder_name):
    """
    Extract plate barcode from folder name.
    
    Args:
        folder_name (str): Folder name like "30082__2025-05-31T01_01_45-Measurement 1"
        
    Returns:
        str: Plate barcode (e.g., "30082")
    """
    return folder_name.split('__')[0]


def process_indexfile(indexfile_path):
    """
    Process a single indexfile.txt and extract the first measurement signature.
    
    Args:
        indexfile_path (Path): Path to the indexfile.txt
        
    Returns:
        str: First measurement signature found, or None
    """
    try:
        with open(indexfile_path, 'r', encoding='utf-8') as file:
            # Read header line to find URL column
            header = file.readline().strip()
            header_cols = header.split('\t')
            
            # Find URL column index
            url_col_index = None
            for i, col in enumerate(header_cols):
                if 'URL' in col.upper():
                    url_col_index = i
                    break
            
            if url_col_index is None:
                print(f"Warning: No URL column found in {indexfile_path}")
                return None
            
            # Process first data line to get measurement signature
            first_line = file.readline().strip()
            if first_line:
                columns = first_line.split('\t')
                if len(columns) > url_col_index:
                    url = columns[url_col_index]
                    return extract_measurement_signature(url)
    except Exception as e:
        print(f"Error processing {indexfile_path}: {e}")
    
    return None


def process_indexfiles_directory(indexfiles_dir):
    """
    Process all indexfile.txt files in the directory structure.
    
    Args:
        indexfiles_dir (Path): Path to the indexfiles directory
        
    Returns:
        list: List of tuples (plate_barcode, measurement_signature)
    """
    results = []
    
    # Iterate through all subdirectories
    for folder_path in indexfiles_dir.iterdir():
        if folder_path.is_dir():
            # Extract plate barcode from folder name
            plate_barcode = extract_plate_barcode(folder_path.name)
            
            # Look for indexfile.txt in this folder
            indexfile_path = folder_path / 'indexfile.txt'
            
            if indexfile_path.exists():
                measurement_signature = process_indexfile(indexfile_path)
                
                if measurement_signature:
                    results.append((plate_barcode, measurement_signature))
                    print(f"Processed: {plate_barcode} -> {measurement_signature}")
                else:
                    print(f"Warning: No measurement signature found for {plate_barcode}")
            else:
                print(f"Warning: indexfile.txt not found in {folder_path}")
    
    return results


def save_results_to_csv(results, output_path):
    """
    Save results to CSV file.
    
    Args:
        results (list): List of tuples (plate_barcode, measurement_signature)
        output_path (Path): Path to output CSV file
    """
    # Sort results by plate barcode numerically
    sorted_results = sorted(results, key=lambda x: int(x[0]))
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['Plate_Barcode', 'Measurement_Signature'])
        
        # Write data rows
        for plate_barcode, measurement_signature in sorted_results:
            writer.writerow([plate_barcode, measurement_signature])
    
    print(f"Results saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Extract plate barcodes and measurement signatures from indexfiles'
    )
    parser.add_argument(
        '-i', '--input-dir',
        type=str,
        required=True,
        help='Directory containing indexfiles subdirectories'
    )
    
    args = parser.parse_args()
    
    # Convert to Path object
    indexfiles_dir = Path(args.input_dir)
    
    # Validate input directory
    if not indexfiles_dir.exists():
        print(f"Error: Directory {indexfiles_dir} does not exist")
        return 1
    
    if not indexfiles_dir.is_dir():
        print(f"Error: {indexfiles_dir} is not a directory")
        return 1
    
    print(f"Processing indexfiles directory: {indexfiles_dir}")
    
    # Process all indexfiles
    results = process_indexfiles_directory(indexfiles_dir)
    
    if not results:
        print("No results found. Please check your directory structure and indexfile.txt files.")
        return 1
    
    # Save results to CSV
    output_path = indexfiles_dir / 'plates_measurement_signatures.csv'
    save_results_to_csv(results, output_path)
    
    print(f"Successfully processed {len(results)} indexfiles")
    return 0


if __name__ == '__main__':
    exit(main())