# pre_process.sh {job_dir} {run_name} {exec_path} {adcirc_input} {run_proc}
set -x

# Read command line inputs
JOB_DIR=${1}
RUN_NAME=${2}
ADCIRC_EXEC=${3}
ADCIRC_INPUT=${4}
ADCIRC_RUN_PROC=${5}

# Load necessary modules
module load python3 pylauncher netcdf/4.3.3.1 hdf5/1.8.16
module list
pwd
date

# Create Run Dir
RUN_DIR="${JOB_DIR}/${RUN_NAME}"

# Copy input files to run dir
cp -r ${ADCIRC_INPUT} ${RUN_DIR}

# Navigate to run dir 
cd $RUN_DIR

# Create start timestamp file
START_TS=`date +"%Y-%m-%d-%H:%M:%S"`
touch "start_${START_TS}"

# Run adcprep
printf '%s\n1\nfort.14\n' ${ADCIRC_RUN_PROC} | "${ADCIRC_EXEC}/adcprep" > adcprep1.log

# Create adcprep timestamp file
ADCPREP1_TS=`date +"%Y-%m-%d-%H:%M:%S"`
touch "adcprep1_${ADCPREP1_TS}"

printf '%s\n2\n' ${ADCIRC_RUN_PROC} | "${ADCIRC_EXEC}/adcprep" >adcprep2.log

# Create adcprep timestamp file
ADCPREP2_TS=`date +"%Y-%m-%d-%H:%M:%S"`
touch "adcprep2_${ADCPREP2_TS}"

exit 0
