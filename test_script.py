from sultan.api import Sultan, SSHConfig

config = SSHConfig(port=2222)

with Sultan.load(hostname='localhost', user='vagrant', log=True, ssh_config=config) as sultan:
    result = sultan.sudo('yum install -y httpd').run()
    print 'STDOUT: ', '\n'.join(result.stdout)
    print 'STDERR: ', '\n'.join(result.stderr)
