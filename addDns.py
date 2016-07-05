import os
import socket

# def addDns(lines):
#     for line in lines:
#         domain = line.split(',')[1]
#         tld = domain.split('.')[1]
#         hasDnsTrail = ("com" in tld) or ("net" in tld) or ("org" in tld) or ("name" in tld)
#         hasDnsTrail = hasDnsTrail or ('biz' in tld) or ('info' in tld) or ("mobi" in tld)
#
#         if (hasDnsTrail):
#             dns


path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

def add_ip(lines):
    newLines = []
    for line in lines:
        try:
            url = line.split(',')[1]
            try:
                # TODO: extend to list of ips, not just single ip
                ip = socket.gethostbyname_ex(url)[-1][0]
            except socket.error:
                ip = "no ips available"
        except:
            ip = "badformat"
            print(newLine)
        newLine = (line.replace("\n", "") + ", " + str(ip))
        newLines.append(newLine)
    return newLines


def add_ips():
    # get all sites
    sites = col.find({})

    for site in sites:
        url = site['url']
        try:
            ips = socket.gethostbyname_ex(url)[-1]
        except socket.error:
            ips = []

        result = col.update_one({'url': url},
                    {
                    '$set': {
                        'currentIPS': ips
                        }
                    }
                    )
        if result.acknowledged:
            print("added %d ips to url: %s" % (len(ips), url))
        else:
            print("didn't add ips to db, something went wrong!")





for filename in os.listdir('ranking_files'):
    os.chdir(dir_path + "/ranking_files")
    print(filename)
    print(filename[0])
    if (filename[0] != '.'):
        f = open(filename)
        lines = f.readlines()
        new_lines = add_ip(lines)
        print(new_lines)
        f.close()

        os.chdir(dir_path + "/rankingWithIP")

        f = open(filename, 'w')
        for line in new_lines:
            f.write(line + "\n")
        f.close()
