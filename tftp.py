import os

def create_tftp_request(tftp_ip, src_path, dst_path):
    # copy tftp://10.10.2.204/tftpboot/ubuntu-16.04.2-desktop-amd64.iso /home/group-five/tftp/
    # os.system("copy tftp://{%s}/{%s} {%s}").format(tftp_ip, src_path, dst_path) 
    # tftp 192.168.1.1 -c put myfile theirfile
    # tftp_string = "copy tftp://" + tftp_ip + src_path + " " + dst_path
    
    tftp_string = "tftp -v " + tftp_ip + " -c get -l " + dst_path + " -r " + src_path
    print tftp_string
    os.system(tftp_string)

def main():
    tftp_ip = "10.10.2.204"
    src_path = "/tftpboot/ubuntu-16.04.2-desktop-amd64.iso"
    dst_path = "/home/group-five/tftp/"
    create_tftp_request(tftp_ip, src_path, dst_path)

if __name__ == "__main__":
    main()

