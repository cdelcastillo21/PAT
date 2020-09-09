import os
import argparse


def cleanup_job(job_dir, output_dir):
    # Current working directory should be parent directory of job directory
    root_dir = os.getcwd()

    # Process output dir files and write to csv file:
    # number_run_process, number_write_process, start_time, adcprep1_time, adcprep2_time, end_time
    runs = os.listdir(output_dir)                                                                                                                                                                                                       
   
    output_file  = open(os.path.join(root_dir, 'results.csv'), 'w')
    for r in runs:
        files = os.listdir(os.path.join(output_dir, r))
        start_time = [i for i in files if 'start_' in i]
        adcprep1_time = [i for i in files if 'adcprep1_' in i]
        adcprep2_time = [i for i in files if 'adcprep2_' in i]
        end_time = [i for i in files if 'end_' in i]
        
        # TODO: Add error checking if time strings not found

        start_time = start_time[0].split('_')[1]
        adcprep1_time = adcprep1_time[0].split('_')[1]
        adcprep2_time = adcprep2_time[0].split('_')[1]
        end_time = end_time[0].split('_')[1]

        run_info = r.split('_')
        rp = run_info[1]
        wp = run_info[2]

        # Write line to output csv file
        output_file.write(','.join([rp, wp, start_time, adcprep1_time, adcprep2_time, end_time]) + "\n")
   
    output_file.close()
	



if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('job_dir', type=str, help="Absolute path to job data.")
    parser.add_argument('output_dir', type=str, help="Absolute path within job dir to output dir.")
    args = parser.parse_args()

    # Initialize job  
    cleanup_job(args.job_dir, args.output_dir)

