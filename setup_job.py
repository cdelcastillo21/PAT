import os
import argparse
from generator import gen_function


def init_job(exec_path, adcirc_input, total_job_proc, output_dir):

    # Current working directory should be job directory
    job_dir = os.getcwd()
    root_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    adcirc_exec = os.path.join(exec_path, 'padcirc')

    # Run generator function to generate list of 
    # (number run process, num write process) pairs to run adcirc simulation for
    process_vals = gen_function(adcirc_input)
 
    # Find max total processes in list of process_vals to scan through. Make sure not more than total_job_proc
    if max([pair[0]+pair[1] for pair in process_vals])>total_job_proc:
        print("ERROR")

    # Create parallel lines file
    # Each line has format [NUM_PROC],[PRE PROCESS COMMAND];[MAIN PARALLEL COMMAND];[POST PROCESS COMMAND]
    pl_file = os.path.join(job_dir, 'parallel_lines.csv')
    fp = open(pl_file, 'w')
    pl_line = "{ppj},pre_process.sh {job_dir} {run_name} {exec_path} {adcirc_input} {run_proc};"
    pl_line += "{adcirc_exec} -I {run_dir} -O {run_dir} -W {write_proc};"
    pl_line += "post_process.sh {job_dir} {run_name} {output_dir}"

    for p_vals in process_vals:
        tot_proc = p_vals[0] + p_vals[1]
        run_name = 'run_' + str(p_vals[0]) + '_' + str(p_vals[1])
        run_dir = os.path.join(job_dir, run_name)
        next_line = pl_line.format(ppj=tot_proc, job_dir=job_dir, run_name=run_name, run_dir=run_dir,
                                   exec_path=exec_path, adcirc_input=adcirc_input, run_proc=p_vals[0],
                                   write_proc=p_vals[1], adcirc_exec=adcirc_exec, output_dir=output_dir)
        fp.write(next_line + "\n")
    fp.close()

    # Create one line python file that will launch pylauncher. This is what submit script will call
    launch_script = """import pylauncher4 
pylauncher4.IbrunLauncher("{file}", cores="file", debug="job+host+task+exec", pre_post_process=True)""".format(file=pl_file)
    fp = open(os.path.join(job_dir, 'launch.py'), 'w')
    fp.write(launch_script)
    fp.close()


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('exec_dir', type=str, help="Absolute path to folder containing adcirc executables.")
    parser.add_argument('adcirc_input', type=str, help="Absolute path to adcirc input files")
    parser.add_argument('total_job_proc', type=int, help="Total processes handed to pylauncher.")
    parser.add_argument('output_dir', type=str, help="Directory to store all output produced.")
    args = parser.parse_args()

    # Initialize job  
    init_job(args.exec_dir, args.adcirc_input, args.total_job_proc, args.output_dir)

