import os

'''def create_tftp_request(tftp_ip, src_path, dst_path):
    # copy tftp://10.10.2.204/tftpboot/ubuntu-16.04.2-desktop-amd64.iso /home/group-five/tftp/
    # os.system("copy tftp://{%s}/{%s} {%s}").format(tftp_ip, src_path, dst_path) 
    # tftp 192.168.1.1 -c put myfile theirfile
    # tftp_string = "copy tftp://" + tftp_ip + src_path + " " + dst_path
    
    tftp_string = "tftp -v " + tftp_ip + " -c get -l " + dst_path + " -r " + src_path
    print tftp_string
    os.system(tftp_string)
'''

# Perform TFTP copy
def create_tftp_transfer(tftp_ip, src_file):
    path = '/home/group-five/tftp/'
    os.chdir(path)
    os.system('pwd')
    connect = 'tftp ' + tftp_ip
    print connect
    os.system(connect)
    getfile = 'get ' + src_file
    print getfile
    os.system(getfile)
    count = 0
    while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = sys.stdin.readline()
        if line == "tftp>":
            print 'File transfer complete'
            os.system('quit')
        else: # an empty line means stdin has been closed
            print('eof')
            exit(0)
    else:
        print 'Failed to request TFTP file'


def main():
    tftp_ip = "10.10.2.204"
    src_file = "ubuntu-16.04.2-desktop-amd64.iso"
    # dst_path = "/home/group-five/tftp/"
    # create_tftp_request(tftp_ip, src_path, dst_path)
    create_tftp_transfer(tftp_ip, src_file)    

if __name__ == "__main__":
    main()

