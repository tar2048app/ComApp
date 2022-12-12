#!/usr/bin/env python3 

import os
import httpx
import json
import tarfile

createReq = """{
  "Image": "httpd",
  "HostConfig": {
    "PortBindings": {
      "80/tcp": [
        {
          "HostPort": "8080"
        }
      ]
    }
  }
}"""

def main():
    print('hello world, meet docker!')
    
    try:
        os.stat('/var/run/docker.sock')
    except FileNotFoundError as e:
        print("You didn't install docker first!")
        return

    # Requests can't handle unix sockets by default (boooo! go home!), so...
    trans = httpx.HTTPTransport(uds="/var/run/docker.sock")
    client = httpx.Client(transport=trans)

    # Before I start doing this a dumb way, I do want to note that the 'real'
    # way to do with would be pip install docker, and then:

    #import docker
    #client = docker.from_env()
    #client.containers.run('httpd', volumes=[os.getcwd()+"/public_web"+":/usr/local/apache2/htdocs/"], ports={"80/tcp":8080})

    # And then you curl localhost:8080. But that's boring!

    # When I started setting up for this, I realized that I hadn't ever used
    # docker API directly before, which seemed like sort of a shame.  Its
    # not super big, so here we go!

    ## 1. We create the container...

    resp = client.post('http://localhost/containers/create', 
                        headers={"Content-type": "application/json"}, 
                        data=createReq)

    print(resp.text)

    # Now we hope that Docker's API doesn't change:

    containerId = json.loads(resp.text)['Id']


    ## 2. We move our files onto it...

    tarball = open(os.getcwd()+"/index.tar", "rb").read()

    resp = client.put('http://localhost/containers/'+containerId+'/archive?path=/usr/local/apache2/htdocs/', 
                       headers={"Content-type": "application/x-tar"},
                       data=tarball)

    ## 3. Now we start it!

    resp = client.post('http://localhost/containers/'+containerId+'/start', 
                        headers={"Content-type": "application/json"})

    print("created docker container " + containerId + "! cya! curl localhost:8080!")


if __name__ == "__main__":
    main()
