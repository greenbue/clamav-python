import os
import pyclamd

def scan_file(file_path):
  try:
    # cd = pyclamd.ClamdAgnostic()
    cd = pyclamd.ClamdNetworkSocket('localhost', 3310)
    # cd = pyclamd.ClamdUnixSocket()

    if os.path.exists(file_path):
      scan_result = cd.scan_file(file_path)

      if scan_result == None:
        print file_path + " is clean."
      else:
        print file_path + " is infected with " + scan_result[file_path][1] + ". " + scan_result[file_path][0]
    else:
      print "File not found."
  except Exception as e:
    print "Error during Clam Scan:", str(e)

def scan_stream(file_stream):
  try:
    cd = pyclamd.ClamdNetworkSocket('localhost', 3310)

    if cd.ping():
      # Scan the file stream in chunks
      CHUNK_SIZE = 8192  # Adjust the chunk size as per your needs

      while True:
        chunk = file_stream.read(CHUNK_SIZE)
        if not chunk:
          break

        scan_result = cd.scan_stream(chunk)

      return scan_result
    else:
      return 'Failed to connect to ClamAV server'
  except pyclamd.ConnectionError as e:
    print "Error during Clam Scan:", str(e)

current_directory = os.path.dirname(os.path.abspath(__file__))

print "\nScanning file from directory"
filename = os.path.join(current_directory, 'files', 'textfile.txt')
scan_file(filename)

print "\nScanning file Stream"
with open(filename, 'rb') as file:
  scan_result = scan_stream(file)

print('Scan result for {}: {}'.format(filename, scan_result))

print "\nScanning file from directory"
filename = os.path.join(current_directory, 'files', 'eicar_test.txt')
scan_file(filename)

print "\nScanning file Stream"
with open(filename, 'rb') as file:
  scan_result = scan_stream(file)

print('Scan result for {}: {}'.format(filename, scan_result))
