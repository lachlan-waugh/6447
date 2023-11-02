#!/bin/bash

if [[ "$(docker image inspect plsiamlegit/6447-ubuntu:pwndocker 2> /dev/null)" == "[]" ]]; then
    docker run -d --rm -h banana --name banana -v $(pwd):/ctf/work --cap-add=SYS_PTRACE plsiamlegit/6447-ubuntu:pwndocker
fi

docker exec -it banana /bin/bash
