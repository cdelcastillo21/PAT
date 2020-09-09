import pandas as pd


def process_data(results_file):
  headers = ['run_proc', 'write_proc', 'start_dt', 'adcprep1_dt', 'adcprep2_dt', 'end_dt']
  dtypes = {'run_proc': 'int', 'write_proc': 'int', 'start_dt': 'str', 'adcprep1_dt': 'str', 'adcprep2_dt': 'str', 'end_dt': 'str'}                                                                                                   
  parse_dates = ['start_dt', 'adcprep1_dt', 'adcprep2_dt', 'end_dt']                                                                                                                                                                  
  res = pd.read_csv('./AK_PSCAN_results.csv', sep=',', header=None, names=headers, dtype=dtypes, parse_dates=parse_dates)                                                                                                             
  res['adcprep1_secs'] = (res.adcprep1_dt-res.start_dt).astype('timedelta64[s]')
  res['adcprep2_secs'] = (res.adcprep2_dt-res.adcprep1_dt).astype('timedelta64[s]')                                                                                                                                                   
  res['padcirc_secs'] = (res.end_dt-res.adcprep2_dt).astype('timedelta64[s]')                                                                                                                                                         

if __name__ == "__main__":
  # Parse arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('results_file', type=str, help="Absolute path to results file.")
  args = parser.parse_args()

  # Initialize job  
  process_data(arsg.results_file)
