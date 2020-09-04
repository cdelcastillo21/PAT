# Print commands and their arguments as they are executed.
# set -x

${AGAVE_JOB_CALLBACK_RUNNING}

# Load necessary modules
module load python3 pylauncher netcdf/4.3.3.1 hdf5/1.8.16
module list
pwd
date

CWD=$(pwd)
JOB_DIR="${CWD}/${AGAVE_JOB_NAME}"
OUTPUT_DIR="${JOB_DIR}/output"

# Create scan job directories and sub directories
mkdir ${JOB_DIR}
mkdir ${OUTPUT_DIR}

# Copy python and shell scripts to job directory
cp "${CWD}/setup_job.py" "${CWD}/pylauncher4.py" "${CWD}/pre_process.sh" \
	"${CWD}/post_process.sh" "${JOB_DIR}/"

# Put generator in top level directory so we can load
cp ${GENERATOR_SCRIPT} "${JOB_DIR}/generator.py"

# Switch to job directory
cd ${JOB_DIR}

# Call setup_job.py ->
#  - Writes parallelines.csv file for pylauncher to use
#  - Creates launcher script that starts pylauncher
python3 setup_job.py ${ADCIRC_EXECS} ${ADCIRC_INPUTS} \
	${AGAVE_JOB_NODE_COUNT} ${OUTPUT_DIR}

# Launch pylauncher
# python3 launch.py 

if [ ! $? ]; then
	echo "ADCIRC exited with an error status. $?" >&2
	${AGAVE_JOB_CALLBACK_FAILURE}
	exit
fi

exit 0
