# pl_line += "post_process.sh {job_dir} {run_name} {output_dir}"
set -x

# Read command line inputs
JOB_DIR=${1}
RUN_NAME=${2}
OUTPUT_DIR=${3}

RUN_DIR="${JOB_DIR}/${RUN_NAME}"
RUN_OUTPUT_DIR="${OUTPUT_DIR}/${RUN_NAME}"

# Load necessary modules
module load python3 pylauncher netcdf/4.3.3.1 hdf5/1.8.16
module list
pwd
date

# Navigate to run dir and run adcprep
cd ${RUN_DIR}

# Create End timestamp file
END_TS=`date +"%Y-%m-%d-%H:%M:%S"`
touch "end_${END_TS}"

# Create output Dir
mkdir "${RUN_OUTPUT_DIR}"

# Copy log and timestamp files
cp ${RUN_DIR}/*.log ${RUN_OUTPUT_DIR}/
cp ${RUN_DIR}/start_* ${RUN_OUTPUT_DIR}/
cp ${RUN_DIR}/end_* ${RUN_OUTPUT_DIR}/
cp ${RUN_DIR}/adcprep1_* ${RUN_OUTPUT_DIR}/
cp ${RUN_DIR}/adcprep2_* ${RUN_OUTPUT_DIR}/

# Clean run directory
cd ${JOB_DIR}
rm -r ${RUN_DIR}

exit 0
